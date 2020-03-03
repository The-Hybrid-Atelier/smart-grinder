import matplotlib.pyplot as plt

data = ""


with open("testData.dat", 'r') as f:
    data = f.read()



x = []
for point in data.split(",")[:-1]:
    x.append(int(point))



plt.plot(range(len(x)), x)
plt.show()