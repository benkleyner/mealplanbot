import discord
from discord.ext import commands
import os
import schedule
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from keep_alive import keep_alive

# Load bot token
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Channel ID
CHANNEL_ID = 1197930110062436405  # Replace with your actual channel ID

# AEPi Lunch & Dinner Menus
lunch_menu = {
    "Monday": "Scrambled Egg, Turkey Bacon & Chicken Biscuits\nHome Fried Potatoes\nSalad",
    "Tuesday": "Beef, Bean & Cheese Chimichangas(2)\nSaffron Tomato Rice\nChopped Salad",
    "Wednesday": "Soup & Sandwich\nBroccoli Cheddar Soup\nGrilled Chicken & Turkey Bacon on Toasted Ciabatta w/ lettuce, tomato and pesto mayo\nCurly Fries w/ spicy mayo (on side)",
    "Thursday": "Open-Face Hot Meatloaf Sandwich w/ Gravy on Garlic Texas Toast\nMini Hash brown Rounds\nSalad",
    "Friday": "Beef & Chicken Lo Mein w/ Stir Fry Veg\nIceberg Salad w/ ginger dressing\nChicken Pot Stickers",
}

dinner_menu = {
    "Monday": "Southern Smothered Chicken Legs in Mushroom Thyme Gravy\nSmall Roasted Round Potatoes\nCrispy Kale with Garlic\nDinner roll",
    "Tuesday": "Braised Southwest Beef\nCilantro Rice\nBaked Black Beans\nSalad with Chipotle Ranch",
    "Wednesday": "Grilled Chicken Alfredo w/ Asparagus\nCaesar Salad\nGarlic butter breadsticks\nLemon Cake",
    "Thursday": "Crispy Orange Chicken & Broccoli\nSteamed Jasmine Rice\nSalad with sesame dressing",
    "Friday": "Go to Chabad or Hillel or else you suck!",
}


def get_lunch_menu():
    return lunch_menu.get(datetime.today().strftime("%A"), "No menu available today!")


def get_dinner_menu():
    return dinner_menu.get(datetime.today().strftime("%A"), "No menu available today!")


async def send_lunch_menu():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"🍽️ Today's Lunch Menu:\n\n{get_lunch_menu()}")


async def send_dinner_menu():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"🍽️ Today's Dinner Menu:\n\n{get_dinner_menu()}")


# Scheduled tasks
async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)


def schedule_task():
    schedule.every().day.at("11:30").do(lambda: bot.loop.create_task(send_lunch_menu()))
    schedule.every().day.at("16:00").do(
        lambda: bot.loop.create_task(send_dinner_menu())
    )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await asyncio.sleep(5)
    bot.loop.create_task(run_schedule())
    print("✅ Scheduler started!")


@bot.command()
async def lunch(ctx):
    """Shows today's lunch menu."""
    await ctx.send(f"🍽️ Today's Lunch Menu:\n\n{get_lunch_menu()}")


@bot.command()
async def dinner(ctx):
    """Shows today's dinner menu."""
    await ctx.send(f"🍽️ Today's Dinner Menu:\n\n{get_dinner_menu()}")


@bot.command()
async def booger(ctx):
    await ctx.send("@flabster")


bot.remove_command("help")  # Removes the built-in help command


@bot.command()
async def help(ctx):
    """Lists all available bot commands."""
    help_message = """**🍽️ AEPi Menu Bot Commands**
- `!lunch` → Shows today's lunch menu.
- `!dinner` → Shows today's dinner menu.
- `!help` → Displays this help message.
"""
    await ctx.send(help_message)


keep_alive()  # Prevents Replit from sleeping
bot.run(TOKEN)
