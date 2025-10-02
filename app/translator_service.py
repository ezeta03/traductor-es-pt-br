from deep_translator import GoogleTranslator

def translate_text(text: str) -> str:
    translator = GoogleTranslator(source="es", target="en")
    return translator.translate(text)
