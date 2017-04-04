# Create a figure with 2x2 subplot layout and make the top left subplot active
import matplotlib.pyplot as plt
import random

a = 1970
b = 2012
year =  ([i for i in range(b - a)])

computer_science = random.sample(range(1, 100), (b-a))
physical_science = random.sample(range(1, 100), (b-a))
health = random.sample(range(1, 100), (b-a))
education = random.sample(range(1, 100), (b-a))

print (computer_science)
print ('--------------------------------------------')
print (physical_science)
print ('--------------------------------------------')
print (health)
print ('--------------------------------------------')
print (education)


# Plot in red the % of degrees awarded to women in Computer Science
plt.plot(year, computer_science, color='red')
plt.title('Computer Science')
plt.subplot(2, 2, 1)# Make the bottom left subplot active in the current 2x2 subplot grid

# Plot in red the % of degrees awarded to women in Computer Science
plt.plot(year, computer_science, color='red')
plt.title('Computer Science')
plt.subplot(2, 2, 2)# Make the bottom left subplot active in the current 2x2 subplot grid

# Plot in blue the % of degrees awarded to women in the Physical Sciences
plt.plot(year, physical_science, color='blue')
plt.title('Physical Sciences')
plt.subplot(2, 2, 3)# Make the top right subplot active in the current 2x2 subplot grid


# Plot in green the % of degrees awarded to women in Health Professions
plt.plot(year, health, color='green')
plt.title('Health Professions')
plt.subplot(2, 2, 4)# Make the bottom right subplot active in the current 2x2 subplot grid


# Plot in yellow the % of degrees awarded to women in Education
plt.plot(year, education, color='yellow')
plt.title('Education')
plt.subplot(2, 2, 4)# Make the bottom right subplot active in the current 2x2 subplot grid

# Improve the spacing between subplots and display them
plt.tight_layout()
plt.show()
