from q2_pepsirf.format_types import (
    PepsirfContingencyTSVFormat, SubjoinMultiFileFmt
)

import os
import qiime2
import subprocess
import tempfile

# Name: subjoin
# Process: runs pepsirf's subjoin module
# Method inputs/parameters: input_type, multi_file, subjoin_input,
# filter_peptide_names, duplicate_evaluation, outfile, pepsirf_binary
# Method outputs/Returned: the subjoin output tsv
# Dependencies: subprocess, os, tempfile
def subjoin(
        input_type: str = "raw",
        multi_file_input: list = None,
        multi_file: SubjoinMultiFileFmt = None,
        subjoin_input: str = None,
        filter_peptide_names: bool = False,
        duplicate_evaluation: str = "include",
        outfile: str = "./subjoin.out",
        pepsirf_binary: str = "pepsirf") -> PepsirfContingencyTSVFormat:

    #collect filepath for TSVFormat
    tsv_output = PepsirfContingencyTSVFormat()

    #collect absolute filepaths for input files and binary if it is a file
    if multi_file:
        multi_file = "%s" % str(multi_file)

    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "%s" % os.path.abspath(pepsirf_binary)

    #create a temp directory to run pepsirf in
    with tempfile.TemporaryDirectory() as tempdir:
        if multi_file:
            #start command with required/defualt parameters
            cmd = (
                "%s subjoin -m %s -d %s -o %s"
                % (
                    pepsirf_binary, multi_file,
                    duplicate_evaluation, tsv_output
                )
            )
        elif subjoin_input:
            cmd = (
                "%s subjoin -i %s -d %s -o %s"
                % (
                    pepsirf_binary, subjoin_input,
                    duplicate_evaluation, tsv_output
                )
            )
        elif multi_file_input:
            mf_input = "-i " + " -i ".join(multi_file_input)
            cmd = (
                "%s subjoin %s -d %s -o %s"
                % (pepsirf_binary, mf_input, duplicate_evaluation, tsv_output)
            )

    if filter_peptide_names:
        cmd += " --filter_peptide_names"

    #add outfile to command
    cmd += " >> %s" % outfile

    #run command in the command line
    subprocess.run(cmd, shell=True, check=True)

    #return norm output
    return tsv_output

