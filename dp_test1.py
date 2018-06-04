#-*- coding:utf-8 -*-
from __future__ import print_function
import math
dimension = 15
#テンプレートデータの読み込み----------------------------------------------------------
temple_data_list = []
data_name = []
for file_num in range(100):
    list_data = []
    file_name = "city_mcepdata/city011/city011_{0:03d}.txt".format(file_num+1)
    with open(file_name,"r") as f:
        for i in range(1):
            line = f.readline()
            #print(line, end="")

        line = f.readline()
        data_name.append(line.strip())
        line = f.readline()
        line = f.readline()
        while line:
            data = line.strip().split()
            float_data = map(float,data)
            list_data.append(float_data) #stripで改行などを削除する
            line = f.readline()
    temple_data_list.append(list_data)
#print(temple_data)
#print(len(list_data)) #これでフレーム数がわかる
#print(data_name)

#-------------------------------------------------------------------------------------

#未知データの読み込み
non_data = []
file_name_non = "city_mcepdata/city011/city011_088.txt"
with open(file_name_non,"r") as f:
    for i in range(1):
        line = f.readline()
        #print(line, end="")

    line = f.readline()
    true_data_name = line.strip()
    line = f.readline()
    line = f.readline()
    while line:
        data = line.strip().split()
        float_data = map(float,data)
        non_data.append(float_data)
        line = f.readline()
#-------------------------------------------------------------------------------------

#ユークリッド距離のラムダ式------------------------------------------------------------
dist = lambda item1_, item2_: math.sqrt(sum([(item_[0]-item_[1])**2 for item_ in list(zip(item1_, item2_))]))
#--------------------------------------------------------------------------------------

#DPマッチングスタート------------------------------------------------------------------
minimum_index_list = []
for temp_data_i in range(100):
    
    #temple_data = temple_data_list[0]
    temple_data = temple_data_list[temp_data_i]
    #row_data_num = len(temple_data_list[0])
    row_data_num = len(temple_data_list[temp_data_i])
    line_data_num = len(non_data)
    #ゴール=>(row_data_num-1, line_data_num-1)
    data_g = [[0 for r in range(row_data_num)] for l in range(line_data_num)] #gの値
    #print(data_g)
    data_d = [[0 for r in range(row_data_num)] for l in range(line_data_num)] #dの値
    
    #距離データ計算
    for line_i in range(line_data_num):
        line_data = non_data[line_i]
        for row_i in range(row_data_num):
            row_data = temple_data[row_i]
            data_d[line_i][row_i] = dist(row_data,line_data)
    
    #print(data_d)
    
    #初期条件
    #print(data_g[0][0])
    #print(data_d[0][0])
    data_g[0][0] = data_d[0][0]
    #print(data_g)
    #境界データ
    #横について
    for row_i in range(1,row_data_num):
        data_g[0][row_i] = data_g[0][row_i-1] + data_d[0][row_i]
    #縦について
    for line_i in range(1,line_data_num):
        data_g[line_i][0] = data_g[line_i-1][0] + data_d[line_i][0]
    #その他の格子点
    for line_i in range(1,line_data_num):
        for row_i in range(1,row_data_num):
            data_min_list = []
            data_min_list.append(data_g[line_i][row_i-1] + data_d[line_i][row_i])
            data_min_list.append(data_g[line_i-1][row_i-1] + 2 * data_d[line_i][row_i])
            data_min_list.append(data_g[line_i-1][row_i] + data_d[line_i][row_i])
            data_g[line_i][row_i]=min(data_min_list)
    
    print("calce_data[{}] : name => {} number => {}".format(temp_data_i+1,data_name[temp_data_i],data_g[line_data_num-1][row_data_num-1]))
    minimum_index_list.append(data_g[line_data_num-1][row_data_num-1])
print("######################################")
print("True_data =>  {}".format(true_data_name))
print("estimate => {}".format(data_name[minimum_index_list.index(min(minimum_index_list))]))
