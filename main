import os
import requests
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("7981498089:AAGAORd5DKZ5VWAnbBsf-VMLAnnLdYTlfgQ")
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"

# Helper function to fetch data from PokéAPI
def fetch_data(endpoint):
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

# Fetch Pokémon data
def get_pokemon_data(name_or_id):
    return fetch_data(f"{POKEAPI_BASE_URL}pokemon/{name_or_id.lower()}")

# Fetch evolution chain data
def get_evolution_chain(url):
    return fetch_data(url)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Pokémon Data Dex Bot! 🐾\n"
        "Type a Pokémon name or number to get detailed information.\n\n"
        "You can also type `/help` for more commands."
    )

# Pokémon search handler
async def search_pokemon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    data = get_pokemon_data(query)

    if data:
        name = data["name"].capitalize()
        id_ = data["id"]
        types = ", ".join(t["type"]["name"].capitalize() for t in data["types"])
        abilities = ", ".join(a["ability"]["name"].capitalize() for a in data["abilities"])
        base_stats = "\n".join(
            f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}"
            for stat in data["stats"]
        )
        sprite_url = data["sprites"]["front_default"]

        # Fetch evolution chain
        species_data = fetch_data(data["species"]["url"])
        evolution_chain_url = species_data["evolution_chain"]["url"]
        evolution_data = get_evolution_chain(evolution_chain_url)

        evolutions = []
        chain = evolution_data["chain"]
        while chain:
            evolutions.append(chain["species"]["name"].capitalize())
            chain = chain["evolves_to"][0] if chain["evolves_to"] else None

        evolution_text = " ➡️ ".join(evolutions)

        # Prepare message
        message = (
            f"📖 *Pokémon Data Dex*\n"
            f"Name: {name}\n"
            f"ID: {id_}\n"
            f"Type(s): {types}\n"
            f"Abilities: {abilities}\n"
            f"Base Stats:\n{base_stats}\n\n"
            f"Evolution Chain: {evolution_text}"
        )

        # Reply with Pokémon details
        await update.message.reply_text(message, parse_mode="Markdown")
        if sprite_url:
            await update.message.reply_photo(photo=sprite_url)
    else:
        await update.message.reply_text("❌ Pokémon not found! Try another name or number.")

# Help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Welcome message\n"
        "/help - List of commands\n"
        "Simply type a Pokémon name or number to fetch its data."
    )

# Main function to run the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_pokemon))

    # Run the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
