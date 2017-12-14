# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 14:59:12 2017

@author: hxji
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 16:45:43 2017

This is for the IR material infractive index calculation with different temperature
@author: hxji
"""
import xlrd
import numpy as np
import matplotlib.pyplot as plt
# IR material data from paper
material_data=xlrd.open_workbook(r'C:\Users\hxji\Documents\GitHub\Dell_git\IR material\IR material_Refractive index.xlsx')
# data comparsion of Si
ori_data = xlrd.open_workbook(r'C:\Users\hxji\Documents\GitHub\Dell_git\IR material\data comparison\Si_ori_data.xlsx')
table_ori = ori_data.sheets()[0]
wave_data = table_ori.col_values(0)[1:]
tem_data = table_ori.row_values(0)[1:]

#table = material_data.sheets()[0] 
# =============================================================================
# Please choose the material name
# =============================================================================
# 0-2: BaF2;LiF;ZnSe, 2005,Leviton
# 3: ZnS, 2013,Leviton
# 4: Homosil, 2017,Leviton
# 5-13: S-LAH55, SLAH55V-1, S-LAH55V-2, S-LAH59, S-TIH14, S-NPH2, S-LAM3, S-NBM51, and S-PHM52, 2015,Leviton
# 14-17: N-BK7; BaLKN3; SF15; E-SF03, 2007
# 18: Corning 7980,2006
# 19-21: Suprasil 3001; S-FTM16; CaF2,2015
# 22: L-BHH2,2015
# 23-25: S-FPL51; S-FTM16_2; S-TIM28,2013
# 26-27: CaF2_2; Heraeus Infrasil 301, 2007
# 28-29: Si; Ge, 2007

#glass_name = "Si"
glass_name = "Si"
table = material_data.sheet_by_name(glass_name)

###############################################################################
# Input the temperature "K"
#t = 295 # unit: K
#wave = np.array([1.1,1.2]) # unit: um
tem = np.array(tem_data)
wave = np.array(wave_data)
#print table_ori.col_values(12)[1:]
###############################################################################
# ZEMAX data of Si
z_si_153 = [4.131495804E-001,2.463711439E-003,6.900066780E-001,1.117604311E-002,8.902159928E-001,9.766150977E+001]
z_si_173 = [7.258904190E-001,1.096731550E-002,3.775772860E-001,2.056039050E-003,8.929591950E-001,9.793921750E+001]
z_si_293 = [5.204689170E-001,1.242035470E-002,5.854193400E-001,3.991761000E-003,8.956652280E-001,9.822483250E+001]
z_si = [z_si_153,z_si_173,z_si_293]
###############################################################################
#tem = np.array([153,173,293])
for k in range(0,len(tem)):
    t = tem[k]
    coefficient_data = []
    coefficient_data_zemax = []
#    print t
    for i in range(1,7):
        data = np.array(table.col_values(i)[1:6])
        t_data = np.array([1,t,t**2,t**3,t**4])
        s = np.dot(data,t_data)
        coefficient_data.append(s)
        if i<4:
            coefficient_data_zemax.append(s)
        else:
            coefficient_data_zemax.append(s**2)    
    new_n_index = []
#    new_n_index2 =[]
    for wave_i in  wave:
        n_index = 1
        n_index2 = 1
        for i in range(0,3):
            n_index = n_index + coefficient_data[i]*wave_i**2/(wave_i**2-coefficient_data[i+3]**2)
#            n_index2 = n_index2 + z_si[k][2*i]*wave_i**2/(wave_i**2-z_si[k][2*i+1])
        n_index_T_wave = np.sqrt(n_index)
#        n_index_T_wave2 = np.sqrt(n_index2)
        
        new_n_index.append(n_index_T_wave)
#        new_n_index2.append(n_index_T_wave2)
    n_ori_50K = table_ori.col_values(k+1)[1:]
    d_n_50K = np.array(new_n_index)-np.array(n_ori_50K)
#    d_n2 = np.array(new_n_index2)-np.array(new_n_index)
#    plt.plot(wave,d_n_50K)
#    plt.scatter(wave,d_n_50K)
#    plt.plot(wave,d_n2)
#    plt.scatter(wave,d_n2)   
#plt.legend(tem)

#data_input = open(r'C:\Users\hxji\Documents\GitHub\Dell_git\IR material\glass_1.dat','w+')
#data_input.writelines("TEMPERATURE 20\n")
#data_input.writelines("PRESSURE 0.0\n")
#
##tem_in = 20 # unit: K
#for i in range(0,len(tem)):
#    data_input.writelines("%f %f\n"%(wave[i],new_n_index[i]))
#data_input.close()


coefficient_data2 = np.array([1.25493787E+001,-1.88270543E+000,-1.23832900E+004,9.24436560E-002,9.07375997E-002,1.25490743E+008])
n_index2 = 1
for i in range(0,3):
    n_index2 = n_index2 + coefficient_data2[i]*wave**2/(wave**2-coefficient_data2[i+3])
n_index_T_wave2 = np.sqrt(n_index2)
d_n3 = np.array(n_index_T_wave2)-n_ori_50K
plt.plot(wave,d_n3)
plt.scatter(wave,d_n3)    
#plt.plot(wave,d_n_50K)
#plt.scatter(wave,d_n_50K)    


