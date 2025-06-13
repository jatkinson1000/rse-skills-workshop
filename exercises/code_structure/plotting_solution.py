import matplotlib.pyplot as plt
import numpy as np

# Styles for markers and lines
colors = ['green', 'blue', 'purple', 'red']
linestyles = ['--', '-', '-.', ':']
markers = ['o', 'x', 'v', '*']

# Function to create a subplot in a 4x4 grid
def plotting_2x2(array, position):
	x = np.array([0, 1, 2, 3])
	plt.subplot(2, 2, position)
	plt.plot(x, array, color = colors[i], linestyle=linestyles[i], marker=markers[i])
	plt.xlabel('x')
	plt.ylabel('y')

# Define value arrays for plotting
arrays = np.zeros((4,4))
arrays[0] = np.array([3, 8, 1, 10])
arrays[1] = np.array([10, 20, 30, 40])
arrays[2] = np.array([5, 11, 14, 20])
arrays[3] = np.array([40, 30, 20, 10])

# Iterate over arrays for plotting
for i in range(4):
	plotting_2x2(arrays[i], i+1)

# Render the plot
plt.show()


