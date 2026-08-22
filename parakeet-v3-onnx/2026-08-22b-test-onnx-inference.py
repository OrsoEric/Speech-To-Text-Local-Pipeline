from time import perf_counter_ns
from pathlib import Path

import onnxruntime as lib_onnx_runtime
import onnx_asr

print(lib_onnx_runtime.get_available_providers())

CS_MODEL_PATH = Path(r"F:\LLM Models\parakeet-tdt-0.6b-v3-onnx")
CS_AUDIO_PATH = Path(r"F:\Data\Project\Project-LLM\Audio Samples\wav\SAMPLE-Ranni-18s.wav")

def load_model(i_s_model_path: Path):
    start_ns = perf_counter_ns()

    cl_model = onnx_asr.load_model(
        "nemo-parakeet-tdt-0.6b-v3",
        i_s_model_path,
        providers=["CPUExecutionProvider"],
    )

    n_elapsed_ms = (perf_counter_ns() - start_ns) / 1_000_000

    return cl_model, n_elapsed_ms


def inference(i_cl_model, i_s_audio_path: Path):
    start_ns = perf_counter_ns()

    s_transcription = i_cl_model.recognize(i_s_audio_path)

    n_elapsed_ms = (perf_counter_ns() - start_ns) / 1_000_000

    return s_transcription, n_elapsed_ms


def main():
    cl_model, load_time_ms = load_model(CS_MODEL_PATH)

    print(f"Model load time: {load_time_ms :.0f} ms")

    s_transcript, inference_time_ms = inference(cl_model, CS_AUDIO_PATH)

    print(f"Inference time: {inference_time_ms :.0f} ms")

    print("TRANSCRIPT: ",s_transcript)

if __name__ == "__main__":
    main()