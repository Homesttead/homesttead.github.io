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
        self.update_interval = 60  # Update every 1 hour (adjust as needed)
        self.up_chance = 65  # Percentage chance for Dowek value to inflate
        self.down_chance = 100 - self.up_chance  # Percentage chance for Dowek value to deflate

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        self.dowek_value = await self.load_dowek_value()
        asyncio.create_task(self.update_coin_value())

    async def on_message(self, message):
        if self.user == message.author:
            return

        if message.content.lower().startswith(f"{self.prefix}stats"):
            await self.show_current_value(message.channel)

        await self.process_commands(message)

    async def update_coin_value(self):
        while True:
            await asyncio.sleep(self.update_interval)

            # Randomly determine whether Dowek value goes up or down
            if random.randint(1, 100) <= self.up_chance:
                # Dowek value goes up
                self.dowek_value *= 1 + (random.uniform(0, 4) / 100)
            else:
                # Dowek value goes down
                self.dowek_value *= 1 - (random.uniform(0, 4) / 100)

            await self.save_dowek_value()
            print(f"Updated coin values - Dowek: {self.dowek_value:.2f}₡")

    async def load_dowek_value(self):
        dowek_value = float(os.environ.get('DOWEK_VALUE', 1.0))
        print(f"Loaded Dowek value: {dowek_value:.2f}₡")
        return dowek_value

    async def save_dowek_value(self):
        os.environ['DOWEK_VALUE'] = str(self.dowek_value)
        print(f"Saved Dowek value: {self.dowek_value:.2f}₡")

    async def show_current_value(self, channel):
        await channel.send(f"**Current Value:** 1.00$ = {self.dowek_value:.2f}₡")

token = os.environ.get('TOKEN')

# Your bot instance
bot = CardassianDowekBot(intents=intents)
bot.run(token)
