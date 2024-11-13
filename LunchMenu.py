import discord
import requests
from bs4 import BeautifulSoup

TOKEN = 'Discord Bot Token'

def crawl_data():
    url = "https://www.daejin.ac.kr/daejin/6396/subview.do"  
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    data = []
    days = ['월', '화', '수', '목', '금', '토', '일']

    current_meal_type = None

    meal_rows = soup.find_all('tr')[1:] 

    for meal_row in meal_rows:
        th = meal_row.find('th')
        if th:
            current_meal_type = th.get_text(strip=True)
            row_data = [f"[{current_meal_type}]"]
            td_elements = meal_row.find_all('td')
            for i, td in enumerate(td_elements):
                meal_content = td.get_text(separator=' ', strip=True)
                if i < len(days): 
                    row_data.append(f"{days[i]}: {meal_content}")  
            data.append(row_data)
        else:
            row_data = [f"[{current_meal_type}]"]
            td_elements = meal_row.find_all('td')
            for i, td in enumerate(td_elements):
                meal_content = td.get_text(separator=' ', strip=True)
                if i < len(days):  
                    row_data.append(f"{days[i]}: {meal_content}")  
            data.append(row_data)

    return data

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == '!lunch':
        table = crawl_data()
        response_message = ""
        for row in table:
            formatted_row = ' \n '.join(row)  
            response_message += formatted_row + '\n'  
        await message.channel.send(response_message)  

bot.run(TOKEN)
