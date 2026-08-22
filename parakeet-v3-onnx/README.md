# install

uv venv .venv --python 3.13

.venv\Scripts\activate

uv pip install onnx-asr
uv pip install onnxruntime
uv pip install huggingface_hub

# sample

F:\Data\Project\Project-LLM\Audio Samples\wav\SAMPLE-Ranni-18s.wav

# run

set HF_HUB_DISABLE_XET=1

python 2026-08-22a.py 

# folder

I can add model folder

cache works different from download and mangle the names... WHY????????

I redownload the small pieces and rename the big one. 

git clone https://huggingface.co/istupakov/parakeet-tdt-0.6b-v3-onnx

# Working wav transcription

<details>
<summary>Logs</summary>

```cmd
(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>uv pip install onnx-asr
Resolved 2 packages in 177ms
░░░░░░░░░░░░░░░░░░░░ [0/2] Installing wheels...                warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 2 packages in 533ms
 + numpy==2.5.2
 + onnx-asr==0.12.0

(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>uv pip install onnxruntime
Resolved 5 packages in 95ms
░░░░░░░░░░░░░░░░░░░░ [0/4] Installing wheels...                warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 4 packages in 277ms
 + flatbuffers==25.12.19
 + onnxruntime==1.29.0
 + packaging==26.3
 + protobuf==7.36.0

(.venv) F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline>python parakeet-v3-onnx\2026-08-22a.py
F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline\parakeet-v3-onnx\2026-08-22a.py:2: SyntaxWarning: invalid escape sequence '\L'
  model = onnx_asr.load_model("nemo-parakeet-tdt-0.6b-v3","F:\LLM Models\parakeet-tdt-0.6b-v3-onnx")
F:\Data\Project\Project-LLM\STT_Models\Speech-To-Text-Local-Pipeline\parakeet-v3-onnx\2026-08-22a.py:3: SyntaxWarning: invalid escape sequence '\D'
  print(model.recognize("F:\Data\Project\Project-LLM\Audio Samples\wav\SAMPLE-Ranni-18s.wav"))
I was entrusted this for thee by Torrent's former master.'Tis a bell for calling forth spirits. Summon them with it. From ash and return to the earth tree. The spirits will obey thine command but briefly. As they recall battles past,
```

</details>

# EOL

<details>
<summary>Logs</summary>

```cmd
xxx
```

</details>