import numpy as np
import matplotlib.pyplot

day_file = 'portfolios/day_array_500.npy'
value_file = 'portfolios/value_array_500.npy'

day_array = np.load(day_file, allow_pickle=True)
value_array = np.load(value_file, allow_pickle=True)

matplotlib.pyplot.plot(day_array, value_array)
matplotlib.pyplot.show()