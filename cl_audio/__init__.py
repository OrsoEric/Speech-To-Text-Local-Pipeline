"""
Library to open audio files and expose their content as simple structures.

The entry point is the Cl_audio class which reads PCM WAV files and returns
their content as an St_wav structure holding the samples, the sample rate
and the duration.
"""

from dataclasses import dataclass, field
from pathlib import Path

import wave

import numpy

@dataclass
class St_wav:
    """
    Structure describing the content of a WAV audio file.
    """

    np_samples: numpy.ndarray
    n_sample_rate_hz: int
    n_duration_s: float = field(init=False)
    n_avg: float = field(init=False)
    n_rms: float = field(init=False)

    def __post_init__(self) -> None:
        self.compute_stats()
        return

    def compute_stats(self) -> None:
        """
        Computes the duration, average amplitude and RMS of the WAV samples.
        """

        self.n_duration_s = (
            float(self.np_samples.shape[0])
            / float(self.n_sample_rate_hz)
        )

        if self.np_samples.size == 0:
            self.n_avg = 0.0
            self.n_rms = 0.0
            return

        self.n_avg = float(numpy.mean(self.np_samples))
        self.n_rms = float(
            numpy.sqrt(numpy.mean(self.np_samples ** 2))
        )
        return

    def __str__(self) -> str:
        return (
            f"WAV:"
            f" duration={self.n_duration_s:.3f} s,"
            f" sample_rate={self.n_sample_rate_hz} Hz,"
            f" samples={self.np_samples.shape[0]},"
            f" avg={self.n_avg:.6f},"
            f" rms={self.n_rms:.6f}"
        )
    
class Cl_audio:

    def read_wav_file(self, i_s_wav_path: str | Path) -> St_wav:
        """
        Opens a PCM WAV file and converts it into an St_wav structure.

        The samples are converted to mono float32 normalized in [-1.0, 1.0]
        whatever the bit depth or the channel count of the source file.

        Parameters:
        i_s_wav_path (str | Path): Path of the WAV file to open.

        Returns:
        St_wav: Structure holding the mono float32 samples, the sample rate and the duration.
        """

        with wave.open(str(i_s_wav_path), "rb") as cl_wav:
            n_sample_rate_hz = cl_wav.getframerate()
            n_channel_count = cl_wav.getnchannels()
            n_sample_width_bytes = cl_wav.getsampwidth()
            n_frame_count = cl_wav.getnframes()

            np_raw_frames = numpy.frombuffer(
                cl_wav.readframes(n_frame_count),
                dtype=numpy.uint8,
            )

        np_samples = self.convert_pcm_frames_to_float32_mono(
            np_raw_frames,
            i_n_sample_width_bytes=n_sample_width_bytes,
            i_n_channel_count=n_channel_count,
        )

        return St_wav(
            np_samples=np_samples,
            n_sample_rate_hz=n_sample_rate_hz,
        )

    @staticmethod
    def convert_pcm_frames_to_float32_mono(
        i_np_raw_frames: numpy.ndarray,
        i_n_sample_width_bytes: int,
        i_n_channel_count: int,
    ) -> numpy.ndarray:
        """
        Converts raw interleaved PCM frames into mono float32 samples normalized in [-1.0, 1.0].

        Supports unsigned 8-bit, signed 16-bit, signed 24-bit and signed 32-bit PCM.
        Multi-channel audio is averaged down to mono.

        Parameters:
        i_np_raw_frames (numpy.ndarray): Raw frame bytes as an uint8 array.
        i_n_sample_width_bytes (int): Size of one sample in bytes (1 to 4).
        i_n_channel_count (int): Number of interleaved channels.

        Returns:
        numpy.ndarray: Mono float32 samples normalized in [-1.0, 1.0].
        """

        if i_n_sample_width_bytes == 1:
            # 8-bit PCM WAV is unsigned
            np_samples = (i_np_raw_frames.astype(numpy.float32) - 128.0) / 128.0

        elif i_n_sample_width_bytes == 2:
            # 16-bit PCM
            np_samples = i_np_raw_frames.view(numpy.int16).astype(numpy.float32)
            np_samples /= 32768.0

        elif i_n_sample_width_bytes == 3:
            # 24-bit PCM stores each sample as three little-endian bytes.
            # NumPy has no native int24 type so the samples are unpacked
            # manually into int32.
            np_bytes_per_sample = i_np_raw_frames.reshape(-1, 3)

            np_samples = (
                np_bytes_per_sample[:, 0].astype(numpy.int32)
                | (np_bytes_per_sample[:, 1].astype(numpy.int32) << 8)
                | (np_bytes_per_sample[:, 2].astype(numpy.int32) << 16)
            )

            # Sign-extend the 24-bit two's-complement values to int32
            np_negative_mask = (np_samples & 0x800000) != 0
            np_samples[np_negative_mask] -= 0x1000000

            np_samples = np_samples.astype(numpy.float32)
            np_samples /= 8388608.0

        elif i_n_sample_width_bytes == 4:
            # 32-bit PCM
            np_samples = i_np_raw_frames.view(numpy.int32).astype(numpy.float32)
            np_samples /= 2147483648.0

        else:
            raise ValueError(
                f"Unsupported WAV sample width: "
                f"{i_n_sample_width_bytes} bytes "
                f"({i_n_sample_width_bytes * 8} bits)"
            )

        if i_n_channel_count > 1:
            np_samples = np_samples.reshape(-1, i_n_channel_count)
            np_samples = np_samples.mean(axis=1)

        return np_samples
