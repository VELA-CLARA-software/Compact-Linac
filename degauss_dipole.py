import time
import magnet as mag
import progressbar

def degauss_dipole():
    dipole = mag.magnet('CPL-LVD-PSU-DIP-01')
    degauss_values = [-4,4,-3,3,-2,2,-1,1,-0.5,0.5,-0.25,0.25,-0.1,0]
    with progressbar.ProgressBar(max_value=len(degauss_values)) as bar:
        for v in degauss_values:
            dipole.set(v)
            bar.update(degauss_values.index(v))
            time.sleep(1)

degauss_dipole()
