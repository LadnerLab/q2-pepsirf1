import subprocess
import qiime2

def _make_pairs_file(column, outpath):
    series = column.to_series()
    pairs = {k: v.index for k,v in series.groupby(series)}
    with open(outpath, 'w') as fh:
        for _, ids in pairs.items():
            fh.write('\t'.join(ids) + '\n')

def enrich(threshold_file: str,
        outfile_suffix: str,
        output: str,
        source: qiime2.CategoricalMetadataColumn,
        join_on: str = None,
        enrichment_failure: str = None,
        output_truncate: bool = False,
        pepsirf_binary: str = "pepsirf") -> None:
    
    #create pairs file
    if source:
        pairsFile = 'pairs.tsv'
        _make_pairs_file(source, pairsFile)

    cmd = 'enrich -t %s -x %s -o %s -s %s' % (threshold_file, outfile_suffix, output, pairsFile)

    if join_on:
        cmd += ' -j %s' % (join_on)
    if enrichment_failure:
        cmd += ' -f %s' % (enrichment_failure)
    if output_truncate:
        cmd += ' --output_filename_truncate'

    subprocess.run(cmd, shell=True)