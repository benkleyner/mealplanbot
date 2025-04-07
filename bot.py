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
CHANNEL_ID = 1197930110062436405

# AEPi Lunch & Dinner Menus - Week 3 (3/31 - 4/2)
lunch_menu = {
    "Monday": "Cheesy Scrambled Eggs\nTurkey Sausage\nFrench Toast Sticks w/ maple syrup\nFresh Fruit",
    "Tuesday": "Chicken Quesadillas\nCilantro Rice\nTortilla chips & Salsa\nSalad",
    "Wednesday": "Tomato Basil Soup\nCroissant Grilled Cheese w/ Turkey Bacon\nKrinkle Cut Garlic Parm Fries \nSalad",
    "Thursday": "BBQ Pulled Chicken Sliders\nAsian Slaw w/ mandarins orange\nSeasoned Fries w/spicy mayo",
    "Friday": "Salmon Kimchi Fried Rice\nVegetable Spring Rolls\nChopped Salad w/ ginger dressing",
}

dinner_menu = {
    "Monday": "Roasted Chicken w/ Caramelized Onions and green peppers\nRosemary Garlic potatoes\nGreen Beans",
    "Tuesday": "Traditional Taco Night(4)\nYellow Rice\nBlack Bean Dip\nGuacamole\nSour cream",
    "Wednesday": "Meatball Calzones w/ marinara sauce on side\nCaesar salad\nLemon cake w/ fresh berries",
    "Thursday": "Beef & Chicken Stir Fry\nJasmine Rice \nCold Sesame Noodles\nSalad",
    "Friday": "Go to Chabad or Hillel or else you suck!",
}


def get_lunch_menu():
    return lunch_menu.get(datetime.today().strftime("%A"), "No menu available today!")


def get_dinner_menu():
    return dinner_menu.get(datetime.today().strftime("%A"), "No menu available today!")


async def send_lunch_menu():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        day = datetime.today().strftime("%A")
        if day in ["Thursday", "Friday"]:
            await channel.send(f"🍽️ Today's Lunch Menu:\n\n{lunch_menu.get(day)}")
        else:
            await channel.send(f"🍽️ Today's Lunch Menu:\n\n{get_lunch_menu()}")


async def send_dinner_menu():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        day = datetime.today().strftime("%A")
        if day in ["Thursday"]:
            await channel.send(f"🍽️ Today's Dinner Menu:\n\n{dinner_menu.get(day)}")
        elif day == "Friday":
            await channel.send(f"🍽️ Today's Dinner Menu:\n\n{dinner_menu.get(day)}")
        else:
            await channel.send(f"🍽️ Today's Dinner Menu:\n\n{get_dinner_menu()}")


# Scheduled tasks
async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)


def schedule_task():
    # Only schedule announcements for Monday, Tuesday, and Wednesday
    schedule.every().monday.at("11:30").do(
        lambda: bot.loop.create_task(send_lunch_menu())
    )
    schedule.every().tuesday.at("11:30").do(
        lambda: bot.loop.create_task(send_lunch_menu())
    )
    schedule.every().wednesday.at("11:30").do(
        lambda: bot.loop.create_task(send_lunch_menu())
    )

    schedule.every().monday.at("16:00").do(
        lambda: bot.loop.create_task(send_dinner_menu())
    )
    schedule.every().tuesday.at("16:00").do(
        lambda: bot.loop.create_task(send_dinner_menu())
    )
    schedule.every().wednesday.at("16:00").do(
        lambda: bot.loop.create_task(send_dinner_menu())
    )
    schedule.every().friday.at("16:00").do(
        lambda: bot.loop.create_task(send_dinner_menu())
    )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    schedule_task()  # Added this line to ensure tasks are scheduled
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


keep_alive()
bot.run(TOKEN)
