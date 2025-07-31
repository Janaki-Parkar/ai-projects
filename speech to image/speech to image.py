from monsterapi import client
import requests
import webbrowser
import speech_recognition as sr
from deep_translator  import GoogleTranslator

def speech_to_image():
    #mapi key
    api_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjVhYjE3NjAyZTc4ZmQwNDM4YjU1OThlOTcyMTkxYzQ0IiwiY3JlYXRlZF9hdCI6IjIwMjUtMDctMTVUMTU6MTE6MTguNzAyNzIxIn0.KzynP1J6q66gI9vUmiCdE1I0v_f2-wb2fH3E_vrG3bg'
    #ini cli
    monster_client = client(api_key)
    recognizer = sr.Recognizer()

    print('''select a preferred language: 
            1. hindi
            2. marathi
                        ''')
    try:
        lang_choice = int(input("Enter your choice: "))
        if lang_choice == 1:
            lang_code = 'hi-IN'
        elif lang_choice == 2:
            lang_code = 'mr-IN'
        else:
            print("Invalid choice.")
            return
    except ValueError:
        print("Please enter a number.")
        return

    with sr.Microphone() as source:
        print('speak')
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=40)
            or_txt = recognizer.recognize_google(audio, language=lang_code)
            print("🗣️ Original Text:", or_txt)
            print("🔹 Raw audio captured. Transcribing...")

            en_txt =GoogleTranslator(source='auto', target='en').translate(or_txt)
            print("🌍 Translated to English:", en_txt)
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return

        except sr.RequestError as e:
            print(f" API Error: {e}")
            return

    #model
    model='txt2img'

    #i/p data
    in_data={
        'prompt': f'{en_txt}',
        'neg_prompt': ' bad anatomy',
        'samples': 1,
        'steps': 50,
        'aspect_ratio': 'square',
        'guidance_scale': 7.5,
        'seed': 2414
    }
    try:
        res=monster_client.generate(model,in_data)
        #print(res['output'])
        img_url = res['output'][0]
        filename='gen-img.jpg'

        #download the img
        response=requests.get(img_url)

        if response.status_code==200:
            with open(filename,'wb') as file:
                file.write(response.content)
            print('img downloaded')
            #open the file
            webbrowser.open(filename)

        else:
            print("failed to download")
    except Exception as e:
        print('ms api error')

speech_to_image()
