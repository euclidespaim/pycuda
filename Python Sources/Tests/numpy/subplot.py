# Create a figure with 1x2 subplot and make the left subplot active
import matplotlib.pyplot as plt

# Plot in blue the % of degrees awarded to women in the Physical Sciences
plt.plot(year, physical_sciences, color='blue')
plt.title('Physical Sciences')

# Make the right subplot active in the current 1x2 subplot grid
plt.subplot(1, 2, 1)

# Plot in red the % of degrees awarded to women in Computer Science
plt.plot(year, computer_science, color='red')
plt.title('Computer Science')

plt.subplot(1, 2, 2)
plt.plot(year, physical_sciences, color='blue')
plt.title('Physical Science')

# Use plt.tight_layout() to improve the spacing between subplots
plt.tight_layout()
plt.show()
