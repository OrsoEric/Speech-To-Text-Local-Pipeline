import sounddevice as sd
import numpy
from typing import List, Tuple, Any
import queue


class Cl_microphone:
    """
    A lightweight microphone wrapper that enumerates available input devices,
    captures audio in real‑time and enqueues the raw samples for downstream
    consumers.  The implementation is deliberately minimal – it does **not**
    perform voice activity detection or any advanced signal processing.
    """

    # ------------------------------------------------------------------
    # CONSTANTS
    # ------------------------------------------------------------------
    cn_sample_rate: int = 16000  #: Default sample rate used by all streams (Hz)

    # ------------------------------------------------------------------
    # MEMBER VARIABLES
    # ------------------------------------------------------------------
    _input_stream: sd.InputStream | None = None                 #: Internal sounddevice stream instance
    c_audio_queue: queue.Queue[Tuple[numpy.ndarray, bool]] = queue.Queue()   #: Queue for raw audio samples

    # ------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------

    def list_microphones(self) -> List[str]:
        """
        Enumerate all available input devices on the system.

        Returns:
            List[str]: A list containing the human‑readable names of each
                       microphone device that can be used with sounddevice.
        """
        devices = sd.query_devices()
        input_device_names: List[str] = [
            device["name"] for device in devices if device["max_input_channels"] > 0
        ]
        return input_device_names

    def start_listening(self, i_device_index: int | None = None) -> None:
        """
        Open the microphone stream and begin capturing audio data.

        Captured samples are immediately placed on ``c_audio_queue``.  The
        method will first terminate any previously opened stream to avoid
        resource leaks.

        Parameters:
            i_device_index (int | None): Index of the desired input device.
                                         If omitted, the default system microphone
                                         is used.

        Raises:
            RuntimeError: If a sounddevice stream cannot be started.
        """
        # Ensure any previous stream is stopped before starting a new one.
        if self._input_stream is not None:
            self.stop_microphone()

        def _audio_callback(
            i_indata: numpy.ndarray,
            i_frames: int,
            i_time: Any,
            i_status: sd.CallbackFlags,
        ) -> None:
            """
            Internal callback fed by sounddevice. It receives raw audio frames
            and enqueues them for further processing.

            Parameters:
                i_indata (numpy.ndarray): Raw audio input buffer.
                i_frames (int): Number of frames in the current chunk.
                i_time (Any): Timing information (unused).
                i_status (sd.CallbackFlags): Status flags indicating errors or
                                             under‑/overflow conditions.
            """
            if i_status:
                # Logging is omitted to keep this snippet self‑contained,
                # but a real implementation should record status details.
                pass

            # Strip any singleton dimensions and copy the data to avoid
            # shared memory between threads.
            l_audio_chunk = numpy.array(i_indata).copy().squeeze()
            # The bool flag is placeholder; it could be used for VAD results in
            # future extensions.  For now, we simply mark all frames as "valid".
            b_valid_frame: bool = True
            self.c_audio_queue.put((l_audio_chunk, b_valid_frame))

        # Determine blocksize so that the callback receives at least a few
        # milliseconds of audio (here ~10 ms).
        i_blocksize: int = int(self.cn_sample_rate * 0.01)

        try:
            self._input_stream = sd.InputStream(
                samplerate=self.cn_sample_rate,
                channels=1,
                device=i_device_index,
                callback=_audio_callback,
                blocksize=i_blocksize,
            )
            self._input_stream.start()
        except sd.PortAudioError as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to start microphone stream: {exc}") from exc

    def stop_microphone(self) -> None:
        """
        Terminate the active microphone capture session.

        If a stream is running it will be stopped and closed, ensuring that
        resources such as audio devices are released cleanly.
        """
        if self._input_stream is not None:
            try:
                self._input_stream.stop()
                self._input_stream.close()
            finally:
                self._input_stream = None

    def get_audio_queue(self) -> queue.Queue[Tuple[numpy.ndarray, bool]]:
        """
        Retrieve the internal queue that stores captured audio samples.

        Returns:
            queue.Queue: The thread‑safe queue holding tuples of
                         (audio_buffer, validity_flag).
        """
        return self.c_audio_queue
