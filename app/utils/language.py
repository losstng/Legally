from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 42 
# detectorfactory is a factory that creates language dectector, essentially our engine
# If you don’t set a seed, running the same detection multiple times on the same text 
# could return different results (especially for short or ambiguous text).

SUPPORTED_LANGUAGES = {
    'en': 'English',
    'de': 'German',
    'vi': 'Vietnamese'
}

def detect_language(text: str) -> str:
    try:
        lang = detect(text) # detect using the engine
        if lang in SUPPORTED_LANGUAGES: # dictionary 
            return lang
        return 'en'
    except LangDetectException: # fall back system in case of total failure
        return 'en'