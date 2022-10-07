import setting as s
import discord,dateutil.parser,random,datetime,spotipy,aiohttp,time,asyncio
from discord.ext import commands
from discord.ui import InputText
from discord.ext.ui import Button, View, Message, ViewTracker, MessageProvider, Modal, Select
from discord.ext.ui.combine import AsyncPublisher
from discord.commands import Option
from spotipy.oauth2 import SpotifyClientCredentials
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
#from typing import TypedDict

from PIL import Image, ImageDraw, ImageFont
from sklearn.cluster import KMeans
import numpy as np
from numpy import linalg as LA
import requests,cv2,io


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="a.", intents=discord.Intents.all())
        
class SPB(discord.ui.View):
    def __init__(self, spotify):
        super().__init__()
        self.sp = spotify
    
    @discord.ui.button(label="URL", style=discord.ButtonStyle.green, emoji="<:App_logo_spotify_white:1007559242984734720>")
    async def callback(self, button, interaction:discord.Interaction):
        button.disabled=True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"https://open.spotify.com/track/{self.sp.track_id}")


bot = MyBot()
img_path = 'image.png'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = s.spotify_client_id, client_secret = s.spotify_client_secret))
t_delta = datetime.timedelta(hours=9)
now = datetime.datetime.now(datetime.timezone(t_delta, 'JST'))


@bot.user_command(name="account")
async def accountdetails(interaction:discord.Interaction, usr:discord.Member):
    date_format="%Y/%m/%d %H:%M"
    e=discord.Embed(description=f"**Name:** {usr}\n**Id  :** {usr.id}\n").set_thumbnail(url=usr.display_avatar)
    e.add_field(name=f"Creation Account", value=f"**`{usr.created_at.strftime(date_format)}`**")
    e.add_field(name="サーバー参加日", value= f"**`{usr.joined_at.strftime(date_format)}`**")
    await interaction.response.send_message(embed=e, ephemeral=True)

@bot.command(aliases=["i"], description="ランダムに絵文字で罵倒するよ")
async def insult(c):
    await c.send(random.choice(s.word_list))

@bot.command(aliases=["ilen"], description="insultのレパートリー数を取得")
async def 絵文字リスト数(ctx):await ctx.send("```" + str(len(s.word_list)) + "```")

@bot.slash_command(name="embed", description="Embedを生成するよ。どこか間違えてたらエラーとしか出ないよ")
async def embed(interaction,
        color:Option(str, "Embedのカラー", choices=[
            "Blue|青", "Green|緑", "Orange|オレンジ", "Yellow|黄色", "Red|赤", "Purple|紫", "Pink|ピンク", "Violet|バイトレット", \
            "white|白", "Black|黒", "Brown|褐色", "Gray|グレー", "  Teal|ティール", "Gold|ゴールド", "Crimson|真紅"])=None,
        author:Option(str, "Embedの筆者部分")=None,
        author_url:Option(str, "筆者部分のURL")=None,
        author_icon:Option(str, "筆者のアイコン")=None,
        title:Option(str,"Embedのtitle部分")=None,
        description:Option(str,"Embedの説明文")=None,
        url:Option(str, "Embedのtitleに挿入するURL")=None,
        name_1:Option(str, "引数:valueとセットでないとエラーになるよ。")=None,
        value_1:Option(str, "引数:nameとセットじゃないとエラーになるよ。")=None,
        name_2:Option(str, "引数:valueとセットでないとエラーになるよ。")=None,
        value_2:Option(str, "引数:nameとセットじゃないとエラーになるよ。")=None,
        thumbnail:Option(str, "Embedのサムネイル部分の画像URL")=None,
        image:Option(str, "Embedの画像URL")=None,
        channel:Option(discord.TextChannel, "送信したいチャンネル")=None):
    e = discord.Embed()
    if not author:pass
    else: e.set_author(name=author, url=author_icon, icon_url=author_url)
    if not color:pass
    else:
        match color:
            case "Blue|青":color=0x0000ff
            case "Green|緑":color=0x008000
            case "Orange|オレンジ":color=0xffa500
            case "Yellow|黄色":color=0xffff00
            case "Red|赤":color=0xff0000
            case "Purple|紫":color=0x800080
            case "Pink|ピンク":color=0xffc0cb
            case "Violet|バイトレット":color=0xee82ee
            case "white|白":color=0xffffff
            case "Black|黒":color=0x000001
            case "Brown|褐色":color=0xa52a2a
            case "Gray|グレー":color=0x808080
            case "Teal|ティール":color=0x008080
            case "Gold|ゴールド":color=0xffd700
            case _:color=0xed143d
        e.color=color
    if not title:pass
    else:e.title=title
    if not description:pass
    else:e.description=description
    if not url:pass
    else: e.url=url
    if name_1 and value_1:pass
    else:e.add_field(name=name_1,value=value_1)
    if name_2 and value_2:pass
    else:e.add_field(name=name_2,value=value_2)
    if not thumbnail:pass
    else:e.set_thumbnail(url=thumbnail)
    if not image:pass
    else:e.set_image(url=image)
    if not channel:await interaction.response.send_message(embed=e)
    else:
        channel = discord.utils.get(interaction.guild.channels, name=channel.name)
        msg = await channel.send(embed=e)
        await interaction.response.send_message(
            embed=discord.Embed(title=f"正常に終了しました", description=f"[jump to url](https://discord.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}/)"), ephemeral=True)

@bot.command(aliases=["sc"])
async def spell_check(ctx):
    var = random.randint(1, 5)
    b_e1 = discord.Embed(color = 0x6cd1c1)
    match (var):
        case 1:
            b_e1 = discord.Embed(title="初期化の英単語")
            answer = "initialization"
        case 2:
            b_e1 = discord.Embed(title="代入の英単語")
            answer = "assignment"
        case 3:
            b_e1 = discord.Embed(title="認可されたんティティが要求したときにアクセス及び使用が可能である特性")
            answer = "availability"
        case 4:
            b_e1 = discord.Embed(title="集積回路の英単語")
            answer = "integrated circuit"
        case 5:
            b_e1 = discord.Embed(title="CPUの英単語")
            answer = "central processing unit"
        case 6:
            b_e1 = discord.Embed(title="")
            answer = ""
    await ctx.reply(embed=b_e1)
    s_time = time.perf_counter()
    try:message = await bot.wait_for("message", timeout=15.0, check = lambda m:m.author and m.channel == ctx.channel)
    except asyncio.TimeoutError: await ctx.send(embed=discord.Embed(title = ":timer: 時間切れ！",color = 0xff0000))
    else:
        if message.content.lower() == answer:
            e_time = time.perf_counter()
            await message.reply(f":o: 正解\n{Decimal(str(e_time - s_time)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP) }秒")
        else:await message.reply(f":x: 不正解だよ。バカが。\n:解答 ||*{answer}*||")

@bot.command(aliases=["e"], description="フォント名: Meiryo UI 太字, Meiryo UI 太字 斜体, メイリオ ボールド, メイリオ, ボールドイタリック\nファイル名: meiryob.ttc")
async def emo(ctx, *, word):
    if (4 <= len(word)):X = 400
    elif (3 == len(word)):X = 300
    elif (2 == len(word)):X = 200
    else:X=100
    im = Image.new("RGB", (X, 95), (255, 255, 255))
    im.putalpha(0)
    font = ImageFont.truetype(r"/home/ennui/.local/share/fonts/WRITE_HERE.ttf",size=99)
    draw = ImageDraw.Draw(im)
    draw.text((0, -20), word, fill=(255, 123, 157), font=font)
    im = im.resize((108, 108), resample=0)
    im.save("emoji.png")
    await ctx.reply(file=discord.File("emoji.png"), mention_author=False)

@bot.command()
async def roles(ctx):
    with open("TxtList/rolelist.txt", "w", encoding="utf-8") as f:
        role_ = sorted([role for role in ctx.guild.roles], reverse=True)
        role_.pop()
        f.write(f"Role: {str(len(role_))}\n")
        [f.write(f"[{str(role.id)}] | {role}\n") for role in role_]
    await ctx.reply(file=discord.File("TxtList/rolelist.txt"))

@bot.slash_command(name="invites", description="sa-ba- ni aru invite wo dasu")
async def invites(interactioin, id =None):
    if not int(interactioin.author.id) in s.admin_users:
        await interactioin.response.send_message("帰れ", ephemeral=True)
        return
    if not id:guild = interactioin.guild
    else:guild = bot.get_guild(int(id))
    try:
        vanity = await id.guild.vanity_invite()
        await interactioin.respond(f"VANITY: {str(vanity).replace('https://discord.gg/', ' ')}")
    except:pass
    [await interactioin.respond(f"``{(invite.url).replace('https://discord.gg/', ' ')}``") for invite in await guild.invites()]

@bot.slash_command(name="yufu_yt", description="香港人Yufuさんの勝手に切り抜きした動画リンクを送信。")
async def yufu_yt(interaction:discord.Interaction,
    video:Option(str, "選んでください", choices=["ほんこんじん（編集済み）", "YUFUダイジェスト"])):
    if int(interaction.author.id) in s.yufu_users:
        await interaction.response.send_message("勝手に切り抜いてごめんなさい＞＜", ephemeral=True)
    if video in ("ほんこんじん（編集済み）"):await interaction.response.send_message("https://youtu.be/pP_rrVc0KKY")
    else:await interaction.response.send_message("https://youtu.be/rKb0jmfE020")

@bot.slash_command(name="botinserver", description="管理者専用")
async def inserver(interaction:discord.Interaction):
    if not int(interaction.author.id) in s.admin_users:
        await interaction.response.send_message("gfy")
        return
    with open("TxtList/server.txt", "w", encoding='utf-8') as f:
        [f.write(f"[{str(guild.id):>20} ] {guild.name}\n") for guild in bot.guilds]
    await interaction.response.send_message(file=discord.File("TxtList/server.txt", filename="ServerList.txt"), ephemeral=True)

#if guild.me.guild_permissions.ban_members:

@bot.slash_command(name="global_ban", description="開発者専用")
async def global_ban(interaction, member : discord.Member, reason:str):
    if not int(interaction.author.id) in s.admin_users:
        await interaction.response.send_message("帰れ", ephemeral=True)
        return
    msg_1 = await interaction.response.send_message("<a:Loading_2:1007527284753834014>")
    count = 0
    with open("TxtList/result.txt", "w", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}]\n")
        for guild in bot.guilds:
            try:
                await guild.ban(member, reason=reason)
                f.write(f"SUCCESS [{guild.id:>20} ] : {guild}\n")
                count += 1
            except:
                f.write(f"FAILURE [{guild.id:>20} ] : {guild}\n")
            
    e = discord.Embed(description=f"**Name:** {member}\nID: {member.id:<22}", color=0xff0000).set_footer(text="BAN済みのサーバーも含まれます。")
    e.add_field(name=f"Global BAN Result",value=f"Total: `{str(len(bot.guilds)):>4}`: \nSuccess: `{count:<4}`: ").add_field(name="Reason", value=f"```{reason}```")
    await msg_1.edit_original_message(content=None, embed=e)
    await interaction.respond(file=discord.File("TxtList/result.txt", filename="GbanResult.txt"), ephemeral=True)

@bot.slash_command(name="原神聖遺物スコア計算", desciption="小数点対応")
async def clac_score(interaction,会心率:Option(float,"会心率 / Membership rate")=None,会心ダメージ:Option(float, "会心ダメージ / Membership rate")=None,
        攻撃_防御力:Option(float, "攻撃力 or 防御力 / ATK or DEF")=None,聖遺物:Option(str, "聖遺物を選択してください / Choice your Artifacts" ,choices=["花/羽/杯", "時計/冠"] )=None):
    msg = await interaction.respond("<a:Loading_6:1012760935343063050>")
    if not 攻撃_防御力: 攻撃_防御力=0
    if not 会心ダメージ:会心ダメージ=0
    if not 会心率:会心率=0
    score = 攻撃_防御力 + (会心率 * 2) + 会心ダメージ
    e = discord.Embed(description=f"**スコア** : **{round(score, 1)}**\n\n> 会心率```{会心率} %```\n> 会心ダメージ```{会心ダメージ} %```\n> 攻撃力・防御力```{攻撃_防御力} %```", color=0x6dc1d1)
    e.set_footer(text="20Lv想定でサブスコアのみ計算してます | Beta ver")
    if not 聖遺物:pass
    else:
        if 聖遺物 in ("時計/冠"):
            if score >= 30:e.title="時計/冠 -合格"
            else:e.title="時計/冠 -カスコアやんけ捨てろよwww"
        else:
            if score >= 50:e.title="花/羽/杯 -合格"
            else:e.title="花/羽/杯 -カスコアやんけ捨てろよwww"
    await msg.edit_original_message(content=None,embed=e)

@bot.slash_command(name="絵文字やステッカー", description="絵文字・ステッカー素材集")
async def zipsend(interaction, choose:Option(str, "どれかお選びください", choices=["煽りEmoji", "原神Lineスタンプ"])):
    if "煽りEmoji" in choose:
        with open("TxtList/EMOJI2022_09_07.zip", 'rb') as f:await interaction.response.send_message(file=discord.File(f))
    else:
        with open('TxtList/STICKER OF GENSIN.zip', 'rb') as f:await interaction.response.send_message(file=discord.File(f))

@bot.command()
async def pic(ctx):
    def show_tiled_main_color(color_arr):
        IMG_SIZE = 64
        MARGIN = 15
        width = IMG_SIZE * color_arr.shape[0] + MARGIN * 2
        height = IMG_SIZE + MARGIN * 2
        tiled_color_img = Image.new(mode='RGB', size=(width, height), color='#333333')
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
    file = discord.File("image/stripe_image.png", filename="stripe.png")
    await msg.edit(content="Done<a:VerifyMark_1:987128219658514484>",file=file)
    """はよ続きやれやhttps://note.com/shiftkey/n/n3d95ca76dd1d"""

@bot.slash_command(name="タイプ別憤死", description="さまざまな憤死例を解説")
async def type_funshi(ctx):
    await ctx.respond("""**典型的憤死パターン** <:emoji_15:1004313871705702441>\n
**1.発狂型憤死**
明らかに劣勢な状態になってから露骨に発作を起こしキチガイムーヴを始めるタイプ。
ネタに走って有耶無耶にしようという意図が見え見えである。

**2.生存本能型憤死**
生存本能タイムアウト/ブロック/ミュート/BANを行うタイプ。
憤死回避のために実力行使を行ってしまったが故の行動である。

**3.糖質化型憤死**
明らかな決めつけや思い込みをし始め勝手に憤慨し続けるタイプ。
\*\*\*の圧倒的煽りによって極度のストレスを受けた故の行動である。

**4.ノーダメアピール型憤死**
ノーダメアピールを繰り返し精神的勝利を訴え続けるタイプ。
トマトフェイスを隠しきれていないため周りから見ると滑稽である。

**5.スルー型憤死**
突然話題を変えることで露骨にスルーアピールをするタイプ。
指摘されるとすぐ必死になって否定をしてくることが多い。

[十字軍・深夜祭に行く](https://discord.gg/funshi)""")

@bot.slash_command(name="憤死ワード", description="主に十字軍の神煽りに圧倒され憤慨した者の発する典型的なワードリスト")
async def word_list(interaction):
    await interaction.respond("""**典型的憤死ワード集** <:emoji_15:1004313871705702441>
**・**荒らしで時間無駄にしてて草
**・**しょうもないことして楽しい？
**・**BANすればいいだけ 残念だったな
**・**ムカつくから黙れ
**・**学歴しか誇れないゴミで草
**・**楽しんでて哀れ
**・**暇つぶし楽しかったよ
**・**学歴と頭脳は比例しない
**・**あーもうこいつうるさいから蹴ろう
**・**誤字してて草
**・**十字軍はくだらない組織
**・**あそんでいるだけなんだが？

[十字軍・深夜祭に行く](https://discord.gg/funshi)""") 

@bot.slash_command(name="about", description="About this bot")
async def about(interaction):
    user= bot.get_user(956042267221721119)
    members = 0
    for guild in bot.guilds:members += guild.member_count - 1
    embed= discord.Embed(title="About this bot", description="なぜか日本語と英語が入り混じってます。\n適当にスクリプト書いた。駄作です。<:Cirnohi:1010798243866755114>", color= 0x6dc1d1)
    embed.add_field(name= "Customers",value= f"> **Servers:** {str(len(bot.guilds))}\n> **Members:** {str(members)}", inline= False)
    embed.add_field(name= "Support", value= f"> **Deveroper:** {user.mention}\n> **Source:** [Github](https://github.com/Ennuilw/-/tree/main)\n\
        > **Our server:** [Click me](https://discord.gg/FwgCqwJN7p)", inline= False)
    embed.set_footer(text=f"By: {str(interaction.author)}")
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name="avatar", description="サーバープロフィールのアイコンを取得")
async def avatar(ctx, user:discord.Member=None):
    if not user: user= ctx.author
    avatar= user.display_avatar
    embed= discord.Embed(description= f"{user.mention} Avatar",  color= 0x6dc1d1).set_image(url= avatar).set_footer(text= f"By: {str(ctx.author)}")
    await ctx.respond(embed= embed)

@bot.slash_command(name="avatar_real", description="ユーザープロフィールのアイコンを取得")
async def real_avatar(interaction, user:discord.Member=None):
    if not user:user=interaction.author
    avatar = user.avatar.url
    e = discord.Embed(description= f"{user.mention} Avatar", color= 0x6dc1d1).set_image(url= avatar).set_footer(text= f"By: {str(interaction.author)}")
    await interaction.response.send_message(embed=e)

@bot.slash_command(name="banner", description="ユーザープロフィールからバナーを取得。もしあれば。")
async def banner(interaction:discord.Interaction, user:discord.Member=None):
    if not user:user=interaction.author
    user = await bot.fetch_user(user.id)
    try:
        banner_url = user.banner.url
        avatar=user.display_avatar
        await interaction.respond(embed=discord.Embed(description= f"{user.mention} Banner",  color= 0x6dc1d1).set_image(url= banner_url).set_footer(text= f"By: {str(interaction.author)}"))
    except:await interaction.respond("Bannerが検出できない")

@bot.slash_command(name="track", description="現在アクティビティにあるSpotifyの楽曲のURLを送信")
async def track(ctx, user:discord.Member=None):
    if not user: user=ctx.author
    spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if spotify_result:await ctx.respond(f"> https://open.spotify.com/track/{spotify_result.track_id}")
    else:await ctx.respond(f"{user.display_name} is not listening to Spotify!")

@bot.slash_command(name="spotify", description="アクティビティからSpotifyの楽曲情報を送信")
async def spotify(interaction, user:discord.Member=None):
    if not user:user=interaction.author
    _spotify_result= next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if not _spotify_result :await interaction.respond(f"{user.display_name} is not listening to Spotify!")
    if _spotify_result:
        embed=discord.Embed(color=_spotify_result.color).set_thumbnail(url=_spotify_result.album_cover_url)
        embed.add_field(name="Song Title", value=f"```{_spotify_result.title}```", inline=False)
        artists = _spotify_result.artists
        if not artists[0]: re_result=_spotify_result.artist
        else: re_result = ', '.join(artists)
        embed.add_field(name="Artist[s]", value=f"```{re_result}```").add_field(name="Album", value=f"```{_spotify_result.album}```")
        embed.add_field(name="Time", value=f"```{dateutil.parser.parse(str(_spotify_result.duration)).strftime('%M:%S')}```", inline=False)
        embed.set_footer(text=f"By: {str(interaction.author)}")
        await interaction.respond(embed=embed, view=SPB(_spotify_result))

@bot.command(aliases=["s"])
async def spotify(ctx, user:discord.Member=None):
    if not user:user=ctx.author
    _spotify_result= next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if not _spotify_result:await ctx.send(f"{user.display_name} is not listening to Spotify!")
    if _spotify_result:
        embed=discord.Embed(color=_spotify_result.color).set_thumbnail(url=_spotify_result.album_cover_url)
        embed.add_field(name="Song Title", value=f"```{_spotify_result.title}```", inline=False)
        artists = _spotify_result.artists
        if not artists[0]: re_result=_spotify_result.artist
        else: re_result = ', '.join(artists)
        embed.add_field(name="Artist[s]", value=f"```{re_result}```").add_field(name="Album", value=f"```{_spotify_result.album}```")
        embed.add_field(name="Time", value=f"```{dateutil.parser.parse(str(_spotify_result.duration)).strftime('%M:%S')}```", inline=False)
        embed.set_footer(text=f"By: {str(ctx.author)}")
        await ctx.send(embed=embed, view=SPB(_spotify_result))

@bot.slash_command(name="spotify_songs_search", description="Spotify楽曲を検索・・・日本語だとたまにエラー出る")
async def search(interaction, *, keyword):
    result = sp.search(q=keyword, limit=4)
    sp_str = []
    for idx, track in enumerate(result['tracks']['items']):
        song_url = track['external_urls']['spotify']
        if len(track['name']) > 20:repl_song_name = str(track['name'][0:20] + "... ")
        else:repl_song_name=track['name']
        if len(track['album']['name']) > 15:repl_song_album = str(track['album']['name'][0:15] + "...")
        else:repl_song_album=track['album']['name']
        sp_str.append(f"<:Icon_jumptourl:1007535375033581588> **[{repl_song_name}]({song_url}) - {track['artists'][0]['name']} |** {repl_song_album}")
    await interaction.response.send_message(embed=discord.Embed(description= "\n\n".join(sp_str),color=s.s_c).set_footer(text="Layout: Title - Artists | Album"))

@bot.slash_command(name="抗うつ効果", description="*自己責任* 真面目なものからいろんなものまで")
async def antidepressant(interaction, 
        antidepressant:Option(choices=["", "", "ネタ", ""])
    ):
    if None in antidepressant:pass
    elif "ネタ" in antidepressant:await interaction.respond("<https://milkfactory.jp/products/heapps/movie/>")


@bot.slash_command(name="invite", description="Botをメンションして招待URLを生成。")
async def invite(interaction, mention:discord.Member):
    if mention.bot:
        e=discord.Embed(description=f"**Name:** {mention}\n**ID:** {mention.id}", color=0x6dc1d1)
        date_format="%Y/%m/%d %H:%M"
        e.add_field(name=f"アカウント作成日", value=f"**`{mention.created_at.strftime(date_format)}`**").add_field(name="サーバー参加日", value= f"**`{mention.joined_at.strftime(date_format)}`**")
        e.add_field(name="Select Permissions", value = f"**- [No Perm](https://discord.com/oauth2/authorize?client_id={mention.id}&permissions=0&scope=bot%20applications.commands)**\n\
            **- [Admin](https://discord.com/oauth2/authorize?client_id={mention.id}&permissions=8&scope=bot%20applications.commands)**\n\
            **- [Make yourself](https://discord.com/oauth2/authorize?client_id={mention.id}&permissions=1644971949559&scope=bot%20applications.commands)**", inline=False)
        try:e.set_thumbnail(url=mention.avatar.url)
        except:e.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
        await interaction.respond(embed=e)
    else:await interaction.response.send_message("Botじゃなくね?", ephemeral=True)

@bot.command()
async def invitegen(ctx, id:str):
    e = discord.Embed(description=f"**- [No Perm](https://discord.com/oauth2/authorize?client_id={id}&permissions=0&scope=bot%20applications.commands)**\n\
            **- [Admin](https://discord.com/oauth2/authorize?client_id={id}&permissions=8&scope=bot%20applications.commands)**\n\
            **- [Make yourself](https://discord.com/oauth2/authorize?client_id={id}&permissions=1644971949559&scope=bot%20applications.commands)**")
    await ctx.reply(embed=e)

@bot.slash_command(name="account", description="アカウントの作成・参加日時")
async def account(interaction, user:discord.Member=None):
    if not user:user=interaction.author
    date_format="%Y/%m/%d %H:%M"
    e = discord.Embed(color= 0x6dc1d1).set_author(name=f"{user} (ID: {user.id})")
    e.add_field(name=f"アカウント作成日", value=f"**`{user.created_at.strftime(date_format)}`**").add_field(name="サーバー参加日", value= f"**`{user.joined_at.strftime(date_format)}`**")
    e.set_thumbnail(url=user.display_avatar).set_footer(text= f"By: {str(interaction.author)}")
    await interaction.response.send_message(embed=e)

@bot.slash_command(name="userinfo", description="ユーザー情報を送信")
async def userinfo(interaction:discord.Interaction, user:discord.Member=None):
    if not user: user= interaction.author
    date_format="%Y/%m/%d"
    s = str(user.status)
    s_icon = ""
    if s == "online":s_icon = "🟢"
    elif s == "idle":s_icon = "🟡"
    elif s == "dnd":s_icon = "🔴"
    else:s_icon = "⚫"
    embed= discord.Embed(description= f"**ID : {user.id:>21}**\n**Status : `{s_icon} {s}`**", color= 0x6dc1d1)
    embed.set_thumbnail(url=user.display_avatar)
    embed.add_field(name= "Name", value= f"> {user}", inline= True)
    embed.add_field(name= "Nickname", value= f"> {user.display_name}", inline= True)
    if len(user.roles) >= 1:
        new_role = ([r.mention for r in user.roles][1:])
        embed.add_field(name= f"Roles `{len(user.roles)-1}`", value= f"> {' '.join(new_role[::-1])}", inline=False)
    embed.add_field(name= "Createion Account", value= f"> `{user.created_at.strftime(date_format)}`", inline= True)
    embed.add_field(name= "Joined Server", value= f"> `{user.joined_at.strftime(date_format)}`", inline= True)
    user = await bot.fetch_user(user.id)
    try:embed.set_image(url=user.banner.url)
    except:pass
    embed.set_footer(text= f"By: {str(interaction.author)} | To see more account details use \"/account\"")
    await interaction.respond(embed= embed)

@bot.slash_command(name="leave")
async def leave(interaction, guild_id=None):
    if not int(interaction.author.id) in s.admin_users:
        await interaction.response.send_message("帰れ", ephemeral=True)
        return
    guild = bot.get_guild(int(guild_id))
    await guild.leave()
    await interaction.respond(f"{guild}から脱退した。")

@bot.slash_command(name="serverinfo", description="Get info about server")
async def serverinfo(ctx):
    guild = ctx.guild
    tchannels= len(guild.text_channels)
    vchannels= len(guild.voice_channels)
    roles= [role for role in guild.roles]
    emojis= len([1 for emoji in guild.emojis])
    e_gif = len([1 for e in guild.emojis if e.animated])
    online= [1 for user in guild.members if user.status != discord.Status.offline]
    stickers = [sticker  for sticker in guild.stickers]
    embed= discord.Embed(title=f"{guild.name}", description= f":crown: **Owner : **{guild.owner.mention}\n\
        :id: **Server id : `{guild.id}`**\n:calendar_spiral: **Createion : `{guild.created_at.strftime('%Y/%m/%d')}`**", color= 0x6dc1d1)
    try:embed.set_thumbnail(url= guild.icon.url)
    except:pass
    embed.add_field(name= ":shield: Role", value= f"Roles: **{len(roles)}**", inline= True)
    embed.add_field(name= f":gem: Boost [{guild.premium_subscription_count}]", value= f"Tier: ** {guild.premium_tier}**")
    try:
        vanity =  await guild.vanity_invite()
        embed.add_field(name=":link: Vanity URL", value=f"`{str(vanity).replace('https://discord.gg/', '')}`")
    except:embed.add_field(name=":link: Vanity URL", value=f"`None`")
    embed.add_field(name= f":grinning: Emoji [{emojis}]", value= f"Static: **{emojis - e_gif}**\nAnimated: **{e_gif}**\nStickers: **{len(stickers)}**")
    embed.add_field(name= f":busts_in_silhouette: Members [{guild.member_count}]", 
            value= f"User: **{str(sum(1 for member in guild.members if not member.bot))}** | Bot: **{str(sum(1 for member in guild.members if member.bot))}**\nOnline: **{len(online)}**")
    embed.add_field(name= f":speech_left: Channels [{tchannels+vchannels}]", 
            value= f"Text: **{tchannels}** | Voice: **{vchannels}**\nCategory: **{len(guild.categories)}**",inline= True)
    embed.set_footer(text= f"By: {str(ctx.author)}")
    try:
        req= await bot.http.request(discord.http.Route("GET", "/guilds/{sid}", sid= guild.id))
        banner_id= req["banner"]
        if banner_id:
            banner_url_png= f"https://cdn.discordapp.com/banners/{guild.id}/{banner_id}.png?size=1024"
            banner_url_gif= f"https://cdn.discordapp.com/banners/{guild.id}/{banner_id}.gif?size=1024"
            embed.add_field(name="Banner", value=f"[PNG]({banner_url_png}) | [GIF]({banner_url_gif})")
        await ctx.respond(embed=embed)
    except:await ctx.respond(embed=embed)

@bot.slash_command(name="invitesplash", description="サーバーの招待背景を表示")
async def invite_splash(ctx):
    try:await ctx.respond(embed=discord.Embed(color= 0x6dc1d1).set_image(url=ctx.guild.splash))
    except:await ctx.respond("ERROR")

@bot.slash_command(name="purge", description="指定した数字分メッセージを削除")
@commands.has_permissions(manage_messages= True)
async def purge(interaction:discord.Interaction, amount:Option(int, "整数を入力")):
    deleted = await interaction.channel.purge(limit=amount)
    e = discord.Embed(description=f"Message Purged!```{len(deleted)} messages```\nAutomatically deleted after 5 seconds").set_footer(text=f"By: {interaction.author}")
    await interaction.response.send_message(embed=e, delete_after=5)

@bot.slash_command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_member(interaction:discord.Interaction, user:discord.Member, reason:Option(str, "ユーザーをBANする理由。無くても可。")= None):
    if not reason: reason = "No reason provided."
    user.kick(reason=reason)
    e=discord.Embed(title=f":wave::wave: {user}", description=f"ID: {user.id}", color=0xff0000).add_field(name="Reason", value=f"```{reason}```")
    await interaction.respond(embed=e)

@bot.slash_command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(interaction:discord.Interaction, user:discord.Member, reason:Option(str, "ユーザーをBANする理由。無くても可。")= None):
    if not reason:reason="No reason"
    await user.ban(reason=reason)
    e=discord.Embed(title=f":wave::wave: {user}", description=f"ID: {user.id}", color=0xff0000).add_field(name="Reason", value=f"```{reason}```")
    await interaction.respond(embed=e)

@bot.slash_command(name="nuke", description="チャンネルを再作成")
@commands.has_permissions(administrator=True)
async def delete(interaction, channel:discord.TextChannel=None):
    if not channel:channel=interaction.channel
    else:channel = discord.utils.get(interaction.guild.channels, name=channel.name)
    pos = channel.position
    await channel.delete()
    new_channel = await channel.clone()
    await new_channel.edit(position=pos)

@bot.slash_command(name="inserver", description="管理者専用", guild_ids=[941978430206009394])
async def inserver(interaction:discord.Interaction):
    if not int(interaction.author.id) in s.admin_users:
        await interaction.send("gfy", ephemeral=True)
        return
    with open("TxtList/server.txt", "w", encoding='utf-8') as f:
        for guild in bot.guilds:f.write(f"[{str(guild.id)}] {guild.name}\n")
    await interaction.response.send_message(file=discord.File("TxtList/server.txt", filename="ServerList.txt"), ephemeral=True)

@bot.slash_command(name="xserver", description="server idを入れてね!このボットが入ってるサーバーの情報を取得")
async def xserver(interaction, id):
    if not int(interaction.author.id) in s.admin_users:
        await interaction.respond("帰れ。", ephemeral=True)
        return
    guild = bot.get_guild(int(id))
    tchannels= len(guild.text_channels)
    vchannels= len(guild.voice_channels)
    roles= [role for role in guild.roles]
    emojis= len([1 for emoji in guild.emojis])
    e_gif = len([1 for e in guild.emojis if e.animated])
    online= [1 for user in guild.members if user.status != discord.Status.offline]
    stickers = [sticker  for sticker in guild.stickers]
    embed= discord.Embed(title=f"{guild.name}", description= f":crown: **Owner : **{guild.owner.mention}\n\
        :id: **Server id : `{guild.id}`**\n:calendar_spiral: **Createion : `{guild.created_at.strftime('%Y/%m/%d')}`**", color= 0x6dc1d1)
    try:embed.set_thumbnail(url= guild.icon.url)
    except:pass
    embed.add_field(name= ":shield: Role", value= f"Roles: **{len(roles)}**", inline= True)
    embed.add_field(name= f":gem: Boost [{guild.premium_subscription_count}]", value= f"Tier: ** {guild.premium_tier}**")
    try:
        vanity =  await guild.vanity_invite()
        embed.add_field(name=":link: Vanity URL", value=f"`{str(vanity).replace('https://discord.gg/', '')}`")
    except:embed.add_field(name=":link: Vanity URL", value=f"`None`")
    embed.add_field(name= f":grinning: Emoji [{emojis}]", value= f"Static: **{emojis - e_gif}**\nAnimated: **{e_gif}**\nStickers: **{len(stickers)}**")
    embed.add_field(name= f":busts_in_silhouette: Members [{guild.member_count}]", 
            value= f"User: **{str(sum(1 for member in guild.members if not member.bot))}** | Bot: **{str(sum(1 for member in guild.members if member.bot))}**\nOnline: **{len(online)}**")
    embed.add_field(name= f":speech_left: Channels [{tchannels+vchannels}]", 
            value= f"Text: **{tchannels}** | Voice: **{vchannels}**\nCategory: **{len(guild.categories)}**",inline= True)
    embed.set_footer(text= f"By: {str(interaction.author)}")
    try:
        req= await bot.http.request(discord.http.Route("GET", "/guilds/{sid}", sid= guild.id))
        banner_id= req["banner"]
        if banner_id:
            banner_url_png= f"https://cdn.discordapp.com/banners/{guild.id}/{banner_id}.png?size=1024"
            banner_url_gif= f"https://cdn.discordapp.com/banners/{guild.id}/{banner_id}.gif?size=1024"
            embed.add_field(name="Banner", value=f"[PNG]({banner_url_png}) | [GIF]({banner_url_gif})")
    except:await interaction.respond(embed=embed, ephemeral = True)
    finally:await interaction.respond(embed=embed, ephemeral = True)

@bot.slash_command(name="memberlist", description="admin only")
async def member_list(interaction, id=None):
    if not int(interaction.author.id) in s.admin_users:
        await interaction.response.send_message("gfy", ephemeral=True)
        return
    if not id:id = interaction.guild.id
    guild = bot.get_guild(int(id))
    with open("TxtList/memberlist.txt", "w", encoding="utf-8") as f:
        f.write(f"TOTAL: {len(guild.members):>7}\n├USER: {str(sum(1 for user in guild.members if not user.bot)):>7}\n└BOT : {str(sum(1 for member in guild.members if member.bot)):>7}\n\nUser only\n")
        [f.write(f"[{user.id:>20} ] {user}\n") for user in guild.members if not user.bot]
    await interaction.response.send_message(file=discord.File("TxtList/memberlist.txt"), ephemeral=True)
    with open("TxtList/botlist.txt", "w", encoding="utf-8") as f:
        f.write("Bot only\n")
        [f.write(f"[{user.id:>20} ] {user}\n")  for user in guild.members if user.bot] #f.write(f"[{user.id:>20} ]  {user}\n") if not user.bot else 
    await interaction.followup.send(file=discord.File("TxtList/botlist.txt"), ephemeral=True)

@bot.event
async def on_application__command_error(interaction, error):
    await interaction.respond(embed=discord.Embed(description=error, color=0xff0000))

@bot.event
async def on_command_error(ctx, error):
    await ctx.reply(embed=discord.Embed(description=error, color=0xff0000))

bot.run(s.a_token)
