from langchain_community.llms import Ollama
import os

# --- Configuración General de la Aplicación ---
APP_CONFIG = {
    "title": "BERTraco Asistente",
    "queue_max_size": 10
}

# --- Configuración del Modelo de Lenguaje (LLM) ---
LLM_CONFIG = {
    "model_name": "qwen:0.5b",
    "model": Ollama(model="qwen:0.5b")
}

# --- Configuración del Historial de Chat ---
HISTORY_CONFIG = {
    "max_exchanges": 3 # Mantiene los últimos 3 intercambios (pregunta + respuesta)
}

# --- Configuración de la Traducción ---
TRANSLATION_CONFIG = {
    "source_lang_code": "es",
    "target_lang_code": "en"
}

# --- Configuración de la Voz (Animalese) ---
AUDIO_CONFIG = {
    "samples_folder": os.path.join(os.path.dirname(__file__), "../audios"),
    "pitch_range_semitones": 4,
    "gap_ms": 10
}

# --- Configuración de la Interfaz de Usuario (Cara) ---
FACE_UI = {
    "canvas_width": 200,
    "canvas_height": 200,
    "bg_color": "white",
    "eye1_coords": (45, 50, 85, 80),
    "eye2_coords": (115, 50, 155, 80),
    "pupil1_coords": (58, 58, 72, 72),
    "pupil2_coords": (128, 58, 142, 72),
    "mouth_y": 130,
    "mouth_x1": 70,
    "mouth_x2": 130,
    "mouth_open_height": 145,
    "tongue_coords": (85, 135, 115, 170)
}

# --- Configuración de Animaciones ---
ANIMATION_CONFIG = {
    "interval_ms": 500,
    "idle_delay_min_s": 1.5,
    "idle_delay_max_s": 5.0,
    "sleep_timeout_s": 10.0
}