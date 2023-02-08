from q2_pepsirf.format_types import PeptideFastaFmt, ProteinFastaFmt, PepsirfLinkTSVFormat

import os
import qiime2
import subprocess
import tempfile

# Name: link
# Process: runs pepsirf's link module
# Method inputs/parameters: protein_file, peptide_file, meta,
# kmer_size, kmer_redundancy_control, outfile, pepsirf_binary
# Method outputs/Returned: the link tsv
# Dependencies: subprocess, os, tempfile
def link(
        protein_file: ProteinFastaFmt,
        peptide_file: PeptideFastaFmt,
        meta: str,
        kmer_size: int,
        kmer_redundancy_control: bool = False,
        outfile: str = "./link.out",
        pepsirf_binary: str = "pepsirf") -> PepsirfLinkTSVFormat:

    #collect filepath for TSVFormat
    tsv_output = PepsirfLinkTSVFormat()

    #collect absolute filepaths for input files and binary if it is a file
    protein_file = "%s" % str(protein_file)
    peptide_file = "%s" % str(peptide_file)

    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "%s" % os.path.abspath(pepsirf_binary)

    #create a temp directory to run pepsirf in
    with tempfile.TemporaryDirectory() as tempdir:
        #start command with required/defualt parameters
        cmd = (
            "%s link --protein_file %s --peptide_file %s"
            " --meta %s -k %s -o %s"
            % (
                pepsirf_binary, protein_file, peptide_file,
                meta, str(kmer_size), tsv_output
            )
        )

        #check if optional parameters are inputted and add to command
        if kmer_redundancy_control:
            cmd += " -r"

        #add outfile to command
        cmd += " >> %s" % outfile

        #run command in the command line
        subprocess.run(cmd, shell=True, check=True)

    #return norm output
    return tsv_output

