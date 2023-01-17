from q2_pepsirf.format_types import(PepsirfContingencyTSVFormat, PepsirfDemuxDiagnosticFormat, PepsirfDemuxFastqFmt,
                                    PepsirfDemuxFifFmt, PepsirfDemuxIndexFmt, PepsirfDemuxLibraryFmt,
                                    PepsirfDemuxSampleListFmt
                                    )
import os
import subprocess
import tempfile
import qiime2

# Name: demux
# Process: runs pepsirf's demux module (currently in the development branch)
# Method inputs/parameters: input_r1, index, samplelist, seq input_r2, fif,
# library, read_per_loop, num_threads, phred_base, phred_min_score, sindex,
# translate_aggregates, concatemer, sname, index1, index2, outfile, pepsirf_binary
# Method outputs/Returned: the raw data and diagnostic data
# Dependencies: subprocess, os, tempfile
def demux(
        input_r1: PepsirfDemuxFastqFmt,
        index: PepsirfDemuxIndexFmt,
        samplelist: PepsirfDemuxSampleListFmt,
        seq: str,
        input_r2: PepsirfDemuxFastqFmt = None,
        fif: PepsirfDemuxFifFmt = None,
        library: PepsirfDemuxLibraryFmt = None,
        read_per_loop: int = 100000,
        num_threads: int = 2,
        phred_base: int = 33,
        phred_min_score: int = 0,
        sindex: str = None,
        translate_aggregates: bool = False,
        concatemer: bool = False,
        sname: str = "SampleName",
        index1: str = None,
        index2: str = "0,0,0",
        outfile: str = "./deconv.out",
        pepsirf_binary: str = "pepsirf") -> (PepsirfContingencyTSVFormat, PepsirfDemuxDiagnosticFormat):
    
    #collect filepath for outputs
    raw_data = PepsirfContingencyTSVFormat()
    diagnostic_data = PepsirfDemuxDiagnosticFormat()

    #collect absolute filepaths for input files and binary if it is a file
    input_r1 = "%s" % (str(input_r1))
    input_r2 = "%s" % (str(input_r2))
    index = "%s" % (str(index))
    samplelist = "%s" % (str(samplelist))

    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "%s" % (os.path.abspath(pepsirf_binary))

    #create a temp directory to run pepsirf in
    with tempfile.TemporaryDirectory() as tempdir:

        #start command with required/defualt parameters
        cmd = ("%s demux --input_r1 %s --input_r2 %s"
               " --seq %s -r %s -t %s"
               " --phred_base %s -i %s -s %s"
               " --phred_min_sore %s --sname %s -d %s"
               " -o %s"
              % (pepsirf_binary, input_r1, input_r2,
                 seq, read_per_loop, num_threads, 
                 phred_base, index, samplelist,
                 phred_min_score, sname, diagnostic_data, 
                 raw_data
                 )
               )

        #check if optional parameters are inputted and add to command
        if fif:
            fif = "%s" % (str(fif))
            cmd += " -f %s" % (fif)
        if library:
            library = "%s" % (str(library))
            cmd += " -l %s" % (library)
        if translate_aggregates:
            cmd += " --translate_aggregates"
        if concatemer:
            cmd += " --concatemer"
        if index1:
            cmd += " --index1 %s" % (index1)
        if index2:
            cmd += " --index2 %s" % (index2)
        if sindex:
            cmd += " --sindex %s " % (sindex)

        #add outfile to command
        cmd += " >> %s" % (outfile)

        #run command
        subprocess.run(cmd, shell=True, check=True)

    #return output
    return raw_data, diagnostic_data

