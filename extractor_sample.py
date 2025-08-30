from Bio import Entrez, SeqIO
import os
import time
# Entrez for NCBI access; SeqIO for sequence file operations; os for directories; time for rate limiting

Entrez.email = "example@gmail.com"
# provides email for database access

out_dir = "FGF5_MSA"
# gives name for folder creation
os.makedirs(out_dir, exist_ok=True)
# makes a folder with the given output directory name (out_dir); doesn't give error if the folder already exists

gene = 'FGF5'
organisms = ["Canis lupus familiaris", "Felis catus", "Mus musculus", "Oryctolagus cuniculus", "Homo sapiens sapiens"]
# defines the gene and the list of organisms

for org in organisms:
    # runs a for loop for using all organisms one by one
    sr_query = f'{gene}[Gene] AND {org}[Organism] AND biomol_genomic[PROP] NOT WGS[Filter]'
    sr_handle = Entrez.esearch(db="nucleotide", term=sr_query, retmax=2)
    sr_results = Entrez.read(sr_handle)
    sr_handle.close()
    # runs the search with specific parameters and filters (non-shotgun sequences only) provided; reads the search result 

    id_list = sr_results["IdList"]
    print(f"\n \033[92mFound \033[0m{len(id_list)} \033[92mrecords with defined nucleotide sequences")
	# prints the status of the query

    for i, ncbi_id in enumerate(id_list, 1):
	# runs a for loop for aearching all the organisms one by one
        try:
            print(f"\n \033[94mFetching ID: \033[0m{ncbi_id}")
            # print fetching status
            ft_handle = Entrez.efetch(db="nucleotide", id=ncbi_id, rettype="fasta", retmode="text")
            ft_record = SeqIO.read(ft_handle, "fasta")
            ft_handle.close()
            # fetches NCBI IDs for saving

            org_cl = org.replace(" ", "_")
            fasta_file = os.path.join(out_dir, f"{org_cl}_{ncbi_id}.fasta")
            with open(fasta_file, "w") as f:
                SeqIO.write(ft_record, f, "fasta")
          		# creates and saves the FASTA file
            print(f"\n \033[92mFASTA saved \033[0m{fasta_file}")
	    	# print saving status for FASTA files

            time.sleep(1)
            # intentional delay for complying with server rate limit

        except Exception as err:
            print(f"\n \033[91mError with ID \033[0m{ncbi_id}: {err}")
	   		# read and print errors if any

