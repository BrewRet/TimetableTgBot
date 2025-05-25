import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time


# Вывод расписания по входящей дате
def ShowLessons(date : datetime, keys:dict) -> str:
    week_day = {
    0 : "Понедельник",
    1 : "Вторник",
    2 : "Среда",
    3 : "Четверг",
    4 : "Пятница",
    5 : "Суббота",
    6 : "Воскресенье"
}
    if date.strftime('%d.%m.%Y') not in keys or date.weekday() == 6:
        return 'В данный день пар нет'
    return f"{date.strftime('%d.%m.%Y')}, {week_day[date.weekday()]}:"+ "\n"+ ''.join(keys[date.strftime('%d.%m.%Y')])

# Парсинг timetable.tusur.ru для получения расписания за входящую неделю
def GetLessons(week:int) -> list: 
    url = "https://timetable.tusur.ru/faculties/fb/groups/724-2"
    payload = {'week_id':week}
    responce = requests.get(url, params=payload)
    src = responce.text
    tmp = []
    lessons = []
    soup = BeautifulSoup(src, 'html.parser')
    time = soup.find_all('div', class_='modal-body')
    les = soup.find_all("h4", class_="modal-title text-center")
    for i in range(len(les)):
        lessons.append((les[i].text + time[i].text).replace("Дата проведения:", '').replace("Вид занятия:","")
                     .replace("Время проведения:", '').replace("Ссылка на электронный ресурс:", ''))
    for data in lessons:
        tmp.append(("-------\n"+ re.sub("  +", '\n', re.sub("\n+","  ", data))).split("Преподаватель:")[0])
    lessons = tmp
    return lessons
          

# Преобразование полученного списка в словарь для более удобного доступа к информации
# с ключем равным дате
def LessonsToDict(lessons:list, _date=datetime.now().date()) -> dict:
    keys = dict()
    for data in lessons:
        info = ''.join(re.findall(r'[0-3][0-9].[0-1][0-9].[0-3][0-9]{3}', data))
        info_date = datetime.strptime(info, "%d.%m.%Y").date()
        if info_date >= _date:
            if info not in keys:
                keys[info] = [data.replace(info, "")]
            else: keys[info] += [data.replace(info, "")]
    for key, val in keys.items():
        keys[key] = list(dict.fromkeys(val))
    return keys



ROOT_DATE = datetime(2010, 8, 9)
dict_lessons = {}


    
now = datetime.now()
tmrw = now + timedelta(days=1)

current_week = (now - ROOT_DATE).days//7
next_week = current_week+1

lessons_current_week = GetLessons(current_week)
lessons_next_week = GetLessons(next_week)
dict_lessons = LessonsToDict(lessons_current_week)
dict_lessons.update(LessonsToDict(lessons_next_week))

today = ShowLessons(now, dict_lessons)
tomorrow = ShowLessons(tmrw, dict_lessons)
print(dict_lessons)
#time.sleep(900)
        






