import subprocess, os
import tempfile, qiime2

from q2_pepsirf.format_types import (PepsirfContingencyTSVFormat,
                                    PeptideBinFormat,
                                    ZscoreNanFormat)

def zscore(
    scores: PepsirfContingencyTSVFormat,
    bins: PeptideBinFormat,
    trim: float = 2.5,
    hdi: float = 0.0,
    num_threads: int = 2,
    pepsirf_binary: str = "pepsirf") -> tuple[PepsirfContingencyTSVFormat, ZscoreNanFormat]:

    zscore_output = PepsirfContingencyTSVFormat()
    nan_report = ZscoreNanFormat()

    scores = os.path.abspath(scores)

    bins = os.path.abspath(bins)

    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "'%s'" % (os.path.abspath(pepsirf_binary))

    with tempfile.TemporaryDirectory() as tempdir:
        
        cmd = "%s zscore -s %s -b %s -t %s -d %s -o %s -n %s --num_threads %s" % (
            pepsirf_binary, str(PepsirfContingencyTSVFormat),
            str(bins), str(trim), str(hdi), str(zscore_output),
            str(nan_report), str(num_threads))

        subprocess.run(cmd, shell=True)

        return [zscore_output, nan_report]