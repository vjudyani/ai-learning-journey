# Day 3 — Functions, error handling, VCF file parsing
# Goal: write clean reusable functions and handle real-world messy data

# ─── Part 1: Better functions ───────────────────────────────────────

def calculate_gc_content(sequence):
    """
    Calculate GC content of a DNA sequence.
    Returns a percentage rounded to 2 decimal places.
    """
    if not sequence:
        return 0.0
    
    sequence = sequence.upper()
    g_count = sequence.count("G")
    c_count = sequence.count("C")
    gc_content = (g_count + c_count) / len(sequence) * 100
    return round(gc_content, 2)


def classify_variant(allele_freq, classification):
    """
    Returns clinical priority based on frequency and classification.
    This is deterministic logic — exactly what AI systems use as guardrails.
    """
    high_risk = ["Pathogenic", "Likely Pathogenic"]
    
    if classification in high_risk and allele_freq < 0.01:
        return "HIGH PRIORITY"
    elif classification in high_risk and allele_freq >= 0.01:
        return "MODERATE PRIORITY"
    elif classification == "VUS":
        return "NEEDS REVIEW"
    else:
        return "LOW PRIORITY"


# Test your functions
sequences = ["ATGCGCTA", "GGGGCCCC", "ATATATAT", "", "atgcATGC"]
for seq in sequences:
    print(f"Sequence: {seq:10s} | GC content: {calculate_gc_content(seq)}%")

print()
test_variants = [
    ("BRCA1", 0.001, "Pathogenic"),
    ("KRAS",  0.003, "Likely Pathogenic"),
    ("EGFR",  0.15,  "Pathogenic"),
    ("TP53",  0.45,  "Benign"),
    ("MLH1",  0.08,  "VUS"),
]

for gene, freq, classification in test_variants:
    priority = classify_variant(freq, classification)
    print(f"{gene:6s} | freq: {freq:.3f} | {classification:20s} | {priority}")


# ─── Part 2: Error handling ──────────────────────────────────────────

print("\n=== Error handling ===")

def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print(f"Cannot divide {a} by zero")
        return None
    except TypeError:
        print(f"Invalid input types: {type(a)}, {type(b)}")
        return None

print(safe_divide(10, 2))     # works fine
print(safe_divide(10, 0))     # zero division
print(safe_divide(10, "x"))   # wrong type


# ─── Part 3: Write and read a VCF-style file ─────────────────────────

print("\n=== Writing VCF file ===")

vcf_content = """##fileformat=VCFv4.2
##reference=GRCh38
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
17\t43044295\trs80357906\tA\tT\t100\tPASS\tGENE=BRCA1;AF=0.001;CLASS=Pathogenic
13\t32315474\trs28897743\tG\tA\t95\tPASS\tGENE=BRCA2;AF=0.450;CLASS=Benign
17\t7674220\trs28934578\tC\tT\t88\tPASS\tGENE=TP53;AF=0.002;CLASS=Pathogenic
7\t55259515\trs121434568\tT\tA\t72\tFAIL\tGENE=EGFR;AF=0.120;CLASS=VUS
12\t25398284\trs112445441\tG\tT\t91\tPASS\tGENE=KRAS;AF=0.003;CLASS=Likely_Pathogenic
"""

with open("day03/sample.vcf", "w") as f:
    f.write(vcf_content)
print("sample.vcf written successfully")


print("\n=== Parsing VCF file ===")

def parse_info(info_string):
    """Parse the INFO column into a dictionary."""
    info_dict = {}
    for item in info_string.split(";"):
        if "=" in item:
            key, value = item.split("=")
            info_dict[key] = value
    return info_dict


def parse_vcf(filepath):
    """
    Parse a VCF file and return a list of variant dictionaries.
    Skips header lines starting with #.
    """
    variants = []
    
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                
                # skip header lines
                if line.startswith("#"):
                    continue
                
                # skip empty lines
                if not line:
                    continue
                
                # parse the 8 VCF columns
                parts = line.split("\t")
                if len(parts) < 8:
                    print(f"Skipping malformed line: {line}")
                    continue
                
                chrom, pos, vid, ref, alt, qual, filter_status, info = parts[:8]
                
                info_dict = parse_info(info)
                
                variant = {
                    "chrom":      chrom,
                    "pos":        int(pos),
                    "id":         vid,
                    "ref":        ref,
                    "alt":        alt,
                    "qual":       float(qual),
                    "filter":     filter_status,
                    "gene":       info_dict.get("GENE", "Unknown"),
                    "allele_freq": float(info_dict.get("AF", 0)),
                    "classification": info_dict.get("CLASS", "Unknown").replace("_", " ")
                }
                variants.append(variant)
                
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return []
    
    return variants


variants = parse_vcf("day03/sample.vcf")

print(f"Parsed {len(variants)} variants\n")

for v in variants:
    priority = classify_variant(v["allele_freq"], v["classification"])
    print(f"{v['gene']:6s} | chr{v['chrom']:2s}:{v['pos']} | "
          f"filter: {v['filter']:4s} | {v['classification']:20s} | {priority}")