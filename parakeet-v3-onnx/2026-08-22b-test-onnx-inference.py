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

    cl_session_options = lib_onnx_runtime.SessionOptions()
    cl_session_options.enable_profiling = True

    #increase verbosirty
    #lib_onnx_runtime.set_default_logger_severity(1)
    
    cl_model = onnx_asr.load_model(
        "nemo-parakeet-tdt-0.6b-v3",
        i_s_model_path,
        providers=C_S_ONNX_EXECUTION_PROVIDERS,
        sess_options=cl_session_options,
    )
    #restore verbosity
    #lib_onnx_runtime.set_default_logger_severity(2)

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


def inspect_profiles(i_cl_model):
    print()
    print("=== NODE EXECUTION INSPECTION ===")

    for name, session in find_sessions(i_cl_model):

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

        inspect_profile_events(
            name,
            events,
        )


def inspect_profile_events(i_s_session_name, i_events):
    """
    Print the execution-provider information contained
    in ONNX Runtime profiling events.
    """

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

        # Print a representative event so we can inspect the
        # schema used by this particular ONNX Runtime build.
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


def main():
    cl_model, load_time_ms = load_model(C_S_MODEL_PATH)

    print(f"Model load time: {load_time_ms :.0f} ms")

    s_transcript, inference_time_ms = inference(cl_model, C_S_AUDIO_PATH)

    print(f"Inference time: {inference_time_ms :.0f} ms")

    inspect_profiles(cl_model)

    print("TRANSCRIPT: ",s_transcript)

if __name__ == "__main__":
    main()