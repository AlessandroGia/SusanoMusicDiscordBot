import os


class Servers:

    def __init__(self) -> None:
        self.FILE = "servers.txt"

    @staticmethod
    def currentDirectory() -> str:
        return os.path.dirname(os.path.abspath(__file__))

    def aggiungiServer(self, idg: int) -> None:

        currdir = self.currentDirectory()
        servers = self.getServers()

        if idg not in servers:
            servers.append(idg)

        with open(currdir + os.sep + self.FILE, 'w') as file:
            for server in servers:
                file.write('%s\n' % server)

    def getServers(self) -> list:

        currdir = self.currentDirectory()
        servers = []

        if not os.path.isfile(currdir + os.sep + self.FILE):
            file = open(currdir + os.sep + self.FILE, 'w+')
            file.close()
        else:
            with open(currdir + os.sep + self.FILE, 'r') as files:
                for file in files:
                    servers.append(int(file[:-1]))

        return servers
