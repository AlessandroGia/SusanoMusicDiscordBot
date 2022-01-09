import discord


class HandlerTimeOutBot:

    def __init__(self):
        self.channels = {}

    def channelUp(self, vc: discord.VoiceClient) -> None:
        self.channels[vc] = 1

    def removeChannel(self, vc: discord.VoiceClient) -> None:
        del(self.channels[vc])

    async def checkAFK(self) -> None:
        # print(self.channels)
        for channel in self.channels.keys():
            if not self.channels[channel]:
                if channel.is_connected():
                    await channel.disconnect()
            else:
                if not channel.is_playing():
                    self.channels[channel] = 0
