import matplotlib.pyplot as plt
import random

import numpy

a = 1970
b = 2012
year =  ([i for i in range(b - a)])

computer_science = random.sample(range(1, 100), (b-a))
physical_sciences = random.sample(range(1, 100), (b-a))
health = random.sample(range(1, 100), (b-a))
education = random.sample(range(1, 100), (b-a))
print (computer_science)
print ('--------------------------------------------')
print (physical_sciences)

# Set the style to 'ggplot'
plt.style.use('ggplot')

# Create a figure with 2x2 subplot layout
plt.subplot(2, 2, 1)

# Plot the enrollment % of women in the Physical Sciences
plt.plot(year, physical_sciences, color='blue')
plt.title('Physical Sciences')

# Plot the enrollment % of women in Computer Science
plt.subplot(2, 2, 2)
plt.plot(year, computer_science, color='red')
plt.title('Computer Science')

# Add annotation
cs_max = max(computer_science)
yr_max = year[numpy.argmax(computer_science)]
plt.annotate('Maximum', xy=(yr_max, cs_max), xytext=(yr_max-1, cs_max-10), arrowprops=dict(facecolor='black'))

# Plot the enrollmment % of women in Health professions
plt.subplot(2, 2, 3)
plt.plot(year, health, color='green')
plt.title('Health Professions')

# Plot the enrollment % of women in Education
plt.subplot(2, 2, 4)
plt.plot(year, education, color='orange')
plt.title('Education')

# Improve spacing between subplots and display them
plt.tight_layout()
plt.show()
