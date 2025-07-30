import numpy as np
from RsSmw import *
import analizator
import generator

generator.com_check()
analizator.com_prep()
analizator.com_check()

init_frequency = int(24.25E9)
end_frequency = int(27.5E9)
scope = np.arange(init_frequency, end_frequency+50E6, 50E6)
for i in scope:
    generator.meas_prep(True, enums.FreqMode.CW, 15, i)
    analizator.meas_prep(i, int(1E6), "MAXHold ", -35, "10000 Hz")
    analizator.trace_get()

analizator.close()
print('Program successfully ended.')
exit()




