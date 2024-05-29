import discord
import requests
from bs4 import BeautifulSoup

# 봇 토큰 설정
TOKEN = ''

# 웹 페이지 크롤링 함수
def crawl_data():
    url = "https://www.daejin.ac.kr/daejin/6396/subview.do"  # 실제 웹 페이지의 URL로 변경해야 합니다.

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    thead = soup.find('thead')
    header_data = [th.text.strip().replace('/', '') for th in thead.find_all('th')]

    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')

    meal_times = ["<아침","<간편식","<한식","<누들송","<크레이지팬","<돈카츠락","<저녁"]
    row_data =  [[meal_time] + [td.text.strip() for td in row.find_all('td')] for meal_time, row in zip(meal_times, rows)]

    table = [header_data] + row_data

    return table

# 봇 클라이언트 생성
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# 봇이 준비되었을 때 동작할 이벤트
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# 메시지 이벤트 처리
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == '!lunch':
        table = crawl_data()
        for i, row in enumerate(table):
            formatted_row = '> \n'.join(row)  # 각 항목을 슬래시(>\n)로 구분하여 문자열로 변환
            await message.channel.send(formatted_row)  # 변환된 문자열을 디스코드 채널에 전송

# 봇 실행
bot.run(TOKEN)
