import os
import requests
import json

class botFunctions:
  default_prefix = "$"
  url = ""
  main_link = "https://api.nomics.com/v1/currencies/ticker?key=" + os.getenv('API KEY') + "&ids="
  default_coin = "BTC"
  default_time_interval = "&interval=1H"
  curr = "&convert="
  default_currency = "USD"
  pagination = "&per-page=100&page=1"

  #aggregating similar parts
  currency_part = curr + default_currency + pagination

  #url
  url = main_link + default_coin + default_time_interval + curr + default_currency + pagination

  gecko_url = "https://api.coingecko.com/api/v3"

  def get_price(self,coin_name):
    new_coin = coin_name.upper()
    new_url = self.main_link + new_coin + self.default_time_interval + self.currency_part
    response = requests.get(new_url)
    json_data = json.loads(response.text)
    price = json_data[0]['price']
    return price

  def change_default_currency(self,new_currency):
    self.default_currency = new_currency #Already in capital
    self.currency_part = self.curr + self.default_currency + self.pagination


  def get_dominance(self,coin_name):
    coin_name = coin_name.upper()
    new_url = self.main_link + coin_name + self.default_time_interval + self.currency_part
    response = requests.get(new_url)
    json_data = json.loads(response.text)
    dominance = float(json_data[0]['market_cap_dominance'])
    dominance = round(dominance * 100,3)
    if dominance == 0.000:
      return "Less than 0.0001"
    return str(dominance)

  def get_highest_price(self,coin_name):
    coin_name = coin_name.upper()
    new_url = self.main_link + coin_name + self.default_time_interval + self.currency_part
    response = requests.get(new_url)
    json_data = json.loads(response.text)
    highest_price = json_data[0]['high']
    return highest_price

  def get_rank(self,coin_name):
    coin_name = coin_name.upper()
    new_url = self.main_link + coin_name + self.default_time_interval + self.currency_part
    response = requests.get(new_url)
    json_data = json.loads(response.text)
    rank = json_data[0]['rank']
    return rank

  def checkPing(self):
    new_url = self.url
    response = requests.get(new_url)
    json_data = json.loads(response.text)
    
    new_url_2 = self.gecko_url + "/ping"
    response2 = requests.get(new_url_2)
    json_data_2 = json.loads(response2.text)

    if len(json_data) and len(json_data_2) == 0 :
      return False

    return True

  def getFullName(self,coin_name):
    new_coin = coin_name.upper()
    new_url = self.main_link + new_coin + self.default_time_interval + self.currency_part
    response = requests.get(new_url)
    json_data = json.loads(response.text)
    name = json_data[0]['name']
    return name
    

  def get_trending_data(self):
    new_url = self.gecko_url + "/search/trending"
    response = requests.get(new_url)
    json_data = json.loads(response.text)
    trending_list = json_data['coins']
    
    return trending_list

  def get_top_k_marketCap(self,k):
    url = self.gecko_url + "/coins/markets?vs_currency="+self.default_currency+"&order=market_cap_desc&per_page="+ str(k) +"&page=1&sparkline=false"
    response = requests.get(url)
    json_data = json.loads(response.text)
    
    return json_data

  def get_top_k_volume(self,k):
    url = self.gecko_url + "/coins/markets?vs_currency="+self.default_currency+"&order=volume_desc&per_page="+ str(k) +"&page=1&sparkline=false"
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data
#----------------------------------XXX----------------------------------------

  command_text = """1. '$hello' :- Greetings from the bot.
 Alias :- '$hi','$hey'

2. '$price ticker' :- To get current price of the ticker.
Here ticker is short form of the crypto for which you want to get the price.
For ex :- Ticker for Bitcoin is 'BTC' not 'bitcoin'
Some common tickers : ['BTC','ETH','DOGE','XRP','SOL','MATIC']

3. '$change currency' :- To convert the currency in which you want to see the results. By default it is 'USD' (United states Dollar)
NOTE :- Use standard shortform to change the default currency.
Some common standard Shortforms for currencies : ['USD','INR','EUR','AUD']

4. '$dominance ticker' :- To get the dominance for the particular ticker.
Dominance :- A measure of particular crytocurrency's value in the context of the larger cryptocurrency market. Given in percentage.
 Alias :- '$dom','$d','$percent'

5. '$high ticker' :- To get the highest price of all time for a particular ticker. Again ticker here is the standard shortform for the particular cryptocurrency. Ex :- 'BTC','ETH','XRP'
Alias : '$h','$highestprice'

6. "$rank ticker" :- To get the current market rank of the ticker.Again ticker here is the standard shortform for the particular cryptocurrency. Ex :- 'BTC','ETH','XRP'
 Alias : '$r'

7. '$ping' :- To check the running status of the bot.

8. '$trending' :- To get the top trending coins of the day.(MAX : 7 coins)

9. '$topmarket k' :- To get the top "k" coins by market capitalisation.
Here k is any integer between 1 and 50(inclusive)

10. '$topvolume k' :- To get the top "k" coins by market Volume. 
Here k is any integer between 1 and 50(inclusive) 

11. "$cmd" : To get all commands on the discord """

  def get_command_info(self):
    return self.command_text
