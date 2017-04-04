import random
import matplotlib.pyplot as plt

a = 1970
b = 2012
year =  ([i for i in range(b - a)])

computer_science = random.sample(range(1, 100), (b-a))
physical_science = random.sample(range(1, 100), (b-a))
print (computer_science)
print ('--------------------------------------------')
print (physical_science)


# Specify the label 'Computer Science'
plt.plot(year, computer_science, color='red', label='Computer Science')

# Specify the label 'Physical Sciences'
plt.plot(year, physical_science, color='blue', label='Physical Sciences')

# Add a legend at the lower center
plt.legend(loc='lower center')

# Add axis labels and title
plt.xlabel('Year')
plt.ylabel('Enrollment (%)')
plt.title('Undergraduate enrollment of women')
plt.show()
