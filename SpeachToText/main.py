import PySimpleGUI as sg
import speech_recognition as sr
from gtts import gTTS
import os

def main():
    sg.theme('DarkPurple4')

    layout = [
        [sg.Text("Speech to Text", size=(30, 1), font=("Helvetica", 20), justification='center')],
        [sg.Multiline(size=(70, 20), key="-Output-", disabled=True, autoscroll=True, font=("Helvetica", 14))],
        [
            sg.Button("Record", button_color=('white', '#1f77b4'), font=("Helvetica", 14), size=(10, 2)),
            sg.Button("Speak", button_color=('white', '#2ca02c'), font=("Helvetica", 14), size=(10, 2)),
            sg.Button("Save", button_color=('white', '#ffa500'), font=("Helvetica", 14), size=(10, 2)),
            sg.Button("Clear", button_color=('white', '#808080'), font=("Helvetica", 14), size=(10, 2)),
            sg.Button("Toggle Theme", button_color=('white', '#808080'), font=("Helvetica", 14), size=(12, 2))
        ]
    ]

    window = sg.Window("Speech to Text", layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Record":
            recognize_speech(window)
        elif event == "Speak":
            speak_text(window)
        elif event == "Save":
            save_text(window)
        elif event == "Clear":
            clear_text(window)
        elif event == "Toggle Theme":
            toggle_theme(window)

    window.close()

def recognize_speech(window):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        window["-Output-"].update("")  # Очищаем содержимое перед записью речи
        window["-Output-"].set_focus()  # Устанавливаем фокус на поле вывода
        window.refresh()  # Обновляем окно для отображения фокуса

        try:
            audio = r.listen(source)
            text = r.recognize_google(audio)
            window["-Output-"].print(text)
        except sr.UnknownValueError:
            window["-Output-"].print("Unable to recognize speech")
        except sr.RequestError as e:
            window["-Output-"].print(f"Error: {e}")

def speak_text(window):
    text = window["-Output-"].Get().strip()
    if text:
        tts = gTTS(text=text, lang='en')
        tts.save('output.mp3')
        os.system('start output.mp3')

def save_text(window):
    text = window["-Output-"].Get().strip()
    if text:
        filename = sg.popup_get_file('Save Text', save_as=True, default_extension=".txt")
        if filename:
            with open(filename, 'w') as file:
                file.write(text)
                sg.popup(f'Text saved to {filename}')

def clear_text(window):
    window["-Output-"].update("")

def toggle_theme(window):
    current_theme = sg.theme()
    if current_theme == "DarkBlue3":
        new_theme = "LightGrey"
    else:
        new_theme = "DarkBlue3"
    sg.theme(new_theme)
    window.close()
    main()

if __name__ == "__main__":
    main()
