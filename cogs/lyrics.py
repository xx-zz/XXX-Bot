import discord
from discord.ext import commands
from bs4 import BeautifulSoup

from xxx import helpers


BASE_URL_GENIUS_API = "http://api.genius.com/search"


class Lyrics:
    """Commands associated with fetching lyrics of song"""


    @commands.command(aliases=['ly'])
    @commands.cooldown(6,12)
    async def lyrics(self, ctx, *args):
        """
        Description:     Get the lyrics of a song.
        Usage:           x ly [song] 
        Alternate Usage: x ly [song] | [artist]
        """

        data = await self.parse_args(args)

        songs_json = await helpers.make_request(ctx, BASE_URL_GENIUS_API, data, ctx.bot.config["genius_headers"])

        count = 0 
        for hit in songs_json["response"]["hits"]:
            await ctx.channel.trigger_typing()
            data = await self.create_embed(await self.get_song_details(hit))
            #Mechanism to display top 3 results returned by api. Can be changed as required
            count += 1
            if count == 4:
                break
            await ctx.send(embed=data)

        message = await ctx.bot.wait_for('message',check = lambda message: message.author == ctx.message.author and message.channel == ctx.message.channel)

        #check if value sent by user is in range. 
        if int(message.content) in [i for i in list(range(1, 4))]:
            await ctx.send('Understood!')
            await ctx.channel.trigger_typing()
            count = 0

            for hit in songs_json["response"]["hits"]:
                count += 1
                song_details = await self.get_song_details(hit)
                if count == int(message.content):
                    break
            
            lyrics = await self.scrape_song_page(await helpers.make_request(ctx, song_details[2]))
            data = await self.create_embed(song_details, len(lyrics), is_lyrics=True)

            #split lyrics by paragraphs to circumvent 2000 word limit
            paragraphs = lyrics.split('\n\n')
            for para in paragraphs:
                data.add_field(name='--', value=para + '..', inline=False)
            
            await ctx.send(embed=data)
        
        else:
            #value entered by user is out of range or some random value
            await ctx.send('Fuck off!')



    async def parse_args(self, args):
        """Return the data dictionary of form {'q': song_title}"""
        
        #I keep forgetting args are tuple lol..
        args_str = ' '.join(args)
        print(args_str)

        if '|' in args_str:
            parameters = await helpers.get_parameters(args_str)
            self.song_title = parameters[0]
            self.artist_name = parameters[1]
            print(self.song_title)
            print(self.artist_name)
        else:
            self.song_title = " ".join(args)
            self.artist_name = None
            print(self.song_title)
        
        data = {'q' : self.song_title}

        return data


   
    async def get_song_details(self, hit):
        """Returns relevant data about song from json file for further processing"""
        artist = hit["result"]["primary_artist"]["name"]
        name = hit["result"]['title_with_featured']
        page_url = hit["result"]["url"]
        thumb_url = hit["result"]["primary_artist"]["image_url"]
        state = hit["result"]["lyrics_state"]
        image_url = hit["result"]["header_image_url"]
        return artist, name, page_url, thumb_url, state, image_url



    async def create_embed(self, song_details, lyrics_len=None, is_lyrics=False):
        """Returns discord.embed object with song_details"""

        if is_lyrics is False:
            data = discord.Embed(description=song_details[0], colour=discord.Color(value=await helpers.get_color()))
            data.set_author(name=song_details[1], url=song_details[2])
            data.set_thumbnail(url=song_details[3])
            data.set_footer(text="Lyrics State: " + song_details[4])
            return data

        data = discord.Embed(description=song_details[0], colour=discord.Color(value=await helpers.get_color()))
        data.set_author(name=song_details[1], url=song_details[2])
        data.set_thumbnail(url=song_details[5])
        data.set_footer(text="Total characters:" + str(lyrics_len))
        return data



    async def scrape_song_page(self, song_page):
        """remove script tags that they put in the middle of the lyrics
           lyrics tag contains the actual lyrics. check their source code for details
        """
        html = BeautifulSoup(song_page.decode('utf-8'), 'html5lib')
        [h.extract() for h in html('script')]
        lyrics = html.find("div", class_="lyrics").get_text()
        return lyrics


      
def setup(bot):
    bot.add_cog(Lyrics()) 


