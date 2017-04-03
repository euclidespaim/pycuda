# Import matplotlib.pyplot
import matplotlib.pyplot as plt

# Plot in blue the % of degrees awarded to women in the Physical Sciences
plt.plot(physical_sciences, year, 'blue')

# Plot in red the % of degrees awarded to women in Computer Science
plt.plot(computer_science, year, 'red')


# Display the plot
plt.show()
