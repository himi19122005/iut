import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
from groq import Groq
import datetime
from discord.ext import tasks

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = 1522801616393076889

FLASK_URL = "http://localhost:5000"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
async def status(ctx):
    try:
        response = requests.get(f"{FLASK_URL}/api/devices", timeout=5)
        response.raise_for_status()
        devices = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Flask API failed: {e}")
        await ctx.send(" Couldn't reach the office dashboard right now.")
        return

    # Organize by room
    rooms = {}
    for device_id, info in devices.items():
        room = info["room"]
        if room not in rooms:
            rooms[room] = {"fans_on": 0, "fans_total": 0, "lights_on": 0, "lights_total": 0}

        if info["type"] == "fan":
            rooms[room]["fans_total"] += 1
            if info["status"] == "on":
                rooms[room]["fans_on"] += 1
        elif info["type"] == "light":
            rooms[room]["lights_total"] += 1
            if info["status"] == "on":
                rooms[room]["lights_on"] += 1

    # Build a plain-text summary for the LLM to rephrase
    lines = []
    total_on = 0
    total_devices = 0
    for room, counts in rooms.items():
        room_on = counts["fans_on"] + counts["lights_on"]
        room_total = counts["fans_total"] + counts["lights_total"]
        total_on += room_on
        total_devices += room_total
        lines.append(
            f"{room}: {counts['fans_on']}/{counts['fans_total']} fans on, "
            f"{counts['lights_on']}/{counts['lights_total']} lights on"
        )

    raw_summary = f"Overall: {total_on}/{total_devices} devices on\n" + "\n".join(lines)

    prompt = (
        "You are a friendly office assistant bot. Turn this raw device status "
        "data into a short, warm, natural message for Discord. Keep it concise "
        "(4-6 lines), dont use  emojis . Don't invent numbers, only use what's given.\n\n"
        f"Data:\n{raw_summary}"
    )

    try:
        llm_response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )
        await ctx.send(llm_response.choices[0].message.content)
    except Exception as e:
        print(f"Groq API failed: {e}")
        await ctx.send(f" *(AI phrasing unavailable, showing raw data)*\n```\n{raw_summary}\n```")

@bot.command()
async def room(ctx, *, room_name: str = None):
    valid_rooms = ["drawingroom", "workroom1", "workroom2"]

    # Normalize user input: lowercase, strip spaces
    if room_name is None:
        await ctx.send("Please tell me which room! Try `!room drawingroom`, `!room workroom1`, or `!room workroom2`.")
        return

    normalized = room_name.lower().replace(" ", "")

    # Allow some friendly aliases
    aliases = {
        "drawing": "drawingroom",
        "drawingroom": "drawingroom",
        "waitingroom": "drawingroom",
        "work1": "workroom1",
        "workroom1": "workroom1",
        "work2": "workroom2",
        "workroom2": "workroom2",
    }

    target_room = aliases.get(normalized)

    if target_room is None:
        await ctx.send(
            f" Sorry, `{room_name}` isn't a room in this office yet! "
            f"We've currently got: **Drawing Room**, **Work Room 1**, and **Work Room 2**."
        )
        return

    try:
        response = requests.get(f"{FLASK_URL}/api/devices", timeout=5)
        response.raise_for_status()
        devices = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Flask API failed: {e}")
        await ctx.send(" Couldn't reach the office dashboard right now.")
        return

    # Filter devices belonging to this room
    room_devices = {k: v for k, v in devices.items() if v["room"] == target_room}

    fans_on = sum(1 for d in room_devices.values() if d["type"] == "fan" and d["status"] == "on")
    fans_total = sum(1 for d in room_devices.values() if d["type"] == "fan")
    lights_on = sum(1 for d in room_devices.values() if d["type"] == "light" and d["status"] == "on")
    lights_total = sum(1 for d in room_devices.values() if d["type"] == "light")

    raw_summary = (
        f"Room: {target_room}\n"
        f"Fans on: {fans_on}/{fans_total}\n"
        f"Lights on: {lights_on}/{lights_total}"
    )

    prompt = (
        "You are a friendly office assistant bot. you are answering to the boss.Turn this raw room status "
        "data into a short, warm, natural Discord message (2-4 lines). "
        "Don't invent numbers, only use what's given.\n\n"
        f"Data:\n{raw_summary}"
    )

    try:
        llm_response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )
        await ctx.send(llm_response.choices[0].message.content)
    except Exception as e:
        print(f"Groq API failed: {e}")
        await ctx.send(f" *(AI phrasing unavailable, showing raw data)*\n```\n{raw_summary}\n```")

@bot.command()
async def usage(ctx):
    try:
        response = requests.get(f"{FLASK_URL}/api/usage", timeout=5)
        response.raise_for_status()
        usage_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Flask API failed: {e}")
        await ctx.send(" Couldn't reach the office dashboard right now.")
        return

    current_watts = usage_data["current_watts"]
    total_kwh = usage_data["total_kwh"]
    estimated_cost = usage_data["estimated_cost"]

    raw_summary = (
        f"Current power draw: {current_watts}W\n"
        f"Estimated usage today: {total_kwh} kWh\n"
        f"Estimated cost today: {estimated_cost} tk"
    )

    prompt = (
        "You are a friendly office assistant bot.You are answering to the boss. Turn this raw power usage "
        "data into a short, natural Discord message (2-3 lines). "
        "Don't invent numbers, only use what's given.\n\n"
        f"Data:\n{raw_summary}"
    )

    try:
        llm_response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )
        await ctx.send(llm_response.choices[0].message.content)
    except Exception as e:
        print(f"Groq API failed: {e}")
        await ctx.send(f" *(AI phrasing unavailable, showing raw data)*\n```\n{raw_summary}\n```")


async def check_after_hours_alert(channel):
    try:
        response = requests.get(f"{FLASK_URL}/api/devices", timeout=5)
        response.raise_for_status()
        devices = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Flask API failed: {e}")
        await channel.send(" Couldn't reach the office dashboard for the after-hours check.")
        return

    on_devices = {k: v for k, v in devices.items() if v["status"] == "on"}

    if not on_devices:
        await channel.send(" After-hours check (9:30 PM): everything's off. Good to go!")
        return

    lines = [" **After-hours check (9:30 PM)** — these devices are still ON:"]
    for device_id, info in on_devices.items():
        lines.append(f"- {info['room']}: {info['type']} ({device_id})")
    lines.append("\nPlease make sure someone turns these off before leaving.")

    await channel.send("\n".join(lines))


@tasks.loop(time=datetime.time(hour=21, minute=30))
async def scheduled_check():
    channel = bot.get_channel(CHANNEL_ID)
    await check_after_hours_alert(channel)


@bot.command()
async def checkafterhours(ctx):
    await check_after_hours_alert(ctx.channel)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    scheduled_check.start()

bot.run(TOKEN)