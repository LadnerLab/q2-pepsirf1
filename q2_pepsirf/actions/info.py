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

    #create PepsirfInfoSNPNFormat output
    snpn_out = PepsirfInfoSNPNFormat()

    #get absolute file path to pepsirf if it is a file
    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "'%s'" % (os.path.abspath(pepsirf_binary))

    #open temp directory
    with tempfile.TemporaryDirectory() as tempdir:

        #put together command based on get input
        if get == "samples":
            cmd = "%s info -i %s -s %s" % (pepsirf_binary, str(input), str(snpn_out))
        elif get == "probes":
            cmd = "%s info -i %s -p %s" % (pepsirf_binary, str(input), str(snpn_out))

        #run command
        subprocess.run(cmd, shell=True)

        #return the SNPN output as qza
        return snpn_out
        
def infoSumOfProbes(
    input: PepsirfContingencyTSVFormat,
    pepsirf_binary: str = "pepsirf") -> PepsirfInfoSumOfProbesFmt:

    #create PepsirfInfoSumOfProbesFmt output
    sum_of_probes_out = PepsirfInfoSumOfProbesFmt()

    #get absolute file path to pepsirf if it is a file
    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "'%s'" % (os.path.abspath(pepsirf_binary))

    #open temp directory
    with tempfile.TemporaryDirectory() as tempdir:

        #put together command
        cmd = "%s info -i %s -c %s" % (pepsirf_binary, str(input), str(sum_of_probes_out))

        #run command
        subprocess.run(cmd, shell=True)

        #return the sum of probes output as qza
        return sum_of_probes_out