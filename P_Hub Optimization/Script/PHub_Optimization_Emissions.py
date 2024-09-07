import pandas as pd
import pulp as pl
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load cost matrices from CSV files
ji_cost_df = pd.read_csv('C:/Users/tmals/EV_Supply_Chain/Phub/Region_Cost Matrices/Emissions/JI_Cost_Matrix_NA.csv', index_col=0)
JI_Cost_Matrix = ji_cost_df.to_numpy()

im_cost_df = pd.read_csv('C:/Users/tmals/EV_Supply_Chain/Phub/Region_Cost Matrices/Emissions/ID_Cost_Matrix_NA.csv', index_col=0)
IM_Cost_Matrix = im_cost_df.to_numpy()

# Define the number of options per each J subset (variable across subsets)
options_per_subset = [11, 8, 10, 5, 6, 4, 3, 5, 5, 5]
num_j_subsets = len(options_per_subset)

# Setup the problem
model = pl.LpProblem("Minimize_Transportation_Costs", pl.LpMinimize)

# Define the variables
J_option_chosen = pl.LpVariable.dicts("J_option", 
                                      ((j, i, k) for j in range(num_j_subsets) for i in range(options_per_subset[j]) for k in range(9)), 
                                      cat='Binary')

I_chosen = pl.LpVariable.dicts("I_hub", range(9), cat='Binary')

# Objective Function
model += pl.lpSum(JI_Cost_Matrix[sum(options_per_subset[:j]) + i][k] * J_option_chosen[j, i, k] for j in range(num_j_subsets) for i in range(options_per_subset[j]) for k in range(9)) + \
         pl.lpSum(IM_Cost_Matrix[k][m] * I_chosen[k] for k in range(9) for m in range(9))

# Constraints
model += pl.lpSum(I_chosen[k] for k in range(9)) == 2

for j in range(num_j_subsets):
    for k in range(9):
        model += pl.lpSum(J_option_chosen[j, i, k] for i in range(options_per_subset[j])) == I_chosen[k]

for j in range(num_j_subsets):
    for i in range(options_per_subset[j]):
        for k in range(9):
            model += J_option_chosen[j, i, k] <= I_chosen[k]

# Solve the problem
model.solve()

# Output results and prepare data for heatmap
cost_matrix = np.zeros((9, 9))  
selected_hubs = []

print("Status:", pl.LpStatus[model.status])
if model.status == pl.LpStatusOptimal:
    print("Optimal solution found:")
    for k in range(9):
        if pl.value(I_chosen[k]) == 1:
            selected_hubs.append(k)
            print(f"Hub I{k+1} selected:")
            total_cost_from_hub = 0
            for j in range(num_j_subsets):
                for i in range(options_per_subset[j]):
                    if pl.value(J_option_chosen[j, i, k]) == 1:
                        j_to_i_cost = JI_Cost_Matrix[sum(options_per_subset[:j]) + i][k]
                        total_cost_from_hub += j_to_i_cost
                        print(f"J{j+1}_{i+1} selected for subset {j+1}, cost: {j_to_i_cost}")
            cost_to_markets = sum(IM_Cost_Matrix[k][m] for m in range(9))
            total_cost_from_hub += cost_to_markets
            average_cost_to_markets = total_cost_from_hub / 9
            cost_matrix[k] = [total_cost_from_hub / 9 for _ in range(9)]  # Store average cost for each market
            print(f"Total cost from hub I{k+1} including market distribution: {total_cost_from_hub}, Average cost: {average_cost_to_markets:.2f}")
else:
    print("No feasible solution found.")
    
# Create a heatmap of the cost matrix
sns.set()
plt.figure(figsize=(10, 8))
sns.heatmap(cost_matrix, annot=True, cmap='YlGnBu', fmt=".2f")
plt.xlabel('Markets')
plt.ylabel('Hubs')
plt.title('Average Cost per Hub and Market')
plt.show()