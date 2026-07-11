import discord
from discord import app_commands
import os
from dotenv import load_dotenv

from flask import Flask
from threading import Thread

load_dotenv()

# Web server section ---
app = Flask('')

@app.route('/')
def home():
    return 'Bot is still alive and running :D'

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t =Thread(target=run)
    t.start()

keep_alive()

# Bot section ---
class botPermission(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        await self.tree.sync()

client = botPermission()

class CTFWriteupModal(discord.ui.Modal, title='Writeup CTF'):
    challenge_name = discord.ui.TextInput(
        label='Challenge Name',
        placeholder='e.g. auka ctf Challenge',
        style=discord.TextStyle.short,
        required=True
    )
    
    info = discord.ui.TextInput(
        label='Platform',
        placeholder='https://...',
        style=discord.TextStyle.short,
        required=True
    )
        
    infoDifficulty = discord.ui.TextInput(
        label='Difficulty',
        placeholder='Easy',
        style=discord.TextStyle.short,
        required=True
    )
    
    objective = discord.ui.TextInput(
        label='Objective',
        placeholder='What is the instruction given in the problem, or what is the description of the problem?',
        style=discord.TextStyle.long,
        required=True
    )
    
    flag = discord.ui.TextInput(
        label='Flag',
        placeholder='flag{...}',
        style=discord.TextStyle.short,
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        markdown_template = f"""
```markdown
# {self.challenge_name.value}

## Challenge Info

- Platform: {self.info.value}
- Difficulty: {self.infoDifficulty.value}

## Objective

- {self.objective.value}

## Files

-

## Flow

-

## cmd

-

## Flag

`{self.flag.value}`
```
"""
        
        await interaction.response.send_message(markdown_template)

@client.tree.command(name="ctf", description="Writeup CTF")
async def ctf(interaction: discord.Interaction):
    await interaction.response.send_modal(CTFWriteupModal())
            
@client.event
async def on_ready():
    print(f'bot {client.user} (CTF Writeup is ready :D)')

client.run(os.getenv('DISCORD_TOKEN'))