import discord
from discord.ext import commands
from models import Artefact
import base_de_donnee

class Economie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="vendre", description="Vendre une relique")
    async def vendre(self, ctx, numero: int):
        await ctx.defer()
        user_id = str(ctx.author.id)
        donnees = base_de_donnee.charger_donnees()
        
        if user_id not in donnees or numero > len(donnees[user_id]["objets"]) or numero < 1:
            return await ctx.followup.send("Relique introuvable.")

        obj_dict = donnees[user_id]["objets"].pop(numero - 1)
        artefact = Artefact(obj_dict['rarete'], obj_dict['nom'], obj_dict['fragments_possedes'], obj_dict['est_reconstitue'])
        artefact.valeur_base = obj_dict['valeur_base']
        
        gain = artefact.prix_revente()
        donnees[user_id]["solde"] += gain
        base_de_donnee.sauvegarder_donnees(donnees)
        
        await ctx.followup.send(f"Relique vendue pour **{gain}€**.")

def setup(bot):
    bot.add_cog(Economie(bot))