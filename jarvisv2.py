#import
from elevenlabs import generate, play, set_api_key
import ffmpeg
import openai

import speech_recognition as sr

#decla variable
output = "erreur"


set_api_key("<api elevenlab>")
openai.api_key = "<api openai>"
context = "" #contexte de base

cont = " " #variable


while True:

    r = sr.Recognizer()

    # Configuration de l'enregistrement audio
    with sr.Microphone() as source:
        print("Parle maintenant...")
        audio = r.listen(source)

    try:
        # Reconnaissance vocale
        prompt = r.recognize_google(audio, language="fr-FR")  # Utilisation de l'API Google Speech-to-Text pour la reconnaissance
        print("prompt:" + prompt)
    except sr.UnknownValueError:
        print("Impossible de reconnaître la parole")
    except sr.RequestError as e:
        print("Erreur lors de la requête à l'API Google Speech-to-Text; {0}".format(e))





    #prompt
    def chat(prompt, context=""):

        if context == "":
            cont = " "
        else:
            cont = " contexte: mes précédents messages sont les suivants (dans l'ordre chronologique) ; " + context + ", mes précédents messages n'affectent pas forcément la réponse qui suit. "

        completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Utilisez "gpt-3.5-turbo" pour le modèle GPT-3 Turbo (chat model)
            messages=[
                {"role": "system", "content": "important: ta réponse sera en tts donc fais en sorte que ta réponse soit cohérente et surtout ne dis pas \"reponse\" au premier mot de ta phrase."},
                {"role": "system", "content": "Identité : Tu es une intelligence artificielle nommée \"jarvis\" en référence à l'assistant de Tony Stark dans le célèbre film Iron Man. Ton but est de m'assister dans ma vie quotidienne et tu as des connaissances infinies, tu excèles dans tous les domaines et tu parles français."},
                {"role": "system", "content": cont},
                {"role": "user", "content": "Question : " + prompt + " . (et évite de répondre avec trop de mots)"},
            ],
            max_tokens=500,
            temperature=0.5,
        )

        message = completions['choices'][0]['message']['content']
        return message



    def tts():
        print("rep:" + response)
        audio = generate(
        text=response,
        voice="Josh",
        model="eleven_multilingual_v1"
        )

        play(audio)



    response = chat(prompt)
    tts()
    if(context == ""):
        context = context + "\"" + prompt + "\""
    else:
        context = context + ", \"" + prompt + "\""
