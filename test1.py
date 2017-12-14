# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 22:09:36 2017

@author: hxji
"""
#import numpy as np
#from nplanck import planck
#import astropy.units as u
#
#temp = 173   # K
#wave = [950,1770]   # nm   1e14 @3000nm,2e14@1500nm
#### Assumption: the input focal ratio to the detector is F/3
#f_ratio = 3.6
#angle = np.arctan(1/f_ratio)
#sr = 2*np.pi*(1-np.cos(angle/2))
##    sr = np.pi
#pixel_size = 12*u.micron # um
#ccd_size = [1024,1024]
#collect_area = ccd_size[0]*pixel_size*ccd_size[1]*pixel_size
#c_area = collect_area.to(u.m**2)
##    sr = np.pi
#total_flux_photons,flux_wat = planck(wave,temp,sr,key='wave')  # key: "wave" or "hertz"
#total_p = total_flux_photons*c_area
#print ("The total flux: %e '%s' at the detector (%d*%d@%.1f um) with F/#=%.2f"%(total_p.value,total_p.unit,ccd_size[0],ccd_size[1],pixel_size.value,f_ratio))
#print "The total flux at the reddest wavelength: %e '%s'"%(flux_wat.value[1],flux_wat.unit)    
#print("The total photons with the wavelength range: [%.2f,%.2f]nm is %e %s"%(wave[0],wave[1],total_flux_photons.value,total_flux_photons.unit))

############################################################################
from PyAstronomy import pyasl

## Wavelength in Angstrom
#wvl = 4000.
## Flux in erg/s
#flux = 1.5e-14
#
## Convert into photons
#photons = pyasl.flux2photons(wvl, flux)
#
## How many photons is this?
#print("%g erg/s at %g A correspond to %g photons/s" \
#        % (flux, wvl, photons))
#
## Converting back
#flux2 = pyasl.photons2flux(wvl, photons)
#
#print("%g photons/s at %g A correspond to %g erg/s" \
#        % (photons, wvl, flux2))


from PyAstronomy import pyasl
import numpy as np
import matplotlib.pylab as plt
# Import six for Python 2/3 compatibility
import six

# Get transmission curve object
tcs = pyasl.TransmissionCurves()

# Add passbands from Spitzer IRAC
tcs.addSpitzerIRACPassbands()

print("Available bands: ", tcs.availableBands())

# Wavelength axis
wvl = np.linspace(3000, 10000, 10000)

# Plot transmission curves for Bessel b, v, and r bands
for (b, c) in six.iteritems({"b":"b", "v":"k", "r":"r"}):
  tc = tcs.getTransCurve("Bessel " + b)
  trans = tc(wvl)
  plt.plot(wvl, trans, c+'-', label="Bessel " + b)

# Plot transmission curves for Johnson U, B, and V bands
for (b, c) in six.iteritems({"U":"m", "B":"b", "V":"k"}):
  tc = tcs.getTransCurve("Johnson " + b)
  trans = tc(wvl)
  plt.plot(wvl, trans, c+'--', label="Johnson " + b)

plt.legend()
plt.xlabel("Wavelength [$\AA$]")
plt.ylabel("Transmission")
plt.show()


## Create Planck spectrum ...
#wvl = np.arange(3000., 10000., 1.0)
#spec = pyasl.planck(T=5777., lam=wvl*1e-10)
## ... and convolve with Johnson V band
#vbs = tcs.convolveWith(wvl, spec, "Johnson V")
#
#plt.plot(wvl, spec, 'b-', label='Input spectrum')
#plt.plot(wvl, vbs, 'r--', label='Convolution with Johnson V band')
#plt.legend()
#plt.show()


#pyasl.listObservatories()
#print(pyasl.observatory("kpno"))


# Instantiate the access class
epl = pyasl.ExoplanetsOrg()


nexa = pyasl.NasaExoplanetArchive()

# See what information is available
cols = nexa.availableColumns()
print()

# Get all information for planet 'wasp-12 b'
# By default, the search is case-insensitive
print("Entry of Wasp-12 b")
print(nexa.selectByPlanetName("Wasp-12 b"))

print()
# Get all data and plot ra vs. dec
dat = nexa.getAllData()
plt.plot(dat.ra, dat.dec, 'b.')
plt.show()