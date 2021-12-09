# AI for gobang, which can generate step 
# Author: Jingkai Zhang 
# Date: 2021.11.20

from math import *
# from GoBang.Config import * 
from Config import *
import numpy as np


# GRID_WIDTH = 40

COLUMN = BOARD_ORDER
ROW = COLUMN 
  
next_point = [0, 0]                            # The next step for AI

ratio = 2                                      # attack ratio
DEPTH = 1                                      # search depth, if depth is bigger, the running speed will become slower exponentially

                                               # Score for different situation
shape_score = [(50, (0, 1, 1, 0, 0)),          # stands for 2 same color in a line 
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),    # four in a row without block 
               (99999999, (1, 1, 1, 1, 1))]    # Five in a row

def ai(list1,list2,list3,list_all):
    global cut_count                           # count the tree cutting time 
    cut_count = 0
    global search_count                        # count the search time 
    search_count = 0
    negamax(False, DEPTH, -99999999, 99999999,list1,list2,list3,list_all)  # negative maximum search
    return next_point[0], next_point[1]


# Implementation of negative maximum search 
def negamax(is_ai, depth, alpha, beta,list1,list2,list3,list_all):
    # Is gave over || the search has reached to the border
    if game_win(list1) or game_win(list2) or depth == 0:
        return evaluation(is_ai,list1,list2)

    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list,list3)                    # sort, in order to boost speed
    # evaluate for every possible next step
    for next_step in blank_list:

        global search_count
        search_count += 1

        # if the piece does not have neighbor, skip 
        if not has_neightnor(next_step,list3):
            continue

        if is_ai:
            list1.append(next_step)            # possible step for AI
        else:
            list2.append(next_step)            # possible step for human
        list3.append(next_step)                # includes both AI and human

        value = -negamax(not is_ai, depth - 1, -beta, -alpha,list1,list2,list3,list_all)
        if is_ai:
            list1.remove(next_step)
        else:
            list2.remove(next_step)
        list3.remove(next_step)

        if value > alpha:                      # the core idea of cutting tree algorithm  
            if depth == DEPTH:
                next_point[0] = next_step[0]
                next_point[1] = next_step[1]
        
            if value >= beta:
                global cut_count
                cut_count += 1
                return beta
            alpha = value

    return alpha


# if the next step is close to the last step of enemy, it might be a good choice 
def order(blank_list,list3):
    last_pt = list3[-1]
    for item in blank_list:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                    blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                    blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))

# check if the piece has a neighbor piece
def has_neightnor(pt,list3):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1]+j) in list3:
                return True
    return False


# evaluation function 
def evaluation(is_ai,list1,list2):
    total_score = 0

    if is_ai:
        my_list = list1
        enemy_list = list2
    else:
        my_list = list2
        enemy_list = list1

    # calculate the total score for human
    score_all_arr = [] 
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)

    # calculate the total score for robot
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

    total_score = my_score - enemy_score*ratio*0.1

    return total_score


# calculate scores in all directions
def cal_score(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
    add_score = 0  
    max_score_shape = (0, None)                     # only count the maximum in one direction

    # if the point has been evaluated, skip
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                if tmp_shap5 == (1,1,1,1,1):
                    pass  
                    # print('wwwwwwwwwwwwwwwwwwwwwwwwwww')
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_decrict, n + (0+offset) * y_derice),
                                               (m + (1+offset) * x_decrict, n + (1+offset) * y_derice),
                                               (m + (2+offset) * x_decrict, n + (2+offset) * y_derice),
                                               (m + (3+offset) * x_decrict, n + (3+offset) * y_derice),
                                               (m + (4+offset) * x_decrict, n + (4+offset) * y_derice)), (x_decrict, y_derice))

    # if two cases intersect, the score will be added 
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0]

# judge if the game is over 
def game_win(list):
    for m in range(COLUMN):
        for n in range(ROW):

            if n < ROW - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (
                    m, n + 3) in list and (m, n + 4) in list:
                return True
            elif m < ROW - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (
                        m + 3, n) in list and (m + 4, n) in list:
                return True
            elif m < ROW - 4 and n < ROW - 4 and (m, n) in list and (m + 1, n + 1) in list and (
                        m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                return True
            elif m < ROW - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (
                        m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                return True
    return False
