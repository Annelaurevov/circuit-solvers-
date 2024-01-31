import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming you have the data in two CSV files
csv_filename1 = 'data/outputs/csv/results_district-1-BreathFirst-1-1000.csv'
csv_filename2 = 'data/outputs/csv/results_district-1-BreathFirst-2-1000.csv'
csv_filename3 = 'data/outputs/csv/results_district-1-Dijkstra100000.csv'
csv_filename4 = 'data/outputs/csv/results_district-1-SwitchPairsBreathFirst-1-1000.csv'
csv_filename5 = 'data/outputs/csv/results_district-1-SwitchPairsBreathFirst-2-1000.csv'
csv_filename6 = 'data/outputs/csv/results_district-1-SwitchPairsDijkstra10000.csv'

# Read data from CSV, skipping the first row
df1 = pd.read_csv(csv_filename1, skiprows=1, header=None, names=['GridCost'])
df2 = pd.read_csv(csv_filename2, skiprows=1, header=None, names=['GridCost'])
df3 = pd.read_csv(csv_filename3, skiprows=1, header=None, names=['GridCost'])
df4 = pd.read_csv(csv_filename4, skiprows=1, header=None, names=['GridCost'])
df5 = pd.read_csv(csv_filename5, skiprows=1, header=None, names=['GridCost'])
df6 = pd.read_csv(csv_filename6, skiprows=1, header=None, names=['GridCost'])


# Add Algorithm column
df1['Algorithm'] = 'Breath first 1'
df2['Algorithm'] = 'Breath first 2'
df3['Algorithm'] = 'Dijkstra'
df4['Algorithm'] = 'Switch with Breath First 1'
df5['Algorithm'] = 'Switch with Breath First 2'
df6['Algorithm'] = 'Switch with Dijkstra'

# Combine the dataframes
combined_df = pd.concat([df1, df2, df3, df4, df5, df6])

# Create a boxplot using seaborn
plt.figure(figsize=(10, 6))
sns.boxplot(x='Algorithm', y='GridCost', data=combined_df, flierprops=dict(marker='o', markersize=8, markerfacecolor='red', alpha=0.5))
plt.title('Boxplot of GridCost')
plt.show()
