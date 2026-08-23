#

from pathlib import Path
import onnx_asr
import onnxruntime as ort

print("ONNX Runtime:", ort.__version__)
print("Available:", ort.get_available_providers())

cl_model = onnx_asr.load_model(
    "nemo-parakeet-tdt-0.6b-v3",
    Path(r"F:\LLM Models\parakeet-tdt-0.6b-v3-onnx")
)

s_transcript : str = cl_model.recognize(Path(r"F:\Data\Project\Project-LLM\Audio Samples\wav\SAMPLE-Ranni-18s.wav"))

print(s_transcript)
