"""
Name: Chi Thieu
Course: ISTA 131
"""
import numpy as np
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# Function to generate a student report based on a student ID
def student_report(db, student_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # Get the student ID
    id = student_id
    lis = []
    all_class = []
    grades = ''
    # Query to get table names
    query = "SELECT name FROM sqlite_master WHERE type = 'table'"
    for row in c.execute(query).fetchall():
        for item in row:
            lis.append(item)
    header = ''
    dashes = ''
    classes = ''
    string = ''
    # Iterate over each table in the database
    for table in lis:
        # Query to fetch student information from each table
        query = 'SELECT last, first, grade, id FROM ' + table + " WHERE id = '" + id + "'"
        for row in c.execute(query):
            header = str(row[0]) + ', ' + str(row[1]) + ', ' + id + '\n'
            dashes = '-' * (len(header)-1) + '\n'
            classes = table.replace('_', ' ') + ': ' + row[2] + '\n'
            all_class.append(classes)
            all_class.sort
    header += dashes
    string += header
    # Concatenate all classes
    for i in range(len(all_class)):
        string += all_class[i]
    return string

# Function to retrieve A-grade students
def A_students(conn, table='ISTA_131_F17', standing=None, max=10):
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    stud_lis = []
    A_studs = []
    if standing != None:
        query = 'SELECT last, first, grade, id FROM ' + table + " WHERE level LIKE '" + standing + "' ORDER BY last, first"
    else:
        query = 'SELECT last, first, grade, id FROM ' + table + ' ORDER BY last, first'
    for row in c.execute(query):
        if row[2] == 'A':
            for elem in row:
                student = str(row[0]) + ', ' + str(row[1])
            stud_lis.append(student)
    for i in range(0, len(stud_lis)):
        if i < max:
            A_studs.append(stud_lis[i])
    return A_studs

# Function to calculate class performance
def class_performance(conn, table='ISTA_131_F17'):
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    query = 'SELECT t1.grade, CAST(t1.count_grade AS REAL)/CAST(t2.total_grades AS REAL) *100 as Math FROM (SELECT grade, COUNT() as count_grade FROM '+table+' GROUP BY grade) t1,(SELECT COUNT() as total_grades FROM '+table+') t2'
    dictionary = {}
    for row in c.execute(query):
        dictionary[row[0]] = round(row[1], 1)
    print(dictionary)
    return dictionary

# Function to read data frame from CSV file
def read_frame():
    cols = ['Jan_r', 'Jan_s', 'Feb_r', 'Feb_s', 'Mar_r', 'Mar_s', 'Apr_r', 'Apr_s', 'May_r', 'May_s', 'Jun_r', 'Jun_s', 'Jul_r', 'Jul_s', 'Aug_r', 'Aug_s','Sep_r', 'Sep_s', 'Oct_r', 'Oct_s', 'Nov_r', 'Nov_s', 'Dec_r', 'Dec_s']
    Frame = pd.read_csv("sunrise_sunset.csv", index_col=0, names=cols, dtype=str)
    return Frame

# Function to get sunrise and sunset series from data frame
def get_series(data):
    sunrise = pd.concat([data['Jan_r'], data['Feb_r'], data['Mar_r'], data['Apr_r'], data['May_r'], data['Jun_r'], data['Jul_r'], data['Aug_r'], data['Sep_r'], data['Oct_r'], data['Nov_r'], data['Dec_r']], ignore_index=True)
    sunrise = sunrise.dropna()
    index = [i for i in range(1, 366)]
    sunrise.index = index
    date_index = pd.date_range('1/1/2018', periods=365)
    sunrise.index = date_index
    sunset = pd.concat([data['Jan_s'],data['Feb_s'], data['Mar_s'], data['Apr_s'], data['May_s'], data['Jun_s'], data['Jul_s'], data['Aug_s'], data['Sep_s'], data['Oct_s'], data['Nov_s'], data['Dec_s']], ignore_index=True)
    sunset = sunset.dropna()
    sunset.index = index
    sunset.index = date_index
    return sunrise, sunset

# Function to find the longest day
def longest_day(sunrise, sunset):
    sunset = sunset.copy()
    for i in sunset.index:
        time = sunset[i]
        minutes = int(time[-2:])
        hours = int(time[:-2])
        time_set = minutes + (hours * 60)
        sunset[i] = time_set
        sunrise = sunrise.copy()
    for i in sunrise.index:
        time = sunrise[i]
        minutes = int(time[-2:])
        hours = int(time[:-2])
        time_rise = minutes + (hours * 60)
        sunrise[i] = time_rise
    length = sunset - sunrise
    for dt in length.index:
        if length[dt] == max(length):
            time = length[dt]
            hours = str(time // 60)
            minutes = str(time % 60)
            return dt, hours + minutes

# Function to calculate the difference in sunrise times
def sunrise_dif(sunrise, dt):
    sunrise = sunrise.astype('int64')
    for i in sunrise.index:
        time = sunrise[i]
        hours = time // 100 * 60
        minutes = time % 100
        total_minutes = minutes + hours
        sunrise[i] = total_minutes
    before = dt - timedelta(90)
    later = dt + timedelta(90)
    dif = sunrise[before] - sunrise[later]
    return dif
