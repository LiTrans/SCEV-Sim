

# Import libraries
import pandas as pd

# Loading Data 
data = pd.read_csv(r"C:/Users/tmals/EV_Supply_Chain/V2/Data/Simulation_Outputs/SCEV_Sim_100kV2.csv")

# Categorize 'Selected_V_index' into different car manufacturers 
def categorize_index(index):
    if 0 <= index <= 4:
        return 'TESLA'
    elif 5 <= index <= 8:
        return 'BYD'
    elif 9 <= index <= 17:
        return 'VW'
    elif 18 <= index <= 24:
        return 'Hyundai'
    return 'Unknown'

data['Car_Model'] = data['Selected_V_index'].apply(categorize_index)

# Replace zeros with NaN to discard them when calculating means
data['High_Ni_Supply_Emissions_Total'].replace(0, pd.NA, inplace=True)
data['LFP_Supply_Emissions_Total'].replace(0, pd.NA, inplace=True)
data['NMC_Supply_Emissions_Total'].replace(0, pd.NA, inplace=True)

# Group by 'Car Model' and calculate the mean for each emission type, ignoring NaN values
emission_means = data.groupby('Car_Model')[['High_Ni_Supply_Emissions_Total', 'LFP_Supply_Emissions_Total', 'NMC_Supply_Emissions_Total']].mean().reset_index()


print(emission_means)

# Save the DataFrame to a CSV file
emission_means.to_csv(r"C:/Users/tmals/EV_Supply_Chain/V2/Average_Emissions_Per_Car_Model223.csv", index=False)
