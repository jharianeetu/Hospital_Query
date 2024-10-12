import pandas as pd

# Load the scraped data
df = pd.read_csv('hospitals.csv')

# Drop any rows with missing values
df.dropna(inplace=True)

# Standardize column names (e.g., convert all text to lowercase)
df.columns = [col.lower() for col in df.columns]

# Example: Clean the 'address' field by removing extra spaces
df['address'] = df['address'].str.strip()

# Save the cleaned data to a new CSV
df.to_csv('cleaned_hospitals.csv', index=False)

print("Data cleaning completed. Cleaned data saved to cleaned_hospitals.csv")
