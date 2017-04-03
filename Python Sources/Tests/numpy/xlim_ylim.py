import array
import matplotlib.pyplot as plt
import random
from datetime import date

a = 1970
b = 2012
year = [i for i in range(b-a)]
for n in range (b-a):
    computer_science = random.sample(range(1, 100), (b-a))
    physical_science = random.sample(range(1, 100), (b-a))
print (computer_science)
print ('--------------------------------------------')
print (physical_science)
# Plot the % of degrees awarded to women in Computer Science and the Physical Sciences
plt.plot(year, computer_science, color='red')
plt.plot(year, physical_science, color='blue')

# Add the axis labels
plt.xlabel('Year')
plt.ylabel('Degrees awarded to women (%)')

# Set the x-axis range
#plt.xlim(a, b)

# Set the y-axis range
#plt.ylim(a, b)

# Add a title and display the plot
plt.title('Degrees awarded to women (1990-2010)\nComputer Science (red)\nPhysical Sciences (blue)')
plt.show()

# Save the image as 'xlim_and_ylim.png'
plt.savefig('xlim_and_ylim.png')
