import paho.mqtt.client as mqtt
import requests
from gtts import gTTS
from pydub import AudioSegment
from pydub import effects
import io
#import subprocess
#import tempfile
#import os

# MQTT settings
MQTT_BROKER = "192.168.1.10"
MQTT_PORT = 1883
MQTT_TOPIC = "DahuaVTO/ring"  
MQTT_USER = "mqtt"
MQTT_PASSWD = "mqtt"

# HTTP settings
DAHUA_VTO_IP = "192.168.50.41"
HTTP_URL = "http://" + DAHUA_VTO_IP + "/cgi-bin/audio.cgi?action=postAudio&httptype=singlepart&channel=1"
CONTENT_TYPE = "Audio/G.711A"
CONTENT_LENGTH = "9999999"
USER_AGENT = "HomeAssistant"
SPEECH_LANGUAGE = "fi"
REQUEST_TIMEOUT = 5000  # Set the request timeout value

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    if msg.topic == MQTT_TOPIC:
        try:
            payload_text = msg.payload.decode("utf-8")
            if payload_text == "ring":
                with open("doorbell_vto.wav", "rb") as audio_file:
                    wav_data = audio_file.read()
            else:
                tts = gTTS(text=payload_text, lang=SPEECH_LANGUAGE)
                mp3_data = io.BytesIO()
                tts.write_to_fp(mp3_data)
                mp3_data.seek(0)

                # Convert MP3 to PCM A-law WAV using pydub
                audio_segment = AudioSegment.from_mp3(mp3_data)
                audio_segment = audio_segment.set_frame_rate(8000)
                audio_segment = audio_segment.set_channels(1)
                corrected_audio_segment = audio_segment.speedup(2)
                wav_data = io.BytesIO()
                audio_segment.export(wav_data, format="alaw", bitrate="8000")
                wav_data.seek(0)


            headers = {
                "Content-Length": CONTENT_LENGTH,
                # "Content-Length": len(wav_data.getvalue()),
                "Content-Type": CONTENT_TYPE,
                "User-Agent": USER_AGENT
            }

            response = requests.put(HTTP_URL, data=wav_data, headers=headers, timeout=REQUEST_TIMEOUT / 1000)

            print("HTTP Response:", response.status_code)
        except Exception as e:
            print("Error:", str(e))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(MQTT_USER, MQTT_PASSWD)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()