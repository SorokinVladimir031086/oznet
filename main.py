#!/usr/bin/python
# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
import telebot
import schedule
import time
from selenium import webdriver
import os


url = "https://betwinner.com/live/Football/"
lis = []
lis1 = []
lis2 = []
TOKEN = '1260366546:AAHmSnNqjDUBfpQwr2D4mTpZKG9_4o4dVUw'
bot = telebot.TeleBot(TOKEN)
op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("--headless")
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(executable_path= os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)

def main():
    try:
        driver.get(url)
        time.sleep(5)
        main_page = driver.current_window_handle
        html = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        print(e)
    matches = html.find_all('div', class_='c-events__item c-events__item_game c-events-scoreboard__wrap')
    for match in matches:
            ss = match.find('a', class_='c-events__name')
            link = ss.get('href')
            teams = match.find('span', class_ ='c-events__teams')
            date_time = match.find('div', class_='c-events__time')
            try:
                vremya = date_time.find('span')
            except Exception as e:
                print(e)
            try:
                taim = date_time.find('span', class_='c-events__overtime')
            except Exception as e:
                print(e)
            goals = match.find_all('span', class_ = 'c-events-scoreboard__cell c-events-scoreboard__cell--all')
            s = 0
            for goal in goals:
                s = s + int(goal.text)
            try:
                if taim.text == '1 Half' and s == 0:
                    try:
                        if int(vremya.text[0:2]) >= 15 and int(vremya.text[0:2]) < 30:
                            print(teams.text, vremya.text, taim.text)
                            driver.execute_script("arguments[0].click();", driver.find_element_by_partial_link_text(teams.text.split()[0]))
                            time.sleep(3)
                            html1 = BeautifulSoup(driver.page_source, 'html.parser')
                            try:
                                try:
                                    bet_groups = html1.find_all('div', class_ = 'bet_group')
                                    for bet_group in bet_groups:
                                        ozns = bet_group.find_all('div', class_ = 'bet-title bet-title_justify')
                                        for ozn in ozns:
                                            if "Both Teams To Score" in ozn.text:
                                                erts = bet_group.find_all('span', class_ = 'koeff')
                                                for ert in erts[1:2]:
                                                    lis2.append(ert.text)
                                except Exception as e:
                                    print(e)

                                print(lis2[0])
                                stats = html1.find_all('div', class_='o-tablo-stat-list__item')
                                for stat in stats:
                                    name_stat = stat.find('div', class_='c-chart-stat__title')
                                    numbers_stat = stat.find_all('div', class_='c-chart-stat__num')
                                    k = 0
                                    for number_stat in numbers_stat:
                                        k = k + int(number_stat.text)
                                    print(name_stat.text, k)
                                    lis.append(name_stat.text)
                                    lis.append(k)
                                print(lis)
                                corners = html1.find_all('div', class_='c-tablo-event', title="Corners")
                                c = 0
                                for corner in corners:
                                    c = c + int(corner.text)
                                    print(corner.text)
                                print(c)

                                if c <= 3 and teams.text not in lis1:
                                    if float(lis2[0]) >= 1.08:
                                        if "Attacks" in lis and int(lis[lis.index("Attacks") + 1]) / int(vremya.text[0:2]) <= 2:
                                            if "Shots on target" in lis and int(lis[lis.index("Shots on target") + 1])<=1:
                                                if "Shots off target" in lis and int(lis[lis.index("Shots off target")+1])/int(vremya.text[0:2]) <= 0.27:

                                                    if "Dangerous attacks" in lis and 15<=int(vremya.text[0:2])<20  and int(lis[lis.index("Dangerous attacks") + 1]) <= 20:

                                                        print(" ознподходит", teams.text, vremya.text, taim.text)
                                                        lis1.append(teams.text)
                                                        bot.send_message(561009671, driver.current_url+'\n'+f'{lis2[0]}'+" "+f'{lis[0]}'+f'{lis[1]}'+f'{lis[2]}'+f'{lis[3]}'+f'{lis[6]}'+f'{lis[7]}'+f'{lis[8]}'+f'{lis[9]}')
                                                    if "Dangerous attacks" in lis and 20 <= int(vremya.text[0:2]) < 25 and int(
                                                            lis[lis.index("Dangerous attacks") + 1]) <= 30:
                                                        print(" ознподходит", teams.text, vremya.text, taim.text)
                                                        lis1.append(teams.text)
                                                        bot.send_message(561009671,
                                                                         driver.current_url + '\n' + f'{lis2[0]}'+" "+f'{lis[0]}'+f'{lis[1]}'+f'{lis[2]}'+f'{lis[3]}'+f'{lis[6]}'+f'{lis[7]}'+f'{lis[8]}'+f'{lis[9]}')
                                                    if "Dangerous attacks" in lis and 25<=int(vremya.text[0:2])<30 and int(
                                                            lis[lis.index("Dangerous attacks") + 1]) <= 40:
                                                        print(" ознподходит", teams.text, vremya.text, taim.text)
                                                        lis1.append(teams.text)
                                                        bot.send_message(561009671,
                                                                         driver.current_url + '\n' + f'{lis2[0]}'+" "+f'{lis[0]}'+f'{lis[1]}'+f'{lis[2]}'+f'{lis[3]}'+f'{lis[6]}'+f'{lis[7]}'+f'{lis[8]}'+f'{lis[9]}')

                                print("--------------------------------------------------")
                            except Exception as e:
                                print(e)
                            lis.clear()
                            lis2.clear()
                            time.sleep(2)
                            driver.back()
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
    print("=====================================================================")

if __name__ == "__main__":
    main()

schedule.every(1).minutes.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)