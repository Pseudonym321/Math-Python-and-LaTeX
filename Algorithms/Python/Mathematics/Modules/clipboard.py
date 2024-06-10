import matplotlib.pyplot as plt
import numpy as np
import cmath

i_array = np.array([n for n in np.linspace(-5,5,50)])
o_array = np.array([cmath.sqrt(5**2-n**2) for n in i_array])

my_figure, axis1 = plt.subplots()
axis1.plot(i_array, o_array)
plt.show()