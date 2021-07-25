import numpy as np
import matplotlib.pyplot

weighted_day_file = 'portfolios/weighted_day.npy'
weighted_value_file = 'portfolios/weighted_value.npy'

equal_day_file = 'portfolios/equal_day.npy'
equal_value_file = 'portfolios/equal_value.npy'

spy_day_file = 'portfolios/spy_day.npy'
spy_value_file = 'portfolios/spy_value.npy'

weighted_day_array = np.load(weighted_day_file, allow_pickle=True)
weighted_value_array = np.load(weighted_value_file, allow_pickle=True)
matplotlib.pyplot.plot(weighted_day_array, weighted_value_array, 'c')

equal_spy_day_array = np.load(equal_day_file, allow_pickle=True)
equal_spy_value_array = np.load(equal_value_file, allow_pickle=True)
matplotlib.pyplot.plot(equal_spy_day_array, equal_spy_value_array, 'b')

spy_day_array = np.load(spy_day_file, allow_pickle=True)
spy_value_array = np.load(spy_value_file, allow_pickle=True)
matplotlib.pyplot.plot(spy_day_array, spy_value_array, 'r')

matplotlib.pyplot.show()