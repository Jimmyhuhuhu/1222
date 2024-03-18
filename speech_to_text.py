import speech_recognition as sr
from googletrans import Translator
import requests
import gradio as gr
import pygame
import tempfile

API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

def generate_music(input_text):
    english_translation = translate_text(input_text)
    audio_bytes = query({"inputs": english_translation})
    return audio_bytes

r = sr.Recognizer()

with sr.Microphone() as source:
    print("請開始說話...")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language='zh-TW')
    print("您說的是：" + text)
    
    english_translation = translate_text(text)
    print("翻譯結果為：", english_translation)
    
    audio_bytes = query({"inputs": english_translation})

    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmpfile.write(audio_bytes)
        tmpfile.close()
        # 初始化 pygame mixer
        pygame.mixer.init()
        # 加载音频文件并播放
        pygame.mixer.music.load(tmpfile.name)
        pygame.mixer.music.play()
        # 等待音频播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    #interface = gr.Interface(
    #    title="Music Generation App",
    #    examples=[english_translation],
    #    fn=generate_music,
    #    inputs=gr.Textbox(lines=5, label="Speak something in Chinese (Traditional)"),
    #    outputs="audio",
    #)
    #interface.launch(debug=True, share=False)
    
except sr.UnknownValueError:
    print("無法辨識您的語音")
except sr.RequestError as e:
    print("無法連線至 Google 語音識別服務：{0}".format(e))