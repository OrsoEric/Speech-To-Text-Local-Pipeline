"""

Real-time speech to text demo connecting Cl_microphone with Cl_asr_parakeet_v3.

The microphone produces base audio chunks of 100 ms. A sliding window of
chunk_length_stt base chunks is joined and fed to the STT model, and each
scan advances the window by chunk_skip base chunks. Every decoded window
is printed with its timestamp start, timestamp end and content.

python demo_c_microphone_stt.py [model_path]

Press Ctrl+C to stop.
"""

import sys
import queue

from pathlib import Path

import numpy

from cl_asr_parakeet_v3 import Cl_asr_parakeet_v3
from cl_audio import St_wav
from cl_microphone import Cl_microphone

C_S_MODEL_PATH = Path(r"F:\LLM Models\parakeet-tdt-0.6b-v3-onnx")

C_N_CHUNK_LENGTH_BASE_MS: float = 100.0
C_N_CHUNK_LENGTH_STT: int = 3
C_N_CHUNK_SKIP: int = 1


class Cl_stream_transcriber:
    """
    Sliding-window transcriber joining microphone base chunks into windows
    fed to the STT model.

    Each scan decodes a window of cn_chunk_length_stt base chunks then
    advances the buffer by cn_chunk_skip base chunks. Timestamps are derived
    from the absolute count of consumed base chunks so they reflect real time
    since the microphone started listening.
    """

    def __init__(
        self,
        i_cl_parakeet: Cl_asr_parakeet_v3,
        i_n_sample_rate_hz: int,
        i_n_chunk_length_base_ms: float,
        i_n_chunk_length_stt: int,
        i_n_chunk_skip: int,
    ) -> None:
        """
        Configure the transcriber.

        Parameters:
            i_cl_parakeet:
                Loaded ASR model wrapper used for inference.

            i_n_sample_rate_hz:
                Sample rate of the microphone chunks in Hz.

            i_n_chunk_length_base_ms:
                Duration of one base chunk in milliseconds.

            i_n_chunk_length_stt:
                Number of base chunks joined into one STT window.

            i_n_chunk_skip:
                Number of base chunks advanced by each scan.
        """
        self.cl_parakeet = i_cl_parakeet
        self.cn_sample_rate = i_n_sample_rate_hz
        self.cn_chunk_duration_s = i_n_chunk_length_base_ms / 1000.0
        self.cn_chunk_length_stt = i_n_chunk_length_stt
        self.cn_chunk_skip = i_n_chunk_skip

        self.np_window_samples: numpy.ndarray = numpy.zeros(0, dtype=numpy.float32)
        self.n_chunks_in_window: int = 0
        self.n_total_chunks_consumed: int = 0

    def push_chunk(self, i_st_chunk: St_wav) -> None:
        """
        Append one base chunk to the sliding window buffer.

        Parameters:
            i_st_chunk (St_wav): Base chunk captured by the microphone.
        """
        self.np_window_samples = numpy.concatenate(
            (self.np_window_samples, i_st_chunk.np_samples)
        )
        self.n_chunks_in_window += 1
        self.n_total_chunks_consumed += 1

    def is_ready(self) -> bool:
        """
        Check whether the buffer holds enough base chunks for one full window.

        Returns:
            bool: True when at least cn_chunk_length_stt chunks are buffered.
        """
        return self.n_chunks_in_window >= self.cn_chunk_length_stt

    def scan(self) -> None:
        """
        Decode the current window then advance it by cn_chunk_skip base chunks.

        The decoded transcript is printed with its timestamp start, timestamp
        end and content. Empty transcripts (silence) are printed as empty.
        """
        n_start_s = (
            self.n_total_chunks_consumed - self.n_chunks_in_window
        ) * self.cn_chunk_duration_s
        n_end_s = self.n_total_chunks_consumed * self.cn_chunk_duration_s

        s_transcript, n_inference_ms = self.cl_parakeet.run_inference_raw(
            self.np_window_samples,
            self.cn_sample_rate,
        )

        print(
            f"[{n_start_s :7.2f}s -> {n_end_s :7.2f}s]"
            f" ({n_inference_ms :5.0f} ms)"
            f" {s_transcript}"
        )

        np_skip_samples = int(self.cn_sample_rate * self.cn_chunk_duration_s)
        np_skip_samples *= self.cn_chunk_skip

        self.np_window_samples = self.np_window_samples[np_skip_samples:]
        self.n_chunks_in_window -= self.cn_chunk_skip


def demo(i_s_model_path: Path = C_S_MODEL_PATH) -> None:
    """
    Streams the microphone through the Parakeet model with a sliding window.

    The function loads the model, lists the available microphones, starts the
    capture on the first device and continuously joins base chunks into STT
    windows. Each window is decoded and printed with its timestamps until the
    user presses Ctrl+C.

    Parameters:
    i_s_model_path (Path): Path of the Parakeet ONNX model directory.
    """

    cl_parakeet = Cl_asr_parakeet_v3()
    cl_parakeet.load_model(i_s_model_path, i_x_profiling=False)

    cl_microphone = Cl_microphone(
        i_sample_rate_hz=24000,
        i_chunk_length_ms=C_N_CHUNK_LENGTH_BASE_MS,
    )

    l_available_device_names = cl_microphone.list_microphones()
    for i_index, s_name in enumerate(l_available_device_names):
        print(f"{i_index}: {s_name}")

    if not l_available_device_names:
        raise RuntimeError("No input devices detected on the system.")

    cl_transcriber = Cl_stream_transcriber(
        i_cl_parakeet=cl_parakeet,
        i_n_sample_rate_hz=cl_microphone.cn_sample_rate,
        i_n_chunk_length_base_ms=C_N_CHUNK_LENGTH_BASE_MS,
        i_n_chunk_length_stt=C_N_CHUNK_LENGTH_STT,
        i_n_chunk_skip=C_N_CHUNK_SKIP,
    )

    cl_microphone.start_listening()

    print("Listening... press Ctrl+C to stop.")
    print()

    try:
        while True:
            try:
                st_chunk = cl_microphone.c_audio_queue.get(timeout=1.0)
                cl_transcriber.push_chunk(st_chunk)
            except queue.Empty:
                # No chunk arrived within the timeout, keep waiting.
                continue

            if not cl_transcriber.is_ready():
                continue

            cl_transcriber.scan()

    except KeyboardInterrupt:
        pass

    finally:
        cl_microphone.stop_microphone()
        print()
        print("Microphone stopped.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        demo(Path(sys.argv[1]))
    else:
        demo()
