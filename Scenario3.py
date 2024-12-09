import numpy as np
import pandas as pd
from Model import EpsteinCivilViolence
import matplotlib.pyplot as plt

# Parameters for the simulation
legitimacy_values = np.linspace(0, 1, 11)  # 0.0 to 1.0 in steps of 0.1
cop_density_values = np.linspace(0.01, 0.1, 10)  # 0.01 to 0.1 in steps of 0.01
citizen_density = 0.7  # Fixed
citizen_vision = 7
cop_vision = 7
max_jail_term = 1000
active_threshold = 0.1
arrest_prob_constant = 2.3
movement = True
max_iters = 200
grid_width = 100
grid_height = 100

# Data storage
phase_results = []

# Simulate across the grid of legitimacy and cop density
for legitimacy in legitimacy_values:
    row_results = []
    for cop_density in cop_density_values:
        print(f"Running simulation for legitimacy: {legitimacy}, cop density: {cop_density}")
        
        # Create the model
        model = EpsteinCivilViolence(
            width=grid_width,
            height=grid_height,
            citizen_density=citizen_density,
            cop_density=cop_density,
            citizen_vision=citizen_vision,
            cop_vision=cop_vision,
            legitimacy=legitimacy,
            max_jail_term=max_jail_term,
            active_threshold=active_threshold,
            arrest_prob_constant=arrest_prob_constant,
            movement=movement,
            max_iters=max_iters,
        )
        
        # Run the simulation
        for _ in range(max_iters):
            model.step()
        
        # Collect the average proportion of active rebels
        data = model.datacollector.get_model_vars_dataframe()
        avg_active_proportion = (data["active"] / (grid_width * grid_height * citizen_density)).max()
        row_results.append(avg_active_proportion)
    
    phase_results.append(row_results)

# Convert results to a DataFrame for visualization
phase_df = pd.DataFrame(phase_results, index=legitimacy_values, columns=cop_density_values)

# Save the results for later analysis
phase_df.to_csv("Scenario3__experiment3_grid_100.csv")
print("Phase diagram data saved to 'phase_diagram_data.csv'")