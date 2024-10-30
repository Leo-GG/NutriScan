import speech_recognition as sr
from typing import Tuple

def get_voice_input(language: str = 'es-ES') -> Tuple[str, bool]:
    """
    Record and transcribe voice input in the specified language
    
    Args:
        language: Language code for speech recognition (e.g., 'en-US', 'es-ES')
    
    Returns:
        Tuple[str, bool]: Transcribed text and success status
    """
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    try:
        # Use microphone as source
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)
            
            try:
                # Attempt to recognize speech using Google's speech recognition
                text = recognizer.recognize_google(audio, language=language)
                return text, True
            except sr.UnknownValueError:
                return "Could not understand audio", False
            except sr.RequestError as e:
                return f"Could not request results; {e}", False
                
    except Exception as e:
        return f"Error accessing microphone: {e}", False
