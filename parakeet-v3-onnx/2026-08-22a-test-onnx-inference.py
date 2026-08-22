#
import onnx_asr
from pathlib import Path


cl_model = onnx_asr.load_model(
    "nemo-parakeet-tdt-0.6b-v3",
    Path(r"F:\LLM Models\parakeet-tdt-0.6b-v3-onnx")
)

s_transcript : str = cl_model.recognize(Path(r"F:\Data\Project\Project-LLM\Audio Samples\wav\SAMPLE-Ranni-18s.wav"))

print(s_transcript)