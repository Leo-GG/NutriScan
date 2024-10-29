import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator

def get_voice_input():
    r = sr.Recognizer()
    translator = GoogleTranslator(source='es', target='en')
    with sr.Microphone() as source:
        st.write("Escuchando... Habla ahora.")  # "Listening... Speak now." in Spanish
        audio = r.listen(source)
        st.write("Procesando el habla...")  # "Processing speech..." in Spanish
    try:
        text = r.recognize_google(audio, language="es-ES")
        st.write(f"Texto reconocido (español): {text}")
        return text
    except sr.UnknownValueError:
        st.error("Lo siento, no pude entender eso.")  # "Sorry, I couldn't understand that." in Spanish
        return None
    except sr.RequestError:
        st.error("Lo siento, hubo un error con el servicio de reconocimiento de voz.")  # Error message in Spanish
        return None
