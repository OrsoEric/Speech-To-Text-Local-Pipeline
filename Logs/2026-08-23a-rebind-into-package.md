#
  
  File "F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline\demo_a_file_parakeet_v3.py", line 272, in <module>
    demo_a_file_parakeet_v3()
    ~~~~~~~~~~~~~~~~~~~~~~~^^
  File "F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline\demo_a_file_parakeet_v3.py", line 262, in demo_a_file_parakeet_v3
    np_waveform, n_sample_rate = read_wav_as_float32_mono(i_s_wav_path)
                                 ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline\demo_a_file_parakeet_v3.py", line 241, in read_wav_as_float32_mono
    dtype=C_DTYPE_BY_SAMPLE_WIDTH[n_sample_width],
          ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
KeyError: 3

# demo now runs

(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>python demo_a_file_parakeet_v3.py 
Available providers: ['WebGpuExecutionProvider', 'CPUExecutionProvider']
Model load time: 2852 ms
DEMO1: load file directly
Inference time: 3156 ms
TRANSCRIPT:  I was entrusted this for thee by Torrent's former master.'Tis a bell for calling forth spirits. Summon them with it. From ash and return to the earth tree. The spirits will obey thine command but briefly. As they recall battles past,
DEMO2: from file extract wav, then feed wav to model
Raw inference time: 1132 ms
TRANSCRIPT RAW:  I was entrusted this for thee by Torrent's former master.'Tis a bell for calling forth spirits. Summon them with it. From ash and return to the earth tree. The spirits will obey thine command but briefly. As they recall battles past,