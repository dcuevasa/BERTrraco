import os
import random
from pydub import AudioSegment
from ..config import AUDIO_CONFIG

def _load_samples(folder: str):
    try:
        files = sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith((".wav", ".mp3", ".m4a"))])
        if not files: return []
        
        segs = []
        for p in files:
            seg = AudioSegment.from_file(p).set_frame_rate(44100).set_sample_width(2).set_channels(1)
            if len(seg) > 30: seg = seg[15:-15] # Limpiar clics
            segs.append(seg)
        return segs
    except FileNotFoundError:
        return []

_animalese_samples = _load_samples(AUDIO_CONFIG["samples_folder"])
if not _animalese_samples:
    print(f"ADVERTENCIA: No se encontraron audios en '{AUDIO_CONFIG['samples_folder']}'. La voz estará desactivada.")

def has_audio_samples():
    return bool(_animalese_samples)

def _change_pitch(seg, semitones):
    speed_factor = 2 ** (semitones / 12.0)
    new_rate = int(seg.frame_rate * speed_factor)
    return seg._spawn(seg.raw_data, overrides={"frame_rate": new_rate}).set_frame_rate(44100)

def text_to_animalese(text: str) -> AudioSegment:
    if not _animalese_samples:
        return AudioSegment.silent(duration=10)

    out = AudioSegment.silent(duration=0)
    silence = AudioSegment.silent(duration=AUDIO_CONFIG["gap_ms"])
    pitch_range = AUDIO_CONFIG["pitch_range_semitones"]

    for char in text:
        if char.isspace():
            out += AudioSegment.silent(duration=80)
            continue
        
        base_sample = random.choice(_animalese_samples)
        semitone_shift = random.uniform(-pitch_range, pitch_range)
        pitched_sample = _change_pitch(base_sample, semitone_shift)
        out += pitched_sample + silence
        
    return out.fade_in(5).fade_out(50)