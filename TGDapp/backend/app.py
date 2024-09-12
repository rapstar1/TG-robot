import asyncio
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from wallet_manager import create_wallet, import_wallet
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 设置模板和静态文件目录
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')  # Flask 现在会在 frontend 文件夹中查找 index.html

TOKEN = '7224912163:AAH46VSr7vyuP5-oaHt7vzwgkD1YUgG28hk'
application = Application.builder().token(TOKEN).build()

@app.route('/api/create-wallet', methods=['POST'])
def api_create_wallet():
    try:
        response = create_wallet()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/import-wallet', methods=['POST'])
def api_import_wallet():
    try:
        data = request.json
        if not data:
            raise ValueError("No data provided")
        response = import_wallet(data)
        return jsonify(response), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

async def create_wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.post('http://localhost:5000/api/create-wallet')
        result = response.json()
        if 'error' in result:
            await update.message.reply_text(f"Error: {result['error']}")
        else:
            await update.message.reply_text(f"Wallet created successfully: {result}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

async def import_wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        wallet_data = context.args[0] if context.args else None
        if not wallet_data:
            await update.message.reply_text("Please provide wallet data to import.")
            return
        response = requests.post('http://localhost:5000/api/import-wallet', json={'wallet_data': wallet_data})
        result = response.json()
        if 'error' in result:
            await update.message.reply_text(f"Error: {result['error']}")
        else:
            await update.message.reply_text(f"Wallet imported successfully: {result}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

application.add_handler(CommandHandler('create_wallet', create_wallet_command))
application.add_handler(CommandHandler('import_wallet', import_wallet_command))

def run_flask():
    app.run(debug=True, use_reloader=False)

def start_bot():
    print("Starting Telegram bot...")
    application.run_polling()

if __name__ == '__main__':
    from threading import Thread
    import nest_asyncio
    nest_asyncio.apply()
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    start_bot()
