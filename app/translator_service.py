from deep_translator import GoogleTranslator

def translate_text(text: str, source: str, target: str) -> str:
    translator = GoogleTranslator(source=source, target=target)
    return translator.translate(text)