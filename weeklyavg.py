'''
    Usage: python3 weeklyavg.py /Users/oscar/Downloads/weight.csv
'''
import sys
import csv
from datetime import datetime, timedelta
from pprint import pprint
import statistics

with open(sys.argv[1], 'r') as my_file:
    read_data = csv.reader(my_file, delimiter=',')
    next(read_data)  # jumps first line in csv (table headers)
    current_week = None
    current_avg: float = 0
    previous_avg: float = 0
    previous_week = None
    weekly_avg: dict = {}
    list_data = list(read_data)
    data = reversed(list_data)
    for row in data:
        raw_date = row[0].split(" ")[0]  # removes time from string
        weight_lbs = float(row[1])
        formatted_date = datetime.strptime(raw_date, "%Y-%m-%d")
        week_start = formatted_date - timedelta(days=formatted_date.weekday())
        formatted_week_start = week_start.strftime('%m-%d-%Y')
        week_end = week_start + timedelta(days=6)
        weekly_avg.setdefault(formatted_week_start, {}).setdefault(
            'values', []).append(weight_lbs)
        if current_week != formatted_week_start or row == list_data[0]:
            previous_week = current_week
            current_week = formatted_week_start
            if previous_week is not None:
                previous_avg = current_avg
                current_avg = statistics.mean(
                    weekly_avg[previous_week]['values'])
                weekly_avg[previous_week]['avg'] = '%.2f' % current_avg
                if previous_avg == 0:
                    weekly_avg[previous_week]['weekly_change'] = '%.2f' % 0
                else:
                    weekly_avg[previous_week]['weekly_change'] = '%.2f' % (
                        current_avg - previous_avg)
    pprint(weekly_avg)
