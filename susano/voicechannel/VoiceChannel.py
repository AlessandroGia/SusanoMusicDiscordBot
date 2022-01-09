from discord import FFmpegOpusAudio
from discord.ext import commands
from discord.ext import tasks
from discord_slash import SlashContext
from youtube_dl import YoutubeDL

from .Coda import Coda

from susano.voicechannel.HandlerTimeOutBot import HandlerTimeOutBot
import susano.exceptions.Exceptions as Exc

import asyncio
import discord
import requests


class VoiceChannel:

    def __init__(self, bot: commands.Bot) -> None:
        self.FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                            'options': '-vn'}
        self.nome = "susano"
        self.immagine = "https://webcdn.hirezstudios.com/smite/god-icons/susano.jpg"

        self.bot = bot
        self.HTOB = HandlerTimeOutBot()

        self.timeoutbot.start()

    @tasks.loop(seconds=300)
    async def timeoutbot(self):
        await self.HTOB.checkAFK()

    @timeoutbot.before_loop
    async def before_timeoutbot(self):
        await self.bot.wait_until_ready()

    @staticmethod
    def __getChannel(ctx: SlashContext) -> discord.VoiceClient:
        return discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    @staticmethod
    def __getGuildId(ctx: SlashContext) -> int:
        return ctx.guild.id

    @staticmethod
    def __check(ctx: SlashContext, vc: discord.VoiceClient) -> None:

        if not ctx.author.voice:
            raise Exc.UserNonConnessoError

        if not vc:
            raise Exc.BotNonPresenteError

        if not ctx.author.voice.channel == ctx.voice_client.channel:
            raise Exc.UserNonNelloStessoCanaleError

    @staticmethod
    def __search(link: str) -> [dict, str]:
        with YoutubeDL({'format': 'bestaudio', 'noplaylist': 'true'}) as ydl:
            try:
                requests.get(link)
            except:
                info = ydl.extract_info(f"ytsearch:{link}", download=False)['entries'][0]
            else:
                info = ydl.extract_info(link, download=False)

        return info

    def __titoloLink(self, link):
        info = self.__search(link)
        return info['title']

    def __inRiproduzione(self, nome: str) -> discord.Embed:
        embed = discord.Embed(title='', description="Riproducendo - " + "**" + nome + "**",
                              colour=discord.Colour.blue())
        embed.set_author(name=self.nome, icon_url=self.immagine)
        return embed

    def __inCoda(self, title: str, pos: int) -> discord.Embed:
        embed = discord.Embed(title='', description="**" + title + "** - aggiunta alla coda: " + str(pos),
                              colour=discord.Colour.blue())
        embed.set_author(name=self.nome, icon_url=self.immagine)
        return embed

    async def __playSong(self, vc: discord.VoiceClient, song: str) -> None:
        source = await FFmpegOpusAudio.from_probe(song, **self.FFMPEG_OPTS)
        vc.play(source)

    def __init(self, ctx: SlashContext):
        vc = self.__getChannel(ctx)
        self.__check(ctx, vc)
        self.HTOB.channelUp(vc)
        idg = self.__getGuildId(ctx)
        return vc, idg

    ##

    async def connect(self, ctx: SlashContext, coda: Coda) -> None:

        if not ctx.author.voice:
            raise Exc.UserNonConnessoError

        if self.__getChannel(ctx):
            raise Exc.BotPresenteError

        await ctx.author.voice.channel.connect()
        self.HTOB.channelUp(self.__getChannel(ctx))
        coda.createQueue(self.__getGuildId(ctx))

    async def disconnect(self, ctx: SlashContext) -> None:

        vc, idguild = self.__init(ctx)
        await vc.disconnect()

    ##

    async def play(self, ctx: SlashContext, url: str, coda: Coda) -> None:

        vc, idg = self.__init(ctx)

        if coda.isEmpty(idg) and not (vc.is_playing() or vc.is_paused()):
            coda.put(idg, url)
            await self.playerhandler(ctx, vc, coda, idg)
        else:
            await ctx.send(embed=self.__inCoda(self.__titoloLink(url), coda.size(idg) + 1))
            coda.put(idg, url)

    async def playerhandler(self, ctx: SlashContext, vc: discord.VoiceClient, coda: Coda, idg: int) -> None:
        while not coda.isEmpty(idg):
            url = coda.get(idg)
            info = self.__search(url)
            await ctx.send(embed=self.__inRiproduzione(info['title']))
            await self.__playSong(vc, info['formats'][0]['url'])
            while vc.is_playing() or vc.is_paused():
                await asyncio.sleep(0.5)

    async def skip(self, ctx: SlashContext, coda: Coda) -> None:

        vc, idg = self.__init(ctx)

        if coda.isEmpty(idg):
            raise Exc.CanzoniNonInCodaError

        vc.stop()

    async def pause(self, ctx: SlashContext) -> None:

        vc, idg = self.__init(ctx)

        if not vc.is_playing():
            raise Exc.BotNonInRiproduzione

        vc.pause()

    async def resume(self, ctx: SlashContext) -> None:

        vc, idg = self.__init(ctx)

        if not vc.is_paused():
            raise Exc.BotNonInPausaError

        vc.resume()

    async def reset(self, ctx: SlashContext, coda: Coda) -> None:

        vc, idg = self.__init(ctx)

        if coda.isEmpty(idg):
            raise Exc.CodaVuota

        coda.clear(idg)
        vc.stop()
