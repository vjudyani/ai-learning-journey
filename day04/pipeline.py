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