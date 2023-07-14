from q2_pepsirf.format_types import(
    PepsirfInfoSNPNDirFmt, PepsirfInfoSNPNFormat, PepsirfInfoSumOfProbesFmt,
    PepsirfContingencyTSVFormat, InfoSNPN
)

import os
import pandas as pd
import qiime2
import subprocess
import tempfile

# Name: infoSNPN
# Process: runs pepsirf's info sample/probes module
# Method inputs/parameters: input, get, outfile, pepsirf_binary
# Method outputs/Returned: the samples names or probes names tsv
# Dependencies: subprocess, os, tempfile
def infoSNPN(
        input: PepsirfContingencyTSVFormat,
        get: str,
        outfile: str = "./info.out",
        pepsirf_binary: str = "pepsirf") -> PepsirfInfoSNPNFormat:

    #create PepsirfInfoSNPNFormat output
    snpn_out = PepsirfInfoSNPNFormat()

    #get absolute file path to pepsirf if it is a file
    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "%s" % os.path.abspath(pepsirf_binary)

    #open temp directory
    with tempfile.TemporaryDirectory() as tempdir:
        #put together command based on get input
        if get == "samples":
            cmd = (
                "%s info -i %s -s %s"
                % (pepsirf_binary, str(input), str(snpn_out))
            )
        elif get == "probes":
            cmd = (
                "%s info -i %s -p %s"
                % (pepsirf_binary, str(input), str(snpn_out))
            )

        #add outfile to command
        cmd += " >> %s" % outfile

        #run command
        subprocess.run(cmd, shell=True, check=True)

    #return the SNPN output as qza
    return snpn_out
        
# Name: infoSumOfProbes
# Process: runs pepsirf's info sum of probes module
# Method inputs/parameters: input, outfile, pepsirf_binary
# Method outputs/Returned: the sum of probes names tsv
# Dependencies: subprocess, os, tempfile
def infoSumOfProbes(
        input: PepsirfContingencyTSVFormat,
        outfile: str = "./info.out",
        pepsirf_binary: str = "pepsirf") -> PepsirfInfoSumOfProbesFmt:

    #create PepsirfInfoSumOfProbesFmt output
    sum_of_probes_out = PepsirfInfoSumOfProbesFmt()

    #get absolute file path to pepsirf if it is a file
    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "%s" % os.path.abspath(pepsirf_binary)

    #open temp directory
    with tempfile.TemporaryDirectory() as tempdir:

        #put together command
        cmd = (
            "%s info -i %s -c %s"
            % (pepsirf_binary, str(input), str(sum_of_probes_out))
        )

        #add outfile to command
        cmd += " >> %s" % outfile

        #run command
        subprocess.run(cmd, shell=True, check=True)

    #return the sum of probes output as qza
    return sum_of_probes_out

