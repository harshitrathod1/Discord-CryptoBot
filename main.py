import os
import discord
from functions import botFunctions
from keep_alive import keep_alive

client = discord.Client()
bot_funcs = botFunctions()

#Asynchronous Python
@client.event
async def on_ready():
    print("We have Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content

    #Greet the user
    if msg.startswith(('$hello', '$hi', '$hey')):
        await message.channel.send("Hi, " + message.author.name +" what's up :)")

    #get the price. The tuple in the argument contains the alias names
    if msg.startswith(("$price")):
        coin_name = msg.split()[1]
        price_quote = bot_funcs.get_price(coin_name)

        gm = "Current "+coin_name+" price is "

        if (float(price_quote) > 1):
            price_quote = price_quote[0:-5]
            await message.channel.send(gm + price_quote + " " + bot_funcs.default_currency+" 💸💸")
        else:
          await message.channel.send(gm + price_quote+" "+bot_funcs.default_currency+" 💸💸") 

    #Change the default currency
    if msg.startswith("$change"):
        new_currency = msg.split()[1].upper()
        bot_funcs.change_default_currency(new_currency)
        await message.channel.send("Default currency changed Successfully")

    #Get the dominance for a particular cryto
    if msg.startswith(('$dominance','$dom','$percent','$d')):
      dominance_coin = msg.split()[1].upper()
      gm = "The Dominance for "+dominance_coin+" is "

      await message.channel.send(gm + bot_funcs.get_dominance(dominance_coin)+"%")

    #Get the all time high price for a particular coin
    if msg.startswith(('$high','$h','$highestprice')):
      coin_name = msg.split()[1].upper()
      gm = "The Highest price of all time in "+coin_name+" is "
      await message.channel.send(gm + bot_funcs.get_highest_price(coin_name)+" "+bot_funcs.default_currency+" 💰💰")

    #Get the rank for a coin
    if msg.startswith(('$rank','$r')):
      coin_name = msg.split()[1].upper()
      gm = coin_name + " stands at "
      await message.channel.send(gm + bot_funcs.get_rank(coin_name)+" place 🤙🤙")

    #check if bot is running fine
    if msg.startswith('$ping'):
      if(bot_funcs.checkPing()):
        await message.channel.send("Everything is Working fine here :) To the moon 🚀🚀")

    #to get the trending coins of the day
    if msg.startswith('$trending'):
      trending_list = bot_funcs.get_trending_data()
      for item in trending_list:
        head = item['item']['name']
        img = item['item']['small']
        price_in_btc = str(item['item']['price_btc'])
        rank = str(item['item']['market_cap_rank'])
        descp = "Price in BTC :- "+ price_in_btc+"\n Rank :- "+ rank
        embedVar = discord.Embed(title=head,color = 0xff471a,description = descp)
        embedVar.set_image(url = img)
        await message.channel.send(embed = embedVar)

    #to get top k coins by market_cap value
    if msg.startswith('$topmarket'):
      k = int(msg.split()[1])
      if k > 50:
        await message.channel.send("Please enter a number less than 50 🤷‍♂️🤷")
      else:
        top_k = bot_funcs.get_top_k_marketCap(k)
        for item in top_k:
          head = item['name']
          img = item['image']
          price = str(item['current_price'])
          rank = str(item['market_cap_rank'])
          descp = "Price in BTC :- "+ price+" "+bot_funcs.default_currency+"\n Rank :- "+ rank
          embedVar = discord.Embed(title=head,color = 0xff471a,description = descp)
          embedVar.set_image(url = img)
          await message.channel.send(embed = embedVar)

    #to get top k coins by volume in the market 
    if msg.startswith('$topvolume'):
      k = int(msg.split()[1])
      if k > 50:
        await message.channel.send("Please enter a number less than 50 🤷‍♂️🤷")
      else:
        top_k = bot_funcs.get_top_k_volume(k)
        for item in top_k:
          head = item['name']
          img = item['image']
          price = str(item['current_price'])
          rank = str(item['market_cap_rank'])
          descp = "Price in BTC :- "+ price+" "+bot_funcs.default_currency+"\n Rank :- "+ rank
          embedVar = discord.Embed(title=head,color = 0xff471a,description = descp)
          embedVar.set_image(url = img)
          await message.channel.send(embed = embedVar)

    #to get the commands list for the bot
    if msg.startswith("$cmd"):
      cmds = bot_funcs.get_command_info()
      embedVar = discord.Embed(title = "Here are BOT commands",description= cmds)
      await message.channel.send(embed = embedVar)


#Start the bot 
keep_alive()
my_secret = os.getenv('TOKEN')
client.run(my_secret)