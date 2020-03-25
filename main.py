import os
import telebot
import requests
from pydub import  AudioSegment
import speech_recognition as sr

__token__ = os.environ['TELEGRAM_BOT_TOKEN']
__download_url__ = 'https://api.telegram.org/file/bot{token}/'.format(token=__token__)

bot = telebot.TeleBot(__token__)

def audio_recognize(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='pt-br')
        print('Audio: \n' + text)

    return text


@bot.message_handler(content_types=['voice'])
def handle_audio(message):
    # get audio file from message
    print('Getting audio message...')
    voice_message = message.voice

    # get audio download link
    print('Getting audio link...')
    audio_path = bot.get_file(voice_message.file_id).file_path
    audio_download_link = __download_url__ + audio_path

    # download audio file
    print('Downloading audio...')
    audio_file = requests.get(audio_download_link)
    audio_filename = 'audio.ogg'

    # save audio locally
    print('Saving audio...')
    open(audio_filename, 'wb').write(audio_file.content)

    # convert .ogg to .wav
    print('Converting audio...')
    AudioSegment.from_file(audio_filename).export('audio.wav', format='wav')
    sound = AudioSegment.from_wav('audio.wav')
    sound = sound.set_channels(1) # stereo to mono
    sound.export('audio.wav', format='wav')

    # audio to text
    print('Getting text audio...')
    audio_text = audio_recognize('audio.wav')

    bot.reply_to(message, audio_text)
    print('Done!')

print('Running telegram bot!')
bot.polling()
