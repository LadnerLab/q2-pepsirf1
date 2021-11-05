import subprocess, os
import tempfile

from q2_pepsirf.format_types import (
     PeptideBinFormat,
    PepsirfContingencyTSVFormat,)

def bin(
    scores: PepsirfContingencyTSVFormat,
    bin_size: int = 300,
    round_to: int = 0,
    pepsirf_binary: str = "pepsirf") -> PeptideBinFormat:
    
    #collect temp file names for bin output
    bin_out = PeptideBinFormat()

    #collect absolute file path name if pepsirf binary is file
    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "'%s'" % (os.path.abspath(pepsirf_binary))

    #open temp file to work in
    with tempfile.TemporaryDirectory() as tempdir:

        #collect command line
        cmd = "%s bin -s %s -b %s -r %s -o %s" % (pepsirf_binary, str(scores), str(bin_size), str(round_to), str(bin_out))

        #run the collected command
        subprocess.run(cmd, shell=True)

        #return the bin outputs as qza's
        return bin_out

