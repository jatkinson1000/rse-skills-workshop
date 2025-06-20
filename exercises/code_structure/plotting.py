import matplotlib.pyplot as plt
import numpy as np

#plot 1:
x = np.array([0, 1, 2, 3])
y = np.array([3, 8, 1, 10])

plt.subplot(2, 2, 1)
plt.plot(x, y, color='green', marker='o', linestyle='--')
plt.xlabel('x')
plt.ylabel('y')

#plot 2:
x = np.array([0, 1, 2, 3])
y = np.array([10, 20, 30, 40])

plt.subplot(2, 2, 2)
plt.plot(x, y, color='blue', marker='x', linestyle='-')
plt.xlabel('x')
plt.ylabel('y')

#plot 3:
x = np.array([0, 1, 2, 3])
y = np.array([5, 11, 14, 20])

plt.subplot(2, 2, 3)
plt.plot(x, y, color='purple', marker='v', linestyle='-.')
plt.xlabel('x')
plt.ylabel('y')

#plot 4:
x = np.array([0, 1, 2, 3])
y = np.array([40, 30, 20, 10])

plt.subplot(2, 2, 4)
plt.plot(x, y, color='red', marker='*', linestyle=':')
plt.xlabel('x')
plt.ylabel('y')


plt.show()


