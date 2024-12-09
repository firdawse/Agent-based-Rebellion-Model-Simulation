# import pandas as pd
# import matplotlib.pyplot as plt

# # Load the phase diagram data
# phase_df = pd.read_csv("phase_diagram_data.csv", index_col=0)

# # Convert DataFrame to a 2D array for plotting
# legitimacy_vals = phase_df.index.values
# cop_density_vals = phase_df.columns.astype(float).values
# phase_matrix = phase_df.values

# # Plotting the phase diagram
# plt.figure(figsize=(10, 8))
# plt.contourf(legitimacy_vals, cop_density_vals, phase_matrix.T, levels=20, cmap='RdYlBu', alpha=0.8)
# plt.colorbar(label='Average Proportion of Active Rebels')
# plt.xlabel('Cop Density')
# plt.ylabel('Government Legitimacy')
# plt.title('Phase Diagram of Civil Violence Model')
# plt.grid(True, linestyle='--', alpha=0.5)
# plt.show()


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))


# Load your CSV file
file_path = 'Scenario3__experiment3_grid_100.csv'  # Replace with your file name
data = pd.read_csv(file_path, index_col=0)  # Assuming legitimacy is the index

# Convert to a NumPy array for easy plotting
legitimacy_vals = data.index.astype(float).to_numpy()  # Rows (legitimacy values)
cop_density_vals = data.columns.astype(float).to_numpy()  # Columns (cop density values)
rebellion_means = data.to_numpy()  # The grid of rebellion values
rebellion_means = scaler.fit_transform(rebellion_means)


# Define thresholds for phases
high_rebellion_threshold = 0.7
moderate_rebellion_threshold = 0.3

# Create the phase plot
plt.figure(figsize=(10, 8))

# Add contours to define the phases
contour = plt.contour(
     legitimacy_vals,cop_density_vals, rebellion_means.T,
    levels=[moderate_rebellion_threshold, high_rebellion_threshold],
    colors=['black', 'red'], linewidths=2
)

# Label contours
plt.clabel(contour, inline=True, fontsize=10, fmt={
    moderate_rebellion_threshold: 'Moderate Rebellion Boundary',
    high_rebellion_threshold: 'High Rebellion Boundary'
})

# Add a filled contour for better visualization
plt.contourf(
    legitimacy_vals, cop_density_vals,  rebellion_means.T,
    levels=[0, moderate_rebellion_threshold, high_rebellion_threshold, 1],
    colors=['lightblue', 'orange', 'red'], alpha=0.7
)

# Add a color bar
plt.colorbar(label='Mean Rebellion Proportion')

# Label axes and title
plt.xlabel('Government Legitimacy')
plt.ylabel('Cop Density')
plt.title('Phase Diagram of Rebellion Dynamics')

# Add annotations for phases
plt.text(0.02, 0.9, 'Stable Phase', fontsize=12, color='blue', ha='center', va='center')
plt.text(0.06, 0.5, 'Moderate Rebellion Phase', fontsize=12, color='orange', ha='center', va='center')
plt.text(0.08, 0.2, 'High Rebellion Phase', fontsize=12, color='red', ha='center', va='center')

plt.grid(alpha=0.5)
plt.show()