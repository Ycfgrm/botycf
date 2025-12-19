import discord
from discord.ext import commands
import random
from models import Artefact, ENIGMES
import base_de_donnee

class Archeologie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="explorer", description="Trouver des fragments d'artefacts")
    async def explorer(self, ctx):
        await ctx.defer()
        user_id = str(ctx.author.id)
        donnees = base_de_donnee.charger_donnees()
        
        if user_id not in donnees:
            donnees[user_id] = {"solde": 0, "objets": []}

        # Logique d'événement aléatoire (15%)
        if random.random() < 0.15:
            evenement = random.choice(["malediction", "tresor_cache"])
            if evenement == "malediction":
                perte = random.randint(5, 15)
                donnees[user_id]["solde"] = max(0, donnees[user_id]["solde"] - perte)
                await ctx.followup.send(f"**MALÉDICTION !** Un piège s'est déclenché. -{perte}€ !")
            else:
                gain = random.randint(20, 60)
                donnees[user_id]["solde"] += gain
                await ctx.followup.send(f"**PASSAGE SECRET !** +{gain}€ !")
            base_de_donnee.sauvegarder_donnees(donnees)
            return

        # Logique Artefact standard
        rarete = random.choices(["Commun", "Rare", "Légendaire"], weights=[70, 25, 5])[0]
        nouvel_artefact = Artefact(rarete)
        
        possede_deja = False
        for item in donnees[user_id]["objets"]:
            if item["nom"] == nouvel_artefact.nom and not item["est_reconstitue"]:
                item["fragments_possedes"] += 1
                possede_deja = True
                if item["fragments_possedes"] >= item["fragments_requis"]:
                    item["est_reconstitue"] = True
                    response = f"**COMPLET !** : **{item['nom']}** !"
                else:
                    response = f"Fragment : **{item['nom']}** ({item['fragments_possedes']}/{item['fragments_requis']})"
                break
                
        if not possede_deja:
            donnees[user_id]["objets"].append(nouvel_artefact.to_dict())
            response = f"⛏️ Découvert : **{nouvel_artefact.nom}** ({rarete})"
        
        base_de_donnee.sauvegarder_donnees(donnees)
        await ctx.followup.send(f"**{ctx.author.name}**, {response}")

    @discord.slash_command(name="musee", description="Voir votre progression")
    async def musee(self, ctx):
        await ctx.defer()
        user_id = str(ctx.author.id)
        donnees = base_de_donnee.charger_donnees()
        user_data = donnees.get(user_id, {"solde": 0, "objets": []})
        
        if not user_data["objets"]:
            return await ctx.followup.send(f"Budget : {user_data['solde']}€\nMusée vide.")
        
        message = f"🏺 **Musée de {ctx.author.name}** | Budget : {user_data['solde']}€\n\n"
        for i, item in enumerate(user_data["objets"], 1):
            status = "COMPLET" if item["est_reconstitue"] else f"{item['fragments_possedes']}/{item['fragments_requis']} frags"
            message += f"{i}. **{item['nom']}** [{item['rarete']}] - {status}\n"
        await ctx.followup.send(message)

    @discord.slash_command(name="oracle", description="Énigme mythologique")
    async def oracle(self, ctx):
        enigme = random.choice(ENIGMES)
        await ctx.respond(f"**L'Oracle interroge :**\n*{enigme['question']}*")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30.0)
            if msg.content.lower() == enigme["reponse"]:
                user_id = str(ctx.author.id)
                donnees = base_de_donnee.charger_donnees()
                recompense = Artefact("Rare")
                if user_id not in donnees: donnees[user_id] = {"solde": 0, "objets": []}
                donnees[user_id]["objets"].append(recompense.to_dict())
                base_de_donnee.sauvegarder_donnees(donnees)
                await ctx.send(f"Bravo ! Fragment de **{recompense.nom}** obtenu.")
            else:
                await ctx.send("Mauvaise réponse...")
        except:
            await ctx.send("Temps écoulé.")

def setup(bot):
    bot.add_cog(Archeologie(bot))