import matplotlib.pyplot as plt
import numpy as np

# Define the lists of location values for each website response
myimage = ['paris', 'paris', 'paris']
ringsofpower_vid = ['lahore', 'paris', 'nyc']
ringsofpower_aud = ['lahore', 'nyc', 'nyc']
samaritan = ['northpole', 'northpole', 'paris', 'lahore', 'mars', 'mars']
harlem = ['northpole', 'northpole', 'paris', 'lahore', 'mars', 'mars']

# Define the time series for the x-axis
max_time = max(len(ringsofpower_vid), len(ringsofpower_aud), len(myimage), len(samaritan), len(harlem))
time = range(max_time)

# Define the desired order of the locations on the y-axis
y_order = ['lahore', 'nyc', 'paris', 'northpole', 'mars']

# Define the vertical offset for each website response
offset = [-0.10, -0.05, 0, 0.05, 0.10]  # Adjust as needed

# Create a figure and axis
fig, ax = plt.subplots()

# Create a numerical mapping for the y-axis values
y_mapping = {loc: i for i, loc in enumerate(y_order)}

# Plot the location values for each website response with vertical offset
ax.plot(time[:len(myimage)], [y_mapping[loc] + offset[0] for loc in myimage], marker='o', label='My Content', linewidth=2, markersize=8)
ax.plot(time[:len(ringsofpower_vid)], [y_mapping[loc] + offset[1] for loc in ringsofpower_vid], marker='o', label='Ring of Power (Video)', linewidth=2, markersize=8)
ax.plot(time[:len(ringsofpower_aud)], [y_mapping[loc] + offset[2] for loc in ringsofpower_aud], marker='o', label='Ring of Power (Audio)', linewidth=2, markersize=8)
ax.plot(time[:len(samaritan)], [y_mapping[loc] + offset[3] for loc in samaritan], marker='o', label='Samaritan', linewidth=2, markersize=8)
ax.plot(time[:len(harlem)], [y_mapping[loc] + offset[4] for loc in harlem], marker='o', label='Harlem', linewidth=2, markersize=8)

# Set the x-axis and y-axis labels
ax.set_xlabel('Time')
ax.set_ylabel('Location', fontsize=12)

# Set the y-axis tick positions and labels with increased font size
ax.set_yticks(range(len(y_order)))
ax.set_yticklabels(y_order, fontsize=18)

# Set the title of the plot
ax.set_title('Location Changes for Website Responses')

# Add a legend with a white background and increased font size
ax.legend(facecolor='white', fontsize=8)

# Adjust the figure size and spacing between subplots
fig.set_size_inches(8, 4)
fig.tight_layout()

# Adjust the limits of the x-axis and y-axis to remove excess space
ax.set_xlim(0, max_time - 1)
ax.set_ylim(-0.5, len(y_order) - 0.5)

# Add gridlines for better readability
ax.grid(True, linestyle='--', alpha=0.5)

# Display the plot
plt.show()
