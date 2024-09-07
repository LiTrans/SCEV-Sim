import pandas as pd

# Step 1: Read the CSV file
file_path = "C:/Users/tmals/EV_Supply_Chain/V2/Data/Simulation_Outputs/SCEV_Sim_100KV2_Countries.csv"
data = pd.read_csv(file_path)

# Define phases and corresponding column pairs with flow values
phases = {
    "Extraction_to_Processing": [
        ('Selected_Li_index', 'Selected_PLi_index', 0.988621),
        ('Selected_Co_index', 'Selected_PCo_index', 0.004675),
        ('Selected_Cu_index', 'Selected_PCu_index', 0.263704),
        ('Selected_Ni_index', 'Selected_PNi_index', 0.543038),
        ('Selected_C_index', 'Selected_PC_index', 0.92093), 
        ('Selected_PC_index', 'Selected_B_index', 0.792),
        ('Selected_Mn_index', 'Selected_B_index', 0.0584),
        ('Selected_Al_index', 'Selected_B_index', 0.208667),
        ('Selected_Fe_index', 'Selected_B_index', 0.48),
        ('Selected_Si_index', 'Selected_B_index', 0.056842),
        ('Selected_P_index', 'Selected_B_index', 0.336)
    ],
    "Extraction/Processing_to_Battery": [
        ('Selected_PLi_index', 'Selected_B_index', 0.5743),
        ('Selected_PCo_index', 'Selected_B_index', 0.0036),
        ('Selected_PCu_index', 'Selected_B_index', 0.2136),
        ('Selected_PNi_index', 'Selected_B_index', 0.429),
        ('Selected_PC_index', 'Selected_B_index', 0.792),
        ('Selected_B_index', 'Selected_B_index', 0.04333),
        ('Selected_B_index', 'Selected_B_index', 0.1878),
        ('Selected_B_index', 'Selected_B_index', 0.312),
        ('Selected_B_index', 'Selected_B_index', 0.0216),
        ('Selected_B_index', 'Selected_B_index', 0.168)
    ],
    "Battery_Production_to_Vehicle_Production": [
        ('Selected_B_index', 'Selected_V_index', 6.78)
    ],
    "Vehicle_Production_to_Market": [
        ('Selected_V_index', 'Selected_M_index', 28.78489)
    ]
}

# Initialize dictionary to store all flows
all_flows = {}

# Consolidate flows for all phases
for phase, column_pairs in phases.items():
    # Initialize dictionary to store flows for the current phase
    phase_flows = {}
    
    # Consolidate flows for the current phase
    for index, row in data.iterrows():
        for origin_col, dest_col, flow_value in column_pairs:
            origin = row[origin_col]
            destination = row[dest_col]
            # Add the flow to the phase flows
            if (origin, destination) in phase_flows:
                phase_flows[(origin, destination)] += flow_value
            else:
                phase_flows[(origin, destination)] = flow_value
    
    # Add phase flows to all flows dictionary
    all_flows[phase] = phase_flows

# Write the results to a single CSV file with different columns for each phase
output_file_path = "MASS_FLOW_SANKEY_DIAGRAM.csv"
with open(output_file_path, 'w') as f:
    f.write("Origin_Country,Destination_Country,")
    for phase in phases:
        f.write(f"{phase}_Flow,")
    f.write("\n")
    
    # Iterate through unique origin-destination pairs
    unique_pairs = set()
    for phase_dict in all_flows.values():
        unique_pairs.update(phase_dict.keys())

    for origin, destination in unique_pairs:
        f.write(f"{origin},{destination},")
        for phase_flows in all_flows.values():
            flow = phase_flows.get((origin, destination), 0)
            f.write(f"{flow},")
        f.write("\n")

print(f"Consolidated flows for all phases have been written to {output_file_path}")
