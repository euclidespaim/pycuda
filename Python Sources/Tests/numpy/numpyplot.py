import matplotlib.pyplot as plt

t = 5
temperature = 7
dewpoint = 3


plt.plot(t, temperature, 'red')
plt.plot(t, dewpoint, 'blue') #appears on same axe
plt.xlabel('date')
plt.title('Temperature & Dew Point')

plt.show()



