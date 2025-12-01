import discord
from structures import bot_data, HistoryStack
from storage import save_data, load_data
from content import quiz_tree, encyclopedia
import features

TOKEN = test

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    load_data()
    print(f"Bot connecté : {client.user}")

@client.event
async def on_disconnect():
    save_data()

@client.event
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    uid = str(message.author.id)
    name = message.author.name       
    bot_data.user_names[uid] = name  
    
    content = message.content
    
    if uid not in bot_data.user_histories:
        bot_data.user_histories[uid] = HistoryStack()
    
    bot_data.user_histories[uid].push(content)
    save_data()

    if content == "!help":
        await message.channel.send(features.get_help_message())
        return

    if content == "!Choixpeau":
        bot_data.current_nodes[uid] = quiz_tree
        await message.channel.send("Le Choixpeau est sur ta tête. " + quiz_tree.text)
        return

    if content == "!reset":
        bot_data.current_nodes[uid] = quiz_tree
        await message.channel.send("On recommence. " + quiz_tree.text)
        return

    if content.startswith("!speak about "):
        await features.handle_speak_about(message)
        return

    if content == "!history":
        history = bot_data.user_histories[uid].get_all()
        await message.channel.send(f"Tes dernières paroles : {history}")
        return

    if content == "!clear_history":
        bot_data.user_histories[uid].clear()
        await message.channel.send("Oubliettes ! Historique effacé.")
        return

    if content.startswith("!savoir "):
        term = content[8:].lower()
        definition = encyclopedia.get(term, "Je ne trouve pas cela dans ma bibliothèque.")
        await message.channel.send(f"📖 {definition}")
        return

    if content.startswith("!hibou "):
        await features.handle_hibou(message)
        return

    if content.startswith("!rapeltout "):
        await features.handle_rapeltout(message)
        return

    if uid in bot_data.current_nodes:
        node = bot_data.current_nodes[uid]
        if not node.is_result:
            choice = None
            if content == "1":
                choice = node.left
            elif content == "2":
                choice = node.right
                 
            if choice:
                bot_data.current_nodes[uid] = choice
                await message.channel.send(choice.text)
                
                if choice.is_result:
                    bot_data.houses[uid] = {
                        "username": bot_data.user_names.get(uid, "Inconnu"),
                        "house": choice.text
                    }
                    save_data()
                    
                    await features.assign_role(message, choice.text)
                    
                    del bot_data.current_nodes[uid]
            else:
                await message.channel.send("Réponds uniquement par 1 ou 2.")

client.run(TOKEN)