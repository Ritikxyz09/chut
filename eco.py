# eco.py
import asyncio
import subprocess
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import AudioPiped

# ====== APNI DETAILS DAAL ======
API_ID = 24788715                # <-- apna API ID
API_HASH = "1803bb45fb125f52ff171f1d550ac5a9"    # <-- apna API HASH
BOT_TOKEN = "8299355346:AAGb7Hat7XZJfNi2GmocXV_Lj8CFY9XnjtE"  # <-- apna BOT TOKEN
# ===============================

app = Client("eco-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call = PyTgCalls(app)


# ---------- AUDIO PROCESS FUNCTION ----------
def process_audio(input_src, out_file):
    cmd = [
        "ffmpeg", "-y",
        "-i", input_src,
        "-af", "volume=10.0,aecho=0.6:0.6:120:0.5",
        "-ar", "48000",
        "-ac", "2",
        "-f", "opus",
        out_file
    ]
    subprocess.check_call(cmd)


# ------------ PLAY COMMAND ----------
@app.on_message(filters.command(["play", "p"]))
async def play_audio(client, message):
    if not message.reply_to_message or not message.reply_to_message.audio:
        return await message.reply("Reply kisi audio file ko karo 🎵")

    msg = await message.reply("Echo + Boost laga raha hoon… 🔊🔥")

    file = await message.reply_to_message.download()
    out = "out.opus"

    # Boost + Echo
    process_audio(file, out)

    # Play in VC
    await call.join_group_call(
        message.chat.id,
        AudioPiped(out)
    )

    await msg.edit("Playing in VC with **Echo + High Volume** 🎤🔥")


# ------------ AUTO END ------------
@call.on_stream_end()
async def stream_end_handler(_, update):
    print("Audio finished.")


# ------------ START BOT ------------
async def main():
    await app.start()
    await call.start()
    print("eco.py bot started! 🔥")
    await idle()

asyncio.run(main())