app_url=""
voice_model=0
import os
import speech_recognition as sr

from gtts import gTTS
from time import sleep
import pyglet


print("""Available Language:
   1.English
   2.Hindi
   3.Bengali
   4.French 
   5.Spanish 
   6.Portuguese 
   7.Chinese
   8.Japanese 
   9.Indonesian 
   10.Russian 
"""
)

lang_code={
    1:"en",
    2:"hi",
    3:"bn",
    4:"fr",
    5:"es",
    6:"pt",
    7:"zh-CN",
    8:"ja",
    9:"id",
    10:"ru" 
}


input_lang_code=int(input("Choose Input language: "))
output_lang_code=int(input("Choose Output language: "))
if output_lang_code==1:
    print("\n")
    print("Available English voice model:\n   1.Natural voice\n   2.Google Text to speech")
    voice_model=int(input("Choose English voice model: "))

    
input_lang = lang_code[input_lang_code]
output_lang=lang_code[output_lang_code]

accent={
1:
    {1:"English (Australia)",
    2:"English (United Kingdom)",
    3:"English (United States)",
    4:"English (Canada)",
    5:"English (India)",
    6:"English (Ireland)",
    7:"English (South Africa)"},
}

domain={1:"com.au",
 2:"co.uk",
 3:"com",
 4:"ca",
 5:"co.in",
 6:"ie",
 7:"co.za"}
my_tld="com"

if output_lang_code==1 and voice_model==2:
    print("\n")
    print("Choose your accent:")
    for i,j in accent[1].items():
        print(f"{i}. {j}")
    accent_code=int(input("Choose Output language accent: "))
    my_tld=domain[accent_code]
# print(input_lang,output_lang,my_tld)   
 
 
from googletrans import Translator
translator = Translator()
def trans(mytext):
    result = translator.translate(mytext,dest=output_lang)
    return str(result.text)
                         
r = sr.Recognizer()

import requests
import base64

file_name="temp.wav"
def natural_SpeakText(mytext):
    r = requests.post(url=app_url+"api/predict/",
    json={"data":
    [mytext]})
    audio_data=r.json()
    raw_data=audio_data["data"][0].replace("data:audio/wav;base64,","")
    wav_file = open(file_name, "wb")
    decode_string = base64.b64decode(raw_data)
    wav_file.write(decode_string)
    music = pyglet.media.load(file_name, streaming=False)
    music.play()
    sleep(music.duration)
    # os.remove(file_name) 
    
def SpeakText(mytext):
    tts = gTTS(text=mytext,tld="ca", lang=output_lang,)
    filename = 'temp.mp3'
    tts.save(filename)
    music = pyglet.media.load(filename, streaming=False)
    music.play()
    sleep(music.duration)
    os.remove(filename) 

if input_lang=="en":
    input_lang="co.in"

print("\nPlease Start talking:\n")    
while(1):	
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2,language=input_lang)
            MyText = MyText.lower()
            print("Input text: "+MyText)
            trans_text=trans(MyText)
            if voice_model==1 and output_lang_code==1:
                try:
                    natural_SpeakText(trans_text)
                except:
                    SpeakText(trans_text)
            else:    
                SpeakText(trans_text)		
    except sr.RequestError as e:
        pass
        
    except sr.UnknownValueError:
        pass
       
