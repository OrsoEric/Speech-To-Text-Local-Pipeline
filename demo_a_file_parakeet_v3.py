"""

python demo/demo_a_file_parakeet_v3.py 


"""

import sys
import wave
from pathlib import Path

import numpy as np

from cl_asr_parakeet_v3 import Cl_asr_parakeet_v3

from time import perf_counter_ns
from pathlib import Path

import numpy as np

C_S_MODEL_PATH = Path(r"F:\LLM Models\parakeet-tdt-0.6b-v3-onnx")
C_S_WAV_PATH = Path(r"F:\Data\Project\Project-LLM\Audio Samples\wav\SAMPLE-Ranni-18s.wav")

C_DTYPE_BY_SAMPLE_WIDTH = {
    2: np.int16,
    4: np.int32,
}

def read_wav_as_float32_mono(i_s_wav_path: Path):
    with wave.open(str(i_s_wav_path), "rb") as cl_wav:
        n_sample_rate = cl_wav.getframerate()
        n_channels = cl_wav.getnchannels()
        n_sample_width = cl_wav.getsampwidth()
        n_frames = cl_wav.getnframes()

        raw_data = cl_wav.readframes(n_frames)

    if n_sample_width == 1:
        # 8-bit PCM WAV is unsigned.
        np_samples = np.frombuffer(
            raw_data,
            dtype=np.uint8,
        ).astype(np.float32)

        np_samples = (np_samples - 128.0) / 128.0

    elif n_sample_width == 2:
        # 16-bit PCM
        np_samples = np.frombuffer(
            raw_data,
            dtype="<i2",
        ).astype(np.float32)

        np_samples /= 32768.0

    elif n_sample_width == 3:
        # 24-bit PCM.
        #
        # WAV stores each sample as 3 little-endian bytes.
        # NumPy has no native int24 type, so unpack manually
        # into int32.
        np_bytes = np.frombuffer(
            raw_data,
            dtype=np.uint8,
        ).reshape(-1, 3)

        np_samples = (
            np_bytes[:, 0].astype(np.int32)
            | (np_bytes[:, 1].astype(np.int32) << 8)
            | (np_bytes[:, 2].astype(np.int32) << 16)
        )

        # Sign-extend 24-bit two's-complement to int32.
        negative = (np_samples & 0x800000) != 0
        np_samples[negative] -= 0x1000000

        np_samples = np_samples.astype(np.float32)
        np_samples /= 8388608.0  # 2^23

    elif n_sample_width == 4:
        # 32-bit PCM
        np_samples = np.frombuffer(
            raw_data,
            dtype="<i4",
        ).astype(np.float32)

        np_samples /= 2147483648.0  # 2^31

    else:
        raise ValueError(
            f"Unsupported WAV sample width: "
            f"{n_sample_width} bytes "
            f"({n_sample_width * 8} bits)"
        )

    if n_channels > 1:
        np_samples = np_samples.reshape(-1, n_channels)
        np_samples = np_samples.mean(axis=1)

    return np_samples, n_sample_rate


def demo(i_s_wav_path: Path = C_S_WAV_PATH):

    cl_parakeet = Cl_asr_parakeet_v3()
    cl_parakeet.load_model(C_S_MODEL_PATH,i_x_profiling=False)

    cl_parakeet.inspect_provider_details()

    print("DEMO1: load file directly")

    s_transcript, n_inference_ms = cl_parakeet.run_inference_file(i_s_wav_path)
    print(f"Inference time: {n_inference_ms :.0f} ms")
    print("TRANSCRIPT: ", s_transcript)

    print("DEMO2: from file extract wav, then feed wav to model")

    np_waveform, n_sample_rate = read_wav_as_float32_mono(i_s_wav_path)
    s_transcript_raw, n_raw_ms = cl_parakeet.run_inference_raw(np_waveform, n_sample_rate)
    print(f"Raw inference time: {n_raw_ms :.0f} ms")
    print("TRANSCRIPT RAW: ", s_transcript_raw)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        demo(Path(sys.argv[1]))
    else:
        demo()
