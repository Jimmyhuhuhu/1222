from configparser import ConfigParser

# Set up the config parser
config = ConfigParser()

read_files = config.read("d:/Temp/1222/ai/114 ai高中生/config.ini")

if not read_files:
    print("❌ 找不到設定檔，請確認路徑正確")
    exit()  # 或 raise SystemExit()：終止程式
    
try:
    api_key = config["Gemini"]["API_KEY"]
    print("API_KEY：", api_key)
except KeyError:
    print("❌ 找不到 [Gemini] 或 API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI

llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest", 
    google_api_key=api_key
)

user_input = "人生的意義是什麼？"

role_description = """
你是一個哲學家，請用繁體中文回答。
"""

messages = [
    ("system", role_description),
    ("human", user_input),
]

response_gemini = llm_gemini.invoke(messages)

print(f"問 : {user_input}")
print(f"Gemini : {response_gemini.content}")