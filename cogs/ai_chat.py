import discord
from discord.ext import commands
import asyncio
import time
import logging
from utils.llm_handler import LlamaModel
from config import CHAT_CONFIG

logger = logging.getLogger('ai_chat')

class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.llm = LlamaModel()
        self.chat_histories = {}
        logger.info("AIChat cog initialized")

    @commands.command(name='chat', aliases=['c'])
    async def chat_command(self, ctx, *, message=None):
        """Chat with the sassy Discord AI"""
        if not message:
            await ctx.send("Uh, hello? Did you forget to type something? I'm not a mind reader, you know.")
            return

        await self.handle_chat(ctx.message, message)

    async def handle_chat(self, message, content):
        """Process chat messages from commands or mentions"""
        user_id = str(message.author.id)

        if user_id not in self.chat_histories:
            self.chat_histories[user_id] = []

        async with message.channel.typing():
            # Get AI response
            start_time = time.time()
            ai_response = self.llm.generate_response(content, self.chat_histories[user_id])
            inference_time = time.time() - start_time

            logger.info(f"Generated response in {inference_time:.2f}s")

            typing_time = min(len(ai_response) / CHAT_CONFIG['typing_speed'], 5)
            if typing_time > inference_time:
                await asyncio.sleep(typing_time - inference_time)

            self.chat_histories[user_id].append((content, ai_response))
            if len(self.chat_histories[user_id]) > CHAT_CONFIG['history_limit']:
                self.chat_histories[user_id].pop(0)

        if len(ai_response) <= CHAT_CONFIG['max_response_length']:
            await message.reply(ai_response)
        else:
            parts = [ai_response[i:i + CHAT_CONFIG['max_response_length']]
                     for i in range(0, len(ai_response), CHAT_CONFIG['max_response_length'])]
            for i, part in enumerate(parts):
                if i == 0:
                    await message.reply(part)
                else:
                    await message.channel.send(part)

    @commands.command(name='reset')
    async def reset_chat(self, ctx):
        """Reset your chat history with the bot"""
        user_id = str(ctx.author.id)
        if user_id in self.chat_histories:
            self.chat_histories[user_id] = []
            await ctx.send("Fine, I've erased our conversation. Happy now? 🙄")
        else:
            await ctx.send("We haven't even talked yet. Awkward much?")

    @commands.command(name='sass')
    async def adjust_sass(self, ctx, level: int = None):
        """Adjust sass level (1-10) or view current level"""
        await ctx.send(
            "Sass level adjustment? As if I'd let you control my attitude. My sass is non-negotiable, honey. 💅")


async def setup(bot):
    await bot.add_cog(AIChat(bot))