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
                        Choices)

from q2_pepsirf.format_types import (
    EnrichedPeptideDirFmt, Normed, NormedDifference, 
    NormedDiffRatio, NormedRatio, NormedSized, 
    PairwiseEnrichment, PeptideIDListFmt, Zscore, RawCounts,
    PepsirfContingencyTSVDirFmt, PepsirfContingencyTSVFormat
    )
import q2_pepsirf.actions as actions

from q2_types.feature_table import FeatureTable, BIOMV210DirFmt


# This is the plugin object. It is what the framework will load and what an
# interface will interact with. Basically every registration we perform will
# involve this object in some way.
plugin = Plugin("pepsirf", version='0.0.1.dev',
                website="https://github.com/LadnerLab/q2-pepsirf")

plugin.register_formats(PepsirfContingencyTSVFormat,
                        PepsirfContingencyTSVDirFmt,
                        PeptideIDListFmt,
                        EnrichedPeptideDirFmt)

plugin.register_semantic_types(Normed, NormedDifference, NormedDiffRatio, NormedRatio, NormedSized, Zscore, RawCounts, PairwiseEnrichment)
plugin.register_semantic_type_to_format(
        FeatureTable[Normed | NormedDifference | NormedDiffRatio | NormedRatio | NormedSized | Zscore | RawCounts],
        BIOMV210DirFmt)
plugin.register_semantic_type_to_format(
        PairwiseEnrichment,
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
        function=actions.norm.norm,
        inputs={
                'peptide_scores': FeatureTable[RawCounts | Normed],
                'negative_control': FeatureTable[RawCounts | Normed]
        },
        parameters={
                'normalize_approach': T_approach,
                'negative_id': Str,
                'negative_names': List[Str],
                'precision': Int,
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

importlib.import_module("q2_pepsirf.transformers")
