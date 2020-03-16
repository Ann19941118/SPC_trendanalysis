# -*- coding: utf-8 -*-
import operator

def test_1_beyond_3sigma(data, center, sigma):
    lcl = center-3*sigma
    ucl = center+3*sigma
    return data[0] > ucl or data[0] < lcl


def test_6_thrund(data, center, sigma):
    list1 = data.copy()
    list1.sort()
    list2 = list1.copy()
    list3 = list2.copy()
    list3.reverse()
    return operator.eq(data, list2) or operator.eq(data, list3)


def test_7_thrund_one_side(data, center, sigma):
    list1 = data.copy()
    list1.sort()
    list2 = list1.copy()
    list3 = list2.copy()
    list3.reverse()

    a = True
    if operator.eq(data, list2) or operator.eq(data, list3):
        j = True
    else:
        j = False
    if not test_violating_runs(data, center, sigma):
        a = False
    return j and a


def test_2_OF_3_BEYOND_2SIGMA_ONE_SIDE(data, center, sigma):
    ucl = center+2*sigma
    ucl1 = center+3*sigma
    lcl = center-2*sigma
    lcl1 = center-3*sigma
    sum = 0
    for i in range(len(data)):
        if lcl1 < data[i] < lcl or ucl1 > data[i] > ucl:
            sum += 1
    a = True
    if sum < 2:
        j = False
    elif sum >= 2:
        j = True
    if not test_violating_runs(data, center, sigma):
        a = False
    return j and a


def test_4_OF_5_BEYOND_1SIGMA_ONE_SIDE(data, center, sigma):
    ucl1 = center+1*sigma
    ucl2 = center+2*sigma
    lcl1 = center-1*sigma
    lcl2 = center-2*sigma
    sum = 0
    for i in range(len(data)):
        if lcl2 < data[i] < lcl1 or ucl2 > data[i] > ucl1:
            sum += 1
    a = True
    if sum < 4:
        j = False
    elif sum >= 4:
        j = True
    if not test_violating_runs(data, center, sigma):
        a = False
    return j and a


def test_8_BEYOND_1SIGMA(data, center, sigma):
    ucl = center + sigma
    lcl = center - sigma
    sum = 0
    a = True
    for i in range(len(data)):
        if data[i] < lcl or data[i] > ucl:
            sum += 1
    if sum < 8:
        j = False
    elif sum >= 8:
        j = True

    return j


def test_15_below_sigma(data, center, sigma):
    ucl = center + sigma
    lcl = center - sigma
    sum = 0
    a = True
    for i in range(len(data)):
        if ucl > data[i] > lcl:
            sum += 1
    if sum < 15:
        j = False
    elif sum >= 15:
        j = True

    return j


def test_violating_runs(data, center, sigma):
    for i in range(1, len(data)):
        if (data[i - 1] - center) * (data[i] - center) < 0:
            return False
    return True


def test_14_up_down(data, center, sigma):
    list_juge = []
    for i in range(12):
        if (data[i+1]-data[i])*(data[i+1]-data[i+2])>0:
            list_juge.append('True')
        else:
            list_juge.append('False')
    if 'False' in list_juge:
        return False

    return True

