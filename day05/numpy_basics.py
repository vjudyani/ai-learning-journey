# Day 5 — NumPy basics
# Goal: understand arrays, matrix operations, and why this matters for ML

import numpy as np

# ─── Part 1: Arrays vs Lists ─────────────────────────────────────────

print("=== Arrays vs Lists ===")

# Regular Python list
python_list = [1, 2, 3, 4, 5]

# NumPy array
numpy_array = np.array([1, 2, 3, 4, 5])

print(f"Python list: {python_list}")
print(f"NumPy array: {numpy_array}")

# The big difference — math on lists vs arrays
print(f"\nList * 2:  {python_list * 2}")   # repeats the list
print(f"Array * 2: {numpy_array * 2}")     # multiplies every element


# ─── Part 2: Creating arrays ─────────────────────────────────────────

print("\n=== Creating arrays ===")

zeros = np.zeros(5)
ones = np.ones(5)
random = np.random.rand(5)
sequence = np.arange(0, 10, 2)   # 0 to 10, step 2

print(f"Zeros:    {zeros}")
print(f"Ones:     {ones}")
print(f"Random:   {np.round(random, 3)}")
print(f"Sequence: {sequence}")


# ─── Part 3: 2D arrays (matrices) ────────────────────────────────────

print("\n=== 2D arrays (matrices) ===")

# Think of this as a table — rows are samples, columns are features
# This is exactly how ML models see your data
variants_matrix = np.array([
    [0.001, 100, 1],   # patient_001: allele_freq, quality, is_pathogenic
    [0.003, 91,  1],   # patient_002
    [0.120, 72,  0],   # patient_003
    [0.450, 95,  0],   # patient_004
    [0.002, 88,  1],   # patient_005
])

print(f"Shape: {variants_matrix.shape}")   # (rows, columns)
print(f"Matrix:\n{variants_matrix}")

# Accessing rows and columns
print(f"\nFirst row (patient 1): {variants_matrix[0]}")
print(f"Last row (patient 5):  {variants_matrix[-1]}")
print(f"All allele freqs:      {variants_matrix[:, 0]}")  # all rows, column 0
print(f"All quality scores:    {variants_matrix[:, 1]}")  # all rows, column 1


# ─── Part 4: Array operations ────────────────────────────────────────

print("\n=== Array operations ===")

allele_freqs = variants_matrix[:, 0]
quality_scores = variants_matrix[:, 1]

print(f"Mean allele freq:    {np.mean(allele_freqs):.4f}")
print(f"Max quality score:   {np.max(quality_scores)}")
print(f"Min quality score:   {np.min(quality_scores)}")
print(f"Std allele freq:     {np.std(allele_freqs):.4f}")

# Boolean filtering — this is how ML models filter data
rare_variants = allele_freqs < 0.01
print(f"\nRare variant mask: {rare_variants}")
print(f"Rare variant rows:\n{variants_matrix[rare_variants]}")


# ─── Part 5: Why this matters for ML ─────────────────────────────────

print("\n=== Dot product — the core of neural networks ===")

# Every neural network layer does: output = input · weights + bias
# This is a dot product

inputs = np.array([0.001, 100, 1])        # one patient's features
weights = np.array([0.5, 0.01, 0.8])      # learned weights
bias = 0.1

output = np.dot(inputs, weights) + bias
print(f"Input features: {inputs}")
print(f"Weights:        {weights}")
print(f"Dot product + bias: {output:.4f}")
print("This single operation is what every neuron in a neural network computes")


# ─── Part 6: Normalization ────────────────────────────────────────────

print("\n=== Normalization ===")
# ML models need features on the same scale
# allele_freq is 0.001, quality is 100 — very different scales
# Normalization brings them to 0-1 range

def normalize(array):
    min_val = np.min(array)
    max_val = np.max(array)
    return (array - min_val) / (max_val - min_val)

raw_quality = variants_matrix[:, 1]
normalized_quality = normalize(raw_quality)

print(f"Raw quality scores:        {raw_quality}")
print(f"Normalized quality scores: {np.round(normalized_quality, 3)}")
print("Now all values are between 0 and 1 — ready for ML")