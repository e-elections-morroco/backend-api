
from io import BytesIO
import io
import speech_recognition as sr
import pyttsx3
import pymysql
from flask import Flask, jsonify, request
from flask_cors import CORS
import base64
from pydub import AudioSegment
from pydantic import BaseModel
from fastapi.responses import JSONResponse



class VoiceBotRequest(BaseModel):
    base64data: str
    provider: str
    langue: str = "arabe"
    database_ip: str

def base64_to_audio_segment(base64_data):
    try:
        # Add padding to the Base64 data if needed
        missing_padding = len(base64_data) % 4
        if missing_padding:
            base64_data += "=" * (4 - missing_padding)

        # Decode the Base64 data
        audio_data = base64.b64decode(base64_data)

        # Store the decoded data in a BytesIO variable
        audio_stream = BytesIO(audio_data)

        # Convert the BytesIO variable to an AudioSegment
        audio_segment = AudioSegment.from_file(audio_stream)

        print("Audio successfully converted to an AudioSegment.")

        return audio_segment
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify(
            status="error",
            error="Error : function base64_to_audio_segment",
            errorMessage=str(e),
        )
        # return None


def recherche_mots_old(tableau, mots):
    for mot in mots:
        if mot not in tableau:
            return 0  # Retourne 0 si au moins l'un des mots n'est pas trouvé
    return 1  # Retourne 1 si tous les mots sont trouvés


def recherche_mots(text, hotwords):
    for hotword in hotwords:
        found = False
        for element in text:
            if element in hotword:
                found = True
                break
        if not found:
            return 0
    return 1

def getParams(actionCode, actionText, orderCode):

    params = {
        "actionCode": actionCode,
        "actionText": actionText,
        "orderCode": orderCode,
    }
    return params


def process_voice_command(base64_audio_data: str, provider: str, langue: str, host: str):
    if langue == "":
        langue = "anglais"

    conn = pymysql.connect(
        host=host,
        user="root",
        password="",
        database="e_elections",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    if langue.lower() == "francais":
        langue = "fr"
    elif langue.lower() == "anglais":
        langue = "en"
    elif langue.lower() == "arabe":
        langue = "ar"
    else:
        return JSONResponse(content={"error": "Langue non prise en charge", "langue": langue}, status_code=400)

    try:
        recognizer = sr.Recognizer()
        text_speech = pyttsx3.init()
    except Exception as e:
        print("Something went wrong:", e)
        return JSONResponse(content={"error": "Speech recognition or text-to-speech initialization failed"}, status_code=500)

    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM voice_commands")
        rows = cursor.fetchall()
        orders = [row[f"order_text_{langue}"] for row in rows]
        hotwords = [row[f"hotwords_{langue}"].split(" ") for row in rows]
        actioncodes = [row[f"action_code"] for row in rows]
        actions = [row[f"action_text"] for row in rows]
        ordercodes = [row[f"id"] for row in rows]

    audio_segment = base64_to_audio_segment(base64_audio_data)

    if provider == "vosk":
        print("Provider: Vosk")
    elif provider == "google":
        if langue.lower() == "fr":
            langue = "fr-FR"
        elif langue.lower() == "en":
            langue = "en-US"
        elif langue.lower() == "ar":
            langue = "ar-AR"
        else:
            langue = "en-US"
        
        if audio_segment is not None:
            recognizer = sr.Recognizer()
            audio_bytes = io.BytesIO()
            audio_segment.export(audio_bytes, format="wav")
            with sr.AudioFile(audio_bytes) as source:
                audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=langue)
            print("Texte reconnu par google:", text)
    else:
        return JSONResponse(content={"error": "Unsupported provider"}, status_code=400)

    try:
        myinput = text
        correct = False
        for i in range(len(orders)):
            order = orders[i]
            hotword = hotwords[i]
            actioncode = actioncodes[i]
            action = actions[i]
            ordercode = ordercodes[i]
            if (
                myinput.lower() == order.lower()
                or recherche_mots(myinput.lower().split(), hotword) == 1
            ):
                correct = True
                break

        if correct:
            print("Action executed successfully")
            return JSONResponse(content={"langue": langue, "text": myinput.lower(), "action": action}, status_code=200)
        else:
            print("Command not recognized")
            return JSONResponse(content={
                "status": "error",
                "error": "Command not recognized",
                "langue": langue,
                "text": myinput.lower(),
                "action": "عذرًا، لا أستطيع الإجابة على هذا السؤال. يمكنني فقط الرد على الأسئلة المتعلقة بموقع الويب الخاص بنا.",
                "provider": provider,
            }, status_code=400)

    except sr.UnknownValueError:
        print(f"Désolé, je n'ai pas compris le son en {langue}")
        return JSONResponse(content={
            "status": "error",
            "error": f"Désolé, je n'ai pas compris le son en {langue}"
        }, status_code=400)

    except sr.RequestError:
        print(f"Désolé, le service est actuellement indisponible en {langue}")
        return JSONResponse(content={
            "status": "error",
            "error": f"Désolé, le service est actuellement indisponible en {langue}"
        }, status_code=500)

    return JSONResponse(content={
        "status": "error",
        "error": "Error: Action not found",
        "errorMessage": audio_segment
    }, status_code=400)


if __name__ == "__main__":
    pass