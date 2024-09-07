
# Import libraries
import pandas as pd

# Loading Data 
data = pd.read_csv(r"C:/Users/tmals/EV_Supply_Chain/V2/Script/SCEV_Sim/SCEV_Sim_V2_Future.csv")

# Categorize 'Selected_M_index' into different car manufacturers 
def categorize_index(index):
    if 0 <= index <= 7:
        return 'North America'
    elif 8 <= index <= 13:
        return 'China'
    elif 16 <= index <= 27:
        return 'European Union and UK'
    else:
        return 'Others'
    return 'Unknown'

data['Market'] = data['Selected_M_index'].apply(categorize_index)

# Replace zeros with NaN to discard them when calculating means
data['High_Ni_Supply_Emissions_Total'].replace(0, pd.NA, inplace=True)
data['LFP_Supply_Emissions_Total'].replace(0, pd.NA, inplace=True)
data['NMC_Supply_Emissions_Total'].replace(0, pd.NA, inplace=True)

# Group by 'Market' and calculate the mean for each emission type, ignoring NaN values
emission_means = data.groupby('Market')[['High_Ni_Supply_Emissions_Total', 'LFP_Supply_Emissions_Total', 'NMC_Supply_Emissions_Total']].mean().reset_index()


print(emission_means)

# Save the DataFrame to a CSV file
emission_means.to_csv(r"C:/Users/tmals/EV_Supply_Chain/V2/Average_Emissions_Per_Market_Future.csv", index=False)
