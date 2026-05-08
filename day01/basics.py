# Day 1 — Python fundamentals
# Goal: understand variables, lists, dicts, loops, functions

# --- Variables and types ---
name = "Vedika"
age = 30
is_researcher = True

print(type(name))
print(type(age))
print(type(is_researcher))

# --- Lists ---
genes = ["BRCA1", "BRCA2", "TP53", "EGFR", "KRAS"]

print(genes[0])        # first item
print(genes[-1])       # last item
print(genes[1:3])      # slicing — items at index 1 and 2

for gene in genes:
    print(f"Gene: {gene}")

# --- Dictionaries ---
variant = {
    "gene": "BRCA1",
    "position": 43044295,
    "ref": "A",
    "alt": "T",
    "classification": "Pathogenic"
}

print(variant["gene"])
print(variant["classification"])

for key, value in variant.items():
    print(f"{key}: {value}")

# --- Functions ---
def is_pathogenic(classification):
    return classification == "Pathogenic"

print(is_pathogenic(variant["classification"]))  # should print True
print(is_pathogenic("Benign"))                   # should print False

# --- List of dicts (this is how real genomic data looks) ---
variants = [
    {"gene": "BRCA1", "classification": "Pathogenic"},
    {"gene": "TP53",  "classification": "Likely Pathogenic"},
    {"gene": "KRAS",  "classification": "Benign"},
    {"gene": "EGFR",  "classification": "Pathogenic"},
]

# Filter only pathogenic variants using list comprehension
pathogenic = [v for v in variants if v["classification"] == "Pathogenic"]

print(f"\nPathogenic variants found: {len(pathogenic)}")
for v in pathogenic:
    print(f"  {v['gene']}")