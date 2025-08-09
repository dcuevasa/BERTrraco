import argostranslate.package
import argostranslate.translate
from ..config import TRANSLATION_CONFIG

def _setup_translation():
    """Descarga e instala modelos si es necesario."""
    from_code = TRANSLATION_CONFIG["source_lang_code"]
    to_code = TRANSLATION_CONFIG["target_lang_code"]
    
    installed_langs = argostranslate.translate.get_installed_languages()
    from_lang = next((lang for lang in installed_langs if lang.code == from_code), None)
    to_lang = next((lang for lang in installed_langs if lang.code == to_code), None)

    if from_lang and to_lang and from_lang.get_translation(to_lang) and to_lang.get_translation(from_lang):
        print(f"Modelos de traducción ({from_code} <-> {to_code}) ya están instalados.")
        return from_lang.get_translation(to_lang), to_lang.get_translation(from_lang)

    print("Modelos de traducción no encontrados. Descargando e instalando...")
    try:
        argostranslate.package.update_package_index()
        available = argostranslate.package.get_available_packages()
        
        def find_and_install(f_code, t_code):
            pkg = next((p for p in available if p.from_code == f_code and p.to_code == t_code), None)
            if pkg:
                pkg.install()
            else:
                raise ValueError(f"No se encontró paquete de {f_code} a {t_code}")

        find_and_install(from_code, to_code)
        find_and_install(to_code, from_code)
        
        # Recargar y devolver
        installed = argostranslate.translate.get_installed_languages()
        from_lang = next(lang for lang in installed if lang.code == from_code)
        to_lang = next(lang for lang in installed if lang.code == to_code)
        return from_lang.get_translation(to_lang), to_lang.get_translation(from_lang)

    except Exception as e:
        print(f"Error crítico durante la configuración de la traducción: {e}")
        exit()

# Inicialización perezosa
_es_to_en_translator, _en_to_es_translator = _setup_translation()

def translate_es_to_en(text):
    return _es_to_en_translator.translate(text)

def translate_en_to_es(text):
    return _en_to_es_translator.translate(text)