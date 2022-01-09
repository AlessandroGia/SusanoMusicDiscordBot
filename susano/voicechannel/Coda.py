from queue import Queue

from susano.exceptions.CodaVuotaError import CodaVuotaError


class Coda:

    def __init__(self) -> None:
        self.queue = "queue"
        self.loop = "loop"
        self.current_song = "current_song"
        self.coda = {}

    def createQueue(self, idg: int) -> None:
        # self.coda[idg] = [0, Queue()]

        self.coda[idg] = {}
        self.coda[idg][self.queue] = Queue()
        self.coda[idg][self.current_song] = ""
        self.coda[idg][self.loop] = False

    def setLoop(self, idg: int, loop: bool):
        self.coda[idg][self.loop] = loop

    def getLoop(self, idg: int):
        return self.coda[idg][self.loop]

    def put(self, idg: int, link: str) -> None:
        self.coda[idg][self.queue].put(link)

    def get(self, idg: int) -> str:
        if self.coda[idg][self.queue].empty() and not self.coda[idg][self.queue]:
            raise CodaVuotaError

        if not self.coda[idg][self.loop]:
            self.coda[idg][self.current_song] = self.coda[idg][self.queue].get()
            return self.coda[idg][self.current_song]
        else:
            self.coda[idg][self.queue].put(self.coda[idg][self.current_song])
            self.coda[idg][self.current_song] = self.coda[idg][self.queue].get()
            return self.coda[idg][self.current_song]

    def isEmpty(self, idg: int) -> bool:
        return self.coda[idg][self.queue].empty()

    def size(self, idg: int) -> int:
        return self.coda[idg][self.queue].qsize()

    def clear(self, idg: int) -> None:
        while not self.coda[idg][self.queue].empty():
            self.coda[idg][self.queue].get()
