import os
import speech_recognition as sr

from gtts import gTTS
from time import sleep
import pyglet


input_lang = 'en'
output_lang='hi'

from googletrans import Translator
translator = Translator()
def trans(mytext):
    result = translator.translate(mytext,dest=output_lang)
    return str(result.text)
                                  
r = sr.Recognizer()


def SpeakText(mytext):

    tts = gTTS(text=mytext, lang=output_lang)
    filename = 'temp.mp3'
    tts.save(filename)
    music = pyglet.media.load(filename, streaming=False)
    music.play()
    sleep(music.duration)
    os.remove(filename) 

    
while(1):	
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2,language=input_lang)
            MyText = MyText.lower()
            print("Input text: "+MyText)
            trans_text=trans(MyText)
            SpeakText(trans_text)		
    except sr.RequestError as e:
        pass
        
    except sr.UnknownValueError:
        pass
       
