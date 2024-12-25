import discord
from discord.ext import commands
import clash_commands
from sharkie import version


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = '.', intents = intents)
bot.remove_command('help')

class Clash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_tag(self, tag):
        """Checks if clan tag is correct."""
        if tag[0] != '#':
            return False
        return True
    
    async def invalid_tag(self, ctx, tag):
        """Prints invalid tag embed."""
        await ctx.send(f'invalid tag: {tag}')

    @commands.command()
    async def whois(self, ctx, tag):
        """Returns user information."""

        if not self.check_tag(tag):
            await ctx.send(f'invalid tag: {tag}')

        res = clash_commands.Clash.get_user(tag[1:])
        if len(res) == 2:
            # error
            await ctx.send((res['reason'], res['message']))
        else:
            # 200
            await ctx.send((res['name'], res['clan']['name']))
            
    @commands.command()
    async def clan(self, ctx, tag):
        """Returns information about clan."""

        if not self.check_tag(tag):
            await ctx.send(f'invalid tag: {tag}')

        res = clash_commands.Clash.get_clan(tag[1:])
        if len(res) == 1:
            # error
            embed=discord.Embed(title = res['reason'], description = 'confirm the tag and try again', color = 0xFF0000)
            await ctx.send(embed=embed)
        else:
            # 200
            embed=discord.Embed(
                title = res['name'],
                description = res['description'] + '\n\n' + f'Members: {res["members"]}/50',
                color = 0x7CFC00,
                url=f'https://link.clashofclans.com/en?action=OpenClanProfile&tag=%23{res["tag"][1:]}'
            )
            embed.set_thumbnail(url=res['badgeUrls']['medium'])
            embed.set_footer(text = f'{version}')
                
            await ctx.send(embed=embed)

    @commands.command()
    async def cm(self, ctx, tag):
        """Returns the clan members for the specified clan."""
        if not self.check_tag(tag):
            await ctx.send(f'invalid tag: {tag}')

        res = clash_commands.Clash.get_clan_members(tag[1:])

        if len(res) == 1:
            # error
            embed=discord.Embed(title = res['reason'], description = 'confirm the tag and try again', color = 0xFF0000)
            await ctx.send(embed=embed)
        else:
            # 200
            mem_list = ''
            co_list = ''
            leader = ''
            elder_list = ''

            # loop for formatting, MAX loop == 50
            max_name = 0
            clan_count = 0
            for mem in res['items']:
                clan_count += 1
                name = mem['name']
                max_name = max(max_name, len(name))

            for mem in res['items']:

                name = mem['name']
                mem_tag = mem['tag']

                if mem['role'] == 'admin':
                    elder_list += f'{name} -- `{mem_tag}`\n'
                elif mem['role'] == 'coLeader':
                    co_list += f'{name} -- `{mem_tag}`\n'
                elif mem['role'] == 'member':
                    mem_list += f'{name} -- `{mem_tag}`\n'
                else:
                    leader += f'{name} -- `{mem_tag}`\n'


            if clan_count > 40:
                color = 0xFFA500
            elif clan_count > 20:
                color = 0xADD8E6  
            else:
                color = 0x000000
            embed = discord.Embed(
                title = 'Clan Details',
                color = color  
            )

            embed.add_field(name = 'Clan Leader', value = leader, inline=False)
            embed.add_field(name = 'CoLeaders', value = co_list, inline=False)
            embed.add_field(name = 'Elders', value= elder_list, inline=False)
            embed.add_field(name = 'Members', value = mem_list, inline=False)
            embed.set_footer(text = f'{version}')
            await ctx.send(embed=embed)



        



async def setup(bot):
    await bot.add_cog(Clash(bot))
