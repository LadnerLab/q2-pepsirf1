import subprocess, os
import tempfile
import sys

from q2_pepsirf.format_types import (
     PeptideBinFormat,
    PepsirfContingencyTSVFormat,)

def bin(
    scores: PepsirfContingencyTSVFormat,
    allow_other_normalization: bool = False,
    bin_size: int = 300,
    round_to: int = 0,
    outfile: str = "./bin.out",
    pepsirf_binary: str = "pepsirf") -> PeptideBinFormat:
    
    #collect temp file names for bin output
    bin_out = PeptideBinFormat()

    if allow_other_normalization:
        print("hello world", file=sys.stderr, flush=True) 

    #collect absolute file path name if pepsirf binary is file
    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "'%s'" % (os.path.abspath(pepsirf_binary))

    #open temp file to work in
    with tempfile.TemporaryDirectory() as tempdir:

        #collect command line
        cmd = "%s bin -s %s -b %s -r %s -o %s" % (pepsirf_binary, str(scores), str(bin_size), str(round_to), str(bin_out))

        #add outfile to command
        cmd += ' >> %s' % (outfile)

        #run the collected command
        subprocess.run(cmd, shell=True, check=True)

        #return the bin outputs as qza's
        return bin_out

