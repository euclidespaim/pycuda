import random
import matplotlib.pyplot as plt
import numpy

a = 1970
b = 2012
year =  ([i for i in range(b - a)])

computer_science = random.sample(range(1, 100), (b-a))
physical_science = random.sample(range(1, 100), (b-a))
print (computer_science)
print ('--------------------------------------------')
print (physical_science)


# Plot with legend as before
plt.plot(year, computer_science, color='red', label='Computer Science')
plt.plot(year, physical_science, color='blue', label='Physical Sciences')
plt.legend(loc='bottom right')

# Compute the maximum enrollment of women in Computer Science: cs_max
cs_max = max(computer_science)

# Calculate the year in which there was maximum enrollment of women in Computer Science: yr_max
yr_max = year[numpy.argmax(computer_science)]
# Add a black arrow annotation
plt.annotate('Maximun', xy=(yr_max, cs_max), xytext=(yr_max+5, cs_max+5), arrowprops=dict(facecolor='black'))

# Add axis labels and title
plt.xlabel('Year')
plt.ylabel('Enrollment (%)')
plt.title('Undergraduate enrollment of women')
plt.show()
