# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 16:45:43 2017

This is for the IR material infractive index calculation with different temperature
@author: hxji
"""
import xlrd
import numpy as np

material_data=xlrd.open_workbook(r'C:\Users\hxji\Documents\GitHub\Dell_git\IR material\IR material_Refractive index.xlsx')
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

glass_name = "Suprasil 3001"
table = material_data.sheet_by_name(glass_name)
coefficient_data = []
coefficient_data_zemax = []
###############################################################################
# Input the temperature "K"
t = 173 # unit: K
wave = 1.0 # unit: um
###############################################################################
t_ref_min = table.col_values(1)[6]
t_ref_max = table.col_values(2)[6]
if t<=t_ref_min or t>=t_ref_max:
    print("The temperature %d K is out of the measured data"%t)
    
wave_ref_min = table.col_values(1)[7]
wave_ref_max = table.col_values(2)[7]
if wave<=wave_ref_min or wave>=wave_ref_max:
    print("The wave %d um is out of the measured data"%wave)    
for i in range(1,7):
    data = np.array(table.col_values(i)[1:6])
    t_data = np.array([1,t,t**2,t**3,t**4])
    s = np.dot(data,t_data)
    coefficient_data.append(s)
    if i<4:
        coefficient_data_zemax.append(s)
    else:
        coefficient_data_zemax.append(s**2)
n_index = 1
for i in range(0,3):
    n_index = n_index + coefficient_data[i]*wave**2/(wave**2-coefficient_data[i+3]**2)
n_index_T_wave = np.sqrt(n_index)
print("############################################################################")
print("The Material is '%s'\n"%glass_name)
print("Ref wavlength: [%f,%f]\n"%(wave_ref_min,wave_ref_max))
print("The material index is %f (Temperature of %d K, Wavelength %f um)\n "%(n_index_T_wave,t,wave))
print("############################################################################")
print("The coefficient refractive index is:")
print coefficient_data
print("############################################################################")
print("The coefficient refractive index for ZEMAX input: ")
print coefficient_data_zemax
print("############################################################################")

coefficient_data2 = np.array([1.25493787E+001,-1.88270543E+000,-1.23832900E+004,9.24436560E-002,9.07375997E-002,1.25490743E+008])
n_index2 = 1
for i in range(0,3):
    n_index2 = n_index2 + coefficient_data2[i]*wave**2/(wave**2-coefficient_data2[i+3])
n_index_T_wave2 = np.sqrt(n_index2)


