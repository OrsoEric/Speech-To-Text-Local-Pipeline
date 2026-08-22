# WebGPU

## CPU

(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>uv pip install onnxruntime-webgpu
Resolved 5 packages in 365ms
Prepared 1 package in 3.69s
░░░░░░░░░░░░░░░░░░░░ [0/1] Installing wheels...                warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 1 package in 169ms
 + onnxruntime-webgpu==1.27.0

(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>python parakeet-v3-onnx/2026-08-22b-test-onnx-inference.py
['WebGpuExecutionProvider', 'CPUExecutionProvider']
Model load time: 2823 ms
Inference time: 3428 ms
TRANSCRIPT:  I was entrusted this for thee by Torrent's former master.'Tis a bell for calling forth spirits. Summon them with it. From ash and return to the earth tree. The spirits will obey thine command but briefly. As they recall battles past,

## WebGPU

Model load time: 5592 ms
Inference time: 1708 ms

(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>python parakeet-v3-onnx/2026-08-22b-test-onnx-inference.py
['WebGpuExecutionProvider', 'CPUExecutionProvider']
2026-08-22 12:10:38.2144016 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:10:38.2185123 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:10:38.6900415 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:10:38.6959665 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:10:40.9955870 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:10:41.0139993 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:10:41.0470374 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:10:41.5899491 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:10:41.6227590 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:10:41.7230782 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:10:41.7387833 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:10:42.2114789 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:10:42.2227422 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:10:42.4301010 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:10:42.4424182 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:10:42.8884224 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:10:42.9001352 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:10:43.1169455 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:10:43.1269032 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:10:43.5778154 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
Model load time: 5592 ms
Inference time: 1708 ms
TRANSCRIPT:  I was entrusted this for thee by Torrent's former master.'Tis a bell for calling forth spirits. Summon them with it. From ash and return to the earth tree. The spirits will obey thine command but briefly. As they recall battles past,

# DEBUG ONNX

def find_sessions(obj, path="model"):
    if isinstance(obj, lib_onnx_runtime.InferenceSession):
        print(path)
        print("  providers:", obj.get_providers())
        return

    if hasattr(obj, "__dict__"):
        for name, value in vars(obj).items():
            if isinstance(value, lib_onnx_runtime.InferenceSession):
                print(f"{path}.{name}")
                print("  providers:", value.get_providers())
            elif hasattr(value, "__dict__"):
                find_sessions(value, f"{path}.{name}")


(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>python parakeet-v3-onnx/2026-08-22b-test-onnx-inference.py
['WebGpuExecutionProvider', 'CPUExecutionProvider']
2026-08-22 12:14:40.8185357 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:14:40.8208993 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:14:41.2951951 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:14:41.3045494 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:14:43.5140402 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:14:43.5196682 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:14:43.5524410 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:14:44.1266896 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:14:44.1535677 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:14:44.2334261 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:14:44.2462044 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:14:44.7240074 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:14:44.7362851 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:14:44.9628388 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:14:44.9702035 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:14:45.3977636 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:14:45.4100792 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:14:45.6340799 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
2026-08-22 12:14:45.6459437 [W:onnxruntime:, session_state.cc:1367 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Some nodes were not assigned to the preferred execution providers which may or may not have an negative impact on performance. e.g. ORT explicitly assigns shape related ops to CPU to improve perf.
2026-08-22 12:14:46.1244825 [W:onnxruntime:, session_state.cc:1369 onnxruntime::VerifyEachNodeIsAssignedToAnEp] Rerunning with verbose output on a non-minimal build will show node assignments.
model.asr._preprocessor._preprocessor
  providers: ['WebGpuExecutionProvider', 'CPUExecutionProvider']
model.asr._encoder
  providers: ['WebGpuExecutionProvider', 'CPUExecutionProvider']
model.asr._decoder_joint
  providers: ['WebGpuExecutionProvider', 'CPUExecutionProvider']
Model load time: 5492 ms
Inference time: 1158 ms
TRANSCRIPT:  I was entrusted this for thee by Torrent's former master.'Tis a bell for calling forth spirits. Summon them with it. From ash and return to the earth tree. The spirits will obey thine command but briefly. As they recall battles past,

You have confirmed that all three ONNX Runtime sessions used by onnx_asr have WebGPU registered:


---

# DEBUG WebGPU

ok, this is cool that I get a diagnostics

Model load time: 5598 ms
Inference time: 1293 ms

=== NODE EXECUTION INSPECTION ===

model.asr._preprocessor._preprocessor
  Profile: 'onnxruntime_profile__2026-08-22_12-34-06_118.json'
  Events: 88

  Execution by provider:
    WebGpuExecutionProvider           255.54 ms   (38 events)
    CPUExecutionProvider                0.64 ms   (12 events)

model.asr._encoder
  Profile: 'onnxruntime_profile__2026-08-22_12-34-06_236.json'
  Events: 3311

  Execution by provider:
    WebGpuExecutionProvider           524.79 ms   (1511 events)
    CPUExecutionProvider                8.65 ms   (496 events)

model.asr._decoder_joint
  Profile: 'onnxruntime_profile__2026-08-22_12-34-08_957.json'
  Events: 5531

  Execution by provider:
    WebGpuExecutionProvider           165.17 ms   (2522 events)
    CPUExecutionProvider                1.37 ms   (97 events)