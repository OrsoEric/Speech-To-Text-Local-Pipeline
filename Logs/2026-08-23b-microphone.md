I had a class made for microphone, test it

# dependencies

(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>uv pip install sounddevice
Resolved 3 packages in 408ms
Prepared 3 packages in 146ms
░░░░░░░░░░░░░░░░░░░░ [0/3] Installing wheels...                warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 3 packages in 41ms
 + cffi==2.1.1
 + pycparser==3.0
 + sounddevice==0.5.6

# demo

(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>python demo_b_microphone.py
0: Microsoft Sound Mapper - Input
1: Microphone (Trust GXT234 YUNIX 
2: Primary Sound Capture Driver
3: Microphone (Trust GXT234 YUNIX Microphone)
4: Microphone (Trust GXT234 YUNIX Microphone)
5: Stereo Mix (Realtek HD Audio Stereo input)
6: Line In (Realtek HD Audio Line input)
7: Microphone (Realtek HD Audio Mic input)
8: Microphone (Trust GXT234 YUNIX Microphone)
Received 160 samples with validity=True
Received 160 samples with validity=True
Received 160 samples with validity=True
Received 160 samples with validity=True
Received 160 samples with validity=True
Received 160 samples with validity=True
Received 160 samples with validity=True
Received 160 samples with validity=True
Received 160 samples with validity=True