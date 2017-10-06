import epics
import time

class magnet(object):

    def __init__(self, magnetname, tolerance=0.01):
        super(magnet, self).__init__()
        self.magnetSI = epics.PV(magnetname+':SI')
        self.magnetRI = epics.PV(magnetname+':RI')
        self.tolerance = tolerance

    def get(self):
        self.magnetSI.get()

    def set(self, value):
        self.magnetSI.put(value)
        while not self.isSettled(self.tolerance):
            # print self.magnetRI.get(), ' ', self.magnetSI.get(), ' ratio = ', self.ratio()
            time.sleep(0.1)

    def ratio(self):
        if self.magnetSI.get() == 0:
            return 1+self.magnetRI.get()
        else:
            return self.magnetRI.get() / self.magnetSI.get()

    def isSettled(self, tol):
        return True if self.ratio() > (1-tol) and self.ratio() < (1+tol) else False
