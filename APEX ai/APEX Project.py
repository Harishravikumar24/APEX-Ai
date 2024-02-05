import speech_recognition as aa
import pyttsx3
import webbrowser
import pywhatkit
import datetime
import wikipedia
import cv2
import matplotlib.pyplot as plt
import subprocess
import sys
import psutil
import pyjokes
import pyautogui
from win10toast import ToastNotifier
from instructions_responses import  RESPONSES
import pygame
import requests
from bs4 import BeautifulSoup
import numpy as np
import imageio

print(" ........................................................Installing APEX ................................................wait, Harish")
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
video_file = "apex intro.mp4"
video = imageio.get_reader(video_file)
screen = pygame.display.set_mode(video.get_meta_data()['size'])
music_file = "apex.mp3"
pygame.mixer.init()
pygame.mixer.music.load(music_file)
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play()
clock = pygame.time.Clock()
try:
    for i, data in enumerate(video.iter_data()):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
        data_bytes = np.array(data).tobytes()
        frame_surface = pygame.image.fromstring(data_bytes, video.get_meta_data()['size'], 'RGB')
        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)
except KeyboardInterrupt:
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()



listener = aa.Recognizer()
machine = pyttsx3.init()
voices = machine.getProperty('voices')
def talk(text):
    machine.say(text)
    machine.runAndWait()


def wish():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        talk(RESPONSES['morning'])
    elif hour>=12 and hour<17:
        talk(RESPONSES['afternoon'])
    elif hour>=17 and hour<21:
        talk(RESPONSES['evening'])
    else :
        talk("Good night, Harish, How can i assist you? harish")
def temperature():
    search="temperature in Neyveli"
    url = f"https://www.google.com/search?q={search}"
    r=requests.get(url)
    data=BeautifulSoup(r.text,"html.parser")
    temp = data.find("div",class_="BNeawe").text
    talk(f"current {search} is {temp}")


talk("APEX online. What can I do for you, harish?")
machine.runAndWait()
current_time = datetime.datetime.now().strftime('%I:%M%p')
talk(f'May I inform you that it is {current_time}')
def notepad():
    try:
        if sys.platform.startswith('win'):
            subprocess.Popen(['notepad.exe'])
            talk("Sure Harish, Opening Notepad")

            recognizer = aa.Recognizer()

            with aa.Microphone() as source:
                print("Say Harish")
                talk("What do you want to write, Harish?")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=2)

                try:
                    write = recognizer.recognize_google(audio).lower()
                except aa.UnknownValueError:
                    talk("Sorry, I could not understand what you said.")
                    return

                text_to_write = write
                if text_to_write== '':
                    text_to_write="harish, you asked me to write something I can't understand"
                pyautogui.write(text_to_write)
                talk("Done Harish")

            with aa.Microphone() as source:
                print("Say Harish")
                talk("Do you want to save it, Harish?")
                audio = recognizer.listen(source, timeout=2)

                try:
                    w = recognizer.recognize_google(audio).lower()
                except aa.UnknownValueError:
                    talk("Sorry, I could not understand whether you want to save or not, so i didnt save it harish.")
                    return

            word = w.lower()
            print(word)

            if 'save' in word or 'yes' in word:
                pyautogui.hotkey('ctrl','s')
                with aa.Microphone() as source:
                    print("Say Harish")
                    talk("What name do you want to save it as, Harish?")
                    audio = recognizer.listen(source, timeout=2)
                    a = recognizer.recognize_google(audio)
                save = a.lower()
                if save == '':
                    save = 'Apex file'
                pyautogui.write(save)
                pyautogui.press("enter")
                talk("Ok, done Harish, I saved it!")
            else:
                talk("Ok Harish, I didn't save it")

    except Exception as e:
        print(f"An error occurred: {e}")
def close_notepad():
    try:

        for process in psutil.process_iter(['pid', 'name']):
            if 'notepad.exe' in process.info['name'].lower():
                pid = process.info['pid']
                subprocess.Popen(['taskkill', '/F', '/PID', str(pid)], shell=True)
                talk("Notepad closed successfully.")
                break
        else:
            talk("Notepad is not running.")

    except Exception as e:
        print(f"Error: {e}")


def send_windows_notification(title, message):
    talk("Harish , the the notification will gets display after one minute")
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=60)
    print("done harish,i had set remainder notification which will gets display after  60 seconds")


def take_and_show_picture(camera_index=0, save_path='captured_image.jpg'):
    talk("sure harish, iam going to take a pic .")
    talk("so, smile please!")
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    ret, frame = cap.read()
    cv2.imwrite(save_path, frame)
    cap.release()
    img = cv2.imread(save_path)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Captured Image')
    plt.axis('off')
    plt.show()
    talk(f"Image saved at: {save_path}")
    

def input_instruction():
    instruction = "" 
    try:
        with aa.Microphone() as origin:
            print("listening..")
            speech = listener.listen(origin, timeout=1)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if 'apex' in instruction:
                instruction = instruction.replace('apex', '')
                return instruction
    except aa.WaitTimeoutError:
        print("Harish , iam waiting for speech")
    except aa.UnknownValueError:
        print("Could not understand voice")
        talk("I wouldn't understand your voice , your are in noicey surrounding ")
    except aa.RequestError as e:
        print(f"Speech recognition request failed: {e}")
    return None

def play_apex():
    while True:
        instruction = input_instruction()
        if instruction:
            print(instruction)
            for key, value in RESPONSES.items():
                if key in instruction:
                    if key == 'play':
                        song = instruction.replace(key, '')
                        talk(RESPONSES[key].format(song=song))
                        pywhatkit.playonyt(song)
                        break
                    elif key == 'time':
                        current_time = datetime.datetime.now().strftime('%I:%M%p')
                        talk(RESPONSES[key].format(current_time=current_time))
                    elif key == 'are you listening' or key == 'listening' or key == 'hearing':
                        talk(RESPONSES[key])
                    elif key == 'morning'or key == 'afternoon'or key == 'evening' or key =='night':
                        wish()
                    elif key == 'battery'or key == 'charge'or key == 'power left':
                        battery = psutil.sensors_battery()
                        percentage = battery.percent
                        talk(f"harish ,our sytem have {percentage} persent battery !..")
                    elif 'hi' in key:
                        talk(RESPONSES['hi'])
                    elif 'hey' in key:
                        talk(RESPONSES['hi'])
                    elif 'buddy' in key:
                        talk(RESPONSES['hi'])
                    elif 'hello' in key:
                        talk(RESPONSES['hi'])
                    elif 'weather' in key or'temperature' in key :
                        temperature()
                    elif 'joke' in key:
                        joke=pyjokes.get_joke()
                        print(joke)
                        talk(joke)
                    elif key == 'introduce':
                        talk(RESPONSES[key])
                    elif key == 'whatsapp'or key == 'whats app' :   
                        with aa.Microphone() as origin:
                            talk("what message did you want to send harish!")
                            sp = listener.listen(origin,timeout=1)
                            t = listener.recognize_google(sp)
                            t = t.lower()
                            if t=='':
                                t='some message'
                        whatsapp = t
                        talk("ok,done")
                        hour=int(datetime.datetime.now().hour)
                        current_minute = datetime.datetime.now().minute
                        minute = current_minute + 1
                        pywhatkit.sendwhatmsg("+918807639930", whatsapp,  hour, minute)
                        talk("ok , harish i had typed it, check the message and click enter to send the message.")
                        instruction=''
                    elif key == 'how are you':
                        talk(RESPONSES[key])
                    elif key == 'date':
                        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                        talk(RESPONSES[key].format(current_date=current_date))
                    elif key == 'open the notepad'or key == 'open notepad' :
                        notepad()
                    elif key == 'close the notepad'or key == 'close notepad' :
                        close_notepad()
                    elif key == 'photo'or key == 'on the camera'or key == 'selfie' :
                        take_and_show_picture()
                    elif key == 'notification' or key == 'reminder' or key =='remainder':
                        talk("sure harish , i will help you to send remainder in notification ")
                        machine.runAndWait()
                        talk("what is the tittle of your notification , harish")
                        with aa.Microphone() as origin:
                            s = listener.listen(origin,timeout=1)
                            t = listener.recognize_google(s)
                            t = t.lower()
                        title = t
                        if title =='':
                            title='remainder notification'
                        talk("ok done , next")
                        with aa.Microphone() as origin:
                            talk("what message you want to remember harish")
                            m = listener.listen(origin, timeout=1)
                            mess = listener.recognize_google(m)
                            mess = mess.lower()
                        message = mess
                        if message =='':
                            message= 'hi harish, iam apex ,you told me to set remainder ...this is that ... '
                        send_windows_notification( title,message)
                    elif key == 'what'or key=='who':
                        thing = instruction.strip()
                        print(f"Searching for: {thing}")
                        talk(f"Searching  information about {thing}. Please wait.")
                        try:
                            info = wikipedia.summary(thing, sentences=2)
                            talk(info)
                            talk(RESPONSES[key].format(thing=thing))
                            
                        except wikipedia.exceptions.DisambiguationError as e:
                            print(f"Ambiguous search term: {e}")
                            talk("I'm sorry, but I couldn't find information about that thing.")
                        except wikipedia.exceptions.PageError as e:
                            print(f"Page not found: {e}")
                            talk("I'm sorry, but I couldn't find information about that thing.")
                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")
                            talk("I encountered an unexpected error while searching for information.")
                    elif key == 'thank you':
                        talk(RESPONSES[key])
                    elif key == 'exit program'or key == 'exit the program':
                        talk(RESPONSES[key])
                        quit()
                    elif key == 'shutdown'or key == 'shut down':
                        talk(RESPONSES[key])
                        exit()
                    elif key == 'instagram' or key == 'insta':
                        talk("sure harish, opening your instagram profile")
                        url = "https://www.instagram.com/_crimson_comet/?hl=en" 
                        webbrowser.open_new_tab(url)
                    elif key == 'linkedin' or key == 'linked':
                        talk("sure harish, opening your linkedin profile")
                        url = "https://www.linkedin.com/in/harish-r-12372b28b/" 
                        webbrowser.open_new_tab(url)

                    else:
                        thing = instruction.strip()
                        print(f"Searching for: {thing}")
                        talk(f"Searching  information about {thing}. Please wait.")
                        try:
                            info = wikipedia.summary(thing, sentences=2)
                            talk(info)
                            talk(RESPONSES[key].format(thing=thing))
                        except wikipedia.exceptions.DisambiguationError as e:
                            print(f"Ambiguous search term: {e}")
                            talk("I'm sorry, but I couldn't find information about that thing.")
                        except wikipedia.exceptions.PageError as e:
                            print(f"Page not found: {e}")
                            talk("I'm sorry, but I couldn't find information about that thing.")
                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")
                            talk("I encountered an unexpected error while searching for information.")
    
play_apex()