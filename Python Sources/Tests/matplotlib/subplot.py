# Create a figure with 1x2 subplot and make the left subplot active
import matplotlib.pyplot as plt
import random

a = 1970
b = 2012
year =  ([i for i in range(b - a)])

computer_science = random.sample(range(1, 100), (b-a))
physical_science = random.sample(range(1, 100), (b-a))
print (computer_science)
print ('--------------------------------------------')
print (physical_science)

# Plot in blue the % of degrees awarded to women in the Physical Sciences
plt.plot(year, physical_science, color='blue')
plt.title('Physical Sciences')

# Make the right subplot active in the current 1x2 subplot grid
plt.subplot(2, 1, 1)

# Plot in red the % of degrees awarded to women in Computer Science
plt.plot(year, computer_science, color='red')
plt.title('Computer Science')

plt.subplot(2, 1, 2)
plt.plot(year, physical_science, color='blue')
plt.title('Physical Science')

# Use plt.tight_layout() to improve the spacing between subplots
plt.tight_layout()
plt.show()
