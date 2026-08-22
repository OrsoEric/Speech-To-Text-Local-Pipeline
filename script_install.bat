uv venv .venv --python 3.13

.venv\Scripts\activate

uv pip install onnx-asr
uv pip install onnxruntime
uv pip install huggingface_hub