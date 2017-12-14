"""
Created on Tue Dec 12 16:53:38 2017

@author: hxji
"""

import numpy as np
from astropy import units as u
from astropy.constants import h,k_B,c
from astropy.modeling.blackbody import blackbody_lambda,blackbody_nu

def planck(data,temp,sr_o,key = 'wave'):
    sr = sr_o*u.sr   ### Setting Steradian 
    temperature = temp * u.K
    if key == 'wave':
        wave = [x*10 for x in data]   # change the wavelength nm to Angstrom
        dw = 1
        d_w = dw*u.AA
        wavelengths = np.arange(wave[0], wave[1],dw) * u.AA

        flux_lam = blackbody_lambda(wavelengths, temperature)
        flux_lam_f = flux_lam*sr
        flux_wat = flux_lam_f.to(u.W/u.cm**2/u.AA)  #  Change the blackbody intensity to "Wats/cm^2/A"
        flux_lam_p = flux_lam_f*wavelengths/(h*c)   #  The number of photons
        flux_lam_p = flux_lam_p.to(u.m**-2/u.AA/u.s)
        total_flux_photon = sum(flux_lam_p)*d_w
    elif key == 'hertz':
        dnu = 1e12
        d_nu = dnu*u.Hz
        nu = np.arange(data[0],data[1],dnu)*u.Hz
        flux_nu = blackbody_nu(nu, temperature)
        flux_nu_f = flux_nu*sr
        flux_wat = flux_nu_f.to(u.W/u.cm**2/u.Hz)  #  Change the blackbody intensity to "Wats/cm^2/A"
        flux_nu_p = flux_nu_f/(h*nu)   #  The number of photons
        flux_nu_p = flux_nu_p.to(u.cm**-2/u.Hz/u.s)   
        total_flux_photon = sum(flux_nu_p)*d_nu
    else:
        print "Please re-input the right key"
    return total_flux_photon,flux_wat


if __name__ == "__main__":    
    temp = 173   # K
    wave = [950,1770]   # nm   1e14 @3000nm,2e14@1500nm
    ### Assumption: the input focal ratio to the detector is F/3
    f_ratio = 3.6
    angle = np.arctan(1/3.6)
    sr = 2*np.pi*(1-np.cos(angle/2))
#    sr = np.pi
    pixel_size = 12*u.micron # um
    ccd_size = [1024,1024]
    collect_area = ccd_size[0]*pixel_size*ccd_size[1]*pixel_size
    c_area = collect_area.to(u.m**2)
#    sr = np.pi
    total_flux_photons,flux_wat = planck(wave,temp,sr,key='wave')  # key: "wave" or "hertz"
    total_p = total_flux_photons*c_area
    print ("The total flux: %e '%s' at the detector (%d*%d@%.1f um) with F/#=%.2f"%(total_p.value,total_p.unit,ccd_size[0],ccd_size[1],pixel_size.value,f_ratio))
    print "The total flux at the reddest wavelength: %e '%s'"%(flux_wat.value[1],flux_wat.unit)    
    print("The total photons with the wavelength range: [%.2f,%.2f]nm is %e %s"%(wave[0],wave[1],total_flux_photons.value,total_flux_photons.unit))