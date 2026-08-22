#
import onnx_asr
model = onnx_asr.load_model("nemo-parakeet-tdt-0.6b-v3","F:\LLM Models\parakeet-tdt-0.6b-v3-onnx")
print(model.recognize("F:\Data\Project\Project-LLM\Audio Samples\wav\SAMPLE-Ranni-18s.wav"))