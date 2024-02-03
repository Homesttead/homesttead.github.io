import discord
import asyncio
import json
import random
import os

from keep_alive import keep_alive
keep_alive()

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

class CardassianDowekBot(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.prefix = "!"
        self.coin_data_file = "coin_data.json"
        self.update_interval = 600  # Update every 1 hour (adjust as needed)
        self.dowek_value = 1.0  # Initial Dowek value
        self.up_chance = 65  # Percentage chance for Dowek value to go up
        self.down_chance = 100 - self.up_chance  # Percentage chance for Dowek value to go down

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.load_coin_data()
        asyncio.create_task(self.update_coin_value())

    async def on_message(self, message):
        if self.user == message.author:
            return

        if message.content.lower().startswith(f"{self.prefix}value"):
            await self.show_current_value(message.channel)

    async def update_coin_value(self):
        while True:
            await asyncio.sleep(self.update_interval)
            
            # Randomly determine whether Dowek value goes up or down
            if random.randint(1, 100) <= self.up_chance:
                # Dowek value goes up
                self.dowek_value *= 1 + (random.uniform(0, 10) / 100)
            else:
                # Dowek value goes down
                self.dowek_value *= 1 - (random.uniform(0, 10) / 100)

            await self.save_coin_data()
            print(f"Updated coin values - Dowek: {self.dowek_value:.2f}₡")

    async def load_coin_data(self):
        try:
            with open(self.coin_data_file, "r") as file:
                data = json.load(file)
                self.dowek_value = data.get("dowek_value", 1.0)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            print("Coin data file not found or invalid. Using default values.")

    async def save_coin_data(self):
        data = {"dowek_value": self.dowek_value}
        with open(self.coin_data_file, "w") as file:
            json.dump(data, file)

    async def show_current_value(self, channel):
        await channel.send(f"**Current Value:** 1.00$ = {self.dowek_value:.2f}₡")

token = os.environ.get('TOKEN')

# Your bot instance
bot = CardassianDowekBot(intents=intents)
bot.run(token)
