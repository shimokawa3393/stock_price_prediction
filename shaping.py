import math

import numpy as np
import pandas as pd


class Shaping():
    
    # 配列の軸を入れ替える
    def replaceList(self, settlement_t_body):
        array = np.array(settlement_t_body)
        array = np.transpose(array)
                
        return array[0], array[1], array[2], array[3], array[4]
        
    
    # 決算データの文字列を整数に変換
    def changeNum(self, item): 
        list = []
        
        for x in item:
            num_list = []
            index = x.find('.')
            
            if index != -1:
                x = x[:index]
            
            if x.find(',') != -1:
                num_list = x.split(',')
            else:
                num_list = x
                                
            if '---' in num_list:
                list.append(0)
            else:
                list.append(int(''.join(num_list)))
                
        return list
    
 
    # 決算データを整形する
    def shapePerformance(self, length, item): 
        linspace_list = []
        new_list = []
        
        one_year_business_day = math.floor(length / 3)
        remainder = length % 3
        
        for i in range(3):
            if remainder != 0:
                x = np.linspace(item[i], item[i+1], one_year_business_day + 1)
                remainder -= 1
            else:
                x = np.linspace(item[i], item[i+1], one_year_business_day)
            linspace_list.append(x)

        
        for i in range(len(linspace_list)):
            for j in range(len(linspace_list[i])):
                new_list.append(math.floor(linspace_list[i][j]))
                        
        return new_list
        
    
    def createDF(self, settlement_num):
        df_income = pd.DataFrame(
            {'売上高': settlement_num[0],
            '営業利益': settlement_num[1],
            '経常利益': settlement_num[2],
            '純利益': settlement_num[3],
            '一株利益': settlement_num[4]})
        
        return df_income
    
        