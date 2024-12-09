from mesa.examples.advanced.epstein_civil_violence.agents import (
    Citizen,
    CitizenState,
    Cop,
)
from mesa.examples.advanced.epstein_civil_violence.model import EpsteinCivilViolence
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)
import pandas as pd
import os

# Keep the existing configuration
COP_COLOR = "#000000"

agent_colors = {
    CitizenState.ACTIVE: "#FE6100",
    CitizenState.QUIET: "#648FFF",
    CitizenState.ARRESTED: "#808080",
}

def citizen_cop_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "size": 20,
    }

    if isinstance(agent, Citizen):
        portrayal["color"] = agent_colors[agent.state]
    elif isinstance(agent, Cop):
        portrayal["color"] = COP_COLOR

    return portrayal

def post_process(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.get_figure().set_size_inches(10, 10)

model_params = {
    "height": 40,
    "width": 40,
    "citizen_density": Slider("Initial Agent Density", 0.7, 0.0, 0.9, 0.1),
    "cop_density": Slider("Initial Cop Density", 0.04, 0.0, 0.1, 0.01),
    "citizen_vision": Slider("Citizen Vision", 7, 1, 10, 1),
    "cop_vision": Slider("Cop Vision", 7, 1, 10, 1),
    "legitimacy": Slider("Government Legitimacy", 0.82, 0.0, 1, 0.01),
    "max_jail_term": Slider("Max Jail Term", 30, 0, 50, 1),
}

print(citizen_cop_portrayal)

space_component = make_space_component(
    citizen_cop_portrayal, post_process=post_process, draw_grid=False
)

chart_component = make_plot_component(
    {state.name.lower(): agent_colors[state] for state in CitizenState}
)

def run_simulation(max_steps=200, output_dir='simulation_data'):
    """
    Run the Epstein Civil Violence simulation and collect data
    
    :param max_steps: Maximum number of steps to run the simulation
    :param output_dir: Directory to save output CSV files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize the model
    model = EpsteinCivilViolence(
        height=100, 
        width=100, 
        citizen_density=0.7, 
        cop_density=0.04
    )
    
    # Lists to store data
    model_data_list = []
    agent_data_list = []
    
    # Run the simulation for specified number of steps
    for step in range(max_steps):
        # Collect model-level data
        model_vars = model.datacollector.get_model_vars_dataframe()
        print(model_vars)
        model_vars['step'] = step
        model_data_list.append(model_vars)
        
        # Collect agent-level data
        agent_vars = model.datacollector.get_agent_vars_dataframe()
        print(agent_vars)
        agent_vars['step'] = step
        agent_data_list.append(agent_vars)
        
        # Step the model forward
        model.step()
        
        # Optional: Break if the model is no longer running
        if not model.running:
            break
    
    # Concatenate collected data
    if model_data_list:
        full_model_data = pd.concat(model_data_list)
        full_model_data.to_csv(os.path.join(output_dir, 'model_data.csv'), index=False)
        print(f"Model data saved to {os.path.join(output_dir, 'model_data.csv')}")
    
    if agent_data_list:
        full_agent_data = pd.concat(agent_data_list)
        full_agent_data.to_csv(os.path.join(output_dir, 'agent_data.csv'), index=False)
        print(f"Agent data saved to {os.path.join(output_dir, 'agent_data.csv')}")
    
    return model

# Uncomment and run this to collect simulation data
# run_simulation(max_steps=100)

# Keep the visualization page

page = SolaraViz(
    EpsteinCivilViolence(),
    components=[space_component, chart_component],
    model_params=model_params,
    name="Epstein Civil Violence",
)

page  # noqa