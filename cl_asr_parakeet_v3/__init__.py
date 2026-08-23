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
        self.b_onnx_profiling: bool = False
        self.as_providers: list[str] = []

    def load_model(
        self,
        i_s_model_path: str | Path,
        i_as_providers: list[str] | None = None,
        i_x_profiling: bool = False,
    ):
        start_ns = perf_counter_ns()

        self.b_onnx_profiling = i_x_profiling

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
        if not self.b_onnx_profiling:
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
