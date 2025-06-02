from telegram.ext import Updater, CommandHandler
import requests

API_TOKEN = "7955525199:AAEGswaiBESvwP8lZp_zjos1mKxdksN09_4"

def start(update, context):
    update.message.reply_text("Welcome to Crypto Gas Fee Calculator Bot! Use /gas to get current gas prices.")

def gas(update, context):
    # Example: get Ethereum gas price from Etherscan
    url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
    response = requests.get(url).json()
    gas_price = response['result']['ProposeGasPrice']
    update.message.reply_text(f"Current Ethereum gas price: {gas_price} Gwei")

def main():
    updater = Updater(API_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gas", gas))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
