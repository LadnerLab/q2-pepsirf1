from posixpath import abspath
from q2_pepsirf.format_types import(
    EnrichedPeptideDirFmt, PepsirfContingencyTSVFormat, EnrichThreshFileFormat
)

import csv
import itertools
import os
import qiime2
import subprocess
import tempfile

# Name: _make_pairs_file
# Process: function used to take source metadata and create pairs files
# Method inputs/parameters: column, outpath
# Method outputs/Returned: the pairs result
# Dependencies: itertools
def _make_pairs_file(column, outpath):
    series = column.to_series()
    pairs = {k: v.index for k,v in series.groupby(series)}
    result = []

    for _, ids in pairs.items():
        result.append(list(itertools.combinations(ids, 2)))

    with open(outpath, "w") as fh:
        for pair in result:
            for a, b in pair:
                fh.write(a + "\t" + b + "\n")

    return result

# Name: _make_reps_file
# Process: function used to take source metadata and create replicates files
# Method inputs/parameters: column, outpath
# Method outputs/Returned: None
# Dependencies: itertools
def _make_reps_file(column, outpath):
    series = column.to_series()
    pairs = {k: v.index for k,v in series.groupby(series)}
    with open( outpath, 'w' ) as of:
        for _, reps in pairs.items():
            for rep in reps[:len(reps) - 1]:
                of.write( rep + "\t" )
            of.write( reps[ len(reps) - 1] )
            of.write( "\n" )

# Name: enrich
# Process: runs pepsirf's enrich module
# Method inputs/parameters: source, flex_reps, thresh_file, zscores, col_sum,
# exact_z_thresh, exact_cs_thresh, raw_scores, raw_constraint,
# enrichment_failure, truncate, outfile, pepsirf_binary
# Method outputs/Returned: the enriched directory
# Dependencies: subprocess, os, csv, tempfile
def enrich(
        source: qiime2.CategoricalMetadataColumn,
        flex_reps: bool = False,
        thresh_file: EnrichThreshFileFormat = None,
        zscores: PepsirfContingencyTSVFormat = None,
        col_sum: PepsirfContingencyTSVFormat = None,
        exact_z_thresh: str = None,
        exact_cs_thresh: str = None,
        raw_scores: PepsirfContingencyTSVFormat = None,
        raw_constraint: int = None,
        enrichment_failure: bool = False,
        truncate: bool = False,
        low_raw_reads: bool = False,
        outfile: str = "./enrich.out",
        pepsirf_binary: str = "pepsirf"
) -> EnrichedPeptideDirFmt:
    #create EnrichedPeptideDirFmt output
    dir_fmt_output = EnrichedPeptideDirFmt()

    #get absolute file path to pepsirf if it is a file
    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "%s" % os.path.abspath(pepsirf_binary)

    #open temp directory
    with tempfile.TemporaryDirectory() as tempdir:
        # check invocation by flexible reps
        if flex_reps:
            # make reps file with given source metadata
            tmp_pairs_file = os.path.join(tempdir, "pairs.tsv")
            _make_reps_file(source, tmp_pairs_file)
        else: # otherwise, assume infer pairs
            tmp_pairs_file = os.path.join(tempdir, "pairs.tsv")
            _make_pairs_file(source, tmp_pairs_file)

        #set up default threshold files and peptide enrichment suffix
        tmp_thresh_file = os.path.join(tempdir, "tempThreshFile.tsv")
        out_suffix = "_enriched.txt"

        #create threshold file if not provided
        if not thresh_file:
            #create a temporary thresh file in the temporary directory
            with open(tmp_thresh_file, "w", newline="") as out_file:
                tsv_writer = csv.writer(out_file, delimiter="\t")
                tsv_writer.writerow([str(zscores), exact_z_thresh])
                tsv_writer.writerow([str(col_sum), exact_cs_thresh])
        else:
            tmp_thresh_file = str(thresh_file)

        #put together command
        cmd = (
            "%s enrich -t %s -s %s -x %s -o %s"
            % (
                pepsirf_binary, tmp_thresh_file, tmp_pairs_file,
                out_suffix, str(dir_fmt_output)
            )
        )

        #add optionals to command
        if raw_scores:
            cmd += " -r %s" % str(raw_scores)
        if raw_constraint:
            cmd += " --raw_score_constraint %s" % str(raw_constraint)
        if enrichment_failure:
            enrichment_failure = "failedEnrichment.txt"
            cmd += " -f %s" % enrichment_failure
        if low_raw_reads:
            cmd += " --low_raw_reads"
        if truncate:
            cmd += " --output_filename_truncate"

        #add outfile to command
        cmd += " >> %s" % outfile

        #run command
        s = subprocess.run(cmd, shell=True, check=True)

        #check exit code and raise error if not 0
        if s.returncode > 0:
            raise ValueError(
                "Enrich module failed. Exit code %s." % str(s.returncode)
            )

        # check if failure file exists
        failed = (dir_fmt_output.path/"failedEnrichment.txt")

        # if file doesn't exist create empty file
        if not failed.exists():
            with failed.open("w") as fh:
                pass

        # check if the only file is failed
        # dir_fmt_output.path.iterdir() or #... .path.glob('*_enriched.txt')
        if len(list(dir_fmt_output.path.iterdir())) <= 1:
            raise ValueError("No enriched peptides.")

        #return enrich directory as qza
        return dir_fmt_output
