import matplotlib.pyplot as plt
import numpy as np

# make data
x = np.linspace(0, 10, 100)
y = 4 + 1 * np.sin(2 * x)

# plot

plt.plot(x, y, linewidth=2.0)
plt.title('stress')
plt.legend('i dont know')
plt.show()
