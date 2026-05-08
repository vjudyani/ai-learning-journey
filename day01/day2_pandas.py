# Day 2 - File handling and pandas 
# Goal: read, explore, and filter data like a real dataset 

import pandas as pd 

#-- Create a mock variant dataset (like a VCF- derived table ) ---
data = {
    "gene":           ["BRCA1", "BRCA2", "TP53", "EGFR", "KRAS", "PTEN", "MLH1"],
    "chromosome":     ["17",    "13",    "17",   "7",    "12",   "10",   "3"],
    "position":       [43044295, 32315474, 7674220, 55259515, 25398284, 89692905, 37067453],
    "ref":            ["A",    "G",     "C",    "T",    "G",    "A",    "C"],
    "alt":            ["T",    "A",     "T",    "A",    "T",    "G",    "T"],
    "classification": ["Pathogenic", "Benign", "Pathogenic", "VUS",
                       "Likely Pathogenic", "Benign", "Pathogenic"],
    "allele_freq":    [0.001, 0.45, 0.002, 0.12, 0.003, 0.38, 0.001]
}

df = pd.DataFrame(data)


print("== Shape (rows, columns) ===")
print(df.shape)

print ("\n== First 3 Rows ==")
print(df.head(3))

print("\n=== Column names ===")
print(df.columns.tolist())

print("\n=== Data types ===")
print(df.dtypes)

print("\n=== Summary stats ===")
print(df.describe())

print("\n=== Pathogenic only ===")
pathogenic = df[df["classification"] == "Pathogenic"]
print(pathogenic[["gene", "chromosome", "classification"]])

print("\n=== Rare variants (allele_freq < 0.01) ===")
rare = df[df["allele_freq"] < 0.01]
print(rare[["gene", "allele_freq", "classification"]])

print("\n=== Rare AND pathogenic or likely pathogenic ===")
clinically_relevant = df[
    (df["allele_freq"] < 0.01) &
    (df["classification"].isin(["Pathogenic", "Likely Pathogenic"]))
]
print(clinically_relevant[["gene", "allele_freq", "classification"]])

# --- Save to CSV ---
df.to_csv("day01/variants.csv", index=False)
print("\n=== Saved to variants.csv ===")

# --- Read it back ---
df_loaded = pd.read_csv("day01/variants.csv")
print("\n=== Loaded back from CSV ===")
print(df_loaded.head())