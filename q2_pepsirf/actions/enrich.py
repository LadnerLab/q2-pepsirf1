from posixpath import abspath
import subprocess, os, csv
import tempfile, qiime2

from q2_pepsirf.format_types import (
    EnrichedPeptideDirFmt, 
    PepsirfContingencyTSVFormat,
    EnrichThreshFileFormat
    )

#function used to take source metadata and create pairs files
def _make_pairs_file(column, outpath):
    series = column.to_series()
    pairs = {k: v.index for k,v in series.groupby(series)}
    with open(outpath, 'w') as fh:
        for _, ids in pairs.items():
            fh.write('\t'.join(ids) + '\n')

def enrich(
    source: qiime2.CategoricalMetadataColumn,
    thresh_file: EnrichThreshFileFormat = None,
    zscores: PepsirfContingencyTSVFormat = None,
    exact_z_thresh: str = None,
    raw_scores: PepsirfContingencyTSVFormat = None,
    raw_constraint: int = None,
    enrichment_failure: bool = False,
    truncate: bool = False,
    pepsirf_binary: str = "pepsirf") -> EnrichedPeptideDirFmt:

    #create EnrichedPeptideDirFmt output
    dir_fmt_output = EnrichedPeptideDirFmt()

    #get absolute file path to pepsirf if it is a file
    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "'%s'" % (os.path.abspath(pepsirf_binary))

    #open temp directory
    with tempfile.TemporaryDirectory() as tempdir:

        #make pairs file with given source metadata
        pairsFile = os.path.join(tempdir, 'pairs.tsv')
        _make_pairs_file(source, pairsFile)

        #set up default threshold files and peptide enrichment suffix
        threshFile = "tempThreshFile.tsv"
        outSuffix = "_enriched.txt"

        #create threshold file if not provided
        if not thresh_file:

            #create a temporary thresh file in the temporary directory
            with open(os.path.join(tempdir, threshFile), 'w', newline='') as out_file:
                    tsv_writer = csv.writer(out_file, delimiter='\t')
                    tsv_writer.writerow([str(zscores), exact_z_thresh])
        
        else:
            threshFile = str(thresh_file)

        #put together command
        cmd = "%s enrich -t %s -s %s -x %s -o %s" % (pepsirf_binary, threshFile, pairsFile, outSuffix, str(dir_fmt_output))

        #add optionals to command
        if raw_scores:
            cmd += " -r %s" % (str(raw_scores))
        if raw_constraint:
            cmd += " --raw_score_constraint %s" % (str(raw_constraint))
        if enrichment_failure:
            enrichment_failure = "failedEnrichment.txt"
            cmd += " -f %s" % (enrichment_failure)
        if truncate:
            cmd += " --output_filename_truncate"

        #run command
        subprocess.run(cmd, shell=True, check=True)

        # check if failure file exists
        failed = (dir_fmt_output.path/"failedEnrichment.txt")

        # if file doesn't exist create empty file
        if not failed.exists():
            with failed.open("w") as fh:
                pass

        #return enrich directory as qza
        return dir_fmt_output