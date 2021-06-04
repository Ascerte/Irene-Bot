import discord
from discord.ext import commands
import asyncio
from discord.utils import get
from NinjaParser import NinjaParser
from config import *

reddit_submission_limit = 5

bot = commands.Bot(command_prefix='!')
bot.remove_command("help")
def embed_result(result, ctx):
    emoji = get(ctx.guild.emojis, name="chaos")
    if len(result) == 2:  # two different embeds because currency has no icon
        return discord.Embed(
            description=f'**Item: {result[0]}\n Value: {result[-1]}{emoji}**',
            colour=discord.Colour.from_rgb(145, 48, 191)
        )
    else:
        return discord.Embed(
            description=f'**Item: {result[0]}\n Value: {result[-1]}{emoji}**',
            colour=discord.Colour.from_rgb(145, 48, 191)
        ).set_thumbnail(url=result[1])


def embed_message(string, author=""):
    return discord.Embed(
        description=string, colour=discord.Colour.from_rgb(145, 48, 191)
    ).set_author(name=author)


def spotify_search(sp, arg):
    query = ""
    for i in arg:
        query = query + ' ' + i
    result = sp.search(q=query, limit=1, type='track')
    print(query)
    track = ""
    for i, t in enumerate(result['tracks']['items']):
        track = t['uri']
    return track.split(':')[2]


@bot.event
async def on_ready():
    print("Bot initialized successfully")


@bot.command()
async def wrong(ctx):
    await ctx.send("https://tenor.com/view/trump-wrong-gif-9112613")


@bot.command(name="cheese")
async def cheez(ctx):
    await ctx.send("https://tenor.com/view/james-may-cheese-dairy-gif-17289168")


@bot.command()
async def straightlick(ctx):
    await ctx.send(
        "https://tenor.com/view/jojo-jojos-bizarre-adventure-lick-giorno-gionvanna-bruno-bucciarati-gif-13273306")


@bot.command()
async def heheboy(ctx):
    await ctx.send("https://tenor.com/view/he-hehe-boy-boi-boyi-gif-7890844")


@bot.command()
async def goodolrub(ctx):
    await ctx.send("https://tenor.com/view/meat-good-rub-gif-12963573")


@bot.command()
async def sauce(ctx, *arg):
    if len(arg) == 0:
        await ctx.send("Insufficient arguments")
        return
    elif len(arg) > 1:
        await ctx.send("Too many arguments")
        return
    await ctx.send("http://saucenao.com/search.php?db=999&url=" + arg[0])


@bot.command()
async def reddit(ctx, *arg):
    if len(arg) == 0:
        await ctx.send(embed=embed_message("Insufficient arguments"))
        return
    subreddit = reddit_api.subreddit(arg[0])
    posts = subreddit.hot(limit=50)

    try:
        if subreddit.over18 and not ctx.channel.is_nsfw():
            await ctx.send(embed=embed_message("You are not allowed to post NSFW pictures in this channel."))
        else:
            await ctx.send(embed=embed_message("Please wait! It might take a while"))
            count = 0
            for post in posts:
                if count == reddit_submission_limit:
                    return
                if not post.stickied:
                    if post.over_18 and not ctx.channel.is_nsfw():
                        continue
                    else:
                        count += 1
                        await ctx.send(post.url)
                        await asyncio.sleep(1)
    except:
        await ctx.send(embed=embed_message("Invalid subreddit"))


@bot.command()
async def poepc(ctx, *arg):
    if len(arg) < 2:
        await ctx.send(embed=embed_message("Insufficient arguments"))
        return
    ninjaParser = NinjaParser()
    league = arg[0]
    separator = " "
    query = separator.join(arg[1:])
    result = ninjaParser.query(league, query)
    if result is not None:
        embed = embed_result(result, ctx)
    else:
        embed = embed_message("Item cannot be found")
    await ctx.send(embed=embed)


@bot.command()
async def spotify(ctx, *arg):
    print(arg)
    if len(arg) == 0:
        await ctx.send(embed=embed_message("Insufficient arguments"))
        return
    await ctx.send("https://open.spotify.com/track/" + spotify_search(sp, arg))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == 'hello there':
        await message.channel.send('General Kenobi')
    await bot.process_commands(message)


@bot.command()
async def setup(ctx):
    with open("resources/Chaos.png", "rb") as image:
        image_bytes = image.read()
        await ctx.guild.create_custom_emoji(name="chaos", image=image_bytes)
    await ctx.send(embed=embed_message("Bot initialized successfully"))


@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(title="Irene Bot Help", colour=discord.Colour.from_rgb(145, 48, 191),
                          )
    embed.add_field(name="!help", value="Displays this message", inline=False)
    embed.add_field(name="!spotify", value="Can take multiple arguments and links the spotify song link for the query",
                    inline=False)
    embed.add_field(name="!cheese", value="cheez.gif", inline=False)
    embed.add_field(name="!wrong", value="wrong.gif", inline=False)
    embed.add_field(name="!straightlick", value="bucciaratti.gif", inline=False)
    embed.add_field(name="!heheboy", value="heheboy.gif", inline=False)
    embed.add_field(name="!goodolrub", value="goodolrub.gif", inline=False)
    embed.add_field(name="!sauce",
                    value="Takes an URL to a picture as argument and outputs a link to the respective SAUCENAO page",
                    inline=False)

    embed.add_field(name="!reddit",
                    value="Takes one argument as the name of a subreddit and returns the top 5 posts on the front "
                          "page. Doesn't post NSFW content in non NSFW channels",
                    inline=False)
    embed.add_field(name="!poepc", value="Price checks an item on the poe.ninja API. First argument must be the league",
                    inline=False)
    embed.add_field(name="!setup", value="Setup command for first start up on a server.", inline=False)
    await ctx.send(embed=embed)


bot.run(BOT_TOKEN)
