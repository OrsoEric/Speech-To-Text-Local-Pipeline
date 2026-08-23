"""
Library to slide a decoding window over a live or replayed audio stream.

The entry point is the Cl_transcriber class which joins incoming base chunks
into windows of i_n_chunk_length_stt chunks, decodes each window through the
ASR wrapper given at construction and advances the window by i_n_chunk_skip
base chunks after every scan. Timestamps are derived from the absolute count
of pushed samples so they reflect the real position inside the stream
whatever the pace of the pushes.
"""

import numpy

from cl_audio import St_wav
from cl_asr_parakeet_v3 import Cl_asr_parakeet_v3


class Cl_transcriber:
    """
    Sliding-window speech-to-text transcriber.

    Base chunks are pushed chronologically through push_chunk(). Once the
    buffer holds one full window it can be decoded with scan() which then
    advances it by i_n_chunk_skip base chunks. flush() decodes whatever
    remains at the end of the stream so no audio is left untranscribed. The
    trailing buffer is usually shorter than a full window and models can
    reject or mistranscribe abnormally short inputs, so it is zero-padded
    up to one full window of silence before inference.
    """

    # ------------------------------------------------------------------
    # MEMBER VARIABLES
    # ------------------------------------------------------------------

    np_window_samples: numpy.ndarray
    n_total_samples_pushed: int
    n_scan_count: int

    # ------------------------------------------------------------------
    # INITIALIZATION
    # ------------------------------------------------------------------

    def __init__(
        self,
        i_cl_parakeet: Cl_asr_parakeet_v3,
        i_n_sample_rate_hz: int,
        i_n_chunk_length_base_ms: float = 100.0,
        i_n_chunk_length_stt: int = 3,
        i_n_chunk_skip: int = 1,
    ) -> None:
        """
        Configure the transcriber.

        Parameters:
            i_cl_parakeet:
                Loaded ASR model wrapper exposing run_inference_raw().

            i_n_sample_rate_hz:
                Sample rate of the incoming chunks in Hz.

            i_n_chunk_length_base_ms:
                Duration of one base chunk in milliseconds.

            i_n_chunk_length_stt:
                Number of base chunks joined into one STT window.

            i_n_chunk_skip:
                Number of base chunks advanced by each scan.
        """
        if i_n_sample_rate_hz <= 0:
            raise ValueError("i_n_sample_rate_hz must be greater than 0.")

        if i_n_chunk_length_base_ms <= 0:
            raise ValueError("i_n_chunk_length_base_ms must be greater than 0.")

        if i_n_chunk_length_stt <= 0:
            raise ValueError("i_n_chunk_length_stt must be greater than 0.")

        if i_n_chunk_skip <= 0:
            raise ValueError("i_n_chunk_skip must be greater than 0.")
        if i_n_chunk_skip > i_n_chunk_length_stt:
            raise ValueError(
                "i_n_chunk_skip must not exceed i_n_chunk_length_stt "
                "otherwise samples would be dropped without being decoded."
            )

        self.cl_parakeet = i_cl_parakeet
        self.cn_sample_rate = i_n_sample_rate_hz
        self.cn_chunk_duration_s = i_n_chunk_length_base_ms / 1000.0
        self.cn_chunk_length_stt = i_n_chunk_length_stt
        self.cn_chunk_skip = i_n_chunk_skip

        self.cn_chunk_samples: int = max(
            1,
            round(
                self.cn_sample_rate
                * self.cn_chunk_duration_s
            ),
        )

        self.cn_window_samples: int = max(
            1,
            self.cn_chunk_samples
            * self.cn_chunk_length_stt,
        )

        self.cn_skip_samples: int = max(
            1,
            self.cn_chunk_samples
            * self.cn_chunk_skip,
        )

        self.reset()

    # ------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """
        Clear the buffer and restart the timestamps from zero.
        """
        self.np_window_samples = numpy.zeros(0, dtype=numpy.float32)
        self.n_total_samples_pushed = 0
        self.n_scan_count = 0

    def push_chunk(self, i_st_chunk: St_wav) -> None:
        """
        Append one base chunk to the sliding window buffer.

        Parameters:
            i_st_chunk (St_wav): Base chunk captured by the microphone or
            sliced from a file.
        """
        self.np_window_samples = numpy.concatenate(
            (
                self.np_window_samples,
                i_st_chunk.np_samples.astype(numpy.float32),
            )
        )
        self.n_total_samples_pushed += i_st_chunk.np_samples.shape[0]

    def is_ready(self) -> bool:
        """
        Check whether the buffer holds enough samples for one full window.

        Returns:
            bool: True when at least i_n_chunk_length_stt base chunks worth
            of samples are buffered.
        """
        return self.np_window_samples.shape[0] >= self.cn_window_samples

    def get_timestamps(self) -> tuple[float, float]:
        """
        Compute the timestamps covered by the current window buffer.

        Returns:
            Tuple[float, float]: Timestamp start and end in seconds relative
            to the first pushed sample.
        """
        n_start_s = (
            self.n_total_samples_pushed - self.np_window_samples.shape[0]
        ) / self.cn_sample_rate
        n_end_s = self.n_total_samples_pushed / self.cn_sample_rate

        return n_start_s, n_end_s

    def scan(self) -> tuple[str, float]:
        """
        Decode the current window then advance it by i_n_chunk_skip chunks.

        The decoded transcript is printed with its timestamp start, timestamp
        end and content. Empty transcripts (silence) are printed as empty.

        Returns:
            Tuple[str, float]: The transcript and the inference time in
            milliseconds.
        """
        s_transcript, n_inference_ms = self.decode_buffer(i_x_flush=False)

        self.n_scan_count += 1

        self.np_window_samples = self.np_window_samples[self.cn_skip_samples:]

        return s_transcript, n_inference_ms

    def flush(self) -> tuple[str, float] | None:
        """
        Decode whatever remains in the buffer then clear it.

        Used once the stream ends so the trailing partial window is not lost.
        The remainder is zero-padded up to one full window because it is
        shorter than the windows decoded by scan() and models can fail on
        unusually short inputs. Nothing happens when the buffer is empty.

        Returns:
            Tuple[str, float] | None: The transcript and the inference time
            in milliseconds, or None when there was nothing to decode.
        """
        if self.np_window_samples.shape[0] == 0:
            return None

        s_transcript, n_inference_ms = self.decode_buffer(i_x_flush=True)

        self.np_window_samples = numpy.zeros(0, dtype=numpy.float32)

        return s_transcript, n_inference_ms

    # ------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------

    def decode_buffer(self, i_x_flush: bool) -> tuple[str, float]:
        """
        Decode the current buffer through the ASR model and print the result.

        Parameters:
            i_x_flush (bool): True when decoding the end-of-stream remainder,
            tagging the printed line and disabling the window advance.

        Returns:
            Tuple[str, float]: The transcript and the inference time in
            milliseconds.
        """
        n_start_s, n_end_s = self.get_timestamps()

        s_transcript, n_inference_ms = self.cl_parakeet.run_inference_raw(
            self.get_padded_samples(),
            self.cn_sample_rate,
        )

        s_tag = " [flush]" if i_x_flush else ""

        print(
            f"[{n_start_s :7.2f}s -> {n_end_s :7.2f}s]"
            f" ({n_inference_ms :5.0f} ms)"
            f" {s_transcript}{s_tag}"
        )

        return s_transcript, n_inference_ms

    def get_padded_samples(self) -> numpy.ndarray:
        """
        Return the buffered samples padded with silence up to one full window.

        Returns:
            numpy.ndarray: Mono float32 samples of at least cn_window_samples.
        """
        if self.np_window_samples.shape[0] >= self.cn_window_samples:
            return self.np_window_samples

        np_padded_samples = numpy.zeros(
            self.cn_window_samples,
            dtype=numpy.float32,
        )
        np_padded_samples[: self.np_window_samples.shape[0]] = self.np_window_samples

        return np_padded_samples
