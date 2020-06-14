import pyttsx3
import speech_recognition as sr
import mysql.connector
from difflib import SequenceMatcher as SM
#import random
#import time

recognizer = sr.Recognizer()

microphone = sr.Microphone(device_index = 0)

eng = pyttsx3.init()

# Configuración de la velocidad de la pronunciacion
eng.setProperty("rate",140)
# Volumen de la voz
eng.setProperty("volume",1.0)
# Establecer la voz a utilizar
listVoices = eng.getProperty("voices")
eng.setProperty("voice",listVoices[0].id)

eng.say("hola, bienvenido")
eng.runAndWait()

# Funciones ----------------------------------------------
def recognizerMicAudio():
    palabra = ""
    print("Escuchando...")
    with microphone as source:
        audio = recognizer.listen(source)
        palabra = recognizer.recognize_google(audio, language="es-ES")
    
    return palabra

conexion = mysql.connector.connect( host="localhost", 
                                        user="root", 
                                        passwd="", 
                                        database="asistente")
cursor = conexion.cursor(buffered=True)

palabra = ""

while palabra != "silencio":
    palabra = recognizerMicAudio()
    print(palabra)
    cursor.execute("SELECT * FROM oracion")
    nDatos = cursor.rowcount
    print("Se han encontrado", nDatos)

    for fila in cursor:
        ide = fila[0]
        entrada = fila[1]
        salidad = fila[2]
        print(ide)
        print(entrada)
        print(salidad)
        similitud = SM(None,entrada,palabra).ratio()
        print(similitud)
        if similitud > 0.7:
            eng.say(salidad)
            eng.runAndWait()
    