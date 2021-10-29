#!/usr/bin/env python
import importlib
import q2_pepsirf
from q2_pepsirf.actions.norm import norm

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
                        Float)

from q2_pepsirf.format_types import (
    EnrichedPeptideDirFmt, Normed, NormedDifference, 
    NormedDiffRatio, NormedRatio, NormedSized, 
    PairwiseEnrichment, PeptideIDListFmt, Zscore, RawCounts,
    PepsirfContingencyTSVDirFmt, PepsirfContingencyTSVFormat, 
    ZscoreNan, ZscoreNanDirFmt, ZscoreNanFormat, PeptideBinFormat,
    PeptideBinDirFmt, PeptideBins
    )
import q2_pepsirf.actions as actions
import q2_pepsirf.actions.zscore as zscore

from q2_types.feature_table import FeatureTable, BIOMV210DirFmt


plugin = Plugin("pepsirf", version='0.0.1.dev',
                website="https://github.com/LadnerLab/q2-pepsirf")

plugin.register_formats(PepsirfContingencyTSVFormat,
                        PepsirfContingencyTSVDirFmt,
                        PeptideIDListFmt,
                        EnrichedPeptideDirFmt,
                        ZscoreNanFormat,
                        ZscoreNanDirFmt, 
                        PeptideBinFormat, 
                        PeptideBinDirFmt)

plugin.register_semantic_types(
        Normed, NormedDifference, NormedDiffRatio,
        NormedRatio, NormedSized, Zscore, RawCounts,
        PairwiseEnrichment)
plugin.register_semantic_type_to_format(
        FeatureTable[
                Normed | NormedDifference |
                NormedDiffRatio | NormedRatio 
                | NormedSized | Zscore | RawCounts],
        BIOMV210DirFmt)
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

T_approach, T_out = TypeMap ({
        Str%Choices("col_sum"): Normed,
        Str%Choices("diff"): NormedDifference,
        Str%Choices("diff_ratio"): NormedDiffRatio,
        Str%Choices("ratio"): NormedRatio,
        Str%Choices("size_factors"): NormedSized
})

plugin.methods.register_function(
        function=actions.norm.norm,
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
        description="c=Calculate Z scores for each peptide in each sample with pepsirf's zscore module"
)

importlib.import_module("q2_pepsirf.transformers")
