uv venv .venv --python 3.13

call .venv\Scripts\activate.bat

uv pip install onnx-asr
uv pip install onnxruntime
uv pip install huggingface_hub