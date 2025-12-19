import discord
from discord.ext import commands

class Legendes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="legendes", description="Afficher les 3 personnages les plus puissants du Panthéon")
    async def legendes(self, ctx):
        await ctx.defer()

        # Création de l'Embed principal
        embed = discord.Embed(
            title="⚡ Le Panthéon des Légendes Mythiques ⚡",
            description="Voici les trois divinités les plus rares et les plus puissantes que vous pouvez croiser lors de vos expéditions.",
            color=discord.Color.dark_gold()
        )

        # 1. Zeus (Le plus fort)
        embed.add_field(
            name="1. Zeus (Roi des Dieux)",
            value="**Force :** 100/100\n**Rareté :** Légendaire ⭐\n*Maître de la foudre et de l'Olympe.*",
            inline=False
        )
        # Image de Zeus
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Jupiter_Smyrna_Louvre_Ma13.jpg/220px-Jupiter_Smyrna_Louvre_Ma13.jpg")

        # 2. Athéna
        embed.add_field(
            name="2. Athéna (Déesse de la Sagesse)",
            value="**Force :** 92/100\n**Rareté :** Épique 🛡️\n*Protectrice des cités et stratège hors pair.*",
            inline=True
        )

        # 3. Hadès
        embed.add_field(
            name="3. Hadès (Maître des Enfers)",
            value="**Force :** 90/100\n**Rareté :** Rare 💀\n*Souverain du monde souterrain et des richesses.*",
            inline=True
        )

        # Image principale en bas pour illustrer le Panthéon
        embed.set_image(url="https://images.unsplash.com/photo-1580974511812-4b7197050a3b?q=80&w=1000&auto=format&fit=crop")
        
        embed.set_footer(text="Seuls les archéologues les plus sages peuvent espérer obtenir leurs faveurs.")

        await ctx.followup.send(embed=embed)

def setup(bot):
    bot.add_cog(Legendes(bot))