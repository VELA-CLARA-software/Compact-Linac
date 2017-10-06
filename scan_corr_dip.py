import magnet as mag
import get_image as images
import time
import numpy as np
import epics

def get_image(str=''):
    url = 'http://148.79.170.34/mjpg/video.mjpg'
    cam = images.capture_image(url,str, directory='dipole_scan')

def degauss_dipole():
    dipole = mag.magnet('CPL-LVD-PSU-DIP-01')
    degauss_values = [-4,4,-3,3,-2,2,-1,1,-0.5,0.5,-0.25,0.25,-0.1,0]
    for v in degauss_values:
        dipole.set(v)
        time.sleep(1)

def scan_corrector_dipole(dipole_resolution=0.25, corrector_resolution=0.25):
    corr = mag.magnet('CPL-LVD-PSU-COR-01', tolerance=0.025)
    corr_scan_values = np.arange(-3.5,3.5,corrector_resolution)
    dip = mag.magnet('CPL-LVD-PSU-DIP-01')
    dip_scan_values = np.arange(-4.,4.,dipole_resolution)
    scan_values = zip(*[dip_scan_values,corr_scan_values])
    interlockPV = epics.PV('CPL-RF-MOD-01:SETPULSE')

    # degauss_dipole()
    for d in dip_scan_values:
        for c in corr_scan_values:
            dip.set(d)
            corr.set(c)
            time.sleep(1)
            print interlockPV.get()
            if interlockPV.get() == 1:
                get_image('dip='+str(d)+'_corr='+str(c))
            else:
                while not interlockPV.get() == 1:
                    print 'Interlock DOWN!!'
                    time.sleep(1)
        # time.sleep(1)

scan_corrector_dipole()
