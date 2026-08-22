# Speech-To-Text-Local-Pipeline

Develop a local speech to text pipeline


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

# EOL

<details>
<summary>Logs</summary>

```cmd
xxx
```

</details>