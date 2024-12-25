import discord
import asyncio
from discord.ext import commands


active_reaction_message_id = {} 

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        msg =discord.Embed(colour=discord.Colour.purple(), description="Calculating...")
        msg2=discord.Embed(colour=discord.Colour.purple(), description=f"Fancy ping: **{round(self.bot.latency * 1000)}ms**. \nNB. If the ping is bad #blamehurri")
        msg3 = await ctx.send(embed=msg)
        await asyncio.sleep(1)
        await msg3.edit(embed=msg2)

    @commands.command()
    async def clear(self, ctx, amount=5):
        """Clear set amout of messagess."""
        await ctx.channel.purge(limit=amount+1)

async def setup(bot):
    await bot.add_cog(Admin(bot))

 
