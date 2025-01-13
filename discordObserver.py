import os
from observerAbstract import Observer, Subject
from discord import bot
from dotenv import load_dotenv

load_dotenv()
webhook_url = os.getenv('WEBHOOK_URL')

class discordObserver(Observer):
    """
    Concrete Observers react to the updates issued by the Subject they had been attached to.
    """
    def update(self, subject: Subject) -> None:
        if subject.action == "buy":
            message = "DiscordObserver: Reacting to buy event"
            print(message)
            bot.send_message(message, webhook_url)
        if subject.action == "sell":
            message = "DiscordObserver: Reacting to sell event"
            print(message)
            bot.send_message(message, webhook_url)