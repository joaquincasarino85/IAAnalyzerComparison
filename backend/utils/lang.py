from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # Para resultados consistentes

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "en"  # fallback
