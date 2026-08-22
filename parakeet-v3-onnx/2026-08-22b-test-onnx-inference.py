from time import perf_counter_ns
from pathlib import Path

import json

import onnxruntime as lib_onnx_runtime
import onnx_asr

print(lib_onnx_runtime.get_available_providers())

C_S_MODEL_PATH = Path(r"F:\LLM Models\parakeet-tdt-0.6b-v3-onnx")
C_S_AUDIO_PATH = Path(r"F:\Data\Project\Project-LLM\Audio Samples\wav\SAMPLE-Ranni-18s.wav")

#C_S_ONNX_EXECUTION_PROVIDERS = ["CPUExecutionProvider"]

# faster but with warnings
C_S_ONNX_EXECUTION_PROVIDERS = [ "WebGpuExecutionProvider"]

# it goes a lot slower if I give it both
#C_S_ONNX_EXECUTION_PROVIDERS = [ "WebGpuExecutionProvider", "CPUExecutionProvider" ]

def load_model(i_s_model_path: Path):
    start_ns = perf_counter_ns()

    #lib_onnx_runtime.set_default_logger_severity(0)

    cl_model = onnx_asr.load_model(
        "nemo-parakeet-tdt-0.6b-v3",
        i_s_model_path,
        providers=C_S_ONNX_EXECUTION_PROVIDERS,
    )

    find_sessions(cl_model)

    n_elapsed_ms = (perf_counter_ns() - start_ns) / 1_000_000

    return cl_model, n_elapsed_ms


def inference(i_cl_model, i_s_audio_path: Path):
    start_ns = perf_counter_ns()

    s_transcription = i_cl_model.recognize(i_s_audio_path)

    n_elapsed_ms = (perf_counter_ns() - start_ns) / 1_000_000

    return s_transcription, n_elapsed_ms

def find_sessions(obj, path="model"):
    sessions = []

    if isinstance(obj, lib_onnx_runtime.InferenceSession):
        sessions.append((path, obj))
        return sessions

    if hasattr(obj, "__dict__"):
        for name, value in vars(obj).items():
            if isinstance(value, lib_onnx_runtime.InferenceSession):
                sessions.append((f"{path}.{name}", value))
            elif hasattr(value, "__dict__"):
                sessions.extend(find_sessions(value, f"{path}.{name}"))

    return sessions

def collect_profiles(i_cl_model):
    print("\n=== Profiling ===")

    profiles = []

    for name, session in find_sessions(i_cl_model):
        profile_path = session.end_profiling()

        print(f"{name}")
        print(f"  profile: {profile_path!r}")

        if not profile_path:
            print("  WARNING: ONNX Runtime did not return a profile path.")
            continue

        profile_path = Path(profile_path)

        if not profile_path.is_file():
            print(f"  WARNING: profile does not exist: {profile_path}")
            continue

        profiles.append((name, profile_path))

    return profiles

def analyze_profile(i_s_name: str, i_s_profile_path: Path):
    with i_s_profile_path.open("r", encoding="utf-8") as f:
        events = json.load(f)

    print(f"\n=== {i_s_name} ===")

    execution_times = {}

    for event in events:
        if event.get("ph") != "X":
            continue

        duration_us = event.get("dur", 0)

        if duration_us <= 0:
            continue

        args = event.get("args", {})

        provider = (
            args.get("provider")
            or args.get("execution_provider")
            or args.get("ep")
        )

        if provider is None:
            continue

        execution_times[provider] = (
            execution_times.get(provider, 0) + duration_us
        )

    for provider, duration_us in sorted(
        execution_times.items(),
        key=lambda x: x[1],
        reverse=True,
    ):
        print(
            f"  {provider:<30} "
            f"{duration_us / 1000:>10.2f} ms"
        )


def main():
    cl_model, load_time_ms = load_model(C_S_MODEL_PATH)

    print(f"Model load time: {load_time_ms :.0f} ms")

    s_transcript, inference_time_ms = inference(cl_model, C_S_AUDIO_PATH)

    print(f"Inference time: {inference_time_ms :.0f} ms")

    profiles = collect_profiles(cl_model)

    for name, profile_path in profiles:
        analyze_profile(name, profile_path)

    print("TRANSCRIPT: ",s_transcript)

if __name__ == "__main__":
    main()