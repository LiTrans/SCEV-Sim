# Import libraries
import pandas as pd

# Loading Data 
data = pd.read_csv(r"C:/Users/tmals/EV_Supply_Chain/V2/Data/Simulation_Outputs/SCEV_Sim_100kV2.csv")

# Subtract VM_Emissions from the respective emission values
data['Adjusted_High_Ni_Supply_Emissions'] = data['High_Ni_Supply_Emissions_Total'] - data['VM_Emissions_HN']
data['Adjusted_LFP_Supply_Emissions'] = data['LFP_Supply_Emissions_Total'] - data['VM_Emissions_LFP']
data['Adjusted_NMC_Supply_Emissions'] = data['NMC_Supply_Emissions_Total'] - data['VM_Emissions_NMC']

# Replace zeros with NaN 
data['Adjusted_High_Ni_Supply_Emissions'].replace(0, pd.NA, inplace=True)
data['Adjusted_LFP_Supply_Emissions'].replace(0, pd.NA, inplace=True)
data['Adjusted_NMC_Supply_Emissions'].replace(0, pd.NA, inplace=True)

# Categorize 'Selected_B_index' into different battery manufacturers
def categorize_index(index):
    if 0 <= index <= 12:
        return 'CATL'
    elif 13 <= index <= 15:
        return 'BYD'
    elif 16 <= index <= 19:
        return 'LG'
    elif 20 <= index <= 26:
        return 'Panasonic'
    return 'Unknown'

data['Battery_Model'] = data['Selected_B_index'].apply(categorize_index)

# Group by 'Battery Model' and calculate the mean for each adjusted emission type, ignoring NaN values
emission_means = data.groupby('Battery_Model')[['Adjusted_High_Ni_Supply_Emissions', 'Adjusted_LFP_Supply_Emissions', 'Adjusted_NMC_Supply_Emissions']].mean().reset_index()

print(emission_means)

# Save the DataFrame to a CSV file
emission_means.to_csv(r"C:/Users/tmals/EV_Supply_Chain/V2/Average_Emissions_Per_Battery_Model.csv", index=False)
