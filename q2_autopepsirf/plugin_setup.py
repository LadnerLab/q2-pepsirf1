import importlib

from qiime2.plugin import Plugin, model, Str, MetadataColumn, Categorical, Bool

import q2_autopepsirf.actions as actions

plugin = Plugin("autopepsirf", version="0.0.1.dev",
                website="https://github.com/LadnerLab/q2-autopepsirf")

plugin.methods.register_function(
    function=actions.enrich,
    inputs={},
    parameters={
        "threshold_file": Str,
        "outfile_suffix": Str,
        "join_on": Str,
        "output": Str,
        "source": MetadataColumn[Categorical],
        "enrichment_failure": Bool,
        "output_truncate": Bool
    },
    outputs=[],
    input_descriptions={},
    parameter_descriptions={
        "threshold_file": "The name of a tab-delimited file containing one tab-delimited matrix "
                        "filename and threshold(s), one per line. If using more than one threshold "
                        "for a given matrix, then separate by comma. A matrix file may contain any "
                        "score of interest, as long as it includes scores for each peptide in "
                        "every sample of interest, with peptides on the rows and sample names on the "
                        "columns. The provided thresholds should be comma-separated if more than one is "
                        "provided for a single matrix file.",
        "outfile_suffix": "Suffix to add to all output files. Together, the sample name(s) and the "
                        "suffix will form the name of the output file for each sample. For example, with "
                        "a suffix of '_enriched.txt' and a sample name of ‘sample1’, the name "
                        "of the output file for this sample would be ‘sample1_enriched.txt’. By "
                        "default, no suffix is used.",
        "join_on": "A character or string to use to join replicate sample names in order to "
                "create output file names. For a pair of samples, 'A' and 'B', the resulting "
                "file will have the name 'A~B' if this flag is not given. Otherwise, the given "
                "value will be used in place of '~'.",
        "output": "Directory name to which output files will be written. An output file will be "
                "generated for each sample with at least one enriched peptide. This directory "
                "will be created by the module.",
        "source": "Metadata file containing all sample names and their source groups. "
                "Used to create pairs tsv to run pepsirf enrich module.",
        "enrichment_failure": "For each sample set that does not result in the generation of an enriched "
                            "peptide file, a row of two tab-delimited columns is provided: the "
                            "first column contains the replicate names (comma-delimited) and the second "
                            "column provides the reason why the sample did not result in an enriched "
                            "peptide file. This file is output to the same directory as the enriched peptide "
                            "files. The 'Reason' column will contain one of the following: 'Raw read count "
                            "threshold' or 'No enriched peptides'.",
        "output_truncate": "By default each filename in the output directory will include every replicate"
                        "name joined by the 'join_on' value. Alternatively, if more than two "
                        "replicates are being evaluated, then you may include this flag to stop the "
                        "filenames from including more than 3 samplenames in the output. When this "
                        "flag is used, the output names will be of the form 'A~B~C~1more', for example."
    },
    output_description={},
    name='Call Pepsirf Enrich Module',
    description=(
                "The enrich module determines which peptides are enriched in samples that have been assayed "
                "in n-replicate, as determined by user-specified thresholds. Thresholds can be provided either as "
                "single integers or comma-delimted integer pairs. In order for a peptide to be considered enriched, "
                "all replicates must meet or exceed the lower threshold and at least one replicate must meet "
                "or exceed the higher threshold, independent of order. Note that a peptide must meet each "
                "specified threshold (e.g., zscore, norm count, etc.) in order to be considered enriched. "
                "If any replicates fail the --raw_score_constraint, that sample will be omitted from the analysis."
                )
)

importlib.import_module("q2_reveal.transformers")