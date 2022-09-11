import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import interactions

# APIS

import praw
import py621


## "dude what the fuck is wrong with you, why dont you use cogs?"
## FUCK COGS

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="./", help_command=None, intents=intents)

e621api = py621.public.apiGet(py621.types.e621)
## using api key isn't required
e926api = py621.public.apiGet(py621.types.e926)

######### OTHER LOGIC ######################################### OTHER LOGIC ###############################
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game(name="owo"))
        await asyncio.sleep(15)
        await client.change_presence(activity=discord.Game(name="uwu"))
        await asyncio.sleep(15)


###### CLIENT EVENTS ##################################### CLIENT EVENTS #################################
@client.event
async def on_ready():
    client.loop.create_task(status_task())
    print("!!! ready to destroy >:3 !!!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.mention_everyone:
        return
    if client.user.mentioned_in(message):
     await message.channel.send("""
     ``Command prefix is ./``
     ``e621/e926 - search images on e621.net``
     ``femboy - random image of a femboy from r/femboy``
     """)
    await client.process_commands(message)

########## CLIENT COMMANDS ####################################### CLIENT COMMANDS #########################

@client.command()
async def help(ctx):
    await ctx.send("""
    ``Command prefix is ./``
    ``e621/e926 - search images on e621.net``
    ``femboy - random image of a femboy from r/femboy``
    """)

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
   await ctx.send("reached the end of e621 page", delete_after=3.5)
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
 tags = []
 if "+webm" in key:
    dwd = str("-young -scat")
    key = key.replace('+webm', '')
 else:
    dwd = str("-young -scat -webm")
 ele = str(key)
 vlv = int(0)
 tags.append(dwd)
 tags.append(ele)
 Posts = e621api.getPosts(tags, 60, 1, False)
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
    await react.remove_reaction("🚫", user)
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
    await react.remove_reaction("▶", user)
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
    await react.remove_reaction("◀", user)
  except IndexError:
   print(f'wrapping around on {ctx.message.author.name}s thread')
   await react.remove_reaction("▶", user)
   await ctx.send("reached the end of e621 posts", delete_after=3.5)
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
 await ctx.send(embed=embed)


########## SLASH COMMANDS ####################################### SLASH COMMANDS #########################

@client.slash_command(name="e621bothelp")
async def help(ctx):
    await ctx.send("""
    ``Command prefix is ./``
    ``e621/e926 - search images on e621.net``
    ``femboy - random image of a femboy from r/femboy``
    """)

@client.slash_command(name="e926pool")
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
   await ctx.send("reached the end of e621 page", delete_after=3.5)
   print(f'wrapping around on {ctx.message.author.name}s thread')
  except asyncio.TimeoutError:
   timeout = discord.Embed(title="Dead thread.", description=f'{ctx.message.author.mention} stopped interacting with their thread', color=0x0)
   await react.edit(embed = timeout)
   return

@client.slash_command(name="e926")
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

@client.slash_command(name="e621pool")
@commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
async def e621pool(ctx, *, key):
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

@client.slash_command(name="e621")
@commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
async def e621(ctx, *, key, ctx.author):
 tags = []
 if "+webm" in key:
    dwd = str("-young -scat")
    key = key.replace('+webm', '')
 else:
    dwd = str("-young -scat -webm")
 ele = str(key)
 vlv = int(0)
 tags.append(dwd)
 tags.append(ele)
 Posts = e621api.getPosts(tags, 60, 1, False)
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
    await react.remove_reaction("🚫", user)
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
    await react.remove_reaction("▶", user)
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
    await react.remove_reaction("◀", user)
  except IndexError:
   print(f'wrapping around on {ctx.message.author.name}s thread')
   await react.remove_reaction("▶", user)
   await ctx.send("reached the end of e621 posts", delete_after=3.5)
  except asyncio.TimeoutError:
   timeout = discord.Embed(title="Dead thread.", description=f'{ctx.message.author.mention} stopped interacting with their thread', color=0x0)
   await react.edit(embed = timeout)
   return


@client.slash_command(name="femboy", description="gives an image from the r/femboy subreddit")
async def femboy(ctx):
 reddit = praw.Reddit(check_for_async=False,client_id='tAa1kJciPf5BRVc2O43a0w',client_secret='4GkW7gGdAD2uKWsFsh3ibngzwrxyjA',user_agent='fetched-it-smug0842')
 femboys =reddit.subreddit('femboy').hot()
 post_to_pick = random.randint(1, 100)
 for i in range(0, post_to_pick):
  submission = next(x for x in femboys if not x.stickied)
 embed = discord.Embed(title="Post Link",url='https://reddit.com' + submission.permalink, color=0x0)
 embed.set_image(url=submission.url)
 await ctx.send(embed=embed)

client.run("setyourbottokenhereplease")
