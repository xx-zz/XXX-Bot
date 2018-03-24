import json

import discord
from discord.ext import commands

from xxx import helpers

BASE_API_URL = 'http://api.football-data.org/v1/competitions'

class Soccer:
    """Commands associated with fetching Soccer related data"""

    @commands.command()
    @commands.cooldown(6,12)

    async def table(self, ctx, *args):
        """Fetch standings of given league"""

        raw_data = await helpers.make_request(ctx, BASE_API_URL)
        data = json.loads(raw_data.decode('utf-8'))

        prem_league = data[1]
        prem_teams_url = prem_league['_links']['leagueTable']['href']
        print(prem_teams_url)

        raw_data = await helpers.make_request(ctx, prem_teams_url)
        data = json.loads(raw_data.decode('utf-8'))

        data_embed=discord.Embed(title=f"Matchday {data['matchday']}", description="-------------------------------------------------------------------------------", colour=discord.Color(value=await helpers.get_color()))
        data_embed.set_author(name=data['leagueCaption'])

        count = 0
        for team in data['standing']:
            data_embed.add_field(name='\u200b', value='\u200b', inline=True)
            data_embed.add_field(name=f"{team['position']}.  {team['teamName']}" , value=f"Played: {team['playedGames']}    Points: {team['points']}    Wins: {team['wins']}   Draws: {team['draws']}   Losses: {team['losses']}    GF: {team['goals']}    GA: {team['goalsAgainst']}    GD: {team['goalDifference']}", inline=True)
            count+=1
            if count == 10: break
          
        await ctx.send(embed=data_embed)

        #reacting with forward arrow
        async for message in ctx.channel.history():
            print('test')
            await message.add_reaction('👎')
            


def setup(bot):
    bot.add_cog(Soccer())
