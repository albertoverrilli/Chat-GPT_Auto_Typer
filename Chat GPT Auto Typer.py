import openai
import time
import pyautogui
import threading
from tkinter import *
import tkinter.scrolledtext as ScrolledText

# Define a global flag for controlling typing status
typing_status = {"running": True, "paused": False}

def countdown(time_sec, countdown_label):
    for i in range(time_sec, -1, -1):
        countdown_label.config(text=f"Time until typing starts: {i}s")
        root.update()
        time.sleep(1)
    countdown_label.config(text="")  # Clear countdown label

def pause_resume():
    global typing_status
    if typing_status["paused"]:
        typing_status["paused"] = False
        pause_resume_button.config(text="Pause")
        print('Resumed. Typing will start after 3 seconds.')
        threading.Thread(target=countdown, args=(3, countdown_label)).start()  # Countdown after resume
    else:
        typing_status["paused"] = True
        pause_resume_button.config(text="Resume")
        print('Paused.')

def stop_typing():
    global typing_status
    typing_status["running"] = False
    print('Stopped.')

def mimic_typing(text, typing_speed=0.05):
    global typing_status
    typing_status = {"running": True, "paused": False}  # Reset the state at the start of each new call

    threading.Thread(target=countdown, args=(5, countdown_label)).start()  # Countdown before typing
    time.sleep(5)

    position = 0  # start position
    while position < len(text):
        while typing_status["paused"]:
            time.sleep(0.5)  # if paused, sleep for a while
        if typing_status["running"] is False:
            break  # if stopped, break the loop
        pyautogui.typewrite(text[position])
        position += 1
        time.sleep(typing_speed)

openai.api_key = ''
messages = [
    {"role": "system", "content": "You are a kind helpful assistant."},
]

def send():
    message = entry.get()
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat.choices[0].message.content
    text_area.insert(INSERT, f"ChatGPT: {reply}\n")
    messages.append({"role": "assistant", "content": reply})

    threading.Thread(target=mimic_typing, args=(reply,)).start()

    if typing_status["running"] is False:
        print("Exiting...")

root = Tk()
root.title("ChatGPT GUI")
root.geometry("400x700")

text_area = ScrolledText.ScrolledText(root)
text_area.pack(padx=10, pady=10)

entry = Entry(root)
entry.pack(padx=10, pady=10)

send_button = Button(root, text="Send", command=send)
send_button.pack(padx=10, pady=10)

pause_resume_button = Button(root, text="Pause", command=pause_resume)
pause_resume_button.pack(padx=10, pady=10)

stop_button = Button(root, text="Stop", command=stop_typing)
stop_button.pack(padx=10, pady=10)

countdown_label = Label(root, text="")
countdown_label.pack()

root.mainloop()







