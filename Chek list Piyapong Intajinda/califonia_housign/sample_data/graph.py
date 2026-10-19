import matplotlib.pyplot as plt
import random
xs = []
ys = []
random.seed(2)
for i in range(10):
    x = i + 1
    y = random.randint(0, 100)
    xs.append(x)
    ys.append(y)

print(xs)
print(ys)


plt.scatter(xs, ys)
plt.plot(xs, ys, color='red')
plt.show()