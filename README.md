# Speech-To-Text-Local-Pipeline

Develop a local speech to text pipeline

# ONNX

## onnxruntime 

```cmd
uv pip install onnxruntime
```
['AzureExecutionProvider', 'CPUExecutionProvider']
Model load time: 2869 ms
Inference time: 3364 ms

## onnxruntime-rocm

```cmd
(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>uv pip install onnxruntime-rocm  
  × No solution found when resolving dependencies:
  ╰─▶ Because onnxruntime-rocm==1.22.1 has no wheels with a
      matching Python ABI tag (e.g., `cp313`) and only the
      following versions of onnxruntime-rocm are available:
          onnxruntime-rocm==1.22.1
          onnxruntime-rocm>=1.22.2.post1
      we can conclude that onnxruntime-rocm<1.22.2.post1
      cannot be used.
      And because onnxruntime-rocm>=1.22.2.post1 has no
      wheels with a matching platform tag (e.g., `win_amd64`)
      and you require onnxruntime-rocm, we can conclude that
      your requirements are unsatisfiable.

hint: You require CPython 3.13 (`cp313`), but we only found wheels for `onnxruntime-rocm` (v1.22.1) with the following Python ABI tag: `cp310`
hint: Wheels are available for `onnxruntime-rocm` (v1.22.2.post3) on the following platform: `manylinux_2_34_x86_64`
```

## onnxruntime-webgpu

```cmd
(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>uv pip install onnxruntime-webgpu
Resolved 5 packages in 365ms
Prepared 1 package in 3.69s
░░░░░░░░░░░░░░░░░░░░ [0/1] Installing wheels...                warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 1 package in 169ms
 + onnxruntime-webgpu==1.27.0
```

# Parakeet V3

## Installation

```cmd
uv venv .venv --python 3.13

call .venv\Scripts\activate.bat

uv pip install onnx-asr
uv pip install onnxruntime
uv pip install huggingface_hub
```

## Download Model

```cmd
git clone https://huggingface.co/istupakov/parakeet-tdt-0.6b-v3-onnx
```

## TEST A - SIMPLE INFERENCE

```cmd
python parakeet-v3-onnx/2026-08-22a-test-onnx-inference.py
```

```
(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>python parakeet-v3-onnx/2026-08-22a-test-onnx-inference.py
F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline\parakeet-v3-onnx\2026-08-22a-test-onnx-inference.py:4: SyntaxWarning: invalid escape sequence '\L'
  model = onnx_asr.load_model("nemo-parakeet-tdt-0.6b-v3","F:\LLM Models\parakeet-tdt-0.6b-v3-onnx")
F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline\parakeet-v3-onnx\2026-08-22a-test-onnx-inference.py:5: SyntaxWarning: invalid escape sequence '\D'
  print(model.recognize(Path("F:\Data\Project\Project-LLM\Audio Samples\wav\SAMPLE-Ranni-18s.wav")))
I was entrusted this for thee by Torrent's former master.'Tis a bell for calling forth spirits. Summon them with it. From ash and return to the earth tree. The spirits will obey thine command but briefly. As they recall battles past,
```

# TEST B

```cmd
python parakeet-v3-onnx/2026-08-22b-test-onnx-inference.py
```

# EOL

<details>
<summary>Logs</summary>

```cmd
xxx
```

</details>