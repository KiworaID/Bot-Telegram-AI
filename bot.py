import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
import groq
import json
from datetime import datetime
from collections import deque

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Groq client
client = groq.Groq(api_key=os.getenv('GROQ_API_KEY'))

class KiwAIBot:
    def __init__(self):
        self.conversations = {}
        self.translator = GoogleTranslator()
        self.usage_data = self.load_usage_data()
        self.admin_chat_id = int(os.getenv('ADMIN_CHAT_ID'))
        self.max_history = 5  # Menyimpan 5 pesan terakhir
        
    def load_usage_data(self):
        try:
            with open('usage_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'total_messages': 0,
                'total_tokens': 0,
                'users': {},
                'last_reset': datetime.now().isoformat()
            }
    
    def save_usage_data(self):
        with open('usage_data.json', 'w') as f:
            json.dump(self.usage_data, f, indent=4)
            
    def update_usage(self, chat_id, tokens_used):
        chat_id = str(chat_id)
        self.usage_data['total_messages'] += 1
        self.usage_data['total_tokens'] += tokens_used
        
        if chat_id not in self.usage_data['users']:
            self.usage_data['users'][chat_id] = {
                'messages': 0,
                'tokens': 0,
                'first_interaction': datetime.now().isoformat()
            }
            
        self.usage_data['users'][chat_id]['messages'] += 1
        self.usage_data['users'][chat_id]['tokens'] += tokens_used
        self.save_usage_data()

    def get_conversation_history(self, chat_id):
        if chat_id not in self.conversations:
            self.conversations[chat_id] = {
                'history': deque(maxlen=self.max_history),
                'context': None
            }
        return self.conversations[chat_id]
        
    async def translate_text(self, text: str, dest='en', src='auto'):
        try:
            translator = GoogleTranslator(source=src, target=dest)
            return translator.translate(text)
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text

    async def get_ai_response(self, prompt: str, chat_id: int) -> str:
        try:
            # Dapatkan history chat
            conversation = self.get_conversation_history(chat_id)
            history = conversation['history']
            context = conversation['context']

            # Buat prompt dengan history
            history_text = "\n".join([f"User: {h['user']}\nAI: {h['ai']}" for h in history])
            
            enhanced_prompt = f"""Konteks percakapan sebelumnya:
{history_text}

Konteks tugas/peran saat ini: {context if context else 'Belum ada konteks khusus'}

Pertanyaan/perintah terbaru:
{prompt}

Berikan respons dalam Bahasa Indonesia yang natural dan sesuai dengan konteks percakapan sebelumnya."""

            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": enhanced_prompt}],
                model="llama3-groq-70b-8192-tool-use-preview",
                temperature=0.7,
                max_tokens=1000,
            )
            response = chat_completion.choices[0].message.content
            
            # Update history
            history.append({
                'user': prompt,
                'ai': response
            })
            
            # Update usage statistics
            tokens_used = chat_completion.usage.total_tokens
            self.update_usage(chat_id, tokens_used)
            
            if not response.strip().startswith(('Maaf', 'Hai', 'Halo', 'Baik', 'Terima', 'Saya', 'Untuk', 'Berikut', 'Ini')):
                response = await self.translate_text(response, dest='id', src='en')
            
            return response
        except Exception as e:
            logger.error(f"AI response error: {e}")
            return "Maaf, terjadi kesalahan dalam memproses permintaan Anda."

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_message = """
Halo! Saya KiwAI, asisten AI yang siap membantu Anda.

Untuk berinteraksi dengan saya, gunakan prefix '.' di awal pesan Anda.
Contoh: .apa itu python

Perintah yang tersedia:
/start - Memulai bot
.help - Menampilkan panduan lengkap
.reset - Mereset percakapan (khusus chat ID Anda)
.config - Mengatur konfigurasi (khusus chat ID Anda)
.info - Melihat statistik penggunaan
.context [peran] - Mengatur konteks/peran AI (contoh: .context guru matematika)

Silakan mulai chat dengan mengetik pesan yang diawali dengan '.'!
        """
        await update.message.reply_text(welcome_message)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
KiwAI Bot - Panduan Penggunaan:

Cara Menggunakan Bot:
1. Selalu awali pesan Anda dengan '.'
2. Ketik pertanyaan atau perintah setelah tanda '.'
   Contoh: .jelaskan tentang AI

Perintah Tersedia:
.help - Menampilkan panduan ini
.reset - Mereset konteks percakapan Anda
.config - Melihat dan mengatur konfigurasi Anda
.info - Melihat statistik penggunaan Anda
.context [peran] - Mengatur konteks/peran AI
  Contoh: 
  - .context guru matematika
  - .context chef profesional
  - .context konsultan bisnis

Fitur:
- Mendukung berbagai bahasa input
- Selalu merespons dalam Bahasa Indonesia
- Respons cerdas dengan AI
- Mengingat 5 percakapan terakhir
- Konteks percakapan yang dapat disesuaikan
- Pelacakan penggunaan

Tips:
- Gunakan .context untuk mengatur peran AI sesuai kebutuhan
- Bot akan mengingat 5 percakapan terakhir Anda
- Gunakan .reset jika ingin memulai percakapan baru
- Bot hanya akan merespons pesan yang diawali dengan '.'
        """
        await update.message.reply_text(help_text)

    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = str(update.effective_chat.id)
        if chat_id in self.conversations:
            self.conversations[chat_id] = {
                'history': deque(maxlen=self.max_history),
                'context': None
            }
            await update.message.reply_text("✅ Konteks dan history percakapan Anda telah direset!")
        else:
            await update.message.reply_text("Tidak ada konteks percakapan yang perlu direset.")

    async def set_context(self, update: Update, context: ContextTypes.DEFAULT_TYPE, new_context: str):
        chat_id = str(update.effective_chat.id)
        conversation = self.get_conversation_history(chat_id)
        conversation['context'] = new_context
        await update.message.reply_text(f"✅ Konteks percakapan diatur sebagai: {new_context}")

    async def config(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = str(update.effective_chat.id)
        user_data = self.usage_data['users'].get(chat_id, {
            'messages': 0,
            'tokens': 0,
            'first_interaction': datetime.now().isoformat()
        })
        
        conversation = self.get_conversation_history(chat_id)
        history_count = len(conversation['history'])
        
        config_text = f"""
📊 Konfigurasi Chat ID: {chat_id}

Statistik Penggunaan Anda:
- Total Pesan: {user_data['messages']}
- Total Token: {user_data['tokens']}
- Pertama Kali Menggunakan: {user_data['first_interaction']}

Status Percakapan:
- Pesan dalam History: {history_count}/{self.max_history}
- Konteks Saat Ini: {conversation['context'] if conversation['context'] else 'Belum diatur'}
- Mode AI: llama3-groq-70b-8192-tool-use-preview
- Bahasa Respons: Indonesia
        """
        await update.message.reply_text(config_text)

    async def info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        user_data = self.usage_data['users'].get(str(chat_id), {
            'messages': 0,
            'tokens': 0
        })
        
        conversation = self.get_conversation_history(str(chat_id))
        
        info_text = f"""
📈 Statistik Penggunaan:

Penggunaan Pribadi Anda:
- Total Pesan: {user_data['messages']}
- Total Token: {user_data['tokens']}
- Pesan dalam History: {len(conversation['history'])}/{self.max_history}
- Konteks Aktif: {conversation['context'] if conversation['context'] else 'Tidak ada'}

"""
        
        # Tambahkan statistik global jika admin
        if chat_id == self.admin_chat_id:
            info_text += f"""
Statistik Global:
- Total Pengguna: {len(self.usage_data['users'])}
- Total Pesan: {self.usage_data['total_messages']}
- Total Token: {self.usage_data['total_tokens']}
- Terakhir Reset: {self.usage_data['last_reset']}
"""
        
        await update.message.reply_text(info_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message.text
        chat_id = update.effective_chat.id
        
        # Hanya proses pesan yang dimulai dengan '.'
        if not message.startswith('.'):
            return
            
        # Hapus prefix '.' dari pesan
        command = message[1:].strip().lower()
        
        # Jika pesan kosong setelah menghapus prefix
        if not command:
            await update.message.reply_text("Silakan ketik pertanyaan atau perintah setelah tanda '.'")
            return
        
        # Handle commands
        if command == 'help':
            await self.help(update, context)
            return
        elif command == 'reset':
            await self.reset(update, context)
            return
        elif command == 'config':
            await self.config(update, context)
            return
        elif command == 'info':
            await self.info(update, context)
            return
        elif command.startswith('context '):
            new_context = command[8:].strip()
            if new_context:
                await self.set_context(update, context, new_context)
            else:
                await update.message.reply_text("Mohon tentukan konteks/peran untuk AI. Contoh: .context guru matematika")
            return
            
        # Proses pesan normal
        eng_text = await self.translate_text(command, dest='en', src='auto')
        response = await self.get_ai_response(eng_text, chat_id)
        await update.message.reply_text(response)

def main():
    # Initialize bot
    bot = KiwAIBot()
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))

    # Start bot
    print("Bot started! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 