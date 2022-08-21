import setting as s
import discord,dateutil.parser,random,subprocess,datetime,sys,spotipy,aiohttp,time
from discord.ext import commands
from discord.ui import View, Button, Select

from spotipy.oauth2 import SpotifyClientCredentials

from PIL import Image
from sklearn.cluster import KMeans
import numpy as np
from numpy import linalg as LA
import requests,cv2,io

intents=discord.Intents.all()
bot=commands.Bot(command_prefix="k.", intents=intents)
bot.remove_command("help")
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = s.spotify_client_id, client_secret = s.spotify_client_secret))
Spotify_logo=[s.sp_logo_defa,s.sp_logo_wh]
img_path = 'image.png'

"""
#memberCount = invite.approximate_member_count
#presenceCount = invite.approximate_presence_count
    invite = await ctx.channel.create_invite()
    await ctx.send(f"Here's your invite: {invite}")
    
    if not int(interaction.author.id) in admin_users:

flags = MessageFlags().EPHEMERAL)

"""

"""
@bot.slash_command(name="createinvite", description="読んで字の如く")
async def create_invite(ctx, guild_id=None):
    if not guild_id:guild_id = ctx.guild.id
    guild = bot.get_guild(int(guild_id))
    i = 0
    with open("invite.txt", "w", encoding='utf-8') as f:
        for channel in guild.channels:
            #link = await guild.channels.create_invite(max_age = 0, max_uses = 0)#xkcd=True,
            link = await guild.channels[i].create_invite(max_age=0, max_uses = 0)
            f.write(f"[{link}] - {channel}\n")
            i += 1
    await ctx.respond(file=discord.File("invite.txt", filename=f"{guild}_invite.txt"))
        #await ctx.respond(file=discord.File(f),ephemeral=True)

    if not guild_id:guild_id = ctx.guild.id
    """#Create instant invite
"""
    guild = bot.get_guild(int(guild_id))

    link = await guild.channels[0].create_invite(max_age = 0, max_uses = 0)#xkcd=True, 
    await ctx.respond(link,ephemeral=True)
"""



@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(platform="YouTube",name="Yufu", url=s.Yufu_yt))


@bot.command()
async def invites(ctx, id =None):
    if ctx.author.id != s.Dev:
        await ctx.send("gfy")
        return
    if not id:guild = ctx.guild
    else:guild = bot.get_guild(int(id))
    try:
        vanity = await ctx.guild.vanity_invite()
        await ctx.send(f"VANITY: {str(vanity).replace('https://discord.gg/', ' ')}")
    except:pass
    for invite in await guild.invites(): 
        await ctx.send(f"``{(invite.url).replace('https://discord.gg/', ' ')}``")

@bot.slash_command(name="invite_del", description="サーバーの招待コードを全削除")
async def Delete_invite(ctx):
    guild = ctx.guild
    for invite in await guild.invites():
        await invite.delete()
    await ctx.respond("終わった")

@bot.command()
async def inserver(ctx) -> None:
    if ctx.author.id != s.Dev:
        await ctx.send("gfy")
        return
    with open("server.txt", "w", encoding='utf-8') as f:
        activeservers = bot.guilds
        for guild in activeservers:
             f.write(f"[ {str(guild.id)} ] {guild.name}\n")
    await ctx.send(file=discord.File("server.txt", filename="SERVERLIST.txt"))

@bot.slash_command(name="global_ban", description="開発者専用")
async def global_ban(ctx, member : discord.Member, reason=None):
    if ctx.author.id != 959142919573491722:
        await ctx.response.send_message("開発者専用", ephemeral=True)
        return

    msg_1 = await ctx.response.send_message("Global Banを開始します<a:Loading_2:1007527284753834014>")
    count = 0

    with open("result.txt", "w", encoding='utf-8') as f:
        for guild in bot.guilds:
            if guild.me.guild_permissions.ban_members:
                try:
                    await guild.ban(member, reason=reason)
                    count += 1
                    f.write(f"SUCCESS [ {guild} ][ {guild.id} ]\n")
                except:
                    f.write(f"FAILURE [ {guild} ][ {guild.id} ]\n")
    e = discord.Embed(title=f"{member} {member.id}", color=0xff0000).set_footer(text="BAN済みのサーバーも含まれます")
    e.add_field(name=f"Global BAN Result",value=f"全てのサーバー　`{str(len(bot.guilds))}`\nGban成功数 `{count}`")
    msg = await ctx.respond(embed=e)
    await ctx.respond(file=discord.File("result.txt", filename="GbanResult.txt"), ephemeral=True)

@bot.slash_command(name="stop", description="開発者限定緊急停止")
async def SCRIPT_STOP(ctx):
    if ctx.author.id != s.Dev:
        await ctx.respond("帰れ")
        return
    user = bot.get_user(959142919573491722)
    e = discord.Embed(title="強制終了報告", description=f"{datetime.datetime.now()}",color=0x6dc1d1)
    await user.send(embed=e)
    await ctx.respond(f"{datetime.datetime.now()}\n{ctx.author}\n{ctx.author.id}")    
    sys.exit()

@bot.slash_command(name="夕弦", )
async def ON_BOT(ctx):
    if ctx.author.id != s.Dev:
        await ctx.respond("帰れ", ephemeral=True)
        return
    subprocess.run("cd C:\\Users\\Ennui\\BOT", shell = True)
    subprocess.run("python spam.py", shell=True)
    await ctx.respond("<@968603083414331423>")

@bot.slash_command(name="原神ラインスタンプ", descriptin="原神LINEステッカーをZIPファイルで送信")
async def send_ZipFile(ctx):
    with open('STICKER OF GENSIN.zip', 'rb') as f:
        pic = discord.File(f)
        await ctx.respond("１０秒後削除",file=pic, delete_after=10)

@bot.slash_command(name="原神聖遺物スコア計算", desciption="小数点も要する")
async def clac_score(ctx,会心率:float=None, 会心ダメージ:float=None, 攻撃_防御力:float=None):
    if not 攻撃_防御力: 攻撃_防御力=0
    if not 会心ダメージ:会心ダメージ=0
    if not 会心率:会心率=0
    score = 攻撃_防御力 + (会心率 * 2) + 会心ダメージ
    e = discord.Embed(description=f"**スコア** : **{round(score, 1)}**\n\n> 会心率```{会心率} %```\n> 会心ダメージ```{会心ダメージ} %```\n> 攻撃力・防御力```{攻撃_防御力} %```", color=0x6dc1d1)
    e.set_footer(text="20Lv想定でサブスコアのみ計算してます | Beta ver")
    await ctx.respond(embed=e)

@bot.command()
async def pic(ctx):
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
        return cluster_centers_arr
    msg = await ctx.reply("Please wait a moment.<a:Loading_2:1007527284753834014>")
    r = requests.get(ctx.message.attachments[0].url)
    img = Image.open(io.BytesIO(r.content))
    img.save("image.png")
    color_arr = extract_main_color(img_path, 7)
    show_tiled_main_color(color_arr)
    file = discord.File("./image/stripe_image.png", filename="stripe.png")
    await msg.edit(content="Done<a:VerifyMark_1:987128219658514484>",file=file)

@bot.slash_command(name="タイプ別憤死")
async def type_funshi(ctx):
    text_funshi = """**典型的憤死パターン**<:emoji_15:1004313871705702441>
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
    b = Button(label="十字軍に行く", url="https://discord.gg/hunshi")
    view = View()
    view.add_item(b)

    b.disabled=True
    
    await ctx.respond(text_funshi, view=view)

@bot.slash_command(name="憤死ワード")
async def word_list(ctx):
    b = Button(label="十字軍に行く", url="https://discord.gg/hunshi")
    view = View()
    view.add_item(b)
    b.disabled=True
    await ctx.respond("""**典型的憤死ワード集**<:emoji_15:1004313871705702441>
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

@bot.command()
async def gensin(ctx):
    text = ("""<:gensin_L_sticker_futao_3:1005709133179256894>
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

@bot.slash_command(name="about", description="About this bot")
async def about(ctx):
    user= bot.get_user(956042267221721119)
    members = 0
    for guild in bot.guilds:members += guild.member_count - 1
    embed= discord.Embed(title="About this bot", color= 0x6dc1d1)
    embed.add_field(name= "<:icons_serverinsight:981767862463107132> Customers",value= f"Servers **:** `{str(len(bot.guilds))}`\nMembers **:** `{str(members)}`", inline= False)
    embed.add_field(name= "<:icons_supportteam:1007534581467074642> Dev", value= f"{user.mention}", inline= False)
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.add_field(name="<:icons_info:1007531327333093477> 注釈",value="適当にスクリプト書いた。駄作です。")
    embed.set_footer(text=f"By: {str(ctx.author)}")
    b = Button(label="Support Server", url="https://discord.gg/owen")
    b2 = Button(label="Invite URL", url=f"https://discord.com/oauth2/authorize?client_id=979001395703341096&permissions=1644971949559&scope=bot%20applications.commands")
    b3 = Button(label="source code", url="https://github.com/Ennuilw/-/tree/main")
    view = View()
    view.add_item(b)
    b.disabled = True
    view.add_item(b2)
    view.add_item(b3)

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
    if spotify_result:await ctx.respond(f"> https://open.spotify.com/track/{spotify_result.track_id}")

@bot.slash_command(name="spotify", description="アクティビティからSpotifyの楽曲情報を送信")
async def spotify(ctx, user:discord.Member=None):
    if not user:user=ctx.author
    _spotify_result= next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if _spotify_result is None:await ctx.respond(f"{user.name} is not listening to Spotify!")
    if _spotify_result:
        embed=discord.Embed(color=_spotify_result.color)
        embed.set_thumbnail(url=_spotify_result.album_cover_url)
        embed.add_field(name="Song Title", value=f"```{_spotify_result.title}```", inline=False)
        artists = _spotify_result.artists
        if not artists[0]: re_result=_spotify_result.artist
        else: re_result = ', '.join(artists)
        embed.add_field(name="Artist[s]", value=f"```{re_result}```")
        embed.add_field(name="Album", value=f"```{_spotify_result.album}```")
        embed.add_field(name="Time", value=f"```{dateutil.parser.parse(str(_spotify_result.duration)).strftime('%M:%S')}```", inline=False)
        embed.set_footer(text=f"By: {str(ctx.author)}")
        b = Button(label="URL", style=discord.ButtonStyle.green, emoji="<:App_logo_spotify_p:1007557495436365905>")
        jacket = Button(label="see jacket", style=discord.ButtonStyle.blurple, emoji="<:Icon_api:1007536617470312509>")#, row=1
        view = View()
        view.add_item(b)
        view.add_item(jacket)
        async def Button_1_callback(interaction:discord.Interaction):
            b.disabled=True
            await interaction.response.send_message(f"https://open.spotify.com/track/{_spotify_result.track_id}")

        async def Button_callback(interaction:discord.Interaction):
            await interaction.response.send_message(_spotify_result.album_cover_url, ephemeral=True)

        jacket.callback = Button_callback
        b.callback = Button_1_callback
        await ctx.respond(embed=embed, view=view)

@bot.command(aliases=["s"])
async def spotify(ctx, user:discord.Member=None):
    if not user:user=ctx.author
    _spotify_result= next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if _spotify_result is None:await ctx.respond(f"{user.name} is not listening to Spotify!")
    if _spotify_result:
        embed=discord.Embed(color=_spotify_result.color)
        embed.set_thumbnail(url=_spotify_result.album_cover_url)
        embed.add_field(name="Song Title", value=f"```{_spotify_result.title}```", inline=False)
        artists = _spotify_result.artists
        if not artists[0]: re_result=_spotify_result.artist
        else: re_result = ', '.join(artists)
        embed.add_field(name="Artist[s]", value=f"```{re_result}```")
        embed.add_field(name="Album", value=f"```{_spotify_result.album}```")
        embed.add_field(name="Time", value=f"```{dateutil.parser.parse(str(_spotify_result.duration)).strftime('%M:%S')}```", inline=False)
        embed.set_footer(text=f"By: {str(ctx.author)}")
        b = Button(label="URL", style=discord.ButtonStyle.green, emoji="<:App_logo_spotify_white:1007559242984734720>")
        jacket = Button(label="see jacket", style=discord.ButtonStyle.blurple, emoji="<:Icon_api:1007536617470312509>")#, row=1
        view = View()
        view.add_item(b)
        view.add_item(jacket)
        async def Button_1_callback(interaction:discord.Interaction):
            b.disabled=True
            await interaction.response.send_message(f"https://open.spotify.com/track/{_spotify_result.track_id}")

        async def Button_callback(interaction:discord.Interaction):
            await interaction.response.send_message(_spotify_result.album_cover_url, ephemeral=True)

        jacket.callback = Button_callback
        b.callback = Button_1_callback
        await ctx.respond(embed=embed, view=view)

@bot.slash_command(name="spotify_songs_search", description="Spotify楽曲を検索・・・日本語だと検索エラーとか出る")
async def search(ctx, *, keyword):
    result = sp.search(q=keyword, limit=5)
    view = View()
    i = 0
    e = discord.Embed(description="<:_info:1007535167952392203> **見方**\n```曲名 [アルバム名] - アーティスト```",color=s.s_c).set_thumbnail(url=random.choice(Spotify_logo))
    for idx, track in enumerate(result['tracks']['items']):
        #songs.append(track['external_urls']['spotify'])
        e.add_field(name=f"{idx + 1} - Detales", value=f"```{track['name']} [{track['album']['name']}] - {track['artists'][0]['name']}```", inline=False)
        i += 1
        b = Button(label=str(idx + 1), url = track['external_urls']['spotify'])
        view.add_item(b)
    await ctx.respond(embed=e, view=view)

@bot.slash_command(name="invite", description="メンテナンス中 | Botをメンションして招待URLを生成。 IDを入れるやつは馬鹿")
async def invite(ctx, mention:discord.Member):
    e=discord.Embed(description=f"{mention}(**{mention.id}**)", color=0x6dc1d1)
    date_format="%Y/%m/%d %H:%M"
    e.add_field(name=f"アカウント作成日", value=f"**`{mention.created_at.strftime(date_format)}`**")
    e.add_field(name="サーバー参加日", value= f"**`{mention.joined_at.strftime(date_format)}`**")
    #else:#id = str(id.replace("<@", '').strip())#id = str(id.replace(">", '').strip())
    b = Button(label="No perms", url= f"https://discord.com/oauth2/authorize?client_id={mention.id}&permissions=0&scope=bot%20applications.commands")
    b_2 = Button(label="Admin", url= f"https://discord.com/oauth2/authorize?client_id={mention.id}&permissions=8&scope=bot%20applications.commands")
    b_3 = Button(label="Make yourself",  url= f"https://discord.com/oauth2/authorize?client_id={mention.id}&permissions=1644971949559&scope=bot%20applications.commands")
    view=View()
    view.add_item(b)
    view.add_item(b_2)
    view.add_item(b_3)
    try:e.set_thumbnail(url=mention.avatar.url)
    except:e.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    await ctx.respond(embed=e, view=view)

@bot.command()
async def invitegen(ctx, id:str):
    b = Button(label="No perms", url= f"https://discord.com/oauth2/authorize?client_id={id}&permissions=0&scope=bot%20applications.commands")
    b_2 = Button(label="Admin", url= f"https://discord.com/oauth2/authorize?client_id={id}&permissions=8&scope=bot%20applications.commands")
    b_3 = Button(label="Make yourself",  url= f"https://discord.com/oauth2/authorize?client_id={id}&permissions=1644971949559&scope=bot%20applications.commands")
    view=View()
    view.add_item(b)
    view.add_item(b_2)
    view.add_item(b_3)
    await ctx.respond("出来た", view=view)    

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
    embed= discord.Embed(title= f"{user}", description= f"**ID : `{user.id}`**", color= 0x6dc1d1)
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
    #guild = bot.get_guild(int(guild_id)).leave()
    guild = bot.get_guild(int(guild_id))
    await guild.leave()
    await ctx.respond(f"{guild}から脱退しました。")

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
            value= f"User: **{str(sum(1 for member in guild.members if not member.bot))}**\nBot: **{str(sum(1 for member in guild.members if member.bot))}**\nOnline: **{len(online)}**")
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

@bot.slash_command(name="serverbanner", description="PNG,GIFでサーバーのバナーを取得する")
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
        await ctx.respond(embed=_embed, view=view)
    except:
        embed= discord.Embed(title= "Have you set banner?")
        embed.set_footer(text=str(f"By: {ctx.author}"))
        await ctx.respond(embed= embed)

@bot.slash_command(name="invitesplash", description="サーバーの招待背景を表示")
async def invite_splash(ctx):
    try:await ctx.respond(embed=discord.Embed(color= 0x6dc1d1).set_image(url=ctx.guild.splash))
    except:await ctx.respond("ERROR")

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
            value= f"User: **{str(sum(1 for member in guild.members if not member.bot))}**\nBot: **{str(sum(1 for member in guild.members if member.bot))}**\nOnline: **{len(online)}**")
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
async def source_code(ctx):
    e = discord.Embed(description="PythonなのにClass使ってません:sob:",color=0x6dc1c1)
    b = Button(label="Jump to Github", url="https://github.com/Ennuilw/-/tree/main")
    view=View()
    view.add_item(b)
    await ctx.respond(embed=e, view=view)

@bot.event
async def on_command_error(ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            embed = discord.Embed(title="-MissingPermissions", description=error, color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.errors.ApplicationCommandInvokeError):
            embed = discord.Embed(title="-ApplicationCommandInvokeError", description=error, color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
            embed = discord.Embed(title="-BotMissingPermissions", description=error, color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
            embed = discord.Embed(title="-CommandNotFound", description=f"おいおっさんwんなコマンドねーぞwwwちゃんと見ろメクラwwwww。", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
            embed = discord.Embed(title="-MemberNotFound", description=error, color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            embed = discord.Embed(title="-BadArgument", description=error, color=0xff0000)
            await ctx.send(embed=embed) 
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title="-BadArgument", description=error, color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error,discord.ext.commands.errors.MissingRole):
            embed = discord.Embed(title="-MissingRole", description=error, color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            embed = discord.Embed(title="-CheckFailure", description=error, color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            embed = discord.Embed(title="-CommandInvokeError", description=error, color=0xff0000)
            await ctx.send(embed=embed)
        else:raise error

bot.run(s.token)
