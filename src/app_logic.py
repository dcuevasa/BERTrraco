import time
import simpleaudio as sa
from langchain_core.messages import HumanMessage, AIMessage

from .config import LLM_CONFIG, HISTORY_CONFIG
from .llm.prompt_builder import build_prompt
from .services.translation_service import translate_es_to_en, translate_en_to_es
from .services.audio_service import text_to_animalese, has_audio_samples

def chat_loop(ui_controller, message_queue, audio_queue):
    """Maneja la lógica de chat: traducción, LLM y simulación de streaming."""
    historial_en = []
    llm = LLM_CONFIG["model"]

    while True:
        try:
            pregunta_es = message_queue.get()
            if pregunta_es is None:
                audio_queue.put(None)
                break

            ui_controller.wake_up()
            
            pregunta_en = translate_es_to_en(pregunta_es)
            
            mensajes = build_prompt(pregunta_en, historial_en)
            
            respuesta_en_completa = "".join(llm.stream(mensajes))
            respuesta_es_completa = translate_en_to_es(respuesta_en_completa)

            ui_controller.start_speaking()
            ui_controller.start_assistant_message()
            
            palabras_es = respuesta_es_completa.split()
            for palabra in palabras_es:
                ui_controller.append_assistant_message(f"{palabra} ")
                if has_audio_samples():
                    audio_queue.put(palabra)
                time.sleep(0.1)
            
            sa.stop_all()
            while not audio_queue.empty(): audio_queue.get()

            ui_controller.stop_speaking()
            ui_controller.end_assistant_message()
            
            historial_en.extend([HumanMessage(content=pregunta_en), AIMessage(content=respuesta_en_completa)])
            historial_en = historial_en[-HISTORY_CONFIG["max_exchanges"] * 2:]

        except Exception as e:
            print(f"Error en el chat_loop: {e}")
            audio_queue.put(None)
            break

def audio_loop(audio_queue):
    """Procesa la cola de audio para generar y reproducir sonidos."""
    if not has_audio_samples():
        while audio_queue.get() is not None: pass
        return

    while True:
        text_chunk = audio_queue.get()
        if text_chunk is None:
            break
        
        audio_segment = text_to_animalese(text_chunk)
        play_obj = sa.play_buffer(
            audio_segment.raw_data, audio_segment.channels,
            audio_segment.sample_width, audio_segment.frame_rate
        )
        play_obj.wait_done()