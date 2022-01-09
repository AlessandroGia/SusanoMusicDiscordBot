from discord.ext import commands
from dotenv import load_dotenv
from discord_slash import SlashCommand
# from susano.servers.Servers import Servers

import discord
import os


class Susanoo:

    def __init__(self) -> None:

        # self.__servers = Servers()

        self.intents = discord.Intents.default()
        self.__setintents()

        load_dotenv()
        self.__token = os.getenv('DISCORD_TOKEN')

        self.__bot = commands.Bot(command_prefix="!", self_bot=True, help_command=None,  intents=self.intents)
        self.slash = SlashCommand(self.__bot, sync_commands=True)

    def __setintents(self) -> None:
        self.intents.members = True
        self.intents.presences = True

    def run(self) -> None:

        @self.__bot.event
        async def on_ready() -> None:
            print("Bot avviato")

        # @self.__bot.event
        # async def on_guild_join(guild: discord.Guild) -> None:
            # self.__servers.aggiungiServer(guild.id)

        @self.__bot.event
        async def on_voice_state_update(member: discord.Member, before: discord.VoiceState,
                                        after: discord.VoiceState) -> None:
            idchannels = [x.channel.id for x in self.__bot.voice_clients]

            if before.channel and before.channel.id in idchannels:
                if len(before.channel.members) == 1:
                    vc = self.__bot.voice_clients[idchannels.index(before.channel.id)]
                    await vc.disconnect()

        @commands.command()
        async def load(ctx, ext: str):
            self.__bot.load_extension(f'susano.cogs.{ext}')

        @commands.command()
        async def unload(ctx, ext: str):
            self.__bot.unload_extension(f'susano.cogs.{ext}')

        @commands.command()
        async def reload(ctx, ext: str):
            self.__bot.unload_extension(f'susano.cogs.{ext}')
            self.__bot.load_extension(f'susano.cogs.{ext}')

        for fileName in os.listdir("susano" + os.sep + "cogs"):
            if fileName.endswith('py') and fileName != "__init__.py":
                self.__bot.load_extension(f'susano.cogs.{fileName[:-3]}')

        self.__bot.run(self.__token)


if __name__ == '__main__':
    sus = Susanoo()
    sus.run()
