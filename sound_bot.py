# control-pibot.py
# *** IMPORTANT ***
# serverAddress is your pi's host name. Be sure to replace hostname, below
# with the hostname that you use to log into your Pi.
# If you are running this code from the BostonCollege network, remove .local below
# but REMEMBER if you run this on another Wi-Fi network (e.g. at home), you'll need
# to modify this code to add .local again
serverAddress = "profg-physcomp"

# *** IMPORTANT ***
# The commands below assume your pi's hostname is hostname. If you have a
# different name, then use that name in place of hostname in the mosquitto_pub
# commands, below.
# once running, you can test with the shell commands:
# To play any of the numbered sounds (substitute a diffrent number for "1" for a different sound:
# mosquitto_pub -h hostname.local -t "pibot/move" -m "1"
# To start the robot:
# mosquitto_pub -h hostname.local -t "pibot/move" -m "forward"
# To stop the robot:
# mosquitto_pub -h hostname.local -t "pibot/move" -m "stop"

import pygame
import time
import paho.mqtt.client as mqtt

# don't modify the name below - this is correct
clientName = "PiBot"

mqttClient = mqtt.Client(clientName)
# Flag to indicate subscribe confirmation hasn't been printed yet.
didPrintSubscribeMessage = False

# setup startup sound. Make sure you have a sounds
# folder with a sound named startup.mp3
fileLocation = "/home/pi/robot_sounds/"
pygame.mixer.init()
pygame.mixer.music.load(fileLocation + "startup.wav")
speakerVolume = ".50" # initially sets speaker at 50%
pygame.mixer.music.set_volume(float(speakerVolume))
pygame.mixer.music.play()

def connectionStatus(client, userdata, flags, rc):
    global didPrintSubscribeMessage
    if not didPrintSubscribeMessage:
        didPrintSubscribeMessage = True
        print("subscribing")
        mqttClient.subscribe("pibot/move")
        print("subscribed")

def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')

    if message == "forward":
        print("^^^ moving forward! ^^^")
    elif message == "stop":
        print("!!! stopping!")
    elif message == "backward":
        print("\/ backward \/")
    elif message == "left":
        print("<- left")
    elif message == "right":
        print("-> right")
    elif message.startswith("Vol="):
        speakerVolume = message[4:]
        pygame.mixer.music.set_volume(float(speakerVolume))
    else:
        print("Playing sound at: " + fileLocation + message + ".mp3")
        pygame.mixer.music.stop()
        pygame.mixer.music.load(fileLocation + message + ".mp3") # assumes you have a file$
        pygame.mixer.music.play()

# Set up calling functions to mqttClient
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

# Connect to the MQTT server & loop forever.
# CTRL-C will stop the program from running.
print("server address is:", serverAddress)
mqttClient.connect(serverAddress)
mqttClient.loop_forever()
