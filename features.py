import discord
import asyncio
from content import tree_contains, quiz_tree

def get_help_message():
    return """
    **Commandes Disponibles :**
    `!Choixpeau` : Lance le test pour connaître ta maison.
    `!reset` : Recommence le test au début.
    `!history` : Voir tes dernières actions.
    `!savoir [mot]` : Ouvre le grimoire (ex: !savoir lumos).
    `!hibou @Nom [msg]` : Envoie un message privé.
    `!rapeltout [sec] [msg]` : Programme un rappel.
    `!speak about [sujet]` : Vérifie si un sujet est dans le test.
    """

async def handle_hibou(message):
    try:
        parts = message.content.split(" ", 2)
        if len(parts) < 3:
            await message.channel.send("Usage: !hibou @Destinataire Message")
            return
        
        if message.mentions:
            target_user = message.mentions[0]
            msg_to_send = parts[2]
            await target_user.send(f"🦉 Un hibou vous apporte un message : {msg_to_send}")
            await message.channel.send("Le hibou est parti.")
        else:
            await message.channel.send("Je ne trouve pas le destinataire.")
    except discord.Forbidden:
        await message.channel.send("Le destinataire n'accepte pas les hiboux (DMs fermés).")

async def handle_rapeltout(message):
    parts = message.content.split(" ", 2)
    if len(parts) == 3:
        try:
            seconds = int(parts[1])
            reminder = parts[2]
            await message.channel.send(f" Je deviens rouge dans {seconds} secondes.")
            await asyncio.sleep(seconds)
            await message.channel.send(f" {message.author.mention}, n'oublie pas : {reminder} !")
        except ValueError:
            await message.channel.send("Le temps doit être un nombre entier.")
    else:
        await message.channel.send("Usage: !rapeltout [secondes] [message]")

async def handle_speak_about(message):
    topic = message.content[13:]
    if tree_contains(quiz_tree, topic):
        await message.channel.send(f"Oui, '{topic}' est un sujet abordé par le Choixpeau.")
    else:
        await message.channel.send(f"Non, le Choixpeau ne parle pas de '{topic}'.")

async def assign_role(message, full_text):
    role_name = full_text.split()[0]
    guild = message.guild
    
    if not guild:
        return
    
    existing_role = discord.utils.get(guild.roles, name=role_name)
    
    if not existing_role:
        try:
            existing_role = await guild.create_role(name=role_name, reason="Cérémonie du Choixpeau")
        except discord.Forbidden:
            await message.channel.send("Erreur : Je n'ai pas la permission de créer des rôles.")
            return

    try:
        await message.author.add_roles(existing_role)
        await message.channel.send(f"Le grade **{role_name}** a été ajouté à ton profil serveur.")
    except discord.Forbidden:
        await message.channel.send("Erreur : Je ne peux pas t'attribuer ce rôle (il est peut-être placé plus haut que le mien).")