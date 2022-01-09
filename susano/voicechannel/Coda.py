from queue import Queue

from susano.exceptions.CodaVuota import CodaVuota


class Coda:

    def __init__(self) -> None:
        self.coda = {}

    def createQueue(self, idg: int) -> None:
        self.coda[idg] = Queue()

    def put(self, idg: int, link: str) -> None:
        self.coda[idg].put(link)

    def get(self, idg: int) -> str:
        if self.coda[idg].empty():
            raise CodaVuota
        return self.coda[idg].get()

    def isEmpty(self, idg: int) -> bool:
        return self.coda[idg].empty()

    def size(self, idg: int) -> int:
        return self.coda[idg].qsize()

    def clear(self, idg: int) -> None:
        while not self.coda[idg].empty():
            self.coda[idg].get()
