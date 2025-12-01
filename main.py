import discord
import json
from structures import bot_data, HistoryStack
from storage import save_data, load_data
from content import quiz_tree, encyclopedia
import features

# Function to retrieve the bot token from the config file
def get_token():
    with open("config.json", "r") as f:
        config = json.load(f)
        return config["token"]

TOKEN = get_token()

# Setting up bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

# Event triggered when the bot is ready
@client.event
async def on_ready():
    load_data()  # Load saved data
    print(f"Bot connected : {client.user}")

# Event triggered when the bot disconnects
@client.event
async def on_disconnect():
    save_data()  # Save data before disconnecting

# Event triggered when a message is received
@client.event
async def on_message(message):
    if message.author == client.user:  # Ignore messages from the bot itself
        return

    uid = str(message.author.id)  # User ID
    name = message.author.name  # Username
    bot_data.user_names[uid] = name  # Save username
    
    content = message.content  # Message content
    
    # Initialize user history if not already present
    if uid not in bot_data.user_histories:
        bot_data.user_histories[uid] = HistoryStack()
    
    bot_data.user_histories[uid].push(content)  # Add message to user history
    save_data()  # Save data

    # Handle bot commands
    if content == "!help":
        await message.channel.send(features.get_help_message())
        return

    if content == "!Choixpeau":
        bot_data.current_nodes[uid] = quiz_tree  # Start the quiz
        await message.channel.send("Le Choixpeau est sur ta tête. " + quiz_tree.text)
        return

    if content == "!reset":
        bot_data.current_nodes[uid] = quiz_tree  # Reset the quiz
        await message.channel.send("On recommence. " + quiz_tree.text)
        return

    if content.startswith("!speak about "):
        await features.handle_speak_about(message)  # Check if a topic exists in the quiz
        return

    if content == "!history":
        history = bot_data.user_histories[uid].get_all()  # Get user history
        await message.channel.send(f"Tes dernières paroles : {history}")
        return

    if content == "!clear_history":
        bot_data.user_histories[uid].clear()  # Clear user history
        await message.channel.send("Oubliettes ! Historique effacé.")
        return

    if content.startswith("!savoir "):
        term = content[8:].lower()  # Extract the term
        definition = encyclopedia.get(term, "Je ne trouve pas cela dans ma bibliothèque.")
        await message.channel.send(f" {definition}")
        return

    if content.startswith("!hibou "):
        await features.handle_hibou(message)  # Send a private message
        return

    if content.startswith("!rapeltout "):
        await features.handle_rapeltout(message)  # Set a reminder
        return

    # Handle quiz navigation
    if uid in bot_data.current_nodes:
        node = bot_data.current_nodes[uid]
        if not node.is_result:  # If the current node is not a result
            choice = None
            if content == "1":
                choice = node.left
            elif content == "2":
                choice = node.right
                 
            if choice:  # Move to the next node
                bot_data.current_nodes[uid] = choice
                await message.channel.send(choice.text)
                
                if choice.is_result:  # If the result is reached
                    bot_data.houses[uid] = {
                        "username": bot_data.user_names.get(uid, "Inconnu"),
                        "house": choice.text
                    }
                    save_data()
                    
                    await features.assign_role(message, choice.text)  # Assign a role
                    
                    del bot_data.current_nodes[uid]  # Clear the current node
            else:
                await message.channel.send("Réponds uniquement par 1 ou 2.")  # Invalid input

# Run the bot
client.run(TOKEN)