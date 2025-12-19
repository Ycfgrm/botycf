import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = discord.Bot(intents=discord.Intents.all())

if __name__ == "__main__":
    # On vérifie si le dossier existe pour éviter un crash au lancement
    if os.path.exists('./cogs'):
        for filename in os.listdir('./cogs'):
            # On ignore le fichier __init__.py s'il existe
            if filename.endswith('.py') and filename != '__init__.py':
                try:
                    bot.load_extension(f'cogs.{filename[:-3]}')
                    print(f"Cog chargé avec succès : {filename}")
                except Exception as e:
                    # Si un fichier dans cogs a une erreur, on l'affiche sans éteindre le bot
                    print(f"Erreur sur le fichier {filename} : {e}")
    else:
        print("Attention : Le dossier 'cogs' est introuvable !")

@bot.event
async def on_ready():
    print(f"Archéologue connecté : {bot.user}")

bot.run(TOKEN)