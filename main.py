import setting as s
import discord,dateutil.parser,random,asyncio,time,schedule,subprocess,datetime,sys
from discord import Activity,ActivityType, AutoShardedBot, Sticker
from discord.ext import commands
from discord.ui import View, Button

from PIL import Image, ImageDraw, ImageFont
from sklearn.cluster import KMeans
import numpy as np
from numpy import linalg as LA
import random,requests,io,cv2

intents=discord.Intents.all()
bot=commands.Bot(command_prefix="k.", intents=intents)
bot.remove_command("help")
fav= 0x6dc1c1


@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Streaming(platform="YouTube",name="Yufu", url="https://www.youtube.com/watch?v=pP_rrVc0KKY&list=PL2L2WRV1GvihAXGZGi0mmj_s45fUzg_QF&index=1"))


@bot.slash_command(name="stop", description="開発者限定緊急停止")
@commands.dm_only()
async def SCRIPT_STOP(ctx):
    if ctx.author.id != s.Dev:
        await ctx.respond("帰れ")
        return
    user = bot.get_user(959142919573491722)
    e = discord.Embed(
        title="強制終了報告",
        description=f"{datetime.datetime.now()}")
    await user.send(embed=e)    
    sys.exit()


@bot.command()
async def inserver(ctx):
    with open("server.txt", "w", encoding='utf-8') as f:
        activeservers = bot.guilds
        for guild in activeservers:
             f.write(f"[ {str(guild.id)} ] {guild.name}\n")
    await ctx.send(file=discord.File("server.txt", filename="ServerList.txt"))
#"C:\Users\Ennui\BOT\server.txt"

@bot.command()
async def pic(ctx):
    #print(ctx.message.attachments[0].url)
    r = requests.get(ctx.message.attachments[0].url)
    img = Image.open(io.BytesIO(r.content))
    #img_resize = img.resize((500), int(img.height * 500 / img.width))
    img.save("image.png")
    msg = await ctx.send("Please wait a moment.")
    color_arr = extract_main_color(img_path, 7)
    show_tiled_main_color(color_arr)
    #draw_random_stripe(color_arr, img_path)
    file = discord.File("./image/stripe_image.png", filename="stripe.png")
    await msg.edit(content="Done",file=file)
"""
def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:f.write(r.content)

def draw_random_stripe(color_arr, img_path):
    width = 1024
    height = 1024
    stripe_color_img = Image.new(mode='RGB', size=(width, height), color='#333333')
    current_height = 0
    while current_height < height:
        random_index = random.randrange(color_arr.shape[0])
        color_hex_str = '#%02x%02x%02x' % tuple(color_arr[random_index])
        random_height = random.randrange(5, 70)
        color_img = Image.new(mode='RGB', size=(width, random_height),color=color_hex_str)
        stripe_color_img.paste(im=color_img,box=(0, current_height))
        current_height += random_height
    stripe_color_img.show()
    #stripe_color_img.save('./image/stripe_' + img_path)
"""
def show_tiled_main_color(color_arr):
    IMG_SIZE = 64
    MARGIN = 15
    width = IMG_SIZE * color_arr.shape[0] + MARGIN * 2
    height = IMG_SIZE + MARGIN * 2
    tiled_color_img = Image.new(
        mode='RGB', size=(width, height), color='#333333')
    for i, rgb_arr in enumerate(color_arr):
        color_hex_str = '#%02x%02x%02x' % tuple(rgb_arr)
        color_img = Image.new(mode='RGB', size=(IMG_SIZE, IMG_SIZE),color=color_hex_str)
        tiled_color_img.paste(im=color_img,box=(MARGIN + IMG_SIZE * i, MARGIN))
    #tiled_color_img.show()
    tiled_color_img.save('image\stripe_' + img_path)
def extract_main_color(img_path, color_num):
    cv2_img = cv2.imread(img_path)
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    cv2_img = cv2_img.reshape((cv2_img.shape[0] * cv2_img.shape[1], 3))
    cluster = KMeans(n_clusters=color_num)
    cluster.fit(X=cv2_img)
    cluster_centers_arr = cluster.cluster_centers_.astype(int, copy=False)
    trans_color = cv2_img[0]
    cluster_centers_arr = np.array([i for i in cluster_centers_arr if LA.norm(np.array(i - trans_color), 2) > 50])
    #print("extracted colors array:")
    #print(cluster_centers_arr)
    return cluster_centers_arr
img_path = 'image.png'


@bot.slash_command(name="夕弦", )
async def _ON_BOT(ctx):
    if ctx.author.id != s.Dev:
        await ctx.respond("帰れ", ephemeral=True)
        return
    subprocess.run("cd C:\\Users\\Ennui\\BOT", shell = True)
    subprocess.run("python spam.py", shell=True)
    await ctx.send("<@968603083414331423>")

@bot.slash_command(name="タイプ別憤死")
async def type_funshi(ctx):
    text_funshi = """
**典型的憤死パターン**

_1.発狂型憤死_
明らかに劣勢な状態になってから露骨に発作を起こしキチガイムーヴを始めるタイプ。
ネタに走って有耶無耶にしようという意図が見え見えである。

_2.生存本能型憤死_
生存本能タイムアウト/ブロック/ミュート/BANを行うタイプ。
憤死回避のために実力行使を行ってしまったが故の行動である。

_3.糖質化型憤死_
明らかな決めつけや思い込みをし始め勝手に憤慨し続けるタイプ。
***の圧倒的煽りによって極度のストレスを受けた故の行動である。

_4.ノーダメアピール型憤死_
ノーダメアピールを繰り返し精神的勝利を訴え続けるタイプ。
トマトフェイスを隠しきれていないため周りから見ると滑稽である。

_5.スルー型憤死_
突然話題を変えることで露骨にスルーアピールをするタイプ。
指摘されるとすぐ必死になって否定をしてくることが多い。"""
    await ctx.respond(text_funshi)

@bot.slash_command(name="憤死ワード")
async def word_list(ctx):
    b = Button(label="十字軍に行く", url="https://discord.gg/hunshi")
    view = View()
    view.add_item(b)
    await ctx.respond("""**典型的憤死ワード集**
・荒らしで時間無駄にしてて草
・しょうもないことして楽しい？
・BANすればいいだけ 残念だったな
・ムカつくから黙れ
・学歴しか誇れないゴミで草
・楽しんでて哀れ
・暇つぶし楽しかったよ
・学歴と頭脳は比例しない
・あーもうこいつうるさいから蹴ろう
・誤字してて草
・十字軍はくだらない組織
・あそんでいるだけなんだが？""", view=view) 

@bot.slash_command()
async def boosters(ctx):
    g = ctx.guild.premium_subscribers
    for i in g:await ctx.respond(f"{i}")

@bot.command()
async def gensin(ctx):
    text = ("""
https://discord.gg/fqyPF8UUeE
https://discord.gg/2eQVbVMHVm
https://discord.gg/9Gz4CyBsRv
https://discord.gg/BrzSh25WMz
https://discord.gg/Kq9GVydnES
https://discord.gg/ydnsNmBc8E
https://discord.gg/JF7beMKNVA
https://discord.gg/fndwEM6Jva
https://discord.gg/Z9J8sS7WHT
https://discord.gg/ACRkdBCxzF
https://discord.gg/Te33Pk7H7r
https://discord.gg/TAQEqvfhsy
https://discord.gg/zuDEhDaFYE
https://discord.gg/nxjSEHDHQk
https://discord.gg/nRGvemM9zX
https://discord.gg/MN5AvmyNhz
https://discord.gg/DybNtyENxe
https://discord.gg/WmqCUb2eG3
https://discord.gg/3h6kA43RR8
https://discord.gg/UCCpS3GPRy
https://discord.gg/zkNvzhuxD3
https://discord.gg/SDyn8Vudau
https://discord.gg/bX7JmNs7tD
https://discord.gg/tHx3uHd3xb
https://discord.gg/nBRydBST75
https://discord.gg/gdjeXBkBZy
https://discord.gg/XjK3MkG6KA
https://discord.gg/ruTw66txMb
https://discord.gg/JGmmRfQqFN
https://discord.gg/mQgsjm2G46
https://discord.gg/Kv5cMkUTC7
https://discord.gg/w8Vg4qn5rg
https://discord.gg/RThPD6UP9J
https://discord.gg/eESBqjA6UM
https://discord.gg/TMXkyFa9Bh
https://discord.gg/5pfdeq7NSj
https://discord.gg/qk69HHWKTU
https://discord.gg/anqJZmuSBG
https://discord.gg/qMkrrQzAWQ
https://discord.gg/NZrchaHrWe
https://discord.gg/jmxXaztH4g
https://discord.gg/syapxzqcdR
https://discord.gg/jR2JnsSRuj
https://discord.gg/hQ4mFzw6ME
https://discord.gg/j8ZXvemCwc
https://discord.gg/N9QJha5Agp
https://discord.gg/AQYk9tr7c8
https://discord.gg/vGAWK2T8Hr
https://discord.gg/rphUapSWYt
https://discord.gg/TedNhwqt2g
https://discord.gg/YukvxMVv44
https://discord.gg/XdsKcdyNEm""")
    await ctx.send(text)

@bot.command()
async def yn(ctx):
    await ctx.reply(random.choice(("Yes","No")))

@bot.slash_command(name="about", description="About this bot")
async def about(ctx):
    user= bot.get_user(956042267221721119)
    members = 0
    for guild in bot.guilds:members += guild.member_count - 1
    embed= discord.Embed(color= 0x6dc1d1)
    embed.add_field(name= "Customers",value= f"Servers **:** `{str(len(bot.guilds))}`\nMembers **:** `{str(members)}`", inline= False)
    embed.add_field(name= "Dev", value= f"{user.mention}", inline= False)
    embed.set_author(name= "About this bot")
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.add_field(name="【注釈】",value="適当にスクリプト書いただけ")
    embed.set_footer(text=f"By: {str(ctx.author)}")
    b = Button(label="Support Server", url="https://discord.gg/owen")
    b2 = Button(label="Invite URL", url=f"https://discord.com/oauth2/authorize?client_id=979001395703341096&permissions=1644971949559&scope=bot%20applications.commands")
    view = View()
    view.add_item(b)
    view.add_item(b2)
    await ctx.respond(embed=embed, view=view)

@bot.slash_command(name="avatar", description="サーバープロフィールのアイコンを取得")
async def avatar(ctx, user:discord.Member=None):
    if not user: user= ctx.author
    avatar= user.display_avatar
    embed= discord.Embed(description= f"{user.mention} Avatar",  color= 0x6dc1d1)
    embed.set_author(name= str(user), icon_url= avatar)
    embed.set_image(url= avatar)
    embed.set_footer(text= f"By: {str(ctx.author)}")
    await ctx.respond(embed= embed)

@bot.slash_command(name="banner", description="Get the ")
async def banner(ctx, user:discord.Member=None):
    if not user:user=ctx.author
    user = await bot.fetch_user(user.id)
    try:
        banner_url = user.banner.url
        avatar=user.display_avatar
        e=discord.Embed(description= f"{user.mention} Banner",  color= 0x6dc1d1)
        e.set_author(name= str(user), icon_url= avatar)
        e.set_image(url= banner_url)
        e.set_footer(text= f"By: {str(ctx.author)}")
        await ctx.respond(embed=e)
    except:await ctx.respond("Bannerが検出できない")

@bot.slash_command(name="track", description="現在アクティビティにあるSpotifyの楽曲のURLを送信")
async def track(ctx, user:discord.Member=None):
    if not user: user=ctx.author
    spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if spotify_result is None:await ctx.respond(f"{user.name} is not listening to Spotify!")
    if spotify_result:await ctx.respond(f"https://open.spotify.com/track/{spotify_result.track_id}")

@bot.slash_command(name="spotify", description="アクティビティからSpotifyの楽曲情報を送信")
async def spotify(ctx, user:discord.Member=None):
    if not user:user=ctx.author
    _spotify_result= next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if _spotify_result is None:await ctx.respond(f"{user.name} is not listening to Spotify!")
    if _spotify_result:
        embed=discord.Embed(color=_spotify_result.color)
        embed.set_thumbnail(url=_spotify_result.album_cover_url)
        embed.add_field(name="Song Title", value=f"```{_spotify_result.title}```")
        artists = _spotify_result.artists
        if not artists[0]: re_result=_spotify_result.artist
        else: re_result = ', '.join(artists)
        embed.add_field(name="Artist[s]", value=f"```{re_result}```")
        embed.add_field(name="Album", value=f"```{_spotify_result.album}```", inline=False)
        embed.add_field(name="Time", value=f"```{dateutil.parser.parse(str(_spotify_result.duration)).strftime('%M:%S')}```")
        embed.add_field(name="URL", value=f"```https://open.spotify.com/track/{_spotify_result.track_id}```", inline=False)
        embed.set_footer(text=f"By: {str(ctx.author)}")
        view = View()
        b = Button(label="URL", url=f"https://open.spotify.com/track/{_spotify_result.track_id}")
        jacket = Button(label="see jacket", style=discord.ButtonStyle.green)
        async def Button_callback(interaction:discord.Interaction):
            await interaction.response.send_message(_spotify_result.album_cover_url, ephemeral=True)
        jacket.callback = Button_callback
        view.add_item(b)
        view.add_item(jacket)
        await ctx.respond(embed=embed, view=view)

@bot.command(aliases=["s"])
async def spotify_(ctx, user:discord.Member=None):
    if not user:user=ctx.author
    _spotify_result= next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if _spotify_result is None:await ctx.respond(f"{user.name} is not listening to Spotify!")
    if _spotify_result:
        embed=discord.Embed(color=_spotify_result.color)
        embed.set_thumbnail(url=_spotify_result.album_cover_url)
        embed.add_field(name="Song Title", value=f"```{_spotify_result.title}```")
        artists = _spotify_result.artists
        if not artists[0]: re_result=_spotify_result.artist
        else: re_result = ', '.join(artists)
        embed.add_field(name="Artist[s]", value=f"```{re_result}```")
        embed.add_field(name="Album", value=f"```{_spotify_result.album}```", inline=False)
        embed.add_field(name="Time", value=f"```{dateutil.parser.parse(str(_spotify_result.duration)).strftime('%M:%S')}```")
        embed.add_field(name="URL", value=f"```https://open.spotify.com/track/{_spotify_result.track_id}```", inline=False)
        embed.set_footer(text=f"By: {str(ctx.author)}")
        view = View()
        b = Button(label="URL", url=f"https://open.spotify.com/track/{_spotify_result.track_id}")
        jacket = Button(label="see jacket", style=discord.ButtonStyle.green)
        async def Button_callback(interaction:discord.Interaction):
            await interaction.response.send_message(_spotify_result.album_cover_url, ephemeral=True)
        jacket.callback = Button_callback
        view.add_item(b)
        view.add_item(jacket)
        await ctx.respond(embed=embed, view=view)

@bot.slash_command(name="invite", description="Botをメンションして招待URLを生成")
async def invite(ctx, mention:discord.Member):
    e=discord.Embed(description=f"{id.mention}(**{id.id}**)", color=fav)
    date_format="%Y/%m/%d %H:%M"
    e.add_field(name=f"アカウント作成日", value=f"**`{id.created_at.strftime(date_format)}`**")
    e.add_field(name="サーバー参加日", value= f"**`{id.joined_at.strftime(date_format)}`**")
    #else:#id = str(id.replace("<@", '').strip())#id = str(id.replace(">", '').strip())
    b = Button(label="No perms", url= f"https://discord.com/oauth2/authorize?client_id={id.id}&permissions=0&scope=bot%20applications.commands")
    b_2 = Button(label="Admin", url= f"https://discord.com/oauth2/authorize?client_id={id.id}&permissions=8&scope=bot%20applications.commands")
    b_3 = Button(label="Make yourself",  url= f"https://discord.com/oauth2/authorize?client_id={id.id}&permissions=1644971949559&scope=bot%20applications.commands")
    view=View()
    view.add_item(b)
    view.add_item(b_2)
    view.add_item(b_3)
    try:e.set_thumbnail(url=id.avatar.url)
    except:e.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    await ctx.respond(embed=e, view=view)

@bot.slash_command(name="invitegen", description="BOTのIDから招待URLを作成")
async def gen(ctx, id:str):
    b = Button(label="No perms", url= f"https://discord.com/oauth2/authorize?client_id={id}&permissions=0&scope=bot%20applications.commands")
    b_2 = Button(label="Admin", url= f"https://discord.com/oauth2/authorize?client_id={id}&permissions=8&scope=bot%20applications.commands")
    b_3 = Button(label="Make yourself",  url= f"https://discord.com/oauth2/authorize?client_id={id}&permissions=1644971949559&scope=bot%20applications.commands")
    view=View()
    view.add_item(b)
    view.add_item(b_2)
    view.add_item(b_3)
    await ctx.send("出来た", view=view)    

@bot.slash_command(name="account", description="アカウントの作成・参加日時")
async def account(ctx, user:discord.Member=None):
    if not user:user=ctx.author
    date_format="%Y/%m/%d %H:%M:%S"
    e = discord.Embed(color= 0x6dc1d1)
    e.set_author(name=f"{user}(ID: {user.id})")
    e.add_field(name=f"アカウント作成日", value=f"**`{user.created_at.strftime(date_format)}`**")
    e.add_field(name="サーバー参加日", value= f"**`{user.joined_at.strftime(date_format)}`**")
    e.set_thumbnail(url=user.display_avatar)
    e.set_footer(text= f"By: {str(ctx.author)}")
    await ctx.respond(embed=e)

@bot.slash_command(name="userinfo", description="ユーザー情報を送信")
async def userinfo(ctx, user:discord.Member=None):
    if not user: user= ctx.author
    date_format="%Y/%m/%d"
    s = str(user.status)
    s_icon = ""
    if s == "online":s_icon = "🟢"
    elif s == "idle":s_icon = "🟠"
    elif s == "dnd":s_icon = "🔴"
    elif s == "offline":s_icon = "⚫"
    embed= discord.Embed(title= f"{user}", description= f"**ID : `{user.id}`**", color=fav)
    embed.set_thumbnail(url=user.display_avatar)
    embed.add_field(name= "Name", value= f"> {user}", inline= True)
    embed.add_field(name= "Nickname", value= f"> {user.display_name}", inline= True)
    embed.add_field(name="Status", value=f"> `{s_icon} {s}`", inline=True)
    if len(user.roles) >= 1:
        role_string = " ".join([r.mention for r in user.roles][1:])
        embed.add_field(name= f"Roles `{len(user.roles)-1}`", value= f"> {role_string}", inline=False)
    embed.add_field(name= "Createion Account", value= f"> `{user.created_at.strftime(date_format)}`", inline= True)
    embed.add_field(name= "Joined Server", value= f"> `{user.joined_at.strftime(date_format)}`", inline= True)
    user = await bot.fetch_user(user.id)
    try:embed.set_image(url=user.banner.url)
    except:pass
    embed.set_footer(text= f"By: {str(ctx.author)}")
    await ctx.respond(embed= embed)


@bot.slash_command(name="vanity", description="ｻｰﾊﾞｰのﾊﾞﾆﾃｨURLを表示")
async def vanity(ctx):
    try:
        vanity = await ctx.guild.vanity_invite()
        await ctx.respond(str(vanity).replace('https://discord/', ''))
    except:await ctx.respond("ない")

@bot.slash_command(name="leave")
@commands.has_permissions(administrator=True)
async def leave(ctx, guild_id=None):
    if not guild_id:guild_id=ctx.guild.id
    await bot.get_guild(int(guild_id)).leave()
    await ctx.respond(f"I left: {guild_id.name}")

@bot.slash_command(name="serverinfo", description="Get info about server")
async def serverinfo(ctx):
    guild = ctx.guild
    date_f= "%Y/%m/%d"
    tchannels= len(guild.text_channels)
    vchannels= len(guild.voice_channels)
    roles= [role for role in guild.roles]
    emojis= [1 for emoji in guild.emojis]
    online= [1 for user in guild.members if user.status != discord.Status.offline]
    stickers = [sticker  for sticker in guild.stickers]
    embed= discord.Embed(title=f"{guild.name}", description= f":crown: **Owner : **{guild.owner.mention}\n\
        :id: **Server id : `{guild.id}`**\n\
        :calendar_spiral: Createion : **`{guild.created_at.strftime(date_f)}`**", color= 0x6dc1d1)
    try:embed.set_thumbnail(url= guild.icon.url)
    except:pass
    embed.add_field(name= ":shield: Role", value= f"Roles: **{len(roles)}**", inline= True)
    embed.add_field(name= f":gem: Boost [{guild.premium_subscription_count}]", value= f"Tier: ** {guild.premium_tier}**")
    try:
        vanity =  await guild.vanity_invite()
        embed.add_field(name=":link: Vanity URL", value=f"`{str(vanity).replace('https://discord', '')}`")
    except:embed.add_field(name=":link: Vanity URL", value=f"`None`")        
    embed.add_field(name= ":grinning: Emoji", value= f"Emojis: **{len(emojis)}**\nStickers: **{len(stickers)}**")
    embed.add_field(name= f":busts_in_silhouette: Members [{guild.member_count}]", 
            value= f"User: **{str(sum(1 for member in guild.members if not member.bot))}** |  Bot: **{str(sum(1 for member in guild.members if member.bot))}**\nOnline: **{len(online)}**")
    embed.add_field(name= f":speech_left: Channels [{tchannels+vchannels}]", 
            value= f"Text: **{tchannels}**\nVoice: **{vchannels}**\nCategory: **{len(guild.categories)}**",inline= True)
    try:
        req= await bot.http.request(discord.http.Route("GET", "/guilds/{sid}", sid= guild.id))
        banner_id= req["banner"]
        if banner_id:
            banner_url_png= f"https://cdn.discordapp.com/banners/{guild.id}/{banner_id}.png?size=1024"
            banner_url_gif= f"https://cdn.discordapp.com/banners/{guild.id}/{banner_id}.gif?size=1024"
            embed.set_image(url= banner_url_png)
            embed.set_footer(text= f"By: {str(ctx.author)} ・Banner is png file")
            b= Button(label="See on Gif",style=discord.ButtonStyle.green)
        async def button_callback(interaction):
           await interaction.response.send_message(banner_url_gif, view=None, ephemeral=True)
        b.callback= button_callback
        view=View()
        view.add_item(b)
        await ctx.respond(embed=embed, view=view)
    except:
        embed.set_footer(text= f"By: {str(ctx.author)}")
        await ctx.respond(embed=embed)


@bot.command(aliases=["sb"])
async def serverbanner(ctx):
    try:
        guild=ctx.guild
        req= await bot.http.request(discord.http.Route("GET", "/guilds/{sid}", sid= guild.id))
        banner_id= req["banner"]
        if banner_id:
            banner_url_png= f"https://cdn.discordapp.com/banners/{guild.id}/{banner_id}.png?size=1024"
            banner_url_gif= f"https://cdn.discordapp.com/banners/{guild.id}/{banner_id}.gif?size=1024"
            _embed= discord.Embed(title= "Banner Link", description= f"{guild.name} banner", color= 0x6dc1d1, url= banner_url_png)
            _embed.set_image(url= banner_url_png)
            _embed.set_footer(text= f"By: {str(ctx.author)} ・Banner is png file")
            b= Button(label="Gif",style=discord.ButtonStyle.green)
        async def button_callback(interaction):
            embed= discord.Embed(title= "Banner Link", description= f"{guild.name} banner", color= 0x6dc1d1, url= banner_url_gif)
            embed.set_image(url= banner_url_gif)        
            embed.set_footer(text= str(f"By : {ctx.author}"))
            await interaction.response.edit_message(embed=embed, view=None)
        b.callback= button_callback
        view=View()
        view.add_item(b)
        await ctx.send(embed=_embed, view=view)
    except:
        embed= discord.Embed(title= "Have you set banner?")
        embed.set_footer(text=str(f"By: {ctx.author}"))
        await ctx.send(embed= embed)

@bot.slash_command(name="purge", description="指定した数字分メッセージを削除")
@commands.has_permissions(manage_messages= True)
async def purge(ctx, amount:int):
    deleted= await ctx.channel.purge(limit= amount+1)
    embed= discord.Embed(title="Message Purged!", color = 0x6dc1d1)
    embed.add_field(name= f"{len(deleted)-1} messages", value= "Automatically deleted after 5 seconds")
    embed.set_footer(text= f"By: {ctx.author}")
    await ctx.respond(embed=embed, delete_after=5)

@bot.slash_command(name="kick")
@commands.has_permissions(kick_members= True)
async def kick(ctx, user:discord.Member, reason= None):
    if not reason:reason= "No reason"
    await user.kick(reason=reason)
    embed=discord.Embed(title=f"{user} GoodBye :wave::wave:",description=f"{user.mention} got KICK!!",color=0xff0000)
    embed.add_field(name="Reason", value=f"```{reason}```")
    await ctx.respond(embed=embed)

@bot.slash_command(name="ban")
@commands.has_permissions(ban_members= True)
async def ban(ctx, user:discord.Member, reason= None):
    if not reason:reason="No reason"
    await user.ban(reason=reason)
    embed=discord.Embed(title=f"{user} GoodBye :wave::wave:",description=f"{user.mention} got BAN!!",color=0xff0000)
    embed.add_field(name="Reason", value=f"```{reason}```")
    await ctx.respond(embed=embed)

@bot.slash_command(name="nuke", description="チャンネルを再作成")
@commands.has_permissions(administrator=True)
async def delete(ctx, channel:discord.TextChannel=None, meonly=None):
    if not channel:channel=ctx.channel
    else:channel = discord.utils.get(ctx.guild.channels, name=channel.name)
    pos = channel.position
    await channel.delete()
    new_channel = await channel.clone()
    await new_channel.edit(position=pos)
    if meonly:await ctx.respond(f"<#{new_channel.id}>", ephemeral=True)
    else :await ctx.respond(f"<#{new_channel.id}>")
@bot.command(aliases=["incode"])
async def invitecodeserver(ctx, url):
    if ctx.author.id == s.Dev:
        async with ctx.channel.typing():
            guild = await bot.fetch_invite(url = f"https://discord.gg/{url}")
            date_f= "%Y/%m/%d"
            tchannels= len(guild.text_channels)
            vchannels= len(guild.voice_channels)
            roles= [role for role in guild.roles]
            emojis= [emoji for emoji in guild.emojis]
            online= [1 for user in guild.members if user.status != discord.Status.offline]
            stickers = [sticker  for sticker in guild.stickers]
            embed= discord.Embed(title=f"{guild.name}", description= f":crown: **Owner : **{guild.owner.mention}\n:id: **Server id : `{guild.id}`**", color= 0x6dc1d1)
            try:embed.set_thumbnail(url= guild.icon.url)
            except:pass
            embed.add_field(name= ":shield: Role", value= f"Roles: **{len(roles)}**", inline= True)
            embed.add_field(name= ":grinning: Emoji", value= f"Emojis: **{len(emojis)}**\nStickers: **{len(stickers)}**")
            embed.add_field(name= f":gem: Boost [{guild.premium_subscription_count}]", value= f"Tier: ** {guild.premium_tier}**")
            embed.add_field(name= ":calendar_spiral: Createion", value= f"**`{guild.created_at.strftime(date_f)}`**", inline=True)
            embed.add_field(name= f":busts_in_silhouette: Members [{guild.member_count}]", 
                    value= f"User: **{str(sum(1 for member in guild.members if not member.bot))}** |  Bot: **{str(sum(1 for member in guild.members if member.bot))}**\nOnline: **{len(online)}**")
            embed.add_field(name= f":speech_left: Channels [{tchannels+vchannels}]", 
                    value= f"Text: **{tchannels}** | Voice: **{vchannels}**\nCategory: **{len(guild.categories)}**",inline= True)
            try:
                vanity =  await guild.vanity_invite()
                embed.add_field(name=":link: Vanity URL", value=f"`{str(vanity).replace('https://', '')}`")
            except:embed.add_field(name=":link: Vanity URL", value=f"`None`")        
            try:
                req= await bot.http.request(discord.http.Route("GET", "/guilds/{sid}", sid= guild.id))
                banner_id= req["banner"]
                if banner_id:
                    banner_url= f"https://cdn.discordapp.com/banners/{guild.id}/{banner_id}.png?size=1024"
                    embed.set_image(url= banner_url)
                    embed.set_footer(text= f"By: {str(ctx.author)} | Banner is png file")
            except:embed.set_footer(text= f"By: {str(ctx.author)}")
            await ctx.send(embed= embed)

@bot.slash_command(name="xserver", description="server idを入れてね!このボットが入ってるサーバーの情報を取得")
async def xserver(ctx, id:str):
    guild = bot.get_guild(int(id))
    date_f= "%Y/%m/%d"
    tchannels= len(guild.text_channels)
    vchannels= len(guild.voice_channels)
    roles= [role for role in guild.roles]
    emojis= [1 for emoji in guild.emojis]
    online= [1 for user in guild.members if user.status != discord.Status.offline]
    stickers = [sticker  for sticker in guild.stickers]
    embed= discord.Embed(title=f"{guild.name}", description= f":crown: **Owner : **{guild.owner.mention}\n\
        :id: **Server id : `{guild.id}`**\n\
        :calendar_spiral: Createion : **`{guild.created_at.strftime(date_f)}`**", color= 0x6dc1d1)
    try:embed.set_thumbnail(url= guild.icon.url)
    except:pass
    embed.add_field(name= ":shield: Role", value= f"Roles: **{len(roles)}**", inline= True)
    embed.add_field(name= f":gem: Boost [{guild.premium_subscription_count}]", value= f"Tier: ** {guild.premium_tier}**")
    try:
        vanity =  await guild.vanity_invite()
        embed.add_field(name=":link: Vanity URL", value=f"`{str(vanity).replace('https://discord', '')}`")
    except:embed.add_field(name=":link: Vanity URL", value=f"`None`")        
    embed.add_field(name= ":grinning: Emoji", value= f"Emojis: **{len(emojis)}**\nStickers: **{len(stickers)}**")
    embed.add_field(name= f":busts_in_silhouette: Members [{guild.member_count}]", 
            value= f"User: **{str(sum(1 for member in guild.members if not member.bot))}** |  Bot: **{str(sum(1 for member in guild.members if member.bot))}**\nOnline: **{len(online)}**")
    embed.add_field(name= f":speech_left: Channels [{tchannels+vchannels}]", 
            value= f"Text: **{tchannels}**\nVoice: **{vchannels}**\nCategory: **{len(guild.categories)}**",inline= True)
    try:
        req= await bot.http.request(discord.http.Route("GET", "/guilds/{sid}", sid= guild.id))
        banner_id= req["banner"]
        if banner_id:
            banner_url_png= f"https://cdn.discordapp.com/banners/{guild.id}/{banner_id}.png?size=1024"
            banner_url_gif= f"https://cdn.discordapp.com/banners/{guild.id}/{banner_id}.gif?size=1024"
            embed.set_image(url= banner_url_png)
            embed.set_footer(text= f"By: {str(ctx.author)} ・Banner is png file")
            b= Button(label="See on Gif",style=discord.ButtonStyle.green)
        async def button_callback(interaction):
           await interaction.response.send_message(banner_url_gif, view=None, ephemeral=True)
        b.callback= button_callback
        view=View()
        view.add_item(b)
        await ctx.respond(embed=embed, view=view)
    except:
        embed.set_footer(text= f"By: {str(ctx.author)}")
        await ctx.respond(embed=embed)


@bot.slash_command(name="source", description="スキッドしまくったこのBOTの雑魚ード貼ってます。")
async def _source_code(ctx):
    e = discord.Embed(description="PythonなのにClass使ってません:sob:",color=fav)
    b = Button(label="Jump to Github", url="https://github.com/Ennuilw/-/tree/main")
    view=View()
    view.add_item(b)
    await ctx.respond(embed=e, view=view)



@bot.event
async def on_command_error(ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="-MissingPermissions", description=f"権限不足ですよ。出直せバカ", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
            embed = discord.Embed(title="-BotMissingPermissions", description=f"当botの権限が不当に制限されています。信用ないならなぜ入れたんです？", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
            embed = discord.Embed(title="-CommandNotFound", description=f"おいおっさんｗｗｗそんなこまんどねーぞｗｗｗｗｗちゃんと見ろメクラｗｗｗｗｗ。", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
            embed = discord.Embed(title="-MemberNotFound", description=f"指定されたユーザーが発見されませんでした。", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            embed = discord.Embed(title="-BadArgument", description=f"指定された引数がエラーを起こしているため実行出来ません。", color=0xff0000)
            await ctx.send(embed=embed) 
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title="-BadArgument", description=f"必要な引数が足りません。", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error,discord.ext.commands.errors.MissingRole):
            embed = discord.Embed(title="-MissingRole", description=f"ロール持ってないからだめよ", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            embed = discord.Embed(title="-CheckFailure", description=f"Something error: \ndm only or Dev only command", color=0xff0000)
            await ctx.send(embed=embed)
        else:raise error

bot.run(s.token)
