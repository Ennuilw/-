import setting as s
import discord,dateutil.parser,random,datetime,spotipy,aiohttp,time,asyncio
from discord.ext import commands
from discord.ext.ui import *
from discord.commands import Option
from spotipy.oauth2 import SpotifyClientCredentials
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=",", intents=discord.Intents.all())
        
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

@bot.slash_command(name="about", description="About this bot")
async def about(interaction):
    user= bot.get_user(901518724098568223)
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
    url = avatar.url
    embed= discord.Embed(description= f"> {user.mention} Avatar\n> **[URL]({url})**",color= 0x6dc1d1).set_image(url= avatar).set_footer(text= f"By: {str(ctx.author)}")
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
        song_title = track['name']
        if "[" and "]" in song_title:song_title = song_title.translate(str.maketrans({"[":"(", "[":")"}))
        if len(song_title) > 20:song_title = str(song_title[0:20] + "... ")
        if len(track['album']['name']) > 15:repl_song_album = str(track['album']['name'][0:15] + "...")
        else:repl_song_album=track['album']['name']
        sp_str.append(f"<:Icon_jumptourl:1007535375033581588> **[{song_title}]({song_url}) - {track['artists'][0]['name']} |** {repl_song_album}")
    await interaction.response.send_message(embed=discord.Embed(description= "\n\n".join(sp_str),color=s.s_c).set_footer(text="Layout: Title - Artists | Album"))


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
async def serverinfo(interaction):
    guild = interaction.guild
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
    finally:
        embed.add_field(name="Splash", value=f"[PNG]({interaction.guild.splash})")
        await interaction.respond(embed=embed)


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

@bot.slash_command(name="nuke", description="チャンネルを再作成")
@commands.has_permissions(administrator=True)
async def delete(interaction, channel:discord.TextChannel=None):
    if not channel:channel=interaction.channel
    else:channel = discord.utils.get(interaction.guild.channels, name=channel.name)
    pos = channel.position
    await channel.delete()
    new_channel = await channel.clone()
    await new_channel.edit(position=pos)

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
                f.write(f"SUCCESS [{guild.id:>20} ] {guild}\n")
                count += 1
            except: f.write(f"FAILURE [{guild.id:>20} ] {guild}\n")
    e = discord.Embed(description=f"Name: **{member}**\nID: **{member.id}**", color=0xff0000)
    e.add_field(name=f"Global BAN Result",value=f"Success: **{count:<4}**\nFailure: **{len(bot.guilds) - count}**").add_field(name="Reason", value=f"```{reason}```",inline=False)
    await msg_1.edit_original_message(content=None, embed=e)
    await interaction.respond(file=discord.File("TxtList/result.txt", filename="GbanResult.txt"), ephemeral=True)


@bot.slash_command(name="botinserver", description="管理者専用")
async def inserver(interaction:discord.Interaction):
    if not int(interaction.author.id) in s.admin_users:
        await interaction.response.send_message("gfy")
        return
    with open("TxtList/server.txt", "w", encoding='utf-8') as f:
        [f.write(f"[{str(guild.id):>20} ] {guild.name}\n") for guild in bot.guilds]
    await interaction.response.send_message(file=discord.File("TxtList/server.txt", filename="ServerList.txt"), ephemeral=True)



@bot.slash_command(name="invitesplash", description="サーバーの招待背景を表示")
async def invite_splash(ctx):
    try:await ctx.respond(embed=discord.Embed(color= 0x6dc1d1).set_image(url=ctx.guild.splash))
    except:await ctx.respond("ERROR")


@bot.slash_command(name="inserver", description="管理者専用", guild_ids=[941978430206009394])
async def inserver(interaction:discord.Interaction):
    if not int(interaction.author.id) in s.admin_users:return
    with open("TxtList/server.txt", "w", encoding='utf-8') as f:
        f.write(f"{str(len(bot.guilds))}")
        for guild in bot.guilds:f.write(f"[{str(guild.id)}] {guild.name}\n")
    await interaction.response.send_message(file=discord.File("TxtList/server.txt", filename="ServerList.txt"), ephemeral=True)

@bot.slash_command(name="xserver", description="server idを入れてね!このボットが入ってるサーバーの情報を取得")
async def xserver(interaction, id):
    if not int(interaction.author.id) in s.admin_users:return
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
    try: embed.add_field(name=":link: Vanity URL", value=f"`{str(await guild.vanity_invite()).replace('https://discord.gg/', '')}`")
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
    finally:
        embed.add_field(name="Splash", value=f"[PNG]({guild.splash})")
        await interaction.respond(embed=embed, ephemeral=True)

@bot.slash_command(name="memberlist", description="admin only")
async def member_list(interaction, id=None):
    if not int(interaction.author.id) in s.admin_users:return
    if not id:id = interaction.guild.id
    guild = bot.get_guild(int(id))
    with open("TxtList/memberlist.txt", "w", encoding="utf-8") as f:
        f.write(f"TOTAL: {len(guild.members):>7}\n├USER: {str(sum(1 for user in guild.members if not user.bot)):>7}\n└BOT : {str(sum(1 for member in guild.members if member.bot)):>7}\n\nUser only\n")
        [f.write(f"{user.id:>19}  {user}\n") for user in guild.members if not user.bot]
    await interaction.response.send_message(file=discord.File("TxtList/memberlist.txt"), ephemeral=True)
    with open("TxtList/botlist.txt", "w", encoding="utf-8") as f:
        f.write("Bot only\n")
        [f.write(f"[{user.id:>20} ] {user}\n")  for user in guild.members if user.bot] #f.write(f"[{user.id:>20} ]  {user}\n") if not user.bot else 
    await interaction.followup.send(file=discord.File("TxtList/botlist.txt"), ephemeral=True)

bot.run("MTAxOTAzMzQxMDE1NDUzMjkyOA.Gg3D0E.7DfcizBGlwD3a3cP-Jm2JLJyZrMBPJ_4IFHtbo")