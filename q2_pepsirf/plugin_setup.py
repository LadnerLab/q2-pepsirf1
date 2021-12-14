#!/usr/bin/env python
import importlib
import q2_pepsirf

from qiime2.plugin import (Plugin,
                        SemanticType,
                        model,
                        Int,
                        Range,
                        MetadataColumn,
                        Categorical,
                        Str,
                        List,
                        Visualization,
                        Metadata,
                        TypeMap,
                        Choices,
                        Float,
                        Bool)

from q2_pepsirf.format_types import (
    EnrichedPeptideDirFmt, Normed, NormedDifference, 
    NormedDiffRatio, NormedRatio, NormedSized, 
    PairwiseEnrichment, PeptideIDListFmt, Zscore, RawCounts,
    PepsirfContingencyTSVDirFmt, PepsirfContingencyTSVFormat, 
    ZscoreNan, ZscoreNanDirFmt, ZscoreNanFormat, PeptideBinFormat,
    PeptideBinDirFmt, PeptideBins, PepsirfInfoSumOfProbesDirFmt,
    PepsirfInfoSumOfProbesFmt, InfoSumOfProbes, PepsirfInfoSNPNFormat,
    PepsirfInfoSNPNDirFmt, InfoSNPN, EnrichThresh, EnrichThreshFileDirFmt,
    EnrichThreshFileFormat
    )
import q2_pepsirf.actions as actions
import q2_pepsirf.actions.zscore as zscore
import q2_pepsirf.actions.enrich as enrich
import q2_pepsirf.actions.info as info
import q2_pepsirf.actions.norm as norm
import q2_pepsirf.actions.bin as bin

from q2_types.feature_table import FeatureTable, BIOMV210DirFmt


plugin = Plugin("pepsirf", version=q2_pepsirf.__version__,
                website="https://github.com/LadnerLab/q2-pepsirf1",
                description="Qiime2 Plug-in for the use of pepsirf within qiime.")

plugin.register_formats(PepsirfContingencyTSVFormat,
                        PepsirfContingencyTSVDirFmt,
                        PeptideIDListFmt,
                        EnrichedPeptideDirFmt,
                        ZscoreNanFormat,
                        ZscoreNanDirFmt, 
                        PeptideBinFormat, 
                        PeptideBinDirFmt,
                        PepsirfInfoSNPNDirFmt,
                        PepsirfInfoSNPNFormat,
                        PepsirfInfoSumOfProbesDirFmt,
                        PepsirfInfoSumOfProbesFmt,
                        EnrichThreshFileFormat,
                        EnrichThreshFileDirFmt)

plugin.register_semantic_types(
        Normed, NormedDifference, NormedDiffRatio,
        NormedRatio, NormedSized, Zscore, RawCounts,
        PairwiseEnrichment)
plugin.register_semantic_type_to_format(
        FeatureTable[
                Normed | NormedDifference |
                NormedDiffRatio | NormedRatio 
                | NormedSized | Zscore | RawCounts],
        PepsirfContingencyTSVDirFmt)
plugin.register_semantic_type_to_format(
        PairwiseEnrichment,
        EnrichedPeptideDirFmt
)
plugin.register_semantic_type_to_format(
        ZscoreNan,
        ZscoreNanDirFmt
)
plugin.register_semantic_type_to_format(
        PeptideBins,
        PeptideBinDirFmt
)
plugin.register_semantic_type_to_format(
        InfoSNPN,
        PepsirfInfoSNPNDirFmt
)
plugin.register_semantic_type_to_format(
        InfoSumOfProbes,
        PepsirfInfoSumOfProbesDirFmt
)
plugin.register_semantic_type_to_format(
        EnrichThresh,
        EnrichedPeptideDirFmt
)

T_approach, T_out = TypeMap ({
        Str%Choices("col_sum"): Normed,
        Str%Choices("diff"): NormedDifference,
        Str%Choices("diff_ratio"): NormedDiffRatio,
        Str%Choices("ratio"): NormedRatio,
        Str%Choices("size_factors"): NormedSized
})



plugin.methods.register_function(
        function=norm.norm,
        inputs={
                'peptide_scores': FeatureTable[RawCounts | Normed],
                'negative_control': FeatureTable[RawCounts | Normed]
        },
        parameters={
                'normalize_approach': T_approach,
                'negative_id': Str,
                'negative_names': List[Str],
                'precision': Int % Range(0, None),
                'pepsirf_binary': Str,
        },
        outputs=[
                ('qza_output', FeatureTable[T_out])
        ],
        input_descriptions={
                'peptide_scores': "Name of FeatureTable matrix file containing peptide scores. This file should be in the same format "
                                "as the output from the demux module.",
                'negative_control': "Name of FeatureTable matrix file containing data for sb samples."
        },
        parameter_descriptions={
                'normalize_approach': "'col_sum': Normalize the scores using a column-sum method. Output per peptide is the score per "
                                "million for the sample (i.e., summed across all peptides). "
                                "'size_factors': Normalize the scores using the size factors method (Anders and Huber 2010). "
                                "'diff': Normalize the scores using the difference method. For each peptide and sample, the difference "
                                "between the score and the respective peptide's mean score in the negative controls is determined. "
                                "'ratio': Normalize the scores using the ratio method. For each peptide and sample, the ratio of score "
                                "to the respective peptide's mean score in the negative controls is determined. "
                                "'diff_ratio': Normalize the scores using the difference-ratio method. For each peptide and sample, "
                                "the difference between the score and the respective peptide's mean score in the negative controls is "
                                "first determined. This difference is then divided by the respective peptide's mean score in the "
                                "negative controls.",
                'negative_id': "Optional approach for identifying negative controls. Provide a unique string at the start of all "
                                "negative control samples.",
                'negative_names': "Optional approach for identifying negative controls. "
                                "Space-separated list of negative control sample names.",
                'precision': "Output score precision. The scores written to the output will be output to this many decimal places.",
                'pepsirf_binary': "The binary to call pepsirf on your system."
        },
        output_descriptions={
                'qza_output': "the FeatureTable (.qza) output based on the normalized approach given by user"
        },
        name='pepsirf norm module',
        description="Normalize raw count data with pepsirf's norm module"
)

plugin.methods.register_function(
        function=zscore.zscore,
        inputs={
                'scores': FeatureTable[Normed | RawCounts | NormedDifference | NormedDiffRatio],
                'bins': PeptideBins
        },
        parameters={
                'trim': Float % Range(0.0, 100.0),
                'hdi': Float % Range(0.0, None),
                'num_threads': Int % Range(1, None),
                'pepsirf_binary': Str
        },
        outputs=[
                ('zscore_output', FeatureTable[Zscore]),
                ('nan_report', ZscoreNan)
        ],
        input_descriptions={
                'scores': "Name of the file to use as input. Should be a score matrix in the "
                        "format as output by the demux and subjoin modules. Raw or normalized read counts can be used.",
                'bins': "Name of the file containing bins, one bin per line, as output by the bin module. Each bin contains a "
                        "tab-delimited list of peptide names."
        },
        parameter_descriptions={
                'trim': "Percentile of lowest and highest counts within a bin to ignore when calculating "
                        "the mean and standard deviation.",
                'hdi': "Alternative approach for discarding outliers prior to calculating mean and stdev. If provided, this "
                        "argument will override --trim, which trims evenly from both sides of the distribution. For --hdi, the "
                        "user should provide the high density interval to be used for calculation of mean and stdev. For "
                        "example, '--hdi 0.95' would instruct the program to utilize the 95% highest density interval (from each "
                        "bin) for these calculations.",
                'num_threads': "The number of threads to use for analyses.",
                'pepsirf_binary': "The binary to call pepsirf on your system."
        },
        output_descriptions={
                'zscore_output': "Name for the output Z scores file. This file will be a FeatureTable[Zscore] with the same "
                               "dimensions as the input score file. Each peptide will be written with its z-score within each sample.",
                'nan_report': "Name of the file to write out information regarding peptides that are given a zscore of 'nan'. This "
                        "occurs when the mean score of a bin and the score of the focal peptide are both zero. This will be a "
                        "ZscoreNan file, with three columns per line. The first column will contain the name of the peptide, "
                        "the second will be the name of the sample, and the third will be the bin number of the probe. This bin "
                        "number corresponds to the line number in the bins file, within which the probe was found."
        },
        name='pepsirf zscore module',
        description="Calculate Z scores for each peptide in each sample with pepsirf's zscore module"
)

plugin.methods.register_function(
        function=enrich.enrich,
        inputs={
                'zscores': FeatureTable[Zscore],
                'raw_scores': FeatureTable[RawCounts],
                'thresh_file': EnrichThresh

        },
        parameters={
                'exact_z_thresh': Str,
                'raw_constraint': Int % Range(0, None),
                'enrichment_failure': Bool,
                'truncate': Bool,
                'pepsirf_binary': Str,
                'source': MetadataColumn[Categorical]
        },
        outputs=[
                ('dir_fmt_output', PairwiseEnrichment)
        ],
        input_descriptions={
                'zscores': "FeatureTable containing z scores of the normalized read counts. "
                        "Fist column header must be 'Sequence Name' as produced by pepsirf.",
                'raw_scores': "This matrix must contain the raw counts for each Peptide for every sample of "
                        "interest. If included, '--raw_score_constraint' must also be specified.",
                'thresh_file': " The name of a tab-delimited file containing one tab-delimited matrix filename "
                        "and threshold(s), one per line. If providing more than z score matrix."
        },
        parameter_descriptions={
                'exact_z_thresh': "Exact z score thresholds either individual or combined.",
                'raw_constraint': "The minimum total raw count across all peptides for a sample to be "
                                "included in the analysis.This provides a way to impose a minimum read "
                                "count for a sample to be evaluated.",
                'enrichment_failure': "For each sample set that does not result in the generation of an enriched peptide file, a row of two "
                                "tab-delimited columns is provided: the first column contains the replicate names (comma-delimited) and "
                                "the second column provides the reason why the sample did not result in an enriched peptide file. "
                                "This file is output to the same directory as the enriched peptide files. The 'Reason' column will contain "
                                "one of the following: 'Raw read count threshold' or 'No enriched peptides'.",
                'truncate': "By default each filename in the output directory will include every replicate name joined by the "
                        "'join_on' value. Alternatively, if more than two replicates are being evaluated, then you may include "
                        "this flag to stop the filenames from including more than 3 samplenames in the output. When this flag is "
                        "used, the output names will be of the form 'A~B~C~1more', for example.",
                'pepsirf_binary': "The binary to call pepsirf on your system.",
                'source': "Metadata file containing all sample names and their source groups. "
                        "Used to create pairs tsv to run pepsirf enrich module."
        },
        output_descriptions={
                'dir_fmt_output': "Directory formatted qza containing lists of enriched peptides"
        },
        name='pepsirf enrich module',
        description="Determines which peptides are enriched in samples with pepsirf's enrich module"
)

plugin.methods.register_function(
        function=info.infoSNPN,
        inputs={
                'input': FeatureTable[
                        Normed | NormedDifference | NormedDiffRatio
                        | RawCounts | NormedDiffRatio | NormedSized],
        },
        parameters={
                'get': Str%Choices("samples", "probes"),
                'pepsirf_binary': Str
        },
        outputs=[
                ('snpn_output', InfoSNPN)
        ],
        input_descriptions={
                'input': "An input score matrix to gather information from."
        },
        parameter_descriptions={
                'get': "Specify weather you want to collect sample names or probe/peptide names",
                'pepsirf_binary': "The binary to call pepsirf on your system."
        },
        output_descriptions={
                'snpn_output':"InfoSNPN file in the form of a file with no header, one sample name per line."
        },
        name='pepsirf info (samples/peptide names) module',
        description="Gathers the number of samples and peptides in the matrix using pepsirf's info modules"
)

plugin.methods.register_function(
        function=info.infoSumOfProbes,
        inputs={
                'input': FeatureTable[
                        Normed | NormedDifference | NormedDiffRatio
                        | RawCounts | NormedDiffRatio | NormedSized],
        },
        parameters={
                'pepsirf_binary': Str
        },
        outputs=[
                ('sum_of_probes_output', InfoSumOfProbes)
        ],
        input_descriptions={
                'input': "An input score matrix to gather information from."
        },
        parameter_descriptions={
                'pepsirf_binary': "The binary to call pepsirf on your system."
        },
        output_descriptions={
                'sum_of_probes_output':"InfoSumOfProbes file, The first entry in each column will be the name of the "
                                "sample, and the second will be the sum of the peptide/probe scores for the sample."
        },
        name='pepsirf info (sum of probes) module',
        description="Gathers the sum of probes per sample in the matrix using pepsirf's info module"
)

T_norm, T_flag, T_out = TypeMap ({
        (Normed, Bool%Choices(False)): PeptideBins,
        (NormedDifference | NormedDiffRatio | NormedRatio | NormedSized, Bool%Choices(True)): PeptideBins
})

plugin.methods.register_function(
        function=bin.bin,
        inputs={
                'scores': FeatureTable[T_norm],
        },
        parameters={
                'pepsirf_binary': Str,
                'bin_size': Int % Range(1, None),
                'round_to': Int % Range(0, None),
                'allow_other_normalization': T_flag
        },
        outputs=[
                ('bin_output', T_out)
        ],
        input_descriptions={
                'scores': "Input tab-delimited normalized score matrix file to use for peptide binning. "
                        "This matrix should only contain info for the negative control samples that "
                        "should be used to generate bins (see subjoin module for help generatinig input "
                        "matrix). Peptides with similar scores, summed across the negative controls, "
                        "will be binned together."
        },
        parameter_descriptions={
                'pepsirf_binary': "The binary to call pepsirf on your system.",
                'bin_size': "The minimum number of peptides that a bin must contain. If a bin would be "
                        "created with fewer than bin_size peptides, it will be combined with the next "
                        "bin until at least bin_size peptides are found.",
                'round_to': "The 'rounding factor' for the scores parsed from the score matrix prior to "
                        "binning. Scores found in the matrix will be rounded to the nearest 1/10^x for a "
                        "rounding factor x. For example, a rounding factor of 0 will result in rounding "
                        "to the nearest integer, while a rounding factor of 1 will result in rounding to "
                        "the nearest tenth."
        },
        output_descriptions={
                'bin_output':"PeptideBins file that contains  one bin per line and each "
                        "bin will be a tab-delimited list of the names of the peptides in the bin."
        },
        name='pepsirf bin module',
        description="Creates groups of peptides with similar starting abundances with pepsirf's bin module"
)
importlib.import_module("q2_pepsirf.transformers")
