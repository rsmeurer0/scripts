#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Module Description:


Example:


Todo:
    *Bot para avisar quando der 8 horas
    *Bot para avisar quando deu horário do almoço
    *Bot para avisar caso não tenha uma hora de intervalo durante o dia

"""

__author__ = "Rodrigo Meurer"
__email__ = "rodrigo.meurer@khomp.com"


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time
from datetime import datetime
from datetime import date
import calendar


class bcolors:
    RED   = "\033[1;31m"
    BLUE  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    REVERSE = "\033[;7m"
    B_YELLOW = "\033[0;43m"
    B_BLACK = "\033[0;40m"
    BLACK = "\033[0;30m"

def check_work_regular(work_intervals):
    for interval in work_intervals:
        if interval > 360:
            print("WORK TIME FOR DAY IS IRREGULAR, WORKED MORE THAN 6 STRAIGHT HOURS")
            return False
        else:
            return True

def check_pause_regular(pause_intervals):
    had_lunch_interval = False
    for interval in pause_intervals:
        if interval >= 60:
            had_lunch_interval = True
    return had_lunch_interval

def check_regular(work_intervals, pause_intervals):
    if sum(work_intervals) > 360:
        work = check_work_regular(work_intervals)
        pause = check_pause_regular(pause_intervals)
        return work and pause
    elif sum(work_intervals) == 0:
        return None
    else:
        return True

def get_work_intervals(time_list):
    work_intervals = []
    time_stamps = len(time_list)
    time_list = turn_into_datetime(time_list)
    if time_stamps == 0:
        return work_intervals

    elif time_stamps%2 == 0:
        for i in range(0, time_stamps, 2):
            if i < time_stamps:
                work_intervals.append((time_list[i+1] - time_list[i]).seconds/60)

    elif time_stamps%2 == 1:
        for i in range(0, time_stamps, 2):
            if i+1 < time_stamps:
                work_intervals.append((time_list[i+1] - time_list[i]).seconds/60)
            else:
                now = datetime.today().strftime("%H:%M")
                now = turn_into_datetime(now)
                work_intervals.append((now - time_list[i]).seconds/60)

    return work_intervals

def get_pause_intervals(time_list):
    pause_intervals = []
    time_stamps = len(time_list)
    time_list = turn_into_datetime(time_list)
    if time_stamps < 2:
        return pause_intervals
    pauses = int(time_stamps/2)
    for i in range(0, pauses, 2):
        pause_intervals.append((time_list[i+2] - time_list[i+1]).seconds/60)

    return pause_intervals

def turn_into_datetime(times):

    if type(times) is list:
        time_list = []
        for item in times:
            item = datetime.strptime(item, '%H:%M')
            time_list.append(item)
        return time_list
    else:
        times = datetime.strptime(times, '%H:%M')
        return times



def get_work_time_today(time_list):
    work_intervals = get_work_intervals(time_list)
    work_minutes_today = sum(work_intervals)
    return work_minutes_today


def get_pause_time_today(time_list):
    pause_intervals = get_pause_intervals(time_list)
    pause_minutes_today = sum(pause_intervals)
    return pause_minutes_today

def get_extra_hours(overview_table):
    for row in overview_table.splitlines():
        if 'SALDO' in row:
            extra_hours = row.split()[1]
            return extra_hours
    return "Not Found"

def get_list_of_dates(year, month):
    days_in_month = calendar.monthrange(year, month)[1]
    dates = [date(year, month, day) for day in range(1, days_in_month+1)]
    dates_str_list = []
    for item in dates:
        dates_str_list.append(item.strftime("%d/%m/%Y"))

    return dates_str_list

def login_and_get_info():
    # browser = webdriver.Firefox()
    browser = webdriver.PhantomJS()

    browser.get('https://www.ahgora.com.br/externo/index/empresakhomp')
    assert ':: Ahgora Sistemas ::' in browser.title

    form = browser.find_element_by_id('boxLogin')

    elem = form.find_element_by_id('matricula')  # Find the search box
    elem.send_keys('305' + Keys.TAB)

    elem = browser.find_element_by_id('senha')  # Find the search box
    elem.send_keys('1226' + Keys.RETURN)
    time.sleep(4)

    print("Logged in as:")
    elems = browser.find_elements_by_xpath("//div[@class='col-xs-12 col-sm-9']/dl/dd")
    print(elems[0].text)


    browser.find_element_by_id('espelho_ponto_icon').click()

    time.sleep(5)

    elem = browser.find_element_by_id('titulo_mes')


    tables = browser.find_elements_by_xpath("//tbody")

    overview_table = tables[0].text
    time_table = tables[1].text
    time.sleep(1)
    tables = [overview_table, time_table]
    browser.quit()
    return tables

def get_time_list(time_table, date_of_interest):

    time_list = []
    for item in time_table.splitlines():
        if date_of_interest in item:
            if "KHOMP BATIDAS - KHOMP BATIDAS" in item:
                table_list = item.split("KHOMP BATIDAS - KHOMP BATIDAS")[1]
                table_list = table_list.split(" ")
                table_list.pop(0)
                for item in table_list:
                    if item == "Horas":
                        break
                    time_list.append(item.replace(",",""))
            else:
                table_list = []

    return time_list

def main():

    curr_year = datetime.today().year
    curr_month = datetime.today().month
    list_of_dates = get_list_of_dates(curr_year, curr_month)
    today_str = datetime.today().strftime("%d/%m/%Y")

    tables = login_and_get_info()

    overview_table = tables[0]
    time_table = tables[1]
    print(bcolors.CYAN + "--------------------------------------------------")
    print("|     DATE     | WORK TIME | PAUSE TIME | STATUS |")
    print("--------------------------------------------------" + bcolors.RESET)
    for day in list_of_dates:
        time_list = get_time_list(time_table, day)

        work_time = get_work_time_today(time_list)
        pause_time = get_pause_time_today(time_list)

        work_hours = int(work_time/60)
        work_minutes = int(work_time%60)

        pause_hours = int(pause_time/60)
        pause_minutes = int(pause_time%60)

        work_intervals = get_work_intervals(time_list)
        pause_intervals = get_pause_intervals(time_list)

        ok_status = check_regular(work_intervals, pause_intervals)
        if ok_status == False:
            ok_status = bcolors.RED + str(ok_status) + bcolors.RESET
        if ok_status == True:
            ok_status = bcolors.GREEN + str(ok_status) + bcolors.RESET

        if day == today_str:
            day = bcolors.YELLOW + day + bcolors.RESET

        print("|  %s  |   %02d:%02dh   |   %02d:%02dh   | %s |"%(day, work_hours, work_minutes, pause_hours, pause_minutes, ok_status))

        if day ==  today_str:
            sys.stdout.write(bcolors.RESET)


    extra_hours = get_extra_hours(overview_table)

    print(bcolors.CYAN + "--------------------------------------------------")
    print("|       You have in total %sh extra hours     |" %(extra_hours))
    print("--------------------------------------------------" + bcolors.RESET)







if __name__ == "__main__":
    main()
