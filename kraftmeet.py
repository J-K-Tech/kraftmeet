import discord
from discord import *

class client(discord.Client):
    APPID=000000000000000000000000000000000000000000
    async def on_ready(self):
        pass


    async def on_message(self,message:Message):
        game=message.content.split(" ")
        cl=await self.fetch_channel(message.channel.id)
        gl=await self.fetch_guild(message.guild.id)
        if game[0]=="]m":
            e=""
            for i in gl.roles:
                if i.name==game[1]:
                    e=i.mention
            mms="***"+message.author.mention+"*** wants to play ***"+(e,game[1])[e==""]+"***\n\n\nusers: "+message.author.mention
            nick=game[1]+" session with "+(message.author.nick or message.author.global_name)
            msg=await cl.send(mms)
            await msg.add_reaction('👍')
            await msg.add_reaction('❌')
            tr:Thread= await msg.create_thread(name=nick)
            await message.delete()


    async def on_raw_reaction_add(self,payload:RawReactionActionEvent):
        
        channel = await self.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.fetch_user(payload.user_id)
        creatorid=message.content.split("*** wants")[0].replace("***<@","").replace(">","")
        if message.author.id==self.APPID and not user.id==self.APPID:
            
            if payload.emoji.name=='👍':
                smu=message.content.split("users: ")[1]
                if not user.mention in smu.split(" "):
                    await message.edit(content=(message.content+" "+user.mention))
                    
                    thread = await self.fetch_channel(payload.message_id)
                    await thread.send(user.mention+" joined the match "+smu)
            elif payload.emoji.name=='❌' and str(user.id)==creatorid:
                await message.edit(content=("CLOSED\n\n"+message.content+"\n\nCLOSED"))
                
                thread = await self.fetch_channel(payload.message_id)
                await thread.delete()
                
      
token="token here"
iii=Intents.none()
iii.guild_messages=True
iii.message_content=True
iii.guild_reactions=True
bote= client(intents=iii)      
bote.run(token)
