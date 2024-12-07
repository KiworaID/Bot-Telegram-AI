# KiworaBot - Bot Telegram AI Assistant

Bot Telegram pintar yang menggunakan Groq AI untuk memberikan respons cerdas dalam bahasa Indonesia.

## Fitur

- 💬 Chat dengan AI dalam bahasa Indonesia
- 🔄 Terjemahan otomatis ke bahasa Indonesia
- 📊 Sistem tracking penggunaan
- 👤 Manajemen pengguna
- ⚙️ Konfigurasi mudah

## Persyaratan

- Python 3.8+
- Token Bot Telegram
- API Key Groq
- ID Chat Admin Telegram

## Instalasi

1. Clone repositori ini:
```bash
git clone https://github.com/username/Bot-Telegram-AI.git
cd Bot-Telegram-AI
```

2. Install dependensi yang diperlukan:
```bash
pip install -r requirements.txt
```

3. Salin file `.env.example` ke `.env` dan isi dengan kredensial Anda:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
ADMIN_CHAT_ID=your_admin_chat_id
```

## Cara Penggunaan

1. Jalankan bot:
```bash
python bot.py
```

2. Mulai chat dengan bot Anda di Telegram

## Mendapatkan Kredensial

1. **Token Bot Telegram**:
   - Chat dengan [@BotFather](https://t.me/BotFather) di Telegram
   - Buat bot baru dengan perintah `/newbot`
   - Salin token yang diberikan

2. **API Key Groq**:
   - Daftar di [Groq](https://console.groq.com)
   - Buat API key baru
   - Salin API key

3. **ID Chat Admin**:
   - Chat dengan [@userinfobot](https://t.me/userinfobot) di Telegram
   - Salin ID yang diberikan

## Fitur Administratif

- Reset statistik penggunaan: `/reset_stats` (hanya admin)
- Lihat statistik penggunaan: `/stats` (hanya admin)

## Kontribusi

Kontribusi selalu diterima! Silakan buat pull request atau laporkan masalah melalui issues.

## Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail lebih lanjut. 