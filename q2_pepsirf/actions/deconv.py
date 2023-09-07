from distutils.dir_util import copy_tree
from q2_pepsirf.format_types import(
    PeptideIDListFmt, PepsirfLinkTSVFormat, PepsirfDMPFormat,
    EnrichedPeptideDirFmt, PepsirfDeconvSingularFormat, ScorePerRoundDirFmt,
    PepsirfDeconvBatchDirFmt, PeptideAssignMapDirFmt
)

import os
import subprocess
import tempfile
import qiime2

# Name: collect_cmd
# Process: collects default and required commands for PepSIRF's deconv module
# Method inputs/parameters: pepsirf_binary,enriched, threshold, linked,
# scoring_strategy, score_tie_threhold, score_overlap_threshold,
# tsv_out, score_filtering, id_name_map, single_threaded, score_per_round
# Method outputs/Returned: the full command
# Dependencies: None
def collect_cmd(
        pepsirf_binary, enriched, threshold,
        linked, scoring_strategy, score_tie_threhold,
        score_overlap_threshold, tsv_out, score_filtering,
        id_name_map, single_threaded, score_per_round):

    #start command with required/defualt parameters
    cmd = (
        "%s deconv -e %s --enriched_file_ending paired.txt -t %s -l"
        " %s --scoring_strategy %s --score_tie_threshold %s"
        " --score_overlap_threshold %s -o %s -s %s"
        % (
            pepsirf_binary, enriched, threshold,
            linked, scoring_strategy, score_tie_threhold,
            score_overlap_threshold, tsv_out, score_per_round
        )
    )

    #check if optional parameters are inputted and add to command
    if score_filtering:
        cmd += " --score_filtering"
    if id_name_map:
        id_name_map = "%s" % str(id_name_map)
        cmd += " --id_name_map %s " % id_name_map
    if single_threaded:
        cmd += " --single_threaded"

    return cmd
    
# Name: deconv_singular
# Process: runs PepSIRF's deconv module in singular mode
# Method inputs/parameters: enriched, threshold, linked,
# scoring_stratgey, score_filtering, score_tie_threshold,
# score_ocerlap_threshold, id_name_map, single_threaded,
# outfile, pepsirf_binary
# Method outputs/Returned: deconv tsv output and score-per-round
# output
# Dependencies: Subprocess, os, copy_tree, tempfile
def deconv_singular(
        enriched: PeptideIDListFmt,
        threshold: int,
        linked: PepsirfLinkTSVFormat,
        scoring_strategy: str = "summation",
        score_filtering: bool = False,
        score_tie_threshold: float = 0.0,
        score_overlap_threshold: float = 0.0,
        id_name_map: PepsirfDMPFormat = None,
        single_threaded: bool = False,
        outfile: str = "./deconv.out",
        pepsirf_binary: str = "pepsirf"
    ) -> (PepsirfDeconvSingularFormat, ScorePerRoundDirFmt):
    
    #collect temp file names
    tsv_out = PepsirfDeconvSingularFormat()
    score_per_round = ScorePerRoundDirFmt()

    #collect absolute filepaths for input files and binary if it is a file
    enriched = "%s" % str(enriched)

    linked = "%s" % str(linked)

    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "%s" % os.path.abspath(pepsirf_binary)

    #create a temp directory to run pepsirf in
    with tempfile.TemporaryDirectory() as tempdir:

        #start command with required/defualt parameters
        cmd = collect_cmd(
            pepsirf_binary, enriched, threshold,
            linked, scoring_strategy, score_tie_threshold,
            score_overlap_threshold, tsv_out, score_filtering,
            id_name_map, single_threaded, os.path.join(tempdir, "out_score")
        )

        #add outfile to command
        cmd += " >> %s" % outfile

        #run command in the command line
        subprocess.run(cmd, shell=True, check=True)

        #copy 
        copy_tree(os.path.join(tempdir, "out_score"), str(score_per_round))

    return tsv_out, score_per_round

# Name: deconv_batch
# Process: runs PepSIRF's deconv module in batch mode
# Method inputs/parameters: enriched, threshold, linked,
# outfile_suffix, mapfile_suffix, remove_file_types
# scoring_stratgey, score_filtering, score_tie_threshold,
# score_overlap_threshold, id_name_map, single_threaded,
# outfile, pepsirf_binary
# Method outputs/Returned: deconv dir output, score-per-round
# output, and mapfile dir output
# Dependencies: Subprocess, os, copy_tree, tempfile
def deconv_batch(
        enriched_dir: EnrichedPeptideDirFmt,
        threshold: int,
        linked: PepsirfLinkTSVFormat,
        outfile_suffix: str,
        mapfile_suffix: str,
        scoring_strategy: str = "summation",
        score_filtering: bool = False,
        score_tie_threshold: float = 0.0,
        score_overlap_threshold: float = 0.0,
        id_name_map: PepsirfDMPFormat = None,
        single_threaded: bool = False,
        remove_file_types: bool = False,
        outfile: str = "./deconv.out",
        pepsirf_binary: str = "pepsirf"
    ) -> (
        PepsirfDeconvBatchDirFmt, ScorePerRoundDirFmt,
        PeptideAssignMapDirFmt
    ):
    
    dir_out = PepsirfDeconvBatchDirFmt()
    score_per_round = ScorePerRoundDirFmt()
    map_dir = PeptideAssignMapDirFmt()

    #collect absolute filepaths for input files and binary if it is a file
    enriched = "%s" % str(enriched_dir)
    linked = "%s" % str(linked)

    if os.path.isfile(pepsirf_binary):
        pepsirf_binary = "%s" % os.path.abspath(pepsirf_binary)

    #create a temp directory to run pepsirf in
    with tempfile.TemporaryDirectory() as tempdir:
        temp_enriched = os.path.join(tempdir, "enriched")
        os.mkdir(temp_enriched)

        for name, fmt in enriched_dir.pairwise.iter_views(PeptideIDListFmt):
            qiime2.util.duplicate(str(fmt), os.path.join(temp_enriched, name))

        #start command with required/defualt parameters
        cmd = collect_cmd(
            pepsirf_binary, temp_enriched, threshold,
            linked, scoring_strategy, score_tie_threshold,
            score_overlap_threshold, dir_out, score_filtering,
            id_name_map, single_threaded, os.path.join(tempdir, "out_score")
        )

        cmd += (
            " --outfile_suffix %s --mapfile_suffix %s -p %s"
            % (outfile_suffix, mapfile_suffix, map_dir)
        )

        if remove_file_types:
            cmd += " -r"

        #add outfile to command
        cmd += " >> %s" % outfile

        #run command in the command line
        subprocess.run(cmd, shell=True, check=True)

        copy_tree(os.path.join(tempdir, "out_score"), str(score_per_round))

    return dir_out, score_per_round, map_dir

