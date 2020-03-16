#-*- coding:utf-8 -*-
"""
Main class that provides SPC analysis. It detects SPC rules violations.
It can draw charts using matplotlib.
:arguments:
  data
  user data as flat array/list
"""
from utils import *
import numpy as np
import pandas as pd


RULE_1_BEYOND_3SIGMA = '1个点落在A区以外'
RULE_2_OF_3_BEYOND_2SIGMA_ONE_SIDE = '3个点中有2个点连续落在B区以外'
RULE_4_OF_5_BEYOND_1SIGMA = '5个点中有4个点连续落在中心线同一侧C区以外'
RULE_6_TRENDING = '6个点连续增长或下降'
RULE_8_ON_TWO_SIDE_NONE_C = '8个连续的点落在中心线两侧且无一点在C区'
RULE_9_ON_ONE_SIDE = '9个连续的点在中心线的同一侧'
RULE_14_up_down = '连续14个点交替上下'
RULE_15_below_1sigma = '15个连续点在在中心线两侧C区'


RULES_ALL = [RULE_1_BEYOND_3SIGMA,
             RULE_2_OF_3_BEYOND_2SIGMA_ONE_SIDE,
             RULE_4_OF_5_BEYOND_1SIGMA,
             RULE_6_TRENDING,
             RULE_8_ON_TWO_SIDE_NONE_C,
             RULE_9_ON_ONE_SIDE,
             RULE_14_up_down,
             RULE_15_below_1sigma]

RULES_FUNCS = {
    RULE_1_BEYOND_3SIGMA: (test_1_beyond_3sigma, 1),
    RULE_2_OF_3_BEYOND_2SIGMA_ONE_SIDE: (test_2_OF_3_BEYOND_2SIGMA_ONE_SIDE, 3),
    RULE_4_OF_5_BEYOND_1SIGMA: (test_4_OF_5_BEYOND_1SIGMA_ONE_SIDE, 5),
    RULE_6_TRENDING: (test_6_thrund, 6),
    RULE_8_ON_TWO_SIDE_NONE_C: (test_8_BEYOND_1SIGMA, 8),
    RULE_9_ON_ONE_SIDE: (test_violating_runs, 9),
    RULE_14_up_down: (test_14_up_down, 14),
    RULE_15_below_1sigma: (test_15_below_sigma, 15)}



class SPC_rule(object):
    """
    Main class that provides WECR analysis. It detects WECR rules violations.
    It can draw charts using matplotlib.
    :arguments:
      data
      user data as flat array/list
    """

    def __init__(self, data,  center=None, sigma=None, rule_keys=None):
        '''

        :param data: list/dataframe/np.ndarray
        :param center: mean
        :param sigma:  sigma
        :param rule_keys: list, key of rules, such:[1,2]
            1:RULE_1_BEYOND_3SIGMA = '1个点落在A区以外'
            2:RULE_2_OF_3_BEYOND_2SIGMA_ONE_SIDE = '3个点中有2个点连续落在B区以外'
            3:RULE_4_OF_5_BEYOND_1SIGMA = '5个点中有4个点连续落在中心线同一侧C区以外'
            4:RULE_6_TRENDING = '6个点连续增长或下降'
            5:RULE_8_ON_TWO_SIDE_NONE_C = '8个连续的点落在中心线两侧且无一点在C区'
            6:RULE_9_ON_ONE_SIDE = '9个连续的点在中心线的同一侧'
            7:RULE_14_up_down = '连续14个点交替上下'
            8:RULE_15_below_1sigma = '15个连续点在在中心线两侧C区'
        '''
        if isinstance(data, pd.DataFrame):
            data = data.values
            data = data.reshape((1, -1))
            data = list(data)
        if isinstance(data, np.ndarray):
            data = data.reshape((1, -1))
        elif not isinstance(data, list):
            raise TypeError('please input data of list or pd.Dataframe or np.ndarray')

        self.orig_data = data

        if not center:
            center = np.mean(data)
        self.center = center

        if not sigma:
            sigma = np.std(data, ddof=1)
        self.sigma = sigma

        if not rule_keys:
            rule_new = RULES_ALL
        else:
            rule_new = []
            for key in rule_keys:
                rule_new.append(RULES_ALL[key-1])

        self.rules = rule_new

        self.length = len(data)
        self.violating_points = self._find_violating_points()

    def __repr__(self):
        print(self.get_violating_points())
        return "<spc: (%d)>" % self.__hash__()


    def _find_violating_points(self):

        points_all = {}
        for r in self.rules:
            func, points_num = RULES_FUNCS[r]
            list1 = []
            for i in range(len(self.orig_data)):
                if i < points_num-1:
                    continue
                if func(self.orig_data[i - points_num+1:i+1], self.center, self.sigma):
                    list1.extend(range(i - points_num+1, i+1))
            points_all.setdefault(r, []).extend(list1)

        return points_all


    def get_violating_points(self):
        """Return points that violates rules"""
        points_all = self.violating_points
        points_dict = {}
        for key, values in points_all.items():
            # if values != []:
            points_dict[key] = sorted(set(values))
        return points_dict

