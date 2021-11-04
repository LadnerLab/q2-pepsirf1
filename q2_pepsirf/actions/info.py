import subprocess, os
import tempfile, qiime2

from qiime2.util import duplicate

from q2_pepsirf.format_types import(
    PepsirfInfoSNPNDirFmt,
    PepsirfInfoSNPNFormat,
    PepsirfInfoSumOfProbesFmt,
    PepsirfContingencyTSVFormat,
    InfoSNPN
)

def infoSNPN(
    input: PepsirfContingencyTSVFormat,
    get: str,
    pepsirf_binary: str = "pepsirf") -> PepsirfInfoSNPNFormat:

    snpn_out = PepsirfInfoSNPNFormat()

    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "'%s'" % (os.path.abspath(pepsirf_binary))

    with tempfile.TemporaryDirectory() as tempdir:
        if get == "samples":
            cmd = "%s info -i %s -s %s" % (pepsirf_binary, str(input), str(snpn_out))
        elif get == "probes":
            cmd = "%s info -i %s -p %s" % (pepsirf_binary, str(input), str(snpn_out))

        subprocess.run(cmd, shell=True)

        #return the zscore outputs as qza's
        return snpn_out
        
def infoSumOfProbes(
    input: PepsirfContingencyTSVFormat,
    pepsirf_binary: str = "pepsirf") -> PepsirfInfoSumOfProbesFmt:

    sum_of_probes_out = PepsirfInfoSumOfProbesFmt()

    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "'%s'" % (os.path.abspath(pepsirf_binary))

    with tempfile.TemporaryDirectory() as tempdir:

        cmd = "%s info -i %s -c %s" % (pepsirf_binary, str(input), str(sum_of_probes_out))

        subprocess.run(cmd, shell=True)

        #return the zscore outputs as qza's
        return sum_of_probes_out