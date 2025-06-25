from flask import Flask, render_template, jsonify, send_from_directory
import discord
from discord import app_commands
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
import threading

# Load environment variables from .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)

GIF_PATHS = {
    "heads": "gifs/heads.gif",
    "tails": "gifs/tails.gif"
}

@app.route("/")
def index():
    return render_template("index.html")

def run_flask():
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent for DMs
intents.dm_messages = True      # Enable DM message events
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="coinflip", description="Flip a coin with animated GIF!")
async def coinflip(interaction: discord.Interaction):
    """Flip a coin and display animated GIF result"""
    result = random.choice(["heads", "tails"])
    try:
        gif_path = GIF_PATHS[result]
        if not os.path.exists(gif_path):
            raise FileNotFoundError(f"GIF not found at {gif_path}")
        embed = discord.Embed(
            title="Coin Flip",
            description=f"**Result: {result.upper()}!**",
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Requested by {interaction.user.name}")
        file = discord.File(gif_path, filename=f"{result}.gif")
        embed.set_image(url=f"attachment://{result}.gif")
        await interaction.response.send_message(file=file, embed=embed)
    except Exception as e:
        error_msg = f"🚫 Error: {str(e)}"
        await interaction.response.send_message(error_msg, ephemeral=True)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        if message.content.strip().lower() == "coinflip":
            result = random.choice(["heads", "tails"])
            try:
                gif_path = GIF_PATHS[result]
                if not os.path.exists(gif_path):
                    raise FileNotFoundError(f"GIF not found at {gif_path}")
                embed = discord.Embed(
                    title="Coin Flip",
                    description=f"**Result: {result.upper()}!**",
                    color=discord.Color.gold()
                )
                embed.set_footer(text=f"Requested by {message.author.name}")
                file = discord.File(gif_path, filename=f"{result}.gif")
                embed.set_image(url=f"attachment://{result}.gif")
                await message.channel.send(file=file, embed=embed)
            except Exception as e:
                error_msg = f"🚫 Error: {str(e)}"
                await message.channel.send(error_msg)
    await bot.process_commands(message)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))