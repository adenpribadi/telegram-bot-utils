import openai
from src.utils import read_tokens_from_file

# Membaca semua token dari file config.txt
config_tokens = read_tokens_from_file("config.txt")
# Ambil DEEPSEEK_API_KEY dari dictionary yang didapat
DEEPSEEK_API_KEY = config_tokens.get("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY tidak ditemukan dalam file config.txt")

client = openai.OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def ask_question(text):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": text},
            ],
            stream=False
        )

        return response.choices[0].message.content
    except Exception as e:  # Gunakan Exception umum karena tidak ada OpenAIError
        error_message = str(e)
        if "402" in error_message:
            return "Error: Insufficient Balance. Silakan isi ulang saldo Anda di DeepSeek."
        elif "401" in error_message:
            return "Error: API Key tidak valid. Periksa kembali API Key Anda."
        elif "429" in error_message:
            return "Error: Terlalu banyak permintaan dalam waktu singkat. Coba lagi nanti."
        elif "500" in error_message:
            return "Error: Internal Server Error. Silakan coba lagi nanti."
        else:
            return f"Unexpected Error: {error_message}"

    except Exception as e:
        return f"Unexpected Error: {str(e)}"
