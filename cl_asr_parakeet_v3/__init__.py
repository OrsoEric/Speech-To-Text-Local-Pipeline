from time import perf_counter_ns
from pathlib import Path

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

    def inspect_provider_details(self, i_cl_model=None, i_s_path="model"):
        if i_cl_model is None:
            i_cl_model = self.cl_model

        if i_cl_model is None:
            raise RuntimeError("Model not loaded, call load_model() first")

        if isinstance(i_cl_model, lib_onnx_runtime.InferenceSession):
            print(i_s_path)
            print(f"  providers: {i_cl_model.get_providers()}")
            print()
            return

        if not hasattr(i_cl_model, "__dict__"):
            return

        for s_name, x_value in vars(i_cl_model).items():

            s_path = f"{i_s_path}.{s_name}"

            if isinstance(x_value, lib_onnx_runtime.InferenceSession):
                print(s_path)
                print(f"  providers: {x_value.get_providers()}")
                print()

            elif hasattr(x_value, "__dict__"):
                self.inspect_provider_details(x_value, s_path)