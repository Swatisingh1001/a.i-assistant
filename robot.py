
import speech_recognition as sr
import requests 
import pyttsx3

API_KEY = ' ' # your open a.i api key 


recognizer = sr.Recognizer()
microphone = sr.Microphone()

engine = pyttsx3.init()

voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)  #changing index, changes voices. o for male


def query_chatgpt(prompt):

    url = 'https://api.openai.com/v1/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    data = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 1024,
        'temperature': 0
    }

    response = requests.post(url, headers=headers, json=data)
    ai_response = response.json()['choices'][0]['text']

    return ai_response


print("Hello! I'm your a.i Assistant . Ask me anything and say 'quit' to exit.")

while True:
    
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        text = recognizer.recognize_google(audio)
        
        if text.lower() == 'quit':
            print("Goodbye!")
            break
            
        print(f"You said: {text}")

        response = query_chatgpt(text)
        
        print(f"Assistant : {response}")

        engine.say(response)
        engine.runAndWait()
        
    except sr.UnknownValueError:
        print("Could not understand audio")



