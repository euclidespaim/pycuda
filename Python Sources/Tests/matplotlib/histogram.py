import matplotlib.pyplot as plt
import random

life_exp = random.randint(1,120)

# Build histogram with 5 bins
plt.hist(life_exp, bins = 5)
plt.hist(life_exp, bins = 20)

# Show and clean up plot
plt.show()
plt.clf()

# Build histogram with 20 bins


# Show and clean up again
plt.show()
plt.clf()
