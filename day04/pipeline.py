# Day 4 - Building a variant processing pipeline 
#Goal: Process multiple samples, write clean reusable code, output results 

import pandas as pd
import os

# --- Part 1: generate multiple sample files --------

def create_sample_vcf(filepath, sample_name, variants):
    """write a sample VCF file for one sample"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open (filepath, "w") as f:
        f.write("##fileformat=VCFv4.2\n")
        f.write(f"##sample={sample_name}\n")
        f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
        for v in variants:
            f.write(f"{v['chrom']}\t{v['pos']}\t{v['id']}\t{v['ref']}\t{v['alt']}\t{v['qual']}\t{v['filter']}\t")
            f.write(f"GENE={v['gene']};AF={v['af']};CLASS={v['cls'].replace(' ', '_')}\n")
    print(f"Created sample VCF: {filepath}")


#Sample data for 3 patients
samples = {
    "patient_001": [
        {"chrom":"17","pos":43044295,"id":"rs1","ref":"A","alt":"T","qual":100,"filter":"PASS","gene":"BRCA1","af":0.001,"cls":"Pathogenic"},
        {"chrom":"13","pos":32315474,"id":"rs2","ref":"G","alt":"A","qual":95, "filter":"PASS","gene":"BRCA2","af":0.450,"cls":"Benign"},
        {"chrom":"17","pos":7674220, "id":"rs3","ref":"C","alt":"T","qual":88, "filter":"PASS","gene":"TP53", "af":0.002,"cls":"Pathogenic"},
    ],
    "patient_002": [
        {"chrom":"7", "pos":55259515,"id":"rs4","ref":"T","alt":"A","qual":72, "filter":"FAIL","gene":"EGFR", "af":0.120,"cls":"VUS"},
        {"chrom":"12","pos":25398284,"id":"rs5","ref":"G","alt":"T","qual":91, "filter":"PASS","gene":"KRAS", "af":0.003,"cls":"Likely_Pathogenic"},
        {"chrom":"10","pos":89692905,"id":"rs6","ref":"A","alt":"G","qual":85, "filter":"PASS","gene":"PTEN", "af":0.380,"cls":"Benign"},
    ],
    "patient_003": [
        {"chrom":"3", "pos":37067453,"id":"rs7","ref":"C","alt":"T","qual":90, "filter":"PASS","gene":"MLH1", "af":0.001,"cls":"Pathogenic"},
        {"chrom":"17","pos":43044295,"id":"rs1","ref":"A","alt":"T","qual":98, "filter":"PASS","gene":"BRCA1","af":0.001,"cls":"Pathogenic"},
        {"chrom":"7", "pos":55259515,"id":"rs4","ref":"T","alt":"A","qual":65, "filter":"FAIL","gene":"EGFR", "af":0.120,"cls":"VUS"},
    ]

}      

#Write all sample files 

for sample_name, variants in samples.items():
    create_sample_vcf(f"day04/samples/{sample_name}.vcf", sample_name, variants)


# ─── Part 2: Parse all samples into one DataFrame ────────────────────

def parse_info(info_string):
    """Parse INFO column into a dictionary."""
    info_dict = {}
    for item in info_string.split(";"):
        if "=" in item:
            key, value = item.split("=")
            info_dict[key] = value
    return info_dict


def parse_vcf_to_df(filepath, sample_name):
    """Parse a VCF file and return a DataFrame with sample name added."""
    rows = []

    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue

                parts = line.split("\t")
                if len(parts) < 8:
                    continue

                chrom, pos, vid, ref, alt, qual, filter_status, info = parts[:8]
                info_dict = parse_info(info)

                rows.append({
                    "sample":         sample_name,
                    "chrom":          chrom,
                    "pos":            int(pos),
                    "ref":            ref,
                    "alt":            alt,
                    "qual":           float(qual),
                    "filter":         filter_status,
                    "gene":           info_dict.get("GENE", "Unknown"),
                    "allele_freq":    float(info_dict.get("AF", 0)),
                    "classification": info_dict.get("CLASS", "Unknown").replace("_", " ")
                })
    except FileNotFoundError:
        print(f"File not found: {filepath}")

    return pd.DataFrame(rows)


# Parse all 3 sample files and combine into one DataFrame
print("\n=== Parsing all samples ===")
all_dfs = []

for sample_name in samples.keys():
    filepath = f"day04/samples/{sample_name}.vcf"
    df = parse_vcf_to_df(filepath, sample_name)
    all_dfs.append(df)
    print(f"  {sample_name}: {len(df)} variants loaded")

combined = pd.concat(all_dfs, ignore_index=True)
print(f"\nTotal variants across all samples: {len(combined)}")


# ─── Part 3: Analyse the combined data ───────────────────────────────

print("\n=== Classification breakdown ===")
print(combined["classification"].value_counts())

print("\n=== Variants per sample ===")
print(combined["sample"].value_counts())

print("\n=== PASS filter only ===")
passed = combined[combined["filter"] == "PASS"]
print(f"Variants passing filter: {len(passed)} out of {len(combined)}")

print("\n=== High priority variants (rare + pathogenic) ===")
high_priority = combined[
    (combined["allele_freq"] < 0.01) &
    (combined["classification"].isin(["Pathogenic", "Likely Pathogenic"])) &
    (combined["filter"] == "PASS")
]
print(high_priority[["sample", "gene", "allele_freq", "classification"]])

print("\n=== Genes appearing in multiple patients ===")
gene_counts = combined.groupby("gene")["sample"].nunique()
recurrent = gene_counts[gene_counts > 1]
print(recurrent)


# ─── Part 4: Save results ─────────────────────────────────────────────

combined.to_csv("day04/all_variants.csv", index=False)
high_priority.to_csv("day04/high_priority_variants.csv", index=False)

print("\n=== Saved ===")
print("all_variants.csv — all variants from all samples")
print("high_priority_variants.csv — only actionable variants")