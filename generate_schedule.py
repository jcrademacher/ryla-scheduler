# Shceduling Software
# Date Modified: Jul, 30, 2019
# Author: Tech With Tim
#-----------------------------------------------------------
# GENERAL INFO
#
# Purpose: This scheduling software was used by the office
# staff at one of my previous jobs, a summer camp. It was
# used to generate a set of group schedules for campers based
# on a variety of constraints given to me.
# 
# Schedule Layout:
# The schedule for each group has 6 periods.
# 2 in the morning and 4 in the afternoon. The morning contains 2 sports.
# While the afternoon consists of a lunch, a swim and 2 sports. Lunch and swim
# will always happen the same period each day.
#
# Schedule Rules
# Each schedule has a set of rules that must be followed if possible.
# - No group may have the same activity more than 3 times a week (2 if possible)
# - No group may have the same activity on the same day
# - No two groups can have the same activty at the same time 
# - If an activity exists twice in a week it should be at least one day apart from
#   the last time it occured
# - If an activty exists more than twice in a week it should be in the oppsoite part
#    of the day. Meaning if for example: soccer occurs in the monring, then if it occurs
#    again it will be in the afternoon
# - Group 2 will never place tennis
#
# Details: 
# Each week the office staff manually create a schedule 
# for each group of campers expected in the following week. The goal
# when creating this schedule is to keep each one as diverse as possible.
# Meaning that each group particiaptes in as many activites as possible. This
# is tedious and very difficult to do. Having sometimes up to 10 groups a week
# doing this effectively becomes very diffuclt due to the mathematical complexity
# of balancing activities between the groups and within the individual schedules.
# I compare it to solving a more advanced version of sudoku.
#
# Limitations: 
# Sometimes the constraints selected in the program
# interface are impossible to generate a schedule for. Take for example
# the case in which you have 10 groups and only 8 activities available in
# the morning. Since no activity can run at the same time the schdule is
# impossible to generate.
#
#---------------------------------------------------------------------
# THE CODE
# The code below is written entierly in python using the PyQt5 Module.
# The majority of the UI for this project has been generated using 
# the software: QtDesigner.
#
# UI
# The UI for this project allows the user/schedule creator to select
# the lunch and swim periods for each group. They may then also deselect
# activities that cannot run in the morning or the afternoon, as well as
# add an extra ativity specific to the week. They will also be able to select
# the week the schedule is for. If for some reason their selections make it impossible
# to generate a schdule they may uncheck the box called "best" which will remove
# one constraint from the scheduling process. Then they may regenerate the schedule.
#
# OUTPUT
# If the schedule is able to be generated then the schedule will be
# printed to the console window as well as inserted into a formatted word
# document. This word document will be stored in the bin/generated schedules folder.
# 
# ALGORITHM DESIGN
# The algorithm that performs the scheduling function is designed
# around the BACKTRACKING algorithm. 

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import pprint  # for some nice printing
import random
import time
from word import make_word_doc  # This module writes the output to the word doc
import activities
import numpy as np
from schedule import Schedule


    # def generate_matrix(self, n):
    #     """
    #     Generates a 3d matrix 
    #     """
    #     matrix = []

    #     for group in range(0, n-1):
    #         matrix.append([])
    #         lunch = int(self.comboBoxLunches[group].currentText()[-1])
    #         swim = int(self.comboBoxSwim[group].currentText()[-1])
    #         for row in range(6):
    #             matrix[group].append([])
    #             for i in range(4):
    #                 if i == 0 and row == 0:
    #                     matrix[group][row].append("Name Games")
    #                 elif row+1 == lunch:
    #                     matrix[group][row].append("Lunch")
    #                 elif row+1 == swim:
    #                     matrix[group][row].append("Swim")
    #                 else:  
    #                     matrix[group][row].append("")

    #     return matrix


    # def solve(self):
    #     """
    #     The main implementation of the backtracking algorithm to solve
    #     the constraint satisfaction problem of greating the schdules. This is a
    #     recursice funciton.

    #     :return: Bool
    #     """
    #     morning = self.get_morning_events()
    #     afternoon = self.get_afternoon_events()

    #     # this just ensures we don't always try the same events at the
    #     # same period, making sure groups dont have patterny shcedules.
    #     random.shuffle(morning)
    #     random.shuffle(afternoon)

    #     # find an emoty position to fill
    #     find = self.find_empty()
    #     if not find or time.time() - self.start_time > 5:  # if we have been running for over 5 seconds or we have completed the schedule
    #         return True  # break recursion
    #     else:
    #         group, row, col = find  # decompose position to 3 vectors

    #         if row < 2:  # if position to fill is in morning
    #             events = morning[:] 

    #             # make sure we dont use an activity we've already used in the morning
    #             used_already = self.matrix[group][0] + self.matrix[group][1]

    #             # if group isnt group 2 then remove those used already events
    #             if group != 0:
    #                 for el in used_already:
    #                     try:
    #                         events.remove(el)
    #                     except:
    #                         continue
    #             # we don't do this for group 2 because group 2 has a limited amount of events
    #             # it can participate in and it needs to repeat activities in morning and afternoon
    #         else:
    #             events = afternoon[:]

    #             # add disallowed events if period is 3 or 4 because speciallitys eat/swim period 3/4
    #             if row == 2 or row == 3:
    #                 for event in self.afternoonCheckBoxes:
    #                     if not(event.isChecked()) and event.text() != "CheckBox":
    #                         events.append(event.text())

    #             # same proccess as the morning
    #             used_already = self.matrix[group][2] + self.matrix[group][3] + self.matrix[group][4] + self.matrix[group][5]
    #             if group != 0:
    #                 for el in used_already:
    #                     try:
    #                         events.remove(el)
    #                     except:
    #                         continue

    #         # group 2 cannot place tennis
    #         if group == 0:
    #             try:
    #                 events.remove("Tennis")
    #             except:
    #                 pass

    #     # execute backtracking algorithm
    #     for event in events:
    #         if self.valid(event, (group, row, col)):
    #             # if vaid then add event
    #             self.matrix[group][row][col] = event

    #             if self.solve():  # end recursion
    #                 return True

    #     self.matrix[group][row][col] = ""  # reset position to blank because nothing fit
    #     # we need to keep backtracking
        
    #     return False


    # def find_empty(self):
    #     """
    #     find the first empty square in the matrix/schedule

    #     :return: 3d tuple (Group, Row, Column)
    #     """
    #     for i, group in enumerate(self.matrix):
    #         for j, row in enumerate(group):
    #             for x, event in enumerate(row):
    #                 if event == "":
    #                     return (i, j, x)

    #     return None

    # def valid(self, event, pos):
    #     """
    #     Returns if it is valid to enter a new event
    #     into the given position of the matrix/schedule. This
    #     is where all the constraints of the program are written.
    #     :param event: Str (event to add)
    #     :param pos: 3d tuple (Group, Row, Column)
    #     :return: Bool
    #     """
    #     g, row, col = pos

    #     # check that event does not exist already at that time
    #     for group in range(len(self.matrix)):
    #         if self.matrix[group][row][col] == event and group != g:
    #             return False

    #     # Make sure event does not occur more than 3 times in a week
    #     count = 0
    #     for i, r in enumerate(self.matrix[g]):
    #         count += r.count(event)

    #     if count >= 3:
    #         return False

    #     # check that event is not already in same day
    #     for i in range(6):
    #         if self.matrix[g][i][col] == event and i != row:
    #             return False

    #     if self.best:  # if we best checkbutton is checked
    #         # Make sure if event occrs more than once in a week that they
    #         # are a least one day apart
    #         for i in range(6):
    #             for j in range(4):
    #                 if self.matrix[g][i][j] == event and abs(col-j) <= 1:
    #                     return False

    #     return True 

    # def display_matrix(self):
    #     """
    #     Display the matrix/schedule using some nice printing
    #     and formatting.
    #     :return: None
    #     """
    #     for g, group in enumerate(self.matrix):
    #         print("---------------------")
    #         print("GROUP", str(g+2) + ":")
    #         print("---------------------")
    #         formatted_days = " "*16 + "{day:<16}".format(day="MONDAY") + "{day:<16}".format(day="TUESDAY") + "{day:<16}".format(day="WEDNESDAY") + "{day:<16}".format(day="THURSDAY")
    #         print(formatted_days)
    #         for i, period in enumerate(group):
    #             print("{text:<16}".format(text="PERIOD " + str(i+1) + ":"))
    #             show = ""
    #             for event in period:
    #                 show += "{day:<16}".format(day=event)
    #             print(show)


def run_scheduler():

    # lengths in half hours
    morning_length = 8 
    last_morning_length = 9 
    print("Initializing schedule...")
    sch = Schedule(num_days=4,num_legs=9)

    return sch

# Run the app
if __name__ == "__main__":
    start_time = time.time()
    sch = run_scheduler()
    #make_word_doc(sch)

    # if time.time() - start_time > 5:
    #     print("Unable to generate a schedule that fits the constraints")
    # else:
    #     print("The schedule has been generated")
    print("Schedule generated.")