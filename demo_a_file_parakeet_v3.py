"""

python demo_a_file_parakeet_v3.py


"""

import sys

from pathlib import Path

from cl_asr_parakeet_v3 import Cl_asr_parakeet_v3
from cl_audio import Cl_audio

C_S_MODEL_PATH = Path(r"F:\LLM Models\parakeet-tdt-0.6b-v3-onnx")
C_S_WAV_PATH = Path(r"F:\Data\Project\Project-LLM\Audio Samples\wav\SAMPLE-Ranni-18s.wav")

def demo(i_s_wav_path: Path = C_S_WAV_PATH):
    """
    Loads the Parakeet model and runs two transcription demos on the same WAV file.

    DEMO1 lets the ASR class open the file itself while DEMO2 opens the file
    beforehand as an St_wav structure and feeds it to the model.

    Parameters:
    i_s_wav_path (Path): Path of the WAV file to transcribe.
    """

    cl_parakeet = Cl_asr_parakeet_v3()
    cl_parakeet.load_model(C_S_MODEL_PATH,i_x_profiling=False)

    cl_parakeet.inspect_provider_details()

    if False:
        print("DEMO1: load file directly")

        s_transcript, n_inference_ms = cl_parakeet.run_inference_file(i_s_wav_path)
        print(f"Audio read time: {cl_parakeet.n_last_read_time_ms :.0f} ms")
        print(f"Inference time: {n_inference_ms :.0f} ms")
        print("TRANSCRIPT: ", s_transcript)

    print("DEMO2: open file as St_wav, then feed wav to model")

    cl_audio = Cl_audio()
    st_wav = cl_audio.read_wav_file(i_s_wav_path)
    print(f"WAV: {st_wav}")

    s_transcript_raw, n_raw_ms = cl_parakeet.run_inference_st_wav(st_wav)
    print(f"Raw inference time: {n_raw_ms :.0f} ms")
    print("TRANSCRIPT RAW: ", s_transcript_raw)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        demo(Path(sys.argv[1]))
    else:
        demo()
