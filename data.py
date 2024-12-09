import pandas as pd
import matplotlib.pyplot as plt

# Load the simulation results
results_df = pd.read_csv("rebellion_legitimacy_analysis.csv")  # Replace with your CSV filename

# Aggregate the data: compute the average proportion of active rebels for each legitimacy value
phase_data = (
    results_df.groupby("legitimacy")["active_proportion"]
    .mean()
    .reset_index()
)

# Plot the phase diagram
plt.figure(figsize=(10, 6))
plt.plot(
    phase_data["legitimacy"],
    phase_data["active_proportion"],
    marker="o",
    linestyle="-",
    linewidth=2,
    markersize=6,
)
plt.title("Phase Diagram: Impact of Government Legitimacy on Rebellion", fontsize=14)
plt.xlabel("Government Legitimacy", fontsize=12)
plt.ylabel("Proportion of Active Rebels", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()

# Save and/or display the plot
plt.savefig("phase_diagram.png", dpi=300)
plt.show()