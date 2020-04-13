import os
from dotenv import load_dotenv
import discord
import random


class Bot(discord.Client):
    def __init__(self):
        super().__init__()

    def wordlist(self):
        try:
            with open("wordlist.txt") as f:
                file = f.read()
        except:
            raise
        return random.choice([ x.strip() for x in file.split('\n') if x.strip() != '' ])


    async def on_ready(self):
        """docstring for on_ready"""
        print('Logged in as : ')
        print(self.user.name)
        print(self.user.id)
        print('-------')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        members = [x for x in message.guild.members if ( x.bot ==False and x.status == discord.Status.online) ]
        ##members = [x for x in message.guild.members if ( x.bot ==False ) ]
        members = random.sample(members, len(members))

        if message.content.startswith('!startgame'):

            if len(members)<2:
                await message.channel.send('Vous ne pouvez pas jouer seul-e.')
                return
            try:
                secretcode = self.wordlist() 
            except FileNotFoundError: 
                await message.channel.send(f"Aucune liste de mot n'est définie pour le bot.")
                return

            
            ordre_de_passage = 'Voici le nouvel ordre de passage : \n'
            for key, member in enumerate( members ): 
                ordre_de_passage+=f"{key+1} - {member.name} \n"

            await message.channel.send(ordre_de_passage)

            misterwhite = random.choice(members[1:])
            for member in members:
                if member == misterwhite:
                    ##await message.channel.send(f"{member.name} est mister white")
                    await member.send("Vous êtes Mr-s. White")
                else:
                    ##await message.channel.send(f"{member.name} a eu le mot {secretcode}")
                    await member.send(f"{message.guild.name} : {secretcode} est votre code secret")

if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot = Bot()
    bot.run(TOKEN)
