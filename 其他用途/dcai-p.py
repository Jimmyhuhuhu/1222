! pip install discord google-generativeai nest_asyncio

import discord
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import nest_asyncio
import asyncio
import time

# ====================
# 設定
# ====================
TOKEN = "你的dcbot token"
CHANNEL_ID = int("你的頻道id")
GEMINI_KEY = "你的gemeni apikey"

# 初始化 Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    # 🔒 安全性設定（中等以上危險才會被過濾）
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
    # ⚙️ 生成設定
    generation_config={
        "temperature": 0.9,         # 平衡創造力與穩定
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1024,  # 限制輸出長度，避免洗頻
        "presence_penalty": 0.2,
        "frequency_penalty": 0.1
    }
)

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ====================
# API 錯誤處理
# ====================
async def handle_api_error(channel, e):
    err = str(e)
    if "429" in err or "quota" in err:
        await channel.send("❗ 今日配額已用完，請明日再試或使用自己的 API Key。")
    elif "403" in err:
        await channel.send("❌ API 沒有權限使用 Gemini 模型，請檢查是否啟用帳單或開通 Gemini API。")
    elif "401" in err:
        await channel.send("❌ API Key 無效，請輸入正確的金鑰。")
    elif "400" in err:
        await channel.send("⚠️ 請求錯誤，請檢查輸入內容或圖片格式。")
    elif "ConnectionError" in err or "Failed to establish a new connection" in err:
        await channel.send("⚠️ 無法連接至伺服器，請檢查網路連線。")
    else:
        await channel.send(f"未知錯誤：\n{e}")

# ====================
# Discord Bot 事件
# ====================
@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user} (id={client.user.id})")

@client.event
async def on_message(message: discord.Message):
    if getattr(message.author, "bot", False):
        return

    text = message.content.strip()
    print(f"DEBUG 收到: {message.author.display_name} 說: {text}")

    # 限制頻道
    if CHANNEL_ID and message.channel.id != CHANNEL_ID:
        return

    try:
        prompt = f"你是一個輕鬆聊天的好朋友，請用繁體中文回答：{text}"
        resp = model.generate_content(prompt)

        reply_text = resp.text.strip() if resp and resp.text else "⚠️ 沒有生成回覆"
        await message.channel.send(f"<小陰天>\n{reply_text}")
    except Exception as e:
        await handle_api_error(message.channel, e)

# ====================
# 啟動（Colab 相容）
# ====================
nest_asyncio.apply()
loop = asyncio.get_event_loop()
loop.create_task(client.start(TOKEN))
