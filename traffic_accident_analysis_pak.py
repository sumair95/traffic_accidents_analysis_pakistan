# ===============================
# Traffic Accidents Analysis - Pakistan
# ===============================

# ---- 1. Import Libraries ----
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set seaborn style
sns.set_theme(style="whitegrid")

# ---- 2. Load Data ----
file_path = "D:/Personal Projects/data_analyst_portfolio/traffic-accidents-annual.xlsx"
country_df = pd.read_excel(file_path, sheet_name="Country")
region_df = pd.read_excel(file_path, sheet_name="By Region")

# ---- 3. Inspect Data ----
print("\n--- Country-level Data ---")
print(country_df.info())
print(country_df.head())

print("\n--- Region-level Data ---")
print(region_df.info())
print(region_df.head())

# ---- 4. Data Cleaning & Transformation ----

# Standardize column names (remove spaces, make lowercase)
country_df.columns = country_df.columns.str.strip().str.lower().str.replace(" ", "_")
region_df.columns = region_df.columns.str.strip().str.lower().str.replace(" ", "_")

# Ensure 'year' is string (categorical timeline)
country_df["year"] = country_df["year"].astype(str)
region_df["year"] = region_df["year"].astype(str)

# Check for missing values
print("\nMissing values in Country data:\n", country_df.isna().sum())
print("\nMissing values in Region data:\n", region_df.isna().sum())

# Fill or drop missing values (example: forward fill)
country_df = country_df.fillna(method="ffill")
region_df = region_df.fillna(method="ffill")

# ---- 5. Exploratory Data Analysis (EDA) ----

# Summary statistics
print("\nSummary - Country level:\n", country_df.describe())
print("\nSummary - Region level:\n", region_df.describe())

# Total incidents across all years
total_accidents_pakistan = country_df["total_number_of_accidents"].sum()
avg_accidents_pakistan = country_df["total_number_of_accidents"].mean()
print(f"\nTotal accidents in Pakistan (all years): {total_accidents_pakistan:,}")
print(f"Average annual accidents in Pakistan: {avg_accidents_pakistan:,.0f}")

# Average per region
region_avg = region_df.groupby("region")["total_number_of_accidents"].mean().sort_values(ascending=False)
print("\nAverage annual accidents per region:\n", region_avg)

# ---- 6. Visualization ----

# 6.1 National Trend
plt.figure(figsize=(10,6))
sns.lineplot(data=country_df, x="year", y="total_number_of_accidents", marker="o", label="Pakistan")
plt.xticks(rotation=45)
plt.title("Annual Traffic Accidents in Pakistan")
plt.xlabel("Year")
plt.ylabel("Total Accidents")
plt.tight_layout()
plt.show()

# 6.2 Regional Trends
plt.figure(figsize=(12,7))
sns.lineplot(data=region_df, x="year", y="total_number_of_accidents", hue="region", marker="o")
plt.xticks(rotation=45)
plt.title("Annual Traffic Accidents by Region")
plt.xlabel("Year")
plt.ylabel("Total Accidents")
plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 6.3 Average accidents per region (bar chart)
plt.figure(figsize=(10,6))
sns.barplot(x=region_avg.values, y=region_avg.index, palette="viridis")
plt.title("Average Annual Accidents per Region")
plt.xlabel("Average Accidents")
plt.ylabel("Region")
plt.tight_layout()
plt.show()

# 6.4 Fatal vs Non-Fatal (National Level)
plt.figure(figsize=(10,6))
country_df_melt = country_df.melt(id_vars=["year"], value_vars=["fatal_accidents","non-fatal_accidents"],
                                  var_name="Accident Type", value_name="Count")
sns.lineplot(data=country_df_melt, x="year", y="Count", hue="Accident Type", marker="o")
plt.xticks(rotation=45)
plt.title("Fatal vs Non-Fatal Accidents in Pakistan")
plt.xlabel("Year")
plt.ylabel("Accidents")
plt.tight_layout()
plt.show()

# 6.5 Fatal vs Non-Fatal (Regional Snapshot - Latest Year)
latest_year = region_df["year"].max()
latest_data = region_df[region_df["year"] == latest_year]

plt.figure(figsize=(12,6))
latest_data_melt = latest_data.melt(id_vars=["region"], value_vars=["fatal_accidents","non-fatal_accidents"],
                                    var_name="Accident Type", value_name="Count")
sns.barplot(data=latest_data_melt, x="region", y="Count", hue="Accident Type")
plt.xticks(rotation=45)
plt.title(f"Fatal vs Non-Fatal Accidents by Region ({latest_year})")
plt.xlabel("Region")
plt.ylabel("Accidents")
plt.tight_layout()
plt.show()

# 6.6 Injured & Killed (National Level)
plt.figure(figsize=(10,6))
country_df_melt2 = country_df.melt(id_vars=["year"],
                                   value_vars=["injured","killed"],
                                   var_name="Category", value_name="Count")
sns.lineplot(data=country_df_melt2, x="year", y="Count", hue="Category", marker="o")
plt.xticks(rotation=45)
plt.title("People Injured vs Killed in Road Accidents (Pakistan)")
plt.xlabel("Year")
plt.ylabel("Number of People")
plt.tight_layout()
plt.show()

# 6.7 Vehicles Involved (National Level)
plt.figure(figsize=(10,6))
sns.lineplot(data=country_df, x="year", y="total_number_of_vehicles_involved", marker="o", color="brown")
plt.xticks(rotation=45)
plt.title("Vehicles Involved in Road Accidents (Pakistan)")
plt.xlabel("Year")
plt.ylabel("Vehicles Involved")
plt.tight_layout()
plt.show()

# 6.8 Injured & Killed (Regional Level - Latest Year)
latest_year = region_df["year"].max()
plt.figure(figsize=(12,6))
region_latest_melt = region_df[region_df["year"]==latest_year].melt(
    id_vars=["region"], value_vars=["injured","killed"],
    var_name="Category", value_name="Count")
sns.barplot(data=region_latest_melt, x="region", y="Count", hue="Category")
plt.xticks(rotation=45)
plt.title(f"People Injured vs Killed in Road Accidents by Region ({latest_year})")
plt.xlabel("Region")
plt.ylabel("Number of People")
plt.tight_layout()
plt.show()

# 6.9 Vehicles Involved (Regional Trends)
plt.figure(figsize=(12,7))
sns.lineplot(data=region_df, x="year", y="total_number_of_vehicles_involved", hue="region", marker="o")
plt.xticks(rotation=45)
plt.title("Vehicles Involved in Road Accidents by Region")
plt.xlabel("Year")
plt.ylabel("Vehicles Involved")
plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 6.10 Pie Chart - Incidents by Region (latest year)
latest_year = region_df["year"].max()
latest_data = region_df[region_df["year"] == latest_year]

plt.figure(figsize=(8,8))
plt.pie(latest_data["total_number_of_accidents"],
        labels=latest_data["region"],
        autopct="%1.1f%%", startangle=140)
plt.title(f"Share of Accidents by Region ({latest_year})")
plt.show()

# 6.11 Pie Chart - People Killed by Region (latest year)
plt.figure(figsize=(8,8))
plt.pie(latest_data["killed"],
        labels=latest_data["region"],
        autopct="%1.1f%%", startangle=140)
plt.title(f"Share of People Killed by Region ({latest_year})")
plt.show()

# 6.12 Pie Chart - Vehicles Involved by Region (latest year)
plt.figure(figsize=(8,8))
plt.pie(latest_data["total_number_of_vehicles_involved"],
        labels=latest_data["region"],
        autopct="%1.1f%%", startangle=140)
plt.title(f"Share of Vehicles Involved by Region ({latest_year})")
plt.show()


# ---- End of Analysis ----
