from posixpath import abspath
import subprocess, os, csv
import tempfile, qiime2

from q2_pepsirf.format_types import (
    EnrichedPeptideDirFmt, 
    PepsirfContingencyTSVFormat,)

def _make_pairs_file(column, outpath):
    series = column.to_series()
    pairs = {k: v.index for k,v in series.groupby(series)}
    with open(outpath, 'w') as fh:
        for _, ids in pairs.items():
            fh.write('\t'.join(ids) + '\n')

def enrich(
        zscores: PepsirfContingencyTSVFormat,
        source: qiime2.CategoricalMetadataColumn,
        exact_z_thresh: str,
        raw_scores: PepsirfContingencyTSVFormat = None,
        raw_constraint: int = None,
        enrichment_failure: bool = False,
        truncate: bool = False,
        pepsirf_binary: str = "pepsirf") -> EnrichedPeptideDirFmt:

    dir_fmt_output = EnrichedPeptideDirFmt()
    print(dir_fmt_output)

    # zscores = "%s" % (os.path.abspath(str(zscores)))

    # if raw_scores:
    #     raw_scores = "'%s'" % (os.path.abspath(str(raw_scores)))

    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "'%s'" % (os.path.abspath(pepsirf_binary))

    with tempfile.TemporaryDirectory() as tempdir:

        pairsFile = os.path.join(tempdir, 'pairs.tsv')
        _make_pairs_file(source, pairsFile)

        threshFile = "tempThreshFile.tsv"
        outSuffix = "_enriched.txt"

        with open(threshFile, 'w', newline='') as out_file:
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow([str(zscores), exact_z_thresh])

        cmd = "%s enrich -t %s -s %s -x %s -o %s" % (pepsirf_binary, threshFile, pairsFile, outSuffix, str(dir_fmt_output))

        if raw_scores:
            cmd += " -r %s" % (str(raw_scores))
        if raw_constraint:
            cmd += " --raw_score_constraint %s" % (str(raw_constraint))
        if enrichment_failure:
            enrichment_failure = "failedEnrichment.txt"
            cmd += " -f %s" % (enrichment_failure)
        if truncate:
            cmd += " --output_filename_truncate"

        subprocess.run(cmd, shell=True, check=True)

        with open(threshFile) as fh:
            print(fh.read())

        print(list(os.listdir(dir_fmt_output.path)))

        return dir_fmt_output


#  qiime pepsirf enrich --i-zscores IM0032-pA_PV1_subset_Z-HDI95.qza --m-source-file IM0032-pA_PV1_subset_PN.tsv --m-source-column Source --p-exact-z-thresh 0 --p-pepsirf-binary /mnt/c/Users/ANNAB/Documents/GitHub/q2-enrich/example/pepsirf_1.4.0_linux --o-dir-fmt-output ./enrichOutput2 --verbose