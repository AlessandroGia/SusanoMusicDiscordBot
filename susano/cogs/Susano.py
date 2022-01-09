from susano.voicechannel.VoiceChannel import VoiceChannel
from susano.voicechannel.Coda import Coda
from susano.servers.Servers import Servers
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord.ext import commands

import susano.exceptions.Exceptions as Exc

import discord


class Susano(commands.Cog):

    servers = Servers()

    def __init__(self, bot: commands.Bot) -> None:
        self.nome = "susano"
        self.immagine = "https://webcdn.hirezstudios.com/smite/god-icons/susano.jpg"
        self.bot = bot

        self.red = discord.Colour.red()
        self.blue = discord.Colour.blue()

        self.voiceChannel = VoiceChannel(bot)
        self.coda = Coda()

    def embed(self, mess: str, color: discord.Colour) -> discord.Embed:
        embed = discord.Embed(title="", description=mess, colour=color)
        embed.set_author(name=self.nome, icon_url=self.immagine)
        return embed

    # Join
    @cog_ext.cog_slash(
        name="join",
        description="Consente al bot di entrare nel canale vocale",
        guild_ids=servers.getServers()
    )
    async def _join(self, ctx: SlashContext) -> None:
        try:
            await self.voiceChannel.connect(ctx, self.coda)
            await ctx.send(embed=self.embed("Bot entrato nel canale vocale", self.blue))
        except Exc.UserNonConnessoError:
            await ctx.send(embed=self.embed("Non sei connesso a nessun canale vocale", self.red))
        except Exc.BotPresenteError:
            await ctx.send(embed=self.embed("Il bot e' gia presente nel canale vocale", self.red))
        except Exception as e:
            await ctx.send(embed=self.embed(str(e), self.red))


    # Leave
    @cog_ext.cog_slash(
        name="leave",
        description="Consente al bot di uscire dal canale vocale",
        guild_ids=servers.getServers()
    )
    async def _leave(self, ctx: SlashContext) -> None:
        try:
            await self.voiceChannel.disconnect(ctx)
            await ctx.send(embed=self.embed('Bot uscito dal canale vocale', self.blue))
        except Exc.UserNonConnessoError:
            await ctx.send(embed=self.embed("Non sei connesso a nessun canale vocale", self.red))
        except Exc.BotNonPresenteError:
            await ctx.send(embed=self.embed("Il bot non e' presente nel canale vocale", self.red))
        except Exc.UserNonNelloStessoCanaleError:
            await ctx.send(embed=self.embed("Non sei connesso nello stesso canale vocale del bot", self.red))
        except Exception as e:
            await ctx.send(embed=self.embed("Si e' verificato un errore", self.red))
            print(e.args)

    # Play
    @cog_ext.cog_slash(
        name="play",
        description="Riproduci canzone",
        guild_ids=servers.getServers(),
        options=[
            create_option(
                name="input",
                description="Inserisci il link della canzone",
                required=True,
                option_type=3,
            )
        ]
    )
    async def _play(self, ctx: SlashContext, input: str) -> None:
        try:
            await self.voiceChannel.play(ctx, input, self.coda)
        except Exc.UserNonConnessoError:
            await ctx.send(embed=self.embed("Non sei connesso a nessun canale vocale", self.red))
        except Exc.BotNonPresenteError:
            await ctx.send(embed=self.embed("Il bot non e' presente nel canale vocale", self.red))
        except Exc.UserNonNelloStessoCanaleError:
            await ctx.send(embed=self.embed("Non sei connesso nello stesso canale vocale del bot", self.red))
        except Exception as e:
            print(e.args)
            # await ctx.send(embed=self.embed("Si e' verificato un errore", self.red))
            await ctx.send(embed=self.embed(e.args, self.red))
            print(e.args)

    # Skip
    @cog_ext.cog_slash(
        name="skip",
        description="Riproduce la canzone seguente",
        guild_ids=servers.getServers(),
    )
    async def _skip(self, ctx: SlashContext) -> None:
        try:
            await self.voiceChannel.skip(ctx, self.coda)
            await ctx.send(embed=discord.Embed(title='', description='Canzone skippata', colour=discord.Colour.blue()))
        except Exc.UserNonConnessoError:
            await ctx.send(embed=self.embed("Non sei connesso a nessun canale vocale", self.red))
        except Exc.BotNonPresenteError:
            await ctx.send(embed=self.embed("Il bot non e' presente nel canale vocale", self.red))
        except Exc.UserNonNelloStessoCanaleError:
            await ctx.send(embed=self.embed("Non sei connesso nello stesso canale vocale del bot", self.red))
        except Exc.CanzoniNonInCodaError:
            await ctx.send(embed=self.embed('Non ci sono canzoni in coda', self.red))
        except Exception as e:
            await ctx.send(embed=self.embed("Si e' verificato un errore", self.red))
            print(e.args)

    # Pause
    @cog_ext.cog_slash(
        name="pause",
        description="Ferma canzone",
        guild_ids=servers.getServers(),
    )
    async def _pause(self, ctx: SlashContext) -> None:
        try:
            await self.voiceChannel.pause(ctx)
            await ctx.send(embed=self.embed('Riproduzione fermata', self.blue))
        except Exc.UserNonConnessoError:
            await ctx.send(embed=self.embed("Non sei connesso a nessun canale vocale", self.red))
        except Exc.BotNonPresenteError:
            await ctx.send(embed=self.embed("Il bot non e' presente nel canale vocale", self.red))
        except Exc.UserNonNelloStessoCanaleError:
            await ctx.send(embed=self.embed("Non sei connesso nello stesso canale vocale del bot", self.red))
        except Exc.BotNonInRiproduzione:
            await ctx.send(embed=self.embed('Il bot non sta riproducendo nessuna canzone', self.red))
        except Exception as e:
            await ctx.send(embed=self.embed("Si e' verificato un errore", self.red))
            print(e.args)

    # Resume
    @cog_ext.cog_slash(
        name="resume",
        description="Riprende la canzone messa in pausa",
        guild_ids=servers.getServers()
    )
    async def _resume(self, ctx: SlashContext) -> None:
        try:
            await self.voiceChannel.resume(ctx)
            await ctx.send(embed=self.embed('Riproduzione ripresa', self.blue))
        except Exc.UserNonConnessoError:
            await ctx.send(embed=self.embed("Non sei connesso a nessun canale vocale", self.red))
        except Exc.BotNonPresenteError:
            await ctx.send(embed=self.embed("Il bot non e' presente nel canale vocale", self.red))
        except Exc.UserNonNelloStessoCanaleError:
            await ctx.send(embed=self.embed("Non sei connesso nello stesso canale vocale del bot", self.red))
        except Exc.BotNonInPausaError:
            await ctx.send(embed=self.embed("Il bot non e' in pausa", self.red))
        except Exception as e:
            await ctx.send(embed=self.embed("Si e' verificato un errore", self.red))
            print(e.args)

    # Reset
    @cog_ext.cog_slash(
        name="reset",
        description="Ferma la canzone ed elimina la coda",
        guild_ids=servers.getServers()
    )
    async def _reset(self, ctx: SlashContext) -> None:
        try:
            await self.voiceChannel.reset(ctx, self.coda)
            await ctx.send(embed=self.embed('Coda cancellata', self.blue))
        except Exc.UserNonConnessoError:
            await ctx.send(embed=self.embed("Non sei connesso a nessun canale vocale", self.red))
        except Exc.BotNonPresenteError:
            await ctx.send(embed=self.embed("Il bot non e' presente nel canale vocale", self.red))
        except Exc.UserNonNelloStessoCanaleError:
            await ctx.send(embed=self.embed("Non sei connesso nello stesso canale vocale del bot", self.red))
        except Exc.CodaVuotaError:
            await ctx.send(embed=self.embed("La coda e' vuota", self.red))
        except Exception as e:
            await ctx.send(embed=self.embed("Si e' verificato un errore", self.red))
            print(e.args)

    # Loop
    @cog_ext.cog_slash(
        name="loop",
        description="Mette in loop la coda",
        guild_ids=servers.getServers(),
        options=[
            create_option(
                name="input",
                description="Si o No",
                option_type=4,
                required=True,
                choices=[
                    create_choice(
                        name="Si",
                        value=1
                    ),
                    create_choice(
                        name="No",
                        value=0
                    )
                ]
            )
        ]
    )
    async def _loop(self, ctx: SlashContext, input: int):
        if input:
            input = True
            text = "Si"
        else:
            input = False
            text = "No"
        try:
            await self.voiceChannel.loop(ctx, input, self.coda)
            await ctx.send(embed=self.embed("Loop: " + text, self.blue))
        except Exc.UserNonConnessoError:
            await ctx.send(embed=self.embed("Non sei connesso a nessun canale vocale", self.red))
        except Exc.BotNonPresenteError:
            await ctx.send(embed=self.embed("Il bot non e' presente nel canale vocale", self.red))
        except Exc.UserNonNelloStessoCanaleError:
            await ctx.send(embed=self.embed("Non sei connesso nello stesso canale vocale del bot", self.red))
        except Exc.NessunaCanzoneError:
            await ctx.send(embed=self.embed("Il bot non sta riproducendo nessuna canzone", self.red))
        except Exc.LoopGiaImpostatoError:
            await ctx.send(embed=self.embed("Loop gia' impostato su: " + text, self.red))
        except Exception as e:
            await ctx.send(embed=self.embed("Si e' verificato un errore", self.red))
            print(e.args)



def setup(bot) -> None:
    bot.add_cog(Susano(bot))
