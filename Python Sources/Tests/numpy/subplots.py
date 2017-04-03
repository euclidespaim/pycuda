# Create a figure with 2x2 subplot layout and make the top left subplot active
import matplotlib.pyplot

# Plot in blue the % of degrees awarded to women in the Physical Sciences
plt.plot(year, physical_sciences, color='blue')
plt.title('Physical Sciences')

# Make the top right subplot active in the current 2x2 subplot grid
plt.subplot(2, 2, 1)


# Plot in red the % of degrees awarded to women in Computer Science
plt.plot(year,computer_science, color='red')
plt.title('Computer Science')

# Make the bottom left subplot active in the current 2x2 subplot grid
plt.subplot(2, 2, 2)

# Plot in green the % of degrees awarded to women in Health Professions
plt.plot(year, health, color='green')
plt.title('Health Professions')

# Make the bottom right subplot active in the current 2x2 subplot grid
plt.subplot(2, 2, 3)

# Plot in yellow the % of degrees awarded to women in Education
plt.plot(year, education, color='yellow')
plt.title('Education')
plt.subplot(2, 2, 4)

# Improve the spacing between subplots and display them
plt.tight_layout()
plt.show()
