from observerAbstract import Observer, Subject
from typing import List

class Spender(Subject):

    _observers: List[Observer] = []  
    action: str = ""

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def buy(self) -> None:
        self.action = "buy"
        print("Spender: I'm buying stocks!")
        self.notify()

    def sell(self) -> None:
        self.action = "sell"
        print("Spender: I'm selling stocks!")
        self.notify()