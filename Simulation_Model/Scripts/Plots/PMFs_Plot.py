

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Loading Data 
data = pd.read_csv("C:/Users/tmals/EV_Supply_Chain/V2/Data/SCEV_Sim_100KV2_Countries.csv")

# List of data columns
histograms = ['EP_Emissions_HN', 'EP_Emissions_LFP', 'EP_Emissions_NMC',
              'PB_Emissions_HN', 'PB_Emissions_LFP', 'PB_Emissions_NMC', 'BV_Emissions_HN', 'BV_Emissions_LFP',
              'BV_Emissions_NMC', 'VM_Emissions_HN', 'VM_Emissions_LFP', 'VM_Emissions_NMC',
              'High_Ni_Supply_Emissions_Total', 'LFP_Supply_Emissions_Total', 'NMC_Supply_Emissions_Total']

# Create a figure and a grid of subplots
fig, axs = plt.subplots(5, 3, figsize=(15, 20))

# Flatten the axs array 
axs_flattened = axs.flatten()

# Define a list of colors for the histograms
colors = plt.cm.cividis(np.linspace(0, 1, len(histograms)))

for ax, column, color in zip(axs_flattened, histograms, colors):
    # Filter out zero values from the column before plotting
    non_zero_values = data[column][data[column] != 0]
    
    # Calculate the PMF
    counts, bins = np.histogram(non_zero_values, bins=30, density=False)
    probabilities = counts / counts.sum()

    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    f = interp1d(bin_centers, probabilities, kind='cubic', fill_value="extrapolate")
    xnew = np.linspace(bin_centers[0], bin_centers[-1], 300)
    ynew = f(xnew)

    # Plot the PMF with bars
    ax.bar(bin_centers, probabilities, width=np.diff(bins), color=color, alpha=0.7, align='center')

    # Plot the smooth curve
    ax.plot(xnew, ynew, color="black", linewidth=2)

    # Calculate statistics on non-zero values
    mean = non_zero_values.mean()
    median = non_zero_values.median()
    std_dev = non_zero_values.std()
    
    # Add statistics to the plot
    ax.axvline(mean, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean:.2f}')
    ax.axvline(median, color='blue', linestyle='dashed', linewidth=1, label=f'Median: {median:.2f}')
    ax.text(0.5, 0.8, f'Std: {std_dev:.2f}', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.5))

    if 'Total' in column:
        title = f'PMF for {column.replace("_", " ")}'
    else:
        title = f'PMF for {column.replace("_", " ")} Technology'

    ax.set_title(title, fontsize=10)  # Set the font size for the title
    ax.set_xlabel('Emissions', fontsize=8)
    ax.set_ylabel('Probability', fontsize=8)
    ax.legend(fontsize=6)
    ax.grid(True)

plt.tight_layout(pad=2.0)  # Adjust the padding between plots
plt.show()
