import discord
import asyncio
from content import tree_contains, quiz_tree  # Importing functions and data from content.py

# Returns the help message with available bot commands
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

# Handles the `!hibou` command to send a private message to a mentioned user
async def handle_hibou(message):
    try:
        parts = message.content.split(" ", 2)
        if len(parts) < 3:  # Check if the command has enough arguments
            await message.channel.send("Usage: !hibou @Destinataire Message")
            return
        
        if message.mentions:  # Check if a user is mentioned
            target_user = message.mentions[0]
            msg_to_send = parts[2]
            await target_user.send(f" Un hibou vous apporte un message : {msg_to_send}")
            await message.channel.send("Le hibou est parti.")
        else:
            await message.channel.send("Je ne trouve pas le destinataire.")
    except discord.Forbidden:  # Handle permission errors
        await message.channel.send("Le destinataire n'accepte pas les hiboux (DMs fermés).")

# Handles the `!rapeltout` command to set a reminder
async def handle_rapeltout(message):
    parts = message.content.split(" ", 2)
    if len(parts) == 3:
        try:
            seconds = int(parts[1])  # Parse the delay in seconds
            reminder = parts[2]  # Get the reminder message
            await message.channel.send(f" Je deviens rouge dans {seconds} secondes.")
            await asyncio.sleep(seconds)  # Wait for the specified time
            await message.channel.send(f" {message.author.mention}, n'oublie pas : {reminder} !")
        except ValueError:  # Handle invalid time input
            await message.channel.send("Le temps doit être un nombre entier.")
    else:
        await message.channel.send("Usage: !rapeltout [secondes] [message]")

# Handles the `!speak about` command to check if a topic exists in the quiz tree
async def handle_speak_about(message):
    topic = message.content[13:]  # Extract the topic from the command
    if tree_contains(quiz_tree, topic):  # Check if the topic exists in the tree
        await message.channel.send(f"Oui, '{topic}' est un sujet abordé par le Choixpeau.")
    else:
        await message.channel.send(f"Non, le Choixpeau ne parle pas de '{topic}'.")

# Assigns a role to the user or creates it if it doesn't exist
async def assign_role(message, full_text):
    role_name = full_text.split()[0]  # Extract the role name
    guild = message.guild  # Get the server (guild) object
    
    if not guild:  # Ensure the command is used in a server
        return
    
    # Check if the role already exists
    existing_role = discord.utils.get(guild.roles, name=role_name)
    
    if not existing_role:  # Create the role if it doesn't exist
        try:
            existing_role = await guild.create_role(name=role_name, reason="Cérémonie du Choixpeau")
        except discord.Forbidden:  # Handle permission errors
            await message.channel.send("Erreur : Je n'ai pas la permission de créer des rôles.")
            return

    # Assign the role to the user
    try:
        await message.author.add_roles(existing_role)
        await message.channel.send(f"Le grade **{role_name}** a été ajouté à ton profil serveur.")
    except discord.Forbidden:  # Handle errors if the bot lacks permissions
        await message.channel.send("Erreur : Je ne peux pas t'attribuer ce rôle (il est peut-être placé plus haut que le mien).")