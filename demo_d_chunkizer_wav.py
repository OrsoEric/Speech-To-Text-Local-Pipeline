"""

Offline test of the Cl_transcriber sliding window on a WAV file.

The WAV is split into base chunks of 100 ms which are pushed through the
Cl_transcriber: chunk_length_stt base chunks are joined per STT call and
each scan advances the window by chunk_skip base chunks. Every decoded
window is printed with its timestamp start, timestamp end and content.
Once the file is fully consumed the trailing partial window is flushed
(padded with silence up to one full window) and the whole file is
transcribed in one pass as reference.

python demo_d_chunkizer_wav.py [model_path] [wav_path]
"""

import sys

from pathlib import Path

import numpy

from cl_asr_parakeet_v3 import Cl_asr_parakeet_v3
from cl_audio import Cl_audio, St_wav
from cl_transcriber import Cl_transcriber

C_S_MODEL_PATH = Path(r"F:\LLM Models\parakeet-tdt-0.6b-v3-onnx")
C_S_WAV_PATH = Path(r"F:\Data\Project\Project-LLM\Audio Samples\wav\SAMPLE-Ranni-18s.wav")

C_N_CHUNK_LENGTH_BASE_MS: float = 300.0
C_N_CHUNK_LENGTH_STT: int = 10
C_N_CHUNK_SKIP: int = 1


def split_wav_into_base_chunks(
    i_st_wav: St_wav,
    i_n_chunk_length_ms: float,
) -> list[St_wav]:
    """
    Splits an St_wav into consecutive base chunks of equal duration.

    The last chunk may be shorter whenever the sample count is not an exact
    multiple of the base chunk length, mirroring what happens at the end of
    a microphone stream.

    Parameters:
    i_st_wav (St_wav): Structure holding the samples to split.
    i_n_chunk_length_ms (float): Duration of one base chunk in milliseconds.

    Returns:
    List[St_wav]: Chronological list of base chunks.
    """

    n_chunk_samples = max(
        1,
        round(
            i_st_wav.n_sample_rate_hz
            * i_n_chunk_length_ms
            / 1000.0
        ),
    )

    l_chunks: list[St_wav] = []

    n_offset = 0
    while n_offset < i_st_wav.np_samples.shape[0]:
        np_chunk_samples = i_st_wav.np_samples[n_offset : n_offset + n_chunk_samples]

        l_chunks.append(
            St_wav(
                np_samples=np_chunk_samples.astype(numpy.float32),
                n_sample_rate_hz=i_st_wav.n_sample_rate_hz,
            )
        )

        n_offset += n_chunk_samples

    return l_chunks


def demo(
    i_s_model_path: Path = C_S_MODEL_PATH,
    i_s_wav_path: Path = C_S_WAV_PATH,
) -> None:
    """
    Runs the Cl_transcriber sliding window over a WAV file instead of a live
    stream.

    The function loads the model, slices the WAV into 100 ms base chunks and
    pushes them through Cl_transcriber exactly like the microphone demo does.
    Decoded windows are printed with their timestamps, the tail of the stream
    is flushed, and a single-pass transcription of the whole file is printed
    last as reference.

    Parameters:
    i_s_model_path (Path): Path of the Parakeet ONNX model directory.
    i_s_wav_path (Path): Path of the WAV file to transcribe.
    """

    cl_parakeet = Cl_asr_parakeet_v3()
    cl_parakeet.load_model(i_s_model_path, i_x_profiling=False)

    cl_audio = Cl_audio()
    st_wav = cl_audio.read_wav_file(i_s_wav_path)
    print(f"WAV: {st_wav}")

    l_chunks = split_wav_into_base_chunks(st_wav, C_N_CHUNK_LENGTH_BASE_MS)
    print(
        f"Base chunks: {len(l_chunks)}"
        f" x {C_N_CHUNK_LENGTH_BASE_MS :.0f} ms,"
        f" window={C_N_CHUNK_LENGTH_STT} chunks,"
        f" skip={C_N_CHUNK_SKIP} chunk(s)"
    )
    print()

    cl_transcriber = Cl_transcriber(
        i_cl_parakeet=cl_parakeet,
        i_n_sample_rate_hz=st_wav.n_sample_rate_hz,
        i_n_chunk_length_base_ms=C_N_CHUNK_LENGTH_BASE_MS,
        i_n_chunk_length_stt=C_N_CHUNK_LENGTH_STT,
        i_n_chunk_skip=C_N_CHUNK_SKIP,
    )

    for st_chunk in l_chunks:
        cl_transcriber.push_chunk(st_chunk)

        if not cl_transcriber.is_ready():
            continue

        cl_transcriber.scan()

    # Decode the trailing partial window so no audio is left untranscribed.
    x_flushed = cl_transcriber.flush() is not None

    print()
    print(f"Windows decoded: {cl_transcriber.n_scan_count} (flush={x_flushed})")

    print()
    s_reference, n_reference_ms = cl_parakeet.run_inference_st_wav(st_wav)
    print(f"REFERENCE ({n_reference_ms :.0f} ms): {s_reference}")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        demo(Path(sys.argv[1]), Path(sys.argv[2]))
    elif len(sys.argv) > 1:
        demo(Path(sys.argv[1]))
    else:
        demo()
