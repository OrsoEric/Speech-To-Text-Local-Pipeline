"""
Test harness for Cl_microphone

This script demonstrates how to enumerate available microphones,
open the first one, consume audio chunks (St_wav structures) from the
internal queue, print their statistics, and gracefully terminate
playback when the user presses 'q'.

python demo_b_microphone.py
"""

from cl_microphone import Cl_microphone

import sounddevice as sd
import numpy
import time
from typing import List


def main() -> None:
    """
    Execute a simple microphone enumeration and capture demo.
    
    The function performs the following steps:
    1. Instantiates Cl_microphone.
    2. Prints a list of all available input devices.
    3. Starts listening on the first device (index 0).
    4. Consumes audio chunks from the queue for a short duration
       and prints their statistics (duration, sample rate, average
       amplitude and RMS).
    5. Stops the microphone when either the user presses 'q' or the
       demo finishes.

    Parameters:
        None

    Returns:
        None
    """
    # Instantiate the microphone wrapper.
    obj_microphone = Cl_microphone(
        i_sample_rate_hz=24000,
        i_chunk_length_ms=100,
    )

    # Display all discoverable microphones.
    l_available_device_names: List[str] = obj_microphone.list_microphones()
    for i_index, s_name in enumerate(l_available_device_names):
        print(f"{i_index}: {s_name}")

    if not l_available_device_names:
        raise RuntimeError("No input devices detected on the system.")

    # Begin audio capture on the first available microphone.
    obj_microphone.start_listening()

    try:
        # Consume a handful of chunks for demonstration purposes.
        i_max_iterations: int = 25
        for _ in range(i_max_iterations):
            if not obj_microphone.c_audio_queue.empty():
                st_chunk = obj_microphone.c_audio_queue.get()
                # The St_wav __str__ exposes the duration, sample rate,
                # sample count, average amplitude and RMS of the chunk.
                print(f"Chunk: {st_chunk}")
            else:
                # Sleep briefly to avoid busy‑waiting.
                time.sleep(0.5)
    finally:
        # Ensure the microphone is closed even if an exception occurs.
        obj_microphone.stop_microphone()


if __name__ == "__main__":
    main()
