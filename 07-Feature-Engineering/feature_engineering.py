# -*- coding: utf-8 -*-
"""Feature engineering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sj9dkCzCsUWJ_qlCYVjZEDb1Q5hUvsDX

Based on business goals, I will focus on engineering features that directly contribute to understanding EV adoption trends, consumer behavior, and regional preferences.
"""

# Commented out IPython magic to ensure Python compatibility.
#Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

#to display plots inline
# %matplotlib inline

from google.colab import drive

# Mount Google Drive
drive.mount('/content/gdrive')

# Access your dataset
data_path = '/content/gdrive/My Drive/Colab Notebooks/Electiric vehical/final_after_outlier_cleaned_data.csv'

df = pd.read_csv(data_path)
# Display the first few rows of the DataFrame
df.head()

print(df.columns)

"""**Review the Existing Features:**

Before creating new features, it’s essential to review the existing ones:

- Urban vs. Non-Urban Classification
- CAFV Eligibility Category (High vs. Low)
- Make (Manufacturer)
- Model Year
- County/City
- Electric Vehicle Type (BEV vs. PHEV)

# Feature Engineering for Geographic Distribution Analysis

**Regional Popularity of Makes:**

Purpose: Understand if certain manufacturers are more popular in specific regions.

Method: Calculate the proportion of vehicles from each manufacturer (e.g., Tesla, Nissan) in each county.
"""

df['Make_Proportion'] = df.groupby('County')['Make'].transform(lambda x: x.value_counts(normalize=True))

"""**Interaction Terms: Urbanization and CAFV Eligibility:**

Purpose: Capture the combined effect of urbanization and CAFV eligibility on EV adoption.

Method: Create interaction terms between Urban and CAFV Eligibility Category.

**Creating an 'Urban' Column Based on Available Data**
"""

# List of urban cities (this is just an example, replace with actual cities)
urban_cities = ['Seattle', 'Bellevue', 'Redmond', 'Tacoma', 'Vancouver']

# Create the 'Urban' column based on the City column
df['Urban'] = df['City'].apply(lambda x: 'Urban' if x in urban_cities else 'Non-Urban')

# Alternatively, create the 'Urban' column based on the County column (if more appropriate)
urban_counties = ['King', 'Pierce', 'Snohomish', 'Clark', 'Thurston']
df['Urban'] = df['County'].apply(lambda x: 'Urban' if x in urban_counties else 'Non-Urban')

# Now, i can proceed with the feature engineering and modeling steps that require the 'Urban' column.

print(df.columns)

# If you want to combine the 'Urban' and 'CAFV Eligibility' columns:
df['Urban_CAFV_Interaction'] = df['Urban'].astype(str) + '_' + df['CAFV Eligibility'].astype(str)

# Then, apply one-hot encoding to the new interaction column:
df = pd.get_dummies(df, columns=['Urban_CAFV_Interaction'], drop_first=True)

"""**Vehicle Age**

Purpose: Understand how the age of vehicles impacts their adoption in different regions.

Method: Create a new feature that calculates the vehicle's age by subtracting the Model Year from the current year.
"""

import datetime
current_year = datetime.datetime.now().year
df['Vehicle Age'] = current_year - df['Model Year']

df.head()

print(df.columns)

"""# Feature Engineering for Market Penetration and Growth Trends

**Yearly Growth Rates**

Purpose: Understand how EV adoption grows over time within each region.

Method: Calculate the year-over-year growth rate of EV registrations.
"""

# Step 1: Group by County and Model Year and count the number of Electric Vehicle Types
yearly_ev_count = df.groupby(['County', 'Model Year'])['Electric Vehicle Type'].count().reset_index(name='EV_Count')

# Step 2: Calculate the percentage change (yearly growth rate) within each County
yearly_ev_count['Yearly_Growth_Rate'] = yearly_ev_count.groupby('County')['EV_Count'].pct_change()

# Step 3: Merge the yearly growth rate back to the original dataframe (if needed)
df = df.merge(yearly_ev_count[['County', 'Model Year', 'Yearly_Growth_Rate']], on=['County', 'Model Year'], how='left')

df['Yearly_Growth_Rate'] = df['Yearly_Growth_Rate'].fillna(0)  # Optionally fill NaNs with 0 or another appropriate value

"""**Time Series Features**

Purpose: Capture trends over time for better predictive modeling.

Method: Create features such as Year, Quarter, and Month to capture seasonality and trends in EV adoption.
"""

df['Quarter'] = pd.to_datetime(df['Model Year'], format='%Y').dt.quarter
df['Month'] = pd.to_datetime(df['Model Year'], format='%Y').dt.month

print(df.columns)

df.head()

"""# Feature Engineering for Consumer Behavior Analysis

**Preference Ratio for BEVs vs. PHEVs**

Purpose: Understand regional preferences for BEVs vs. PHEVs.

Method: Calculate the proportion of BEVs and PHEVs within each county or city.
"""

df['BEV_Proportion'] = df.groupby('County')['Electric Vehicle Type'].transform(lambda x: (x == 'BEV').mean())
df['PHEV_Proportion'] = df.groupby('County')['Electric Vehicle Type'].transform(lambda x: (x == 'PHEV').mean())

"""**Manufacturer Dominance**

Purpose: Identify if specific manufacturers dominate certain regions, which could indicate local preferences or incentives.

Method: Calculate the proportion of each manufacturer within each region and create a feature to represent the dominant manufacturer.
"""

df['Dominant_Manufacturer'] = df.groupby('County')['Make'].transform(lambda x: x.value_counts().idxmax())
df['Dominant_Manufacturer_Proportion'] = df.groupby('County')['Make'].transform(lambda x: x.value_counts().max() / x.count())

print(df.columns)

df.head()

"""# Saving the Dataset"""

# Define the path where you want to save the dataset
output_path = '/content/gdrive/My Drive/Colab Notebooks/Electiric vehical/final_dataset_with_features.csv'

# Save the DataFrame to a CSV file
df.to_csv(output_path, index=False)

print(f"Dataset with engineered features saved to {output_path}")