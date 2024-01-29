import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming you have the data in two CSV files
csv_filename1 = 'data/outputs/results_district-1.csv'
csv_filename2 = 'data/outputs/output_district-1-switchpairs.csv'

# Read data from CSV
df1 = pd.read_csv(csv_filename1)
df2 = pd.read_csv(csv_filename2)

# Combine the dataframes with an additional 'Algorithm' column
df1['Algorithm'] = 'Random'
df2['Algorithm'] = 'SwitchPairs'
combined_df = pd.concat([df1, df2])

# Create a boxplot using seaborn
plt.figure(figsize=(10, 6))
sns.boxplot(x='Algorithm', y='GridCost', data=combined_df)
plt.title('Boxplot of GridCost - Random vs SwitchPairs')
plt.show()




