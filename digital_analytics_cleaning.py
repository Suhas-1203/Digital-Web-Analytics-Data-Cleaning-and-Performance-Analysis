import pandas as pd
import numpy as np

# ---------------------------------
# 1. Load Excel Data
# ---------------------------------
file_path = r"C:\Users\suhas\Downloads\Web_Analytic_Dataset.csv.xlsx"
df = pd.read_excel(file_path)

print("Initial Shape:", df.shape)
print(df.head())

# ---------------------------------
# 2. Standardize Column Names
# ---------------------------------
df.columns = df.columns.str.strip().str.replace(" ", "_")

# ---------------------------------
# 3. Helper Function: Clean Numeric Columns
# ---------------------------------
def clean_numeric(series):
    return (
        series.astype(str)
        .str.replace(",", "", regex=True)
        .str.replace("%", "", regex=True)
        .str.replace("<", "", regex=True)   # fixes <0.01
        .replace("nan", np.nan)
        .astype(float)
    )

# ---------------------------------
# 4. Clean Required Numeric Columns
# ---------------------------------
numeric_cols = [
    "Users",
    "New_Users",
    "Sessions",
    "Transactions",
    "Revenue",
    "Conversion_Rate",
    "Bounce_Rate",
    "Pages_per_Session"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = clean_numeric(df[col])

# ---------------------------------
# 5. Handle Avg Session Duration (if exists)
# ---------------------------------
if "Avg_Session_Duration_sec" in df.columns:
    df["Avg_Session_Duration_sec"] = clean_numeric(df["Avg_Session_Duration_sec"])

# ---------------------------------
# 6. Remove Invalid Records
# ---------------------------------
df = df[
    (df["Users"] >= 0) &
    (df["Sessions"] > 0) &
    (df["Bounce_Rate"] <= 100)
]

print("After Cleaning Shape:", df.shape)

# ---------------------------------
# 7. KPI Calculations
# ---------------------------------
df["Calculated_Conversion_Rate"] = (
    df["Transactions"] / df["Sessions"]
) * 100

df["Revenue_per_Session"] = (
    df["Revenue"] / df["Sessions"]
)

# ---------------------------------
# 8. Channel Performance Summary
# ---------------------------------
channel_summary = df.groupby("Source_Medium", as_index=False).agg({
    "Users": "sum",
    "Sessions": "sum",
    "Transactions": "sum",
    "Revenue": "sum",
    "Calculated_Conversion_Rate": "mean",
    "Revenue_per_Session": "mean"
})

# ---------------------------------
# 9. Export Clean Data for Power BI
# ---------------------------------
df.to_csv("clean_web_analytics_data.csv", index=False)
channel_summary.to_csv("channel_performance_summary.csv", index=False)

print("✅ Data cleaning complete.")
print("Files exported:")
print("- clean_web_analytics_data.csv")
print("- channel_performance_summary.csv")
