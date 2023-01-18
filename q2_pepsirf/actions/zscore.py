from q2_pepsirf.format_types import (PepsirfContingencyTSVFormat, PeptideBinFormat, ZscoreNan,
                                     ZscoreNanFormat
                                     )
import os
import subprocess
import tempfile
import qiime2

# Name: zsore
# Process: runs pepsirf's zscore module
# Method inputs/parameters: scores, bins, trim, hdi, num_threads,
#  outfile, pepsirf_binary
# Method outputs/Returned: the zscore output tsv and nan report
# Dependencies: subprocess, os, tempfile
def zscore(
        scores: PepsirfContingencyTSVFormat,
        bins: PeptideBinFormat,
        trim: float = 2.5,
        hdi: float = 0.0,
        num_threads: int = 2,
        outfile: str = "./zscore.out",
        pepsirf_binary: str = "pepsirf") -> (PepsirfContingencyTSVFormat, ZscoreNanFormat):

    #collect temp file names for zscore output
    zscore_output = PepsirfContingencyTSVFormat()
    nan_report = ZscoreNanFormat()

    #collect absolute file path names for inputs
    scores = "%s" % (os.path.abspath(str(scores)))
    bins = "%s" % (os.path.abspath(str(bins)))

    #collect absolute file path name if pepsirf binary is file
    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "%s" % (os.path.abspath(pepsirf_binary))

    #open temp file to work in
    with tempfile.TemporaryDirectory() as tempdir:
        
        #collect command line
        cmd = ("%s zscore -s %s -b %s -t %s"
               " -d %s -o %s -n %s --num_threads %s"
               % (pepsirf_binary, str(scores), str(bins), str(trim),
                  str(hdi), str(zscore_output), str(nan_report), str(num_threads)
                  )
               )

        #add outfile to end of command
        cmd += " >> %s" % (outfile)

        #run the collected command
        subprocess.run(cmd, shell=True, check=True)

        #return the zscore outputs as qza's
        return (zscore_output, nan_report)

