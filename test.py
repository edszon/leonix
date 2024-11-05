import discord
import os
from dotenv import load_dotenv
import random
from gtts import gTTS
import asyncio
import time

load_dotenv() 

bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="hello", description="Say hello to a specific user")
async def hello(ctx: discord.ApplicationContext, username: str):
    await ctx.respond(f"Hey, {username}!")

@bot.slash_command(name="russian", description="Disconnect a user from voice")
async def russian(ctx: discord.ApplicationContext):
    await ctx.respond('Roleta russa iniciada.')
    
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        random_member = random.choice(channel.members)
        random_member_name = random_member.nick or random_member.name
        
        # First TTS message for the selected member
        nuke_audio1 = gTTS(text=f"A arma foi carregada. Tchau, {random_member_name}!", lang="pt-br", slow=False)
        nuke_audio1.save("nuke1.mp3")

        # Connect bot to the voice channel
        voice_client = await channel.connect()
        
        # Play first message, then disconnect the member
        voice_client.play(discord.FFmpegPCMAudio("nuke1.mp3"), 
                          after=lambda e: bot.loop.create_task(disconnect_member_and_play_second(random_member, voice_client, channel)))
        
async def disconnect_member_and_play_second(random_member, voice_client, channel):
    # Disconnect the first selected member
    if random_member.voice:
        time.sleep(2)
        if random_member.id == 145322978429763584:
            voice_client.play(discord.FFmpegPCMAudio("empty.mp3"))
            time.sleep(1)
            empty = gTTS(text=f"Acabou minha munição. Tchau.", lang="pt-br", slow=False)
            empty.save('emptyspeech.mp3')
            voice_client.play(discord.FFmpegPCMAudio("emptyspeech.mp3"))
            time.sleep(3.5)
            await voice_client.disconnect()
            return
        else:
            voice_client.play(discord.FFmpegPCMAudio('gunshot.mp3'))
            await random_member.move_to(None)  # Move the user out of the voice channel
            time.sleep(2)
    
    # Wait to ensure the member is disconnected before proceeding
    await asyncio.sleep(1)

    # Select a second random member for the second TTS message
    remaining_members = [m for m in channel.members if m != random_member and not m.bot]
    if remaining_members:
        second_random_member = random.choice(remaining_members)
        second_member_name = second_random_member.nick or second_random_member.name
    else:
        second_member_name = "ninguém"  # If no members are left, use a placeholder

    # Second TTS message
    nuke_audio2 = gTTS(text=f"Que isso sirva de lição, {second_member_name}!", lang="pt-br", slow=False)
    nuke_audio2.save("nuke2.mp3")

    # Play the second message, then disconnect the bot
    voice_client.play(discord.FFmpegPCMAudio("nuke2.mp3"), 
                      after=lambda e: bot.loop.create_task(disconnect_bot(voice_client)))

async def disconnect_bot(voice_client):
    # Wait for the second audio to finish playing, then disconnect the bot
    while voice_client.is_playing():
        await asyncio.sleep(1)
    await voice_client.disconnect()  # Disconnect the bot from the voice channel

    # Clean up the audio files
    os.remove("nuke1.mp3")
    os.remove("nuke2.mp3")

bot.run(os.getenv('TOKEN'))  # Run the bot with the token
