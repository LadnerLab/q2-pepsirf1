import subprocess, os
import tempfile, qiime2

from q2_pepsirf.format_types import PepsirfContingencyTSVFormat

def norm(
    peptide_scores: PepsirfContingencyTSVFormat,
    normalize_approach: str = "col_sum",
    negative_control: PepsirfContingencyTSVFormat = None,
    negative_id: str = None,
    negative_names: list = None,
    precision: int = 2,
    outfile: str = "./norm.out",
    pepsirf_binary: str = "pepsirf") -> PepsirfContingencyTSVFormat:
    
    #collect filepath for TSVFormat
    tsv_output = PepsirfContingencyTSVFormat()

    #collect absolute filepaths for input files and binary if it is a file
    if peptide_scores:
        peptide_scores = "'%s'" % os.path.abspath(str(peptide_scores))

    if negative_control:
        negative_control = "'%s'" % os.path.abspath(str(negative_control))

    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "'%s'" % (os.path.abspath(pepsirf_binary))

    #create a temp directory to run pepsirf in
    with tempfile.TemporaryDirectory() as tempdir:

        #start command with required/defualt parameters
        cmd = '%s norm -a %s --precision %s -o %s -p %s' % (
            pepsirf_binary, normalize_approach, str(precision),
            str(tsv_output), str(peptide_scores)
            )

        #check if optional parameters are inputted and add to command
        if negative_control:
            cmd += ' --negative_control %s' % (str(negative_control))
        if negative_id:
            cmd += ' -s %s' % (negative_id)
        if negative_names:
            cmd += ' -n %s' % (','.join(negative_names))

        #add outfile to command
        cmd += ' >> %s' % (outfile)

        #run command in the command line
        subprocess.run(cmd, shell=True)

        #return norm output
        return tsv_output
    