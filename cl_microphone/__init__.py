import sounddevice as sd
import numpy
from typing import List, Any
import queue

from cl_audio import St_wav

import sounddevice as sd
import numpy
from typing import List, Any
import queue

from cl_audio import St_wav


class Cl_microphone:
    """
    Lightweight microphone wrapper that enumerates available input devices,
    captures audio in real-time and wraps every captured chunk into an
    St_wav structure before enqueueing it for downstream consumers.
    """

    # ------------------------------------------------------------------
    # MEMBER VARIABLES
    # ------------------------------------------------------------------

    _input_stream: sd.InputStream | None

    # ------------------------------------------------------------------
    # INITIALIZATION
    # ------------------------------------------------------------------

    def __init__(
        self,
        i_sample_rate_hz: int = 16000,
        i_chunk_length_ms: float = 10.0,
    ) -> None:
        """
        Configure the microphone.

        Parameters:
            i_sample_rate_hz:
                Audio sampling rate in Hz.

            i_chunk_length_ms:
                Duration of each captured audio chunk in milliseconds.
                For example, 10.0 means that the callback receives
                approximately 10 ms of audio at a time.
        """
        if i_sample_rate_hz <= 0:
            raise ValueError("i_sample_rate_hz must be greater than 0.")

        if i_chunk_length_ms <= 0:
            raise ValueError("i_chunk_length_ms must be greater than 0.")

        self.cn_sample_rate: int = i_sample_rate_hz
        self.cn_chunk_length_ms: float = i_chunk_length_ms

        # Calculate number of samples/frames per callback.
        self.cn_chunk_size: int = max(
            1,
            round(
                self.cn_sample_rate
                * self.cn_chunk_length_ms
                / 1000.0
            ),
        )

        self._input_stream = None
        self.c_audio_queue: queue.Queue[St_wav] = queue.Queue()

    # ------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------

    def list_microphones(self) -> List[str]:
        """
        Enumerate all available input devices.

        Returns:
            List[str]: Human-readable names of input devices.
        """
        devices = sd.query_devices()

        input_device_names: List[str] = [
            device["name"]
            for device in devices
            if device["max_input_channels"] > 0
        ]

        return input_device_names

    def start_listening(
        self,
        i_device_index: int | None = None,
    ) -> None:
        """
        Open the microphone stream and begin capturing audio data.

        Parameters:
            i_device_index:
                Index of the desired input device. If None, the
                default system microphone is used.

        Raises:
            RuntimeError:
                If the sounddevice stream cannot be started.
        """

        # Ensure any previous stream is stopped.
        if self._input_stream is not None:
            self.stop_microphone()

        def _audio_callback(
            i_indata: numpy.ndarray,
            i_frames: int,
            i_time: Any,
            i_status: sd.CallbackFlags,
        ) -> None:
            """
            Callback invoked by sounddevice for every audio chunk.
            """

            if i_status:
                # Logging could be added here.
                pass

            np_audio_chunk = (
                numpy.array(i_indata)
                .copy()
                .squeeze()
                .astype(numpy.float32)
            )

            st_chunk = St_wav(
                np_samples=np_audio_chunk,
                n_sample_rate_hz=self.cn_sample_rate,
            )

            self.c_audio_queue.put(st_chunk)

        try:
            self._input_stream = sd.InputStream(
                samplerate=self.cn_sample_rate,
                channels=1,
                device=i_device_index,
                callback=_audio_callback,
                blocksize=self.cn_chunk_size,
            )

            self._input_stream.start()

        except sd.PortAudioError as exc:
            self._input_stream = None
            raise RuntimeError(
                f"Failed to start microphone stream: {exc}"
            ) from exc

    def stop_microphone(self) -> None:
        """
        Terminate the active microphone capture session.
        """
        if self._input_stream is not None:
            try:
                self._input_stream.stop()
                self._input_stream.close()
            finally:
                self._input_stream = None

    def get_audio_queue(self) -> queue.Queue[St_wav]:
        """
        Retrieve the queue containing captured audio chunks.
        """
        return self.c_audio_queue