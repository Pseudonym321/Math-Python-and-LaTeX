import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib as mpl

my_figure, axis1 = plt.subplots(figsize=(5,2.7), layout='constrained')
axis1.set_title("My Title")
axis1.set_xlabel("x")
axis1.set_ylabel("y")
x = np.linspace(-5,-1,20)
axis1.plot(x, math.e**(1/x))
x = np.linspace(1,5,20)
axis1.plot(x, math.e**(1/x))


plt.show()