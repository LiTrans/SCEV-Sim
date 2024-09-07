# import libraries

import pandas as pd

# Extract the country from the string
def extract_country(port_string):
    return port_string.split(', ')[-1] if isinstance(port_string, str) and ', ' in port_string else 'Unknown'

# Mappings based on indices
manual_mappings = {
    'Selected_PLi_index': {0: 'China', 1: 'Chile', 2: 'Argentina'},
    'Selected_PCo_index': {11: 'China', 12: 'Finland', 13: 'Canada'},
    'Selected_PCu_index': {19: 'China', 20: 'Chile', 21: 'Japan'},
    'Selected_PNi_index': {29: 'China', 30: 'Indonesia', 31: 'Russia'},
    'Selected_PC_index': {44: 'China', 45: 'Mozambique', 46: 'Brazil'}
}

# Load the data
supply_chain_coord = pd.read_csv("C:/Users/tmals/EV_Supply_Chain/V2/Data/Simulation_Inputs/Simulation_Inputs.csv")
simulation_results = pd.read_csv("C:/Users/tmals/EV_Supply_Chain/V2/Data/Simulation_Outputs/SCEV_Sim_100kV2.csv")

# Create mappings from index to country for mineral ports
mineral_port_dict = supply_chain_coord['mineral_port'].dropna().apply(extract_country).reset_index(drop=True).to_dict()

# Function to map mineral indexes to countries
def map_mineral_index_to_country(index, mapping_dict):
    return mapping_dict.get(index, 'Unknown')

# Function to apply manual mappings for processing ports
def apply_manual_mapping(index, column, manual_dict, related_dict):
    if index in manual_dict:
        return manual_dict[index]
    else:
        # Fallback to related mineral port country if processing port country is not listed
        return related_dict.get(index, 'Unknown')

# Replace index with country for mineral-related indexes
for column in ['Selected_Li_index', 'Selected_Co_index', 'Selected_Cu_index', 
               'Selected_Ni_index', 'Selected_C_index', 'Selected_Mn_index', 
               'Selected_Al_index', 'Selected_Fe_index', 'Selected_Si_index', 'Selected_P_index']:
    simulation_results[column] = simulation_results[column].apply(map_mineral_index_to_country, args=(mineral_port_dict,))

# Apply manual mappings 
for column in manual_mappings:
    related_column = column.replace('P', '', 1)
    simulation_results[column] = simulation_results.apply(
        lambda row: apply_manual_mapping(row[column], column, manual_mappings[column], mineral_port_dict), axis=1)

# Remaining mappings
battery_port_dict = supply_chain_coord['battery_port'].dropna().apply(extract_country).reset_index(drop=True).to_dict()
vehicle_port_dict = supply_chain_coord['vehicle_port'].dropna().apply(extract_country).reset_index(drop=True).to_dict()
market_port_dict = supply_chain_coord['market_port'].dropna().apply(extract_country).reset_index(drop=True).to_dict()

simulation_results['Selected_B_index'] = simulation_results['Selected_B_index'].apply(map_mineral_index_to_country, args=(battery_port_dict,))
simulation_results['Selected_V_index'] = simulation_results['Selected_V_index'].apply(map_mineral_index_to_country, args=(vehicle_port_dict,))
simulation_results['Selected_M_index'] = simulation_results['Selected_M_index'].apply(map_mineral_index_to_country, args=(market_port_dict,))

# Save the updated DataFrame to a new CSV file
output_path = "C:/Users/tmals/EV_Supply_Chain/V2/Data/SCEV_Sim_100KV2_Countries.csv"
simulation_results.to_csv(output_path, index=False)


