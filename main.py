from collections.abc import MutableMapping
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import os
import asyncio

TOKEN = os.getenv("BOT_KEY") 

user_alerts = {}

async def setalert(update: Update, context:
ContextTypes.DEFAULT_TYPE):
    try:
      user_id = update.effective_user.id
      args = context.args  
      if len(args) != 1 or not args[0].isdigit():
          await update.message.reply_text("❌ Please use: `/setalert <Gwei>`\nExample: `/setalert 30`", parse_mode="Markdown")
          return
        
      threshold = int(args[0])
      user_alerts[user_id] = threshold
      await update.message.reply_text(f"🔔 Alert set! You'll be notified when gas price drops below {threshold} Gwei.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error setting alert: {e}")


async def gas_alert_checker(app):
    while True:
        if user_alerts:
            try:
                
                url = os.getenv("ETHER_KEY")
                response = requests.get(url).json()
                current_gas = int(response["result"]["ProposeGasPrice"])

                for user_id, threshold in list(user_alerts.items()):
                    if current_gas <= threshold:
                        await app.bot.send_message(chat_id=user_id, text=f"✅ Gas Alert: ETH gas is now {current_gas} Gwei (below your set {threshold} Gwei)")
                        del user_alerts[user_id]  

            except Exception as e:
                print("Error in gas alert checker:", e)

        await asyncio.sleep(120)  


async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args=context.args
        if len(args) !=2:
            await update.message.reply_text("❌ Please use the format:\n`/calculate gasLimit gasPrice` (Gwei)\nExample: `/calculate 21000 45`", parse_mode="Markdown")
            return

        gas_limit = int(args[0])
        gas_price = int(args[1])

        fee_eth = (gas_limit * gas_price) / 10**9

        price_response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd").json()
        eth_usd = price_response["ethereum"]["usd"]

        fee_usd = fee_eth * eth_usd

        message = (
            "🧮 **Manual Gas Fee Calculation**\n\n"
            f"⛽ Gas Limit: `{gas_limit}`\n"
            f"💸 Gas Price: `{gas_price}` Gwei\n\n"
            f"🔷 Estimated Fee: `{fee_eth:.6f}` ETH\n"
            f"💵 Approx. Cost: `${fee_usd:.2f}` USD"
        )                                            

        await update.message.reply_text(message, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text (f"❌ Error: {e}")


async def multigas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
     eth_url = os.getenv("ETHER_KEY")
     bsc_url = os.getenv("BSC_KEY")
     poly_url = os.getenv("POLY_KEY")

     eth_response = requests.get(eth_url).json()
     bsc_response = requests.get(bsc_url).json()
     poly_response = requests.get(poly_url).json()

     eth = eth_response["result"]["ProposeGasPrice"]
     bsc = bsc_response["result"]["ProposeGasPrice"]
     poly = poly_response["result"]["ProposeGasPrice"]

     message = (
        "⛽ Multi-chain gas prices(gwei)**\n\n"
        f"🔵 **Ethereum**: {eth}` gwei\n"
        f"🟢 **BSC**: {bsc} `gwei\n"
        f"⚫ **Polygon**: {poly}` gwei"
    )

     await update.message.reply_text(message, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error fetching gas prices: {e}")

    
    

async def gas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = os.getenv("ETHER_KEY")
    response = requests.get(url).json()
    gas_price = response["result"]["ProposeGasPrice"]
    await update.message.reply_text(f"Current ETH gas price: {gas_price} Gwei")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Crypto Gas Fee Bot! Use /gas to get current gas prices.")

  

if __name__ == "__main__":
      
      app = ApplicationBuilder().token(TOKEN).build() 
      app.add_handler(CommandHandler("multigas", multigas))
      app.add_handler(CommandHandler("start", start))
      app.add_handler(CommandHandler("gas", gas))
      app.add_handler(CommandHandler("calculate", calculate))
      app.add_handler(CommandHandler("setalert", setalert))

      
      app.job_queue.run_once(lambda _: asyncio.create_task(gas_alert_checker(app)), when=1)


      print("Bot is running...")
      app.run_polling()
