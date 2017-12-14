# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 00:01:55 2017

@author: hxji
"""

from numpy import *
import os, glob, sys
import matplotlib.pyplot as plt
import matplotlib.transforms
import numpy as np
from matplotlib.transforms import offset_copy
import mpldatacursor.datacursor as Datacursor
from scipy import interpolate 
from scipy import integrate

def string_list_to_float_list(x):
    '''
    Convert a list of strings to a list of floats, where a string value of '-' is mapped to a
    floating point value of -1.0, and an empty input list produces a length-10 list of -1.0's.

    Parameters
    ----------
    x : list
        The list of strings to convert

    Returns
    -------
    res : list of floats
        The converted results.
    '''
    npts = len(x)
    if (npts == 0) or ((npts == 1) and (x[0].strip() == '-')):
        return([-1.0]*10)

    res = []
    for a in x:
        if (a.strip() == '-'):
            res.append(-1.0)
        else:
            res.append(float(a))

    return(res)



def glass_data_cube(catalog,glass):
    dir = r'C:\Users\hxji\Documents\Zemax\Glasscat'
    path = os.path.join(dir,catalog)
    filename = path + '.agf'
    f = open(filename, 'r')
    a= f.readlines()
    glass_catalog = {}
    
    for line in a:
        if not line.strip(): continue
        if line.startswith('CC '): continue
        if line.startswith('NM '):
            glass_catalog_glass_IT = []
            nm = line.split()
            glassname = nm[1]
            glass_catalog[glassname] = {}
            glass_catalog[glassname]['dispform'] = int(nm[2])
            glass_catalog[glassname]['nd'] = float(nm[4])
            glass_catalog[glassname]['vd'] = float(nm[5])
            glass_catalog[glassname]['exclude_sub'] = 0 if (len(nm) < 7) else int(nm[6])
            glass_catalog[glassname]['status'] = 0 if (len(nm) < 8) else int(nm[7])
            glass_catalog[glassname]['meltfreq'] = 0 if ((len(nm) < 9) or (nm.count('-') > 0)) else int(nm[8])
    #            IT_m = 0
        elif line.startswith('ED '):
            ed = line.split()
            glass_catalog[glassname]['tce'] = float(ed[1])
            glass_catalog[glassname]['density'] = float(ed[3])
            glass_catalog[glassname]['dpgf'] = float(ed[4])
            glass_catalog[glassname]['ignore_thermal_exp'] = 0 if (len(ed) < 6) else int(ed[5])
        elif line.startswith('CD '):
            cd = line.split()[1:]
            glass_catalog[glassname]['cd'] = [float(a) for a in cd]
        elif line.startswith('TD '):
            td = line.split()[1:]
            glass_catalog[glassname]['td'] = [float(a) for a in td]
        elif line.startswith('OD '):
            od = line.split()[1:]
            od = string_list_to_float_list(od)
            glass_catalog[glassname]['relcost'] = od[0]
            glass_catalog[glassname]['cr'] = od[1]
            glass_catalog[glassname]['fr'] = od[2]
            glass_catalog[glassname]['sr'] = od[3]
            glass_catalog[glassname]['ar'] = od[4]
            if (len(od) == 6):
                glass_catalog[glassname]['pr'] = od[5]
            else:
                glass_catalog[glassname]['pr'] = -1.0
        elif line.startswith('LD '):
            ld = line.split()[1:]
            glass_catalog[glassname]['ld'] = [float(a) for a in ld]
        elif line.startswith('IT '):
            it = line.split()[1:]
            it_row = [float(a) for a in it]
            if ('it' not in glass_catalog[glassname]):
                glass_catalog[glassname]['IT'] = {}
            glass_catalog[glassname]['IT']['wavelength'] = it_row[0]
            glass_catalog[glassname]['IT']['transmission'] = it_row[1]
            glass_catalog[glassname]['IT']['thickness'] = it_row[2]
            glass_catalog_glass_IT.append(it_row)
            glass_catalog[glassname]['IT']['absorb'] = glass_catalog_glass_IT
    f.close()
    if glass not in glass_catalog.keys():
        glass_data = []
        print "no such glass"
    else:
        glass_data = glass_catalog[glass]
    return glass_data

def glass_index(catalog,glass,wave):
    glass_data = glass_data_cube(catalog,glass)
    dispform = glass_data['dispform']
    cd = glass_data['cd']
    ld = glass_data['ld']
    w = wave # unit: um
    if (dispform == 1):
        formula_rhs = cd[0] + (cd[1] * w**2) + (cd[2] * w**-2) + (cd[3] * w**-4) + (cd[4] * w**-6) + (cd[5] * w**-8)
        indices = sqrt(formula_rhs)
    elif (dispform == 2): ## Sellmeier1
        formula_rhs = (cd[0] * w**2 / (w**2 - cd[1])) + (cd[2] * w**2 / (w**2 - cd[3])) + (cd[4] * w**2 / (w**2 - cd[5]))
        indices = sqrt(formula_rhs + 1.0)
    elif (dispform == 3): ## Herzberger
        L = 1.0 / (w**2 - 0.028)
        indices = cd[0] + (cd[1] * L) + (cd[2] * L**2) + (cd[3] * w**2) + (cd[4] * w**4) + (cd[5] * w**6)
    elif (dispform == 4): ## Sellmeier2
        formula_rhs = cd[0] + (cd[1] * w**2 / (w**2 - (cd[2])**2)) + (cd[3] * w**2 / (w**2 - (cd[4])**2))
        indices = sqrt(formula_rhs + 1.0)
    elif (dispform == 5): ## Conrady
        indices = cd[0] + (cd[1] / w) + (cd[2] / w**3.5)
    elif (dispform == 6): ## Sellmeier3
        formula_rhs = (cd[0] * w**2 / (w**2 - cd[1])) + (cd[2] * w**2 / (w**2 - cd[3])) + \
                      (cd[4] * w**2 / (w**2 - cd[5])) + (cd[6] * w**2 / (w**2 - cd[7]))
        indices = sqrt(formula_rhs + 1.0)
    elif (dispform == 7): ## HandbookOfOptics1
        formula_rhs = cd[0] + (cd[1] / (w**2 - cd[2])) - (cd[3] * w**2)
        indices = sqrt(formula_rhs)
    elif (dispform == 8): ## HandbookOfOptics2
        formula_rhs = cd[0] + (cd[1] * w**2 / (w**2 - cd[2])) - (cd[3] * w**2)
        indices = sqrt(formula_rhs)
    elif (dispform == 9): ## Sellmeier4
        formula_rhs = cd[0] + (cd[1] * w**2 / (w**2 - cd[2])) + (cd[3] * w**2 / (w**2 - cd[4]))
        indices = sqrt(formula_rhs)
    elif (dispform == 10): ## Extended1
        formula_rhs = cd[0] + (cd[1] * w**2) + (cd[2] * w**-2) + (cd[3] * w**-4) + (cd[4] * w**-6) + \
                      (cd[5] * w**-8) + (cd[6] * w**-10) + (cd[7] * w**-12)
        indices = sqrt(formula_rhs)
    elif (dispform == 11): ## Sellmeier5
        formula_rhs = (cd[0] * w**2 / (w**2 - cd[1])) + (cd[2] * w**2 / (w**2 - cd[3])) + \
                      (cd[4] * w**2 / (w**2 - cd[5])) + (cd[6] * w**2 / (w**2 - cd[7])) + \
                      (cd[8] * w**2 / (w**2 - cd[9]))
        indices = sqrt(formula_rhs + 1.0)
    elif (dispform == 12): ## Extended2
        formula_rhs = cd[0] + (cd[1] * w**2) + (cd[2] * w**-2) + (cd[3] * w**-4) + (cd[4] * w**-6) + \
                      (cd[5] * w**-8) + (cd[6] * w**4) + (cd[7] * w**6)
        indices = sqrt(formula_rhs)
    else:
        print('Dispersion formula #' + str(dispform) + ' (for glass=' + glass + ' in catalog=' + catalog + ') is not a valid choice.')
        indices = ones_like(w) * nan
        raise ValueError('Dispersion formula #' + str(dispform) + ' (for glass=' + glass + ' in catalog=' + catalog + ') is not a valid choice.')
    if wave < ld[0] or wave > ld[1]:
        print "Wavelength is not in the Zemax setting range"
    return indices
def glass_dispersion(catalog,glass,wave):
    d_wave = 0.001
    n1 = glass_index(catalog,glass,wave)
    n2 = glass_index(catalog,glass,wave+d_wave)
    dn = abs(n2-n1)
    gla_dis = dn/d_wave
    return gla_dis

def glass_IT_data(catalog,glass,waverange,thickness):
    glass_data = glass_data_cube(catalog,glass)
    ld = glass_data['ld']
    print ld
    wave_min = waverange[0]
    wave_max = waverange[1]
    if wave_min < ld[0] or wave_max > ld[1]:
        print "Wavelength input is not in the required range"
    data_num = 1000
    abs_data = glass_data['IT']['absorb']
    wave_abs = []
    gls_abs = []
    thick_abs = []
    for i in range(0,len(abs_data)):
        wave_abs.append(abs_data[i][0])
        gls_abs.append(abs_data[i][1])
        thick_abs.append(abs_data[i][2])
    f = interpolate.interp1d(wave_abs,gls_abs)
    wave_new = np.linspace(wave_min, wave_max, data_num)  
    eff_abs = f(wave_new)**(thickness/thick_abs[0])
    return eff_abs

if (__name__ == '__main__'):
    bb = glass_data_cube('CDGM','H-K9L')
    cc = glass_index('CDGM','H-K9L',0.55) # 
    dd = glass_IT_data('CDGM','H-K9L',[0.37,1.7],10)
    ee = glass_dispersion('CDGM','H-K9L',0.55)