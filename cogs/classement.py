import discord
from discord.ext import commands
import base_de_donnee

class Classement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="classement", description="Afficher les meilleurs archéologues")
    async def classement(self, ctx):
        await ctx.defer()
        donnees = base_de_donnee.charger_donnees()
        
        if not donnees:
            return await ctx.followup.send("L'archive est vide pour le moment.")

       
        liste_joueurs = []
        for user_id, info in donnees.items():
            nb_objets = len(info.get("objets", []))
            solde = info.get("solde", 0)
            liste_joueurs.append((user_id, solde, nb_objets))


        liste_joueurs.sort(key=lambda x: x[1], reverse=True)

       
        embed = discord.Embed(
            title="🏆 Top 5 des Meilleurs Archéologues",
            color=discord.Color.gold(),
            description="Ceux qui ont financé le plus d'expéditions !"
        )

        for i, (uid, solde, nb) in enumerate(liste_joueurs[:5], 1):
            try:
                # On essaie de récupérer le nom de l'utilisateur
                user = await self.bot.fetch_user(int(uid))
                nom = user.name
            except:
                nom = f"Archéologue {uid[:5]}" # Sécurité si l'user n'est plus là

            medaille = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📜"
            embed.add_field(
                name=f"{medaille} n°{i} : {nom}",
                value=f"**{solde}€** | {nb} artefacts trouvés",
                inline=False
            )

        await ctx.followup.send(embed=embed)

def setup(bot):
    bot.add_cog(Classement(bot))