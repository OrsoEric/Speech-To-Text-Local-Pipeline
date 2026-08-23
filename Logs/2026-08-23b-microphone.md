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

# add St_vaw

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
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.010899, rms=0.011122
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008749, rms=0.009572
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.006240, rms=0.007374
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=-0.000350, rms=0.002427
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.003828, rms=0.005531
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008608, rms=0.008909
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.012348, rms=0.012670
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.013458, rms=0.014065
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.006685, rms=0.007223
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008302, rms=0.008510
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008155, rms=0.008579
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.004542, rms=0.005442
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.006208, rms=0.006744
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.005939, rms=0.006596
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008193, rms=0.008542
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.009606, rms=0.009931
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.010341, rms=0.010635
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.011454, rms=0.011917
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008997, rms=0.009332
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.005205, rms=0.005526
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008349, rms=0.008714
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.007228, rms=0.007997
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.006645, rms=0.007466
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008512, rms=0.009231
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.004858, rms=0.005679
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.006574, rms=0.007999
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.009764, rms=0.012192
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.009499, rms=0.009988
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.006340, rms=0.006567
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008287, rms=0.009873
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.006699, rms=0.195300
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.007927, rms=0.222055
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008088, rms=0.014838
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008232, rms=0.010851
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.010176, rms=0.012026
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.007635, rms=0.011970
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.003552, rms=0.005172
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.002142, rms=0.003364
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008885, rms=0.009145
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.010512, rms=0.011030
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.006071, rms=0.006375
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.023091, rms=0.055372
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=-0.008190, rms=0.048588
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.006537, rms=0.073748
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.009081, rms=0.087067
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008343, rms=0.079796
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.007678, rms=0.078170
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.007524, rms=0.085038
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.003678, rms=0.104031
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.005891, rms=0.106809
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.017028, rms=0.045879
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008412, rms=0.023080
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008847, rms=0.029251
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.020283, rms=0.177565
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.002072, rms=0.227295
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=-0.022966, rms=0.238157
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.005200, rms=0.147454
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.002189, rms=0.138255
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.026100, rms=0.144259
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.026294, rms=0.137641
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.015933, rms=0.106705
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=-0.011639, rms=0.026480
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.022165, rms=0.022979
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008664, rms=0.010266
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=-0.002055, rms=0.003734
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.001206, rms=0.002084
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.010078, rms=0.011775
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.012515, rms=0.013024
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.003256, rms=0.003802
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.000321, rms=0.069033
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.010401, rms=0.072982
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.006368, rms=0.041001
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.009645, rms=0.023507
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.007905, rms=0.020568
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.005903, rms=0.048031
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=-0.007651, rms=0.129138
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.001977, rms=0.150893
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008882, rms=0.162188
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.007649, rms=0.152453
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.011740, rms=0.154249
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.010028, rms=0.153458
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=-0.000515, rms=0.134653
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.006642, rms=0.149097
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.021178, rms=0.160693
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.014583, rms=0.157620
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.007973, rms=0.119535
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.014116, rms=0.160394
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.008054, rms=0.078995
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.007802, rms=0.023992
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.007417, rms=0.011604
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.005007, rms=0.006920
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.005929, rms=0.006562
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.009361, rms=0.009938
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.004436, rms=0.004938
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.005644, rms=0.006186
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.006721, rms=0.017251
Chunk: WAV: duration=0.010 s, sample_rate=16000 Hz, samples=160, avg=0.007534, rms=0.009479

# fine tune

change core sampling parameter 