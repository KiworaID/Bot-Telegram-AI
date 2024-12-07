

# KiworaBot - Telegram AI Assistant

Smart Telegram bot powered by Groq AI providing intelligent responses.

## Features

- 💬 Chat with AI in multiple languages
- 🔄 Automatic translation support
- 📊 Usage tracking system
- 👤 User management
- ⚙️ Easy configuration

## Requirements

- Python 3.8+
- Telegram Bot Token
- Groq API Key
- Admin Telegram Chat ID

## Installation

1. Clone this repository:
```bash
git clone https://github.com/username/Bot-Telegram-AI.git
cd Bot-Telegram-AI
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill with your credentials:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
ADMIN_CHAT_ID=your_admin_chat_id
```

## Usage

1. Run the bot:
```bash
python bot.py
```

2. Start chatting with your bot on Telegram

## Getting Credentials

1. **Telegram Bot Token**:
   - Chat with [@BotFather](https://t.me/BotFather) on Telegram
   - Create new bot using `/newbot` command
   - Copy the provided token

2. **Groq API Key**:
   - Register at [Groq](https://console.groq.com)
   - Create new API key
   - Copy the API key

3. **Admin Chat ID**:
   - Chat with [@userinfobot](https://t.me/userinfobot) on Telegram
   - Copy the provided ID

## Administrative Features

- Reset usage statistics: `/reset_stats` (admin only)
- View usage statistics: `/stats` (admin only)

## Contributing

Contributions are always welcome! Please feel free to submit a Pull Request or create an Issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
