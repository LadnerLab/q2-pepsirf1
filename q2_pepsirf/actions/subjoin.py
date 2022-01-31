import subprocess, os
import tempfile, qiime2
from q2_pepsirf.format_types import PepsirfContingencyTSVFormat, SubjoinMultiFileFmt

def subjoin(
    input_type: str = "raw",
    multi_file: SubjoinMultiFileFmt = None,
    subjoin_input: str = None,
    filter_peptide_names: bool = False,
    duplicate_evaluation: str = "include",
    outfile: str = "./subjoin.out",
    pepsirf_binary: str = "pepsirf") -> PepsirfContingencyTSVFormat:

    #collect filepath for TSVFormat
    tsv_output = PepsirfContingencyTSVFormat()

    #collect absolute filepaths for input files and binary if it is a file
    multi_file = "'%s'" % (str(multi_file))

    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "'%s'" % (os.path.abspath(pepsirf_binary))

    #create a temp directory to run pepsirf in
    with tempfile.TemporaryDirectory() as tempdir:

        if multi_file:
            #start command with required/defualt parameters
            cmd = "%s subjoin -m %s -d %s -o %s" % (
                pepsirf_binary, multi_file, duplicate_evaluation, tsv_output
            )
        elif subjoin_input:
            cmd = "%s subjoin -i %s -d %s -o %s" % (
                pepsirf_binary, subjoin_input, duplicate_evaluation, tsv_output
            )

    if filter_peptide_names:
        cmd += " --filter_peptide_names"

    #add outfile to command
    cmd += ' >> %s' % (outfile)

    #run command in the command line
    subprocess.run(cmd, shell=True, check=True)

    #return norm output
    return tsv_output
