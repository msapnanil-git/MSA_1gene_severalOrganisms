import os
from Bio import SeqIO
import subprocess
# SeqIO for sequence file operations; os for directories; subprocess for running external programs

in_dir = "FGF5_MSA"  
# location of FASTA files
out_dir = "FGF5_MSA"
os.makedirs(out_dir, exist_ok=True)
# makes a folder with the given output directory name (out_dir); doesn't give error if the folder already exists

merged_seq_path = os.path.join(out_dir, "merged_seq.fasta")
# defines path of the merged FASTA file

with open(merged_seq_path, "w") as outfile:
    for filename in os.listdir(in_dir):
        if filename.endswith(".fasta") or filename.endswith(".fa"):
            filepath = os.path.join(in_dir, filename)
            for record in SeqIO.parse(filepath, "fasta"):
                SeqIO.write(record, outfile, "fasta")
# merges all the FASTA files from input folder for MSA
print(f"\n \033[92mMerged sequences into  \033[0m{merged_seq_path}")
# prints merging status

msa_out_path = os.path.join(out_dir, "msa_muscle.fasta")
# defines output path for MSA file

try:
    subprocess.run(
        ["muscle", "-align", merged_seq_path, "-output", msa_out_path],
        check=True
    )
# runs alignment in MUSCLE externally and saves the file in output directory (out_dir)
    print(f"\n \033[92mMSA completed. File saved in \033[0m{msa_out_path}")
# prints output status for MSA

except subprocess.CalledProcessError as e:
    print(f"\n \033[91mError running MUSCLE: \033[0m{e}")
# read and print errors if any
