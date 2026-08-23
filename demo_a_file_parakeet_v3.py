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
import json

import numpy as np
import onnxruntime as lib_onnx_runtime
import onnx_asr
from onnx_asr.adapters import TextResultsAsrAdapter

C_S_MODEL_NAME = "nemo-parakeet-tdt-0.6b-v3"

class Cl_asr_parakeet_v3:

    def __init__(self):
        self.cl_model: TextResultsAsrAdapter | None = None
        self.n_load_time_ms: float = 0.0
        self.n_last_inference_time_ms: float = 0.0
        self.x_onnx_profiling: bool = False
        self.as_providers: list[str] = []

    def load_model(
        self,
        i_s_model_path: str | Path,
        i_as_providers: list[str] | None = None,
        i_x_profiling: bool = False,
    ):
        start_ns = perf_counter_ns()

        self.x_onnx_profiling = i_x_profiling

        if i_as_providers is None:
            i_as_providers = list(lib_onnx_runtime.get_available_providers())
        self.as_providers = list(i_as_providers)

        cl_session_options = lib_onnx_runtime.SessionOptions()
        cl_session_options.enable_profiling = i_x_profiling

        # lower the verbosity from default
        lib_onnx_runtime.set_default_logger_severity(3)

        self.cl_model = onnx_asr.load_model(
            C_S_MODEL_NAME,
            str(i_s_model_path),
            providers=self.as_providers,
            sess_options=cl_session_options,
        )

        self.n_load_time_ms = (perf_counter_ns() - start_ns) / 1_000_000

        print(f"Available providers: {lib_onnx_runtime.get_available_providers()}")
        print(f"Model load time: {self.n_load_time_ms :.0f} ms")

        return self.cl_model

    def run_inference_file(self, i_s_audio_path: str | Path):
        if self.cl_model is None:
            raise RuntimeError("Model not loaded, call load_model() first")

        start_ns = perf_counter_ns()

        s_transcription = self.cl_model.recognize(Path(i_s_audio_path))

        self.n_last_inference_time_ms = (perf_counter_ns() - start_ns) / 1_000_000

        return s_transcription, self.n_last_inference_time_ms

    def run_inference_raw(self, i_np_waveform: np.ndarray, i_n_sample_rate: int = 16000):
        if self.cl_model is None:
            raise RuntimeError("Model not loaded, call load_model() first")

        start_ns = perf_counter_ns()

        np_waveform = np.asarray(i_np_waveform, dtype=np.float32)

        s_transcription = self.cl_model.recognize(
            np_waveform,
            sample_rate=i_n_sample_rate,
        )

        self.n_last_inference_time_ms = (perf_counter_ns() - start_ns) / 1_000_000

        return s_transcription, self.n_last_inference_time_ms

    def find_sessions(self, obj, path="model"):
        sessions = []

        if isinstance(obj, lib_onnx_runtime.InferenceSession):
            sessions.append((path, obj))
            return sessions

        if hasattr(obj, "__dict__"):
            for name, value in vars(obj).items():
                if isinstance(value, lib_onnx_runtime.InferenceSession):
                    sessions.append((f"{path}.{name}", value))
                elif hasattr(value, "__dict__"):
                    sessions.extend(self.find_sessions(value, f"{path}.{name}"))

        return sessions

    def inspect_profiles(self):
        if not self.x_onnx_profiling:
            print("ONNX profiling was not enabled, pass i_x_profiling=True to load_model()")
            return

        print()
        print("=== NODE EXECUTION INSPECTION ===")

        for name, session in self.find_sessions(self.cl_model):

            profile_path = session.end_profiling()

            print()
            print(name)
            print(f"  Profile: {profile_path!r}")

            if not profile_path:
                print("  No profile was generated.")
                continue

            profile_path = Path(profile_path)

            if not profile_path.is_file():
                print("  Profile file does not exist.")
                continue

            with profile_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                events = json.load(file)

            self._inspect_profile_events(
                name,
                events,
            )

    def _inspect_profile_events(self, i_s_session_name, i_events):
        provider_time_us = {}
        provider_event_count = {}

        print("  Events:", len(i_events))

        for event in i_events:

            if event.get("ph") != "X":
                continue

            args = event.get("args", {})

            provider = (
                args.get("provider")
                or args.get("execution_provider")
                or args.get("ep")
            )

            if not provider:
                continue

            duration_us = event.get("dur", 0)

            provider_time_us[provider] = (
                provider_time_us.get(provider, 0)
                + duration_us
            )

            provider_event_count[provider] = (
                provider_event_count.get(provider, 0)
                + 1
            )

        if not provider_time_us:
            print("  No provider information found in profile events.")

            for event in i_events:
                if event.get("ph") == "X":
                    print()
                    print("  Example profiling event:")
                    print(
                        json.dumps(
                            event,
                            indent=2,
                        )
                    )
                    break

            return

        print()
        print("  Execution by provider:")

        for provider, duration_us in sorted(
            provider_time_us.items(),
            key=lambda item: item[1],
            reverse=True,
        ):
            count = provider_event_count[provider]

            print(
                f"    {provider:<30}"
                f"{duration_us / 1000:>10.2f} ms"
                f"   ({count} events)"
            )



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
    cl_parakeet.load_model(C_S_MODEL_PATH)

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
