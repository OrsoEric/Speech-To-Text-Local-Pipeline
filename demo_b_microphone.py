"""
Test harness for Cl_microphone

This script demonstrates how to enumerate available microphones,
open the first one, consume audio samples from the internal queue,
and gracefully terminate playback when the user presses 'q'.

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
    4. Consumes audio samples from the queue for a short duration
       and prints basic statistics.
    5. Stops the microphone when either the user presses 'q' or the
       demo finishes.

    Parameters:
        None

    Returns:
        None
    """
    # Instantiate the microphone wrapper.
    obj_microphone = Cl_microphone()

    # Display all discoverable microphones.
    l_available_device_names: List[str] = obj_microphone.list_microphones()
    for i_index, s_name in enumerate(l_available_device_names):
        print(f"{i_index}: {s_name}")

    if not l_available_device_names:
        raise RuntimeError("No input devices detected on the system.")

    # Begin audio capture on the first available microphone.
    obj_microphone.start_listening()

    try:
        # Consume a handful of samples for demonstration purposes.
        i_max_iterations: int = 100
        for _ in range(i_max_iterations):
            if not obj_microphone.c_audio_queue.empty():
                t_sample, b_validity_flag = obj_microphone.c_audio_queue.get()
                print(f"Received {t_sample.shape[0]} samples with validity={b_validity_flag}")
            else:
                # Sleep briefly to avoid busy‑waiting.
                time.sleep(0.5)
    finally:
        # Ensure the microphone is closed even if an exception occurs.
        obj_microphone.stop_microphone()


if __name__ == "__main__":
    main()
