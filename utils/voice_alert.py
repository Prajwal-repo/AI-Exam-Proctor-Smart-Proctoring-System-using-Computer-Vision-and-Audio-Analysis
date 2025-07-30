import torch
import sounddevice as sd
import numpy as np
import torchaudio
import os
from datetime import datetime

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Singleton pattern
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
(get_speech_ts, _, read_audio, _, _) = utils

def is_voice_detected(duration=3, sample_rate=16000):
    try:
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()
        audio = torch.tensor(recording.T)
        speech_ts = get_speech_ts(audio, model, sampling_rate=sample_rate)
        if speech_ts:
            return True, f"{datetime.now().strftime('%H:%M:%S')} - Voice detected for {duration} sec"
        return False, ""
    except Exception as e:
        print("Voice detection error:", e)
        return False
