# Import matplotlib.pyplot
import matplotlib.pyplot as plt

physical_sciences = [i for i in range(10)]
computer_science = [i for i in range(10)]
year = [i for i in range(2016)]

# Plot in blue the % of degrees awarded to women in the Physical Sciences
plt.plot(physical_sciences, year, 'blue')

# Plot in red the % of degrees awarded to women in Computer Science
plt.plot(computer_science, year, 'red')


# Display the plot
plt.show()
