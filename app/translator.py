from deep_translator import GoogleTranslator

def translate_text(text: str) -> str:
    translator = GoogleTranslator(source="es", target="pt")
    return translator.translate(text)
