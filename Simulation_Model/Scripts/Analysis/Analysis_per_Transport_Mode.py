
# Import libraries
import pandas as pd

# Loading Data 
data = pd.read_csv(r"C:/Users/tmals/EV_Supply_Chain/V2/Data/SCEV_Sim_100KV2_Countries.csv")

""" 
Emissions Per Transport Mode per battery for different supply chain stages
""" 

# Obtain Averages
latest_averages = data.iloc[-1]

# Define the emission categories
emissions_data = {
    'EP': {
        'HN': ('Av_EP_Sea_HN', 'Av_EP_Land_HN'),
        'LFP': ('Av_EP_Sea_LFP', 'Av_EP_Land_LFP'),
        'NMC': ('Av_EP_Sea_NMC', 'Av_EP_Land_NMC')
    },
    'PB': {
        'HN': ('Av_PB_Sea_HN', 'Av_PB_Land_HN'),
        'LFP': ('Av_PB_Sea_LFP', 'Av_PB_Land_LFP'),
        'NMC': ('Av_PB_Sea_NMC', 'Av_PB_Land_NMC')
    },
    'BV': {
        'HN': ('Av_BV_Sea_HN', 'Av_BV_Land_HN'),
        'LFP': ('Av_BV_Sea_LFP', 'Av_BV_Land_LFP'),
        'NMC': ('Av_BV_Sea_NMC', 'Av_BV_Land_NMC')
    },
    'VM': {
        'HN': ('Av_VM_Sea_HN', 'Av_VM_Land_HN'),
        'LFP': ('Av_VM_Sea_LFP', 'Av_VM_Land_LFP'),
        'NMC': ('Av_VM_Sea_NMC', 'Av_VM_Land_NMC')
    }
}


results = {
    'Phase': [],
    'Type': [],
    'Sea Emissions': [],
    'Land Emissions': [],
    'Total Emissions': []
}

# Extract and store the data
for phase, types in emissions_data.items():
    for type_, (sea, land) in types.items():
        sea_val = latest_averages[sea]
        land_val = latest_averages[land]
        total_val = sea_val + land_val
        
        results['Phase'].append(phase)
        results['Type'].append(type_)
        results['Sea Emissions'].append(sea_val)
        results['Land Emissions'].append(land_val)
        results['Total Emissions'].append(total_val)

# Convert the results dictionary to a DataFrame
results_df = pd.DataFrame(results)

print(results_df)

# Save the DataFrame to a CSV file
results_df.to_csv(r"C:/Users/tmals/EV_Supply_Chain/V2/Emissions_Breakdown_Per_transport.csv", index=False)
