import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio

# APIS

from pygelbooru import Gelbooru
import praw
import py621



## "dude what the fuck is wrong with you, why dont you use cogs?"
## FUCK COGS

client=commands.Bot(command_prefix="./", help_command=None)

e621api = py621.public.apiGet(py621.types.e621)
## using api key isn't required
e926api = py621.public.apiGet(py621.types.e926)

######### OTHER LOGIC ######################################### OTHER LOGIC ###############################
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game(name="owo"))
        await asyncio.sleep(1000)
        await client.change_presence(activity=discord.Game(name="uwu"))
        await asyncio.sleep(1000)
        await client.change_presence(activity=discord.Game(name="i love you so much alexei <3"))
        await asyncio.sleep(50)


###### CLIENT EVENTS ##################################### CLIENT EVENTS #################################
@client.event
async def on_ready():
    client.loop.create_task(status_task())
    print("!!! ready to destroy >:3 !!!")

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
     await message.channel.send("""
     ``Command prefix is ./ (CRAZY LINUX REFERNCE!!)``
     ``eevee - random image of an eevee``
     ``e621/e926 - search images on e621.net``
     ``femboy - random image of a femboy from r/femboy``
     """)
    await client.process_commands(message)

########## CLIENT COMMANDS ####################################### CLIENT COMMANDS ########################3

@client.command()
async def help(ctx):
    await ctx.send("""
    ``Command prefix is ./ (CRAZY LINUX REFERNCE!!)``
    ``eevee - random image of an eevee``
    ``e621/e926 - search images on e621.net``
    ``femboy - random image of a femboy from r/femboy``
    """)
@client.command()
async def eevee(ctx):
 gelbooru = Gelbooru('GELBOORU API KEY', 'GELBOORU USER ID')
 results = await gelbooru.search_posts(tags=['eevee', 'sort:random'], exclude_tags=['rating:explicit', '1girl', '1boy', '2girls', '2boys', '3girls', '4girls', '3boys', '4boys', '5girls', '6+girls', '7+girls', '5boys', '6+boys', 'anime_coloring'])
 result = results[0]
 embed = discord.Embed(title="mmmm eeve", color=0x0)
 embed.set_image(url=result.file_url)
 embed.set_footer(text=f'https://smug.ga - post ID: {result.id}')
 await ctx.send(embed=embed)

@client.command()
async def damndaniel(ctx):
    await ctx.send("stop")


@client.command(aliases=['e9pool'])
@commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
async def e926pool(ctx, *, key):
 pool_id = (key)
 PostSelect = int(0)
 await ctx.send("fetching posts, this could take awhile...", delete_after=3.5)
 pool = e926api.getPool(pool_id)
 Posts = pool.getPosts()
 Post = Posts[PostSelect]
 post_orgin = str(Post.id)
 try:
  pool_id_try = Post.pools[0]
 except IndexError:
  pool_id_try = ("(None)")
 embed = discord.Embed(title=f'{pool.name}',url='https://e621.net/posts/' + post_orgin, color=0x0)
 embed.set_image(url=Post.file.url)
 embed.set_footer(text=f'In Pool: {pool_id_try} - post ID: {Post.id}')
 react = await ctx.reply(embed=embed)
 await react.add_reaction('◀')
 await react.add_reaction('▶')
 await react.add_reaction('🚫')
 while True:
  try:
   reaction, user = await ctx.bot.wait_for("reaction_add", timeout=200, check=lambda reaction, user: user == ctx.author and reaction.emoji in ["▶", "◀","🚫"])
   if str(reaction.emoji) == "🚫":
    killed = discord.Embed(title="Dead thread.", description=f'{ctx.message.author.mention} manually killed their thread', color=0x0)
    await react.edit(embed = killed)
    return
   if str(reaction.emoji) == "▶":
    PostSelect+=1
    Post = Posts[PostSelect]
    post_orgin = str(Post.id)
    newEmbed = discord.Embed(title=f'{pool.name}',url='https://e621.net/posts/' + post_orgin, color=0x0)
    newEmbed.set_image(url=Post.file.url)
    newEmbed.set_footer(text=f'In Pool: {pool_id_try} - post ID: {Post.id}')
    await react.edit(embed = newEmbed)
   if str(reaction.emoji) == "◀":
    PostSelect-=1
    Post = Posts[PostSelect]
    post_orgin = str(Post.id)
    newEmbed = discord.Embed(title=f'{pool.name}', url='https://e621.net/posts/' + post_orgin, color=0x0)
    newEmbed.set_image(url=Post.file.url)
    newEmbed.set_footer(text=f'In Pool: {pool_id_try} - post ID: {Post.id}')
    await react.edit(embed = newEmbed)
  except IndexError:
   print(f'wrapping around on {ctx.message.author.name}s thread')
  except asyncio.TimeoutError:
   timeout = discord.Embed(title="Dead thread.", description=f'{ctx.message.author.mention} stopped interacting with their thread', color=0x0)
   await react.edit(embed = timeout)
   return


@client.command(aliases=['e9'])
@commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
async def e926(ctx, *, key):
 tags = []
 dwd = str()
 ele = str(key)
 vlv = int(0)
 tags.append(dwd)
 tags.append(ele)
 Posts = e926api.getPosts(tags, 10, 1, False)
 Post = Posts[vlv]
 post_orgin = str(Post.id)
 embed = discord.Embed(title="Post Link",url='https://e621.net/posts/' + post_orgin, color=0x0)
 try:
  embed.set_image(url=Post.file.url)
 except Exception:
  embed = discord.Embed(title="Bad request",url='https://e621.net/posts/' + post_orgin, color=0x0)
  embed.set_image(url="https://cdn.discordapp.com/attachments/940740865129865219/969415635136299068/pointless.png")
 try:
  pool_id_try = Post.pools[0]
 except IndexError:
  pool_id_try = ("(None)")
 embed.set_footer(text=f'In Pool: {pool_id_try} - post ID: {Post.id}')
 react = await ctx.send(embed=embed)
 await react.add_reaction('◀')
 await react.add_reaction('▶')
 await react.add_reaction('🚫')
 while True:
  try:
   reaction, user = await ctx.bot.wait_for("reaction_add", timeout=90, check=lambda reaction, user: user == ctx.author and reaction.emoji in ["▶", "◀","🚫"])
   if str(reaction.emoji) == "🚫":
    killed = discord.Embed(title="Dead thread.", description=f'{ctx.message.author.mention} manually killed their thread', color=0x0)
    await react.edit(embed = killed)
    return
   if str(reaction.emoji) == "▶":
    vlv+=1
    Post = Posts[vlv]
    post_orgin = str(Post.id)
    newEmbed = discord.Embed(title="Post Link",url='https://e621.net/posts/' + post_orgin, color=0x0)
    try:
     newEmbed.set_image(url=Post.file.url)
    except Exception:
     embed = discord.Embed(title="Bad request",url='https://e621.net/posts/' + post_orgin, color=0x0)
     embed.set_image(url="https://cdn.discordapp.com/attachments/940740865129865219/969415635136299068/pointless.png")
    try:
     pool_id_try = Post.pools[0]
    except IndexError:
     pool_id_try = ("(None)")
    newEmbed.set_footer(text=f'In Pool: {pool_id_try} - post ID: {Post.id}')
    await react.edit(embed = newEmbed)
   if str(reaction.emoji) == "◀":
    vlv-=1
    Post = Posts[vlv]
    post_orgin = str(Post.id)
    newEmbed = discord.Embed(title="Post Link",url='https://e621.net/posts/' + post_orgin, color=0x0)
    newEmbed.set_image(url=Post.file.url)
    try:
     pool_id_try = Post.pools[0]
    except IndexError:
     pool_id_try = ("(None)")
    newEmbed.set_footer(text=f'In Pool: {pool_id_try} - post ID: {Post.id}')
    await react.edit(embed = newEmbed)
  except IndexError:
   print(f'wrapping around on {ctx.message.author.name}s thread')
  except asyncio.TimeoutError:
   timeout = discord.Embed(title="Dead thread.", description=f'{ctx.message.author.mention} stopped interacting with their thread', color=0x0)
   await react.edit(embed = timeout)
   return

@client.command(aliases=['e6pool'])
@commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
async def e621pool(ctx, *, key):
 if not ctx.channel.is_nsfw():
  await ctx.send("Only use this command in an nsfw channel", delete_after=2)
  return
 pool_id = (key)
 PostSelect = int(0)
 await ctx.send("fetching posts, this could take awhile...", delete_after=3.5)
 pool = e621api.getPool(pool_id)
 Posts = pool.getPosts()
 Post = Posts[PostSelect]
 post_orgin = str(Post.id)
 try:
  pool_id_try = Post.pools[0]
 except IndexError:
  pool_id_try = ("(None)")
 embed = discord.Embed(title=f'{pool.name}',url='https://e621.net/posts/' + post_orgin, color=0x0)
 embed.set_image(url=Post.file.url)
 embed.set_footer(text=f'In Pool: {pool_id_try} - post ID: {Post.id}')
 react = await ctx.reply(embed=embed)
 await react.add_reaction('◀')
 await react.add_reaction('▶')
 await react.add_reaction('🚫')
 while True:
  try:
   reaction, user = await ctx.bot.wait_for("reaction_add", timeout=200, check=lambda reaction, user: user == ctx.author and reaction.emoji in ["▶", "◀","🚫"])
   if str(reaction.emoji) == "🚫":
    killed = discord.Embed(title="Dead thread.", description=f'{ctx.message.author.mention} manually killed their thread', color=0x0)
    await react.edit(embed = killed)
    return
   if str(reaction.emoji) == "▶":
    PostSelect+=1
    Post = Posts[PostSelect]
    post_orgin = str(Post.id)
    newEmbed = discord.Embed(title=f'{pool.name}',url='https://e621.net/posts/' + post_orgin, color=0x0)
    newEmbed.set_image(url=Post.file.url)
    newEmbed.set_footer(text=f'In Pool: {pool_id_try} - post ID: {Post.id}')
    await react.edit(embed = newEmbed)
   if str(reaction.emoji) == "◀":
    PostSelect-=1
    Post = Posts[PostSelect]
    post_orgin = str(Post.id)
    newEmbed = discord.Embed(title=f'{pool.name}', url='https://e621.net/posts/' + post_orgin, color=0x0)
    newEmbed.set_image(url=Post.file.url)
    newEmbed.set_footer(text=f'In Pool: {pool_id_try} - post ID: {Post.id}')
    await react.edit(embed = newEmbed)
  except IndexError:
   print(f'wrapping around on {ctx.message.author.name}s thread')
  except asyncio.TimeoutError:
   timeout = discord.Embed(title="Dead thread.", description=f'{ctx.message.author.mention} stopped interacting with their thread', color=0x0)
   await react.edit(embed = timeout)
   return

@client.command(aliases=['e6'])
@commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
async def e621(ctx, *, key):
 if not ctx.channel.is_nsfw():
  await ctx.send("Only use this command in an nsfw channel", delete_after=2)
  return
 tags = []
 dwd = str("-young")
 ele = str(key)
 vlv = int(0)
 tags.append(dwd)
 tags.append(ele)
 Posts = e621api.getPosts(tags, 10, 1, False)
 Post = Posts[vlv]
 post_orgin = str(Post.id)
 embed = discord.Embed(title="Post Link",url='https://e621.net/posts/' + post_orgin, color=0x0)
 try:
  embed.set_image(url=Post.file.url)
 except Exception:
  embed = discord.Embed(title="Bad request",url='https://e621.net/posts/' + post_orgin, color=0x0)
  embed.set_image(url="https://cdn.discordapp.com/attachments/940740865129865219/969415635136299068/pointless.png")
 try:
  pool_id_try = Post.pools[0]
 except IndexError:
  pool_id_try = ("(None)")
 embed.set_footer(text=f'In Pool: {pool_id_try} - post ID: {Post.id}')
 react = await ctx.send(embed=embed)
 await react.add_reaction('◀')
 await react.add_reaction('▶')
 await react.add_reaction('🚫')
 while True:
  try:
   reaction, user = await ctx.bot.wait_for("reaction_add", timeout=90, check=lambda reaction, user: user == ctx.author and reaction.emoji in ["▶", "◀","🚫"])
   if str(reaction.emoji) == "🚫":
    killed = discord.Embed(title="Dead thread.", description=f'{ctx.message.author.mention} manually killed their thread', color=0x0)
    await react.edit(embed = killed)
    return
   if str(reaction.emoji) == "▶":
    vlv+=1
    Post = Posts[vlv]
    post_orgin = str(Post.id)
    newEmbed = discord.Embed(title="Post Link",url='https://e621.net/posts/' + post_orgin, color=0x0)
    try:
     newEmbed.set_image(url=Post.file.url)
    except Exception:
     embed = discord.Embed(title="Bad request",url='https://e621.net/posts/' + post_orgin, color=0x0)
     embed.set_image(url="https://cdn.discordapp.com/attachments/940740865129865219/969415635136299068/pointless.png")
    try:
     pool_id_try = Post.pools[0]
    except IndexError:
     pool_id_try = ("(None)")
    newEmbed.set_footer(text=f'In Pool: {pool_id_try} - post ID: {Post.id}')
    await react.edit(embed = newEmbed)
   if str(reaction.emoji) == "◀":
    vlv-=1
    Post = Posts[vlv]
    post_orgin = str(Post.id)
    newEmbed = discord.Embed(title="Post Link",url='https://e621.net/posts/' + post_orgin, color=0x0)
    newEmbed.set_image(url=Post.file.url)
    try:
     pool_id_try = Post.pools[0]
    except IndexError:
     pool_id_try = ("(None)")
    newEmbed.set_footer(text=f'In Pool: {pool_id_try} - post ID: {Post.id}')
    await react.edit(embed = newEmbed)
  except IndexError:
   print(f'wrapping around on {ctx.message.author.name}s thread')
  except asyncio.TimeoutError:
   timeout = discord.Embed(title="Dead thread.", description=f'{ctx.message.author.mention} stopped interacting with their thread', color=0x0)
   await react.edit(embed = timeout)
   return


@client.command()
async def femboy(ctx):
 reddit = praw.Reddit(check_for_async=False,client_id='tAa1kJciPf5BRVc2O43a0w',client_secret='4GkW7gGdAD2uKWsFsh3ibngzwrxyjA',user_agent='fetched-it-smug0842')
 femboys =reddit.subreddit('femboy').hot()
 post_to_pick = random.randint(1, 100)
 for i in range(0, post_to_pick):
  submission = next(x for x in femboys if not x.stickied)
 embed = discord.Embed(title="Post Link",url='https://reddit.com' + submission.permalink, color=0x0)
 embed.set_image(url=submission.url)
 embed.set_footer(text="https://smug.ga")
 await ctx.send(embed=embed)






client.run("TOKEN")
