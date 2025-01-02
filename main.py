import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "8443"))  # Default to 8443 if PORT is not set

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"

# Fetch Pokémon data from PokéAPI
def get_pokemon_data(name_or_id):
    try:
        response = requests.get(f"{POKEAPI_BASE_URL}pokemon/{name_or_id.lower()}")
        return response.json() if response.status_code == 200 else None
    except Exception:
        return None

# Command: Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Pokémon Data Dex! 🔍\n"
        "Type a Pokémon name or number to get its details."
    )

# Pokémon Search
async def search_pokemon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    data = get_pokemon_data(query)

    if data:
        name = data["name"].capitalize()
        id_ = data["id"]
        types = ", ".join(t["type"]["name"].capitalize() for t in data["types"])
        abilities = ", ".join(a["ability"]["name"].capitalize() for a in data["abilities"])
        base_stats = "\n".join(
            f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}" for stat in data["stats"]
        )
        sprite_url = data["sprites"]["front_default"]

        message = (
            f"📖 *Pokémon Data Dex*\n"
            f"Name: {name}\n"
            f"ID: {id_}\n"
            f"Type(s): {types}\n"
            f"Abilities: {abilities}\n"
            f"Base Stats:\n{base_stats}"
        )

        await update.message.reply_text(message, parse_mode="Markdown")
        if sprite_url:
            await update.message.reply_photo(photo=sprite_url)
    else:
        await update.message.reply_text("❌ Pokémon not found. Try another name or number!")

# Command: Help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Welcome message\n"
        "/help - List of commands\n"
        "Simply type a Pokémon name or number to fetch its data."
    )

# Main function
def main():
    if not BOT_TOKEN:
        raise ValueError("Error: BOT_TOKEN is missing. Please set it in your environment variables.")

    app = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_pokemon))

    # Local or deployment environment
    use_webhook = os.getenv("USE_WEBHOOK", "true").lower() == "true"

    if use_webhook:
        # Webhook setup for Render
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=f"https://<your-app-name>.onrender.com/{BOT_TOKEN}"  # Replace with your Render URL
        )
    else:
        # Polling for local development
        print("Running bot in polling mode...")
        app.run_polling()

if __name__ == "__main__":
    main()
