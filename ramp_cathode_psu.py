import epics
import time
import progressbar

rampPV = epics.PV('CPL-LVD-PSU-20KV-01:SI')
ramprange = range(10000,17000,500);

with progressbar.ProgressBar(max_value=len(ramprange)) as bar:
  for i in ramprange:
    time.sleep(30)
    rampPV.put(i)
    bar.update(ramprange.index(i))
