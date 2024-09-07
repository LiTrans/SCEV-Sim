import matplotlib.pyplot as plt
import pandas as pd

# Plot Size 
cm_to_inches = 1 / 2.54  # 1 inch = 2.54 cm

width_cm = 8
height_cm = 7.05

width_in = width_cm * cm_to_inches
height_in = height_cm * cm_to_inches

# Set font properties
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'sans-serif']
plt.rcParams['figure.dpi'] = 300  # High resolution

# Load the data
data = pd.read_csv("C:/Users/tmals/EV_Supply_Chain/V2/Data/Simulation_Outputs/SCEV_Sim_10KV2.csv")

# Data index
data.reset_index(inplace=True, drop=True)
data.index += 1  # Adjusting index to start from 1

# Create the figure and axis
fig, ax = plt.subplots(figsize=(width_in, height_in))

# Define columns
columns_info = {
    'Average_High_Ni_Emissions_Bt': {'color': '#1b9e77', 'label': 'HN'},  # Shiny green
    'Average_LFP_Supply_Emissions_Bt': {'color': '#7570b3', 'label': 'LFP'},  # Dark blue/purple
    'Average_NMCSupply_Emissions_Bt': {'color': '#666666', 'label': 'NMC'}  # Dark gray
}

# Loop through each column, excluding zeros
for column, info in columns_info.items():
    # Filter out zero values
    non_zero_data = data[data[column] != 0]
    ax.plot(non_zero_data.index, non_zero_data[column], label=info['label'], color=info['color'])

# Adjusting the plot area box 
light_gray_rgba = (0.8, 0.8, 0.8, 0.5)  # Light gray color with 50% transparency
for spine in ax.spines.values():
    spine.set_linewidth(0.5)
    spine.set_color(light_gray_rgba)  # Setting the color with transparency

# Adding gridlines, labels, and adjusting the legend
ax.grid(which='major', linestyle='-', linewidth='0.5', color='gray', alpha=0.5)
ax.minorticks_on()
ax.grid(which='minor', linestyle=':', linewidth='0.5', color='gray', alpha=0.3)
ax.set_ylabel('Kg e-CO$_2$/KWh', fontsize=10)

# Positioning the legend 
ax.legend(title='Battery Type', loc='lower right', fontsize=10, title_fontsize=10)

plt.tight_layout(pad=0.4)
plt.show()
