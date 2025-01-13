from observerAbstract import Observer, Subject
from alpaca import alpaca

class alpacaObserver(Observer):
    """
    Concrete Observers react to the updates issued by the Subject they had been attached to.
    """
    def __init__(self, symbol, qty, side, type, time_in_force):
        self.symbol = symbol
        self.qty = qty
        self.side = side    
        self.type = type    
        self.time_in_force = time_in_force

    def update(self, subject: Subject) -> None:
        if subject.action == "buy":
            print("alpacaObserver: Reacting to buy event")
            alpaca.create_order(self.symbol, self.qty, self.side, self.type, self.time_in_force)
        if subject.action == "sell":
            print("alpacaObserver: Reacting to sell event")
            alpaca.create_order(self.symbol, self.qty, self.side, self.type, self.time_in_force)