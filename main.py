# DEPENDENCIAS
try:
    import discord
    import os
    import scrapetube
    import requests
    import asyncio
    import random
    import json
    from bs4 import BeautifulSoup
    from PIL import Image
    from dotenv import load_dotenv
except Error as e:
    print(f"Error obteniendo dependencias: {e}")

# BOT
load_dotenv()
bot = discord.Bot(intents=discord.Intents.all(),activity=discord.Activity(type=discord.ActivityType.watching, name="Iniciando bot, espera..."))

# GROUPS
medidor = bot.create_group(name="medidor")
info = bot.create_group(name = "info")
# COMMANDS
async def update(): # Update the bot status
  while True:
    try:
        data = None
        with open("base.json", "r") as json_data:
          data = json.load(json_data)
        videos = scrapetube.get_channel(channel_username="Xander_Z", limit=1, sort_by="newest")
        lastest_video = None
        for video in videos:
          lastest_video = video["videoId"]
        r = requests.get(f"https://www.youtube.com/watch?v={lastest_video}")
        soup = BeautifulSoup(r.text, features="lxml")
        link = soup.find_all(name="title")[0]
        title = str(link)
        title = title.replace("<title>","")
        title = title.replace("</title>","")
        title = title.replace(" - YouTube","")
        activity = discord.Activity(type=discord.ActivityType.playing, name=f"Viendo {title} de Xander_z")
        await bot.change_presence(activity=activity)
        if lastest_video != data["url"]:
           dict = {
               "url":lastest_video
           }
           with open("base.json", "w") as file:
               json.dump(dict, file)
           notify_channel = bot.get_channel(1144768943643447383)
           author = await bot.fetch_user(1101621392547528734)
           embed = discord.Embed(
             title = "¡Nuevo video de Xander_z!",
             description = "Ve a ver el nuevo video de mi patrón 🛐\n<@&1179171991291428884> 🦖",
             color = discord.Color.from_rgb(188, 241, 132)
           )
           embed.set_author(name="@Xander_z", icon_url = author.avatar.url)
           embed.set_thumbnail(url=bot.user.avatar.url)
           embed.add_field(name=f"'{title}'",value=f"[¡Click para ver el video!](https://www.youtube.com/watch?v={lastest_video})")
           file = discord.File("images/spike.jpg", filename="spike.jpg")
           embed.set_image(url="attachment://spike.jpg")
           await notify_channel.send(embed=embed, file=file)
        print("updating presence")
        await asyncio.sleep(90)
      
    except Exception as error:
        print(f"Algo salio mal, reintentando: {error}")
        await asyncio.sleep(120)

@bot.event
async def on_ready(): # Setup the bot
    print(f"Sesión iniciada cómo {bot.user}")
    await update()
  
@bot.event
async def on_message(message): # Idk what is this
    if message.author == bot.user:
        return
    if message.content.lower() == "han cambiado la imagen de las arqueras":
        if message.channel.id != 1144768943920255117:
            await message.reply("**Solo puedes usarlo en <#1144768943920255117> para evitar spam >.<**")
            await message.add_reaction("✖️")
            return
        embed = discord.Embed(
            title="Sr. Tumbao",
            description = """**Chavales chavales que han cambiado\nla imagen de las arqueras <:emoji_8:1195230058688806932>\nahora están más buenas\nme acabo de enamorar <:emoji_7:1195229495511240805>\n\n¿Tú que opinas?\ncuidadito con lo que dices que me pongo celoso <:emoji_9:1195230587020132353>**""",
            color = discord.Color.from_rgb(255, 173, 140))
        file = discord.File("images/tumbao.png", filename="tumbao.png")
        embed.set_image(url="attachment://tumbao.png")
        await message.reply(embed=embed, file=file)

@bot.event
async def on_message(message): # The boost message
    if message.author == bot.user: return
    if (message.type == discord.MessageType.premium_guild_subscription): return
    if (message.author.id != 1044034580996427816): return
    boost_author = message.author
    embed = discord.Embed(
        title = "¡Gracias por el boost!",
        color = discord.Color.from_rgb(219, 176, 252),
        description="¡Te damos las gracias por tu contribución!"
    )
    embed.set_thumbnail(url=message.guild.icon.url)
    embed.set_author(name=f"De {message.guild.name}", icon_url=bot.user.avatar.url)
    embed.set_footer(text=f"Para '{boost_author.name}'", icon_url=boost_author.avatar.url)
    await boost_author.send(embed=embed)

@info.command(description="¡Conoce mi latencia actual!") # A info command
async def ping(ctx):
    embed = discord.Embed(
        title="¡Pong 🏓!",
        description=f"Tiempo de respuesta: {round(bot.latency * 1000)}ms",
        color=discord.Color.from_rgb(255, 239, 183)
     )
    await ctx.respond(embed=embed)

@medidor.command(description="¡Te diré que tan insano eres!")
async def insanidad(
  ctx,
  usuario: discord.Option(discord.Member, "Selecciona un usuario", required = False, default = None)
):
  if not usuario:
    embed = discord.Embed(
      description=f"**¡Eres {random.randint(0,100)}% insan@!** 👻",
      color=discord.Color.from_rgb(255, 116, 162)
    )
    embed.set_author(name=f"Pedido por @{ctx.author.name}", icon_url=ctx.author.avatar.url)
    embed.set_image(url="https://i.pinimg.com/originals/53/40/bd/5340bd78187d42b45963f76d639e2bbf.gif")
    await ctx.respond(embed=embed)
  else:
    embed = discord.Embed(
      description=f"**¡<@{usuario.id}> es {random.randint(0,100)}% insan@!** 👻",
      color=discord.Color.from_rgb(255, 116, 162)
    )
    embed.set_author(name=f"Pedido por @{ctx.author.name}", icon_url=ctx.author.avatar.url)
    embed.set_image(url="https://i.pinimg.com/originals/53/40/bd/5340bd78187d42b45963f76d639e2bbf.gif")
    await ctx.respond(embed=embed)

@info.command(description="¡Mira mi código fuente!")
async def fuente(ctx):
    embed = discord.Embed(
        title="**Sobre mí** <:buzz:1194513196611010560>", 
        color=discord.Color.from_rgb(104, 227, 213),
        description="ʕ•́ᴥ•̀ʔっ Holi, soy un bot creado para añadir funcionalidades y mecanicas al servidor de Xander_z para hacer más divertida tu instancia en este servidor :D")
    author = await bot.fetch_user("1044034580996427816") # Yo :b
    embed.add_field(name="Repositorio de GitHub", value="[Click para ver](https://github.com/iSparkiy/Xanderborg)")
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_image(url="https://piks.eldesmarque.com/bin/esports/2021/06/buzz.jpg")
    embed.set_footer(text=f"¡Bot creado por @{author.name}!" , icon_url=author.avatar.url)
    await ctx.respond(embed=embed, ephemeral=False)

# RUN
bot.run(os.getenv('TOKEN'))
