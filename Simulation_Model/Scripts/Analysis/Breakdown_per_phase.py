# Import libraries
import pandas as pd

# Loading Data 
data = pd.read_csv(r"C:/Users/tmals/EV_Supply_Chain/V2/Data/SCEV_Sim_100KV2_Countries.csv")

data.columns = [col.strip() for col in data.columns]

# Extract data
last_row_values = {
    'High_Ni': {
        'EP': data['Av_EP_Emissions_HN'].iloc[-1],
        'PB': data['Av_PB_Emissions_HN'].iloc[-1],
        'BV': data['Av_BV_Emissions_HN'].iloc[-1],
        'VM': data['Av_VM_Emissions_HN'].iloc[-1],
        'Total': data['Average_High_Ni_Emissions_Bt'].iloc[-1]
    },
    'LFP': {
        'EP': data['Av_EP_Emissions_LFP'].iloc[-1],
        'PB': data['Av_PB_Emissions_LFP'].iloc[-1],
        'BV': data['Av_BV_Emissions_LFP'].iloc[-1],
        'VM': data['Av_VM_Emissions_LFP'].iloc[-1],
        'Total': data['Average_LFP_Supply_Emissions_Bt'].iloc[-1]
    },
    'NMC': {
        'EP': data['Av_EP_Emissions_NMC'].iloc[-1],
        'PB': data['Av_PB_Emissions_NMC'].iloc[-1],
        'BV': data['Av_BV_Emissions_NMC'].iloc[-1],
        'VM': data['Av_VM_Emissions_NMC'].iloc[-1],
        'Total': data['Average_NMCSupply_Emissions_Bt'].iloc[-1]
    }
}

# Convert the dictionary to a DataFrame
last_row_values_df = pd.DataFrame(last_row_values).T

print(last_row_values_df)

# Save Outputs
last_row_values_df.to_csv(r"C:/Users/tmals/EV_Supply_Chain/V2/Breakdown_per_phase.csv", index=True)
