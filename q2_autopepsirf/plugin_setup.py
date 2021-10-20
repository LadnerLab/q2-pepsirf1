#!/usr/bin/env python
import importlib
import q2_autopepsirf

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
                        Metadata)

from q2_autopepsirf.format_types import (
    Normed, NormedDifference, NormedDiffRatio, Zscore, RawCounts,
    PepsirfContingencyTSVDirFmt, PepsirfContingencyTSVFormat
    )
import q2_autopepsirf.actions as actions

from q2_types.feature_table import FeatureTable, BIOMV210DirFmt


# This is the plugin object. It is what the framework will load and what an
# interface will interact with. Basically every registration we perform will
# involve this object in some way.
plugin = Plugin("autopepsirf", version=q2_autopepsirf.__version__,
                website="https://github.com/LadnerLab/q2-autopepsirf")

plugin.register_formats(PepsirfContingencyTSVFormat,
                        PepsirfContingencyTSVDirFmt)

plugin.register_semantic_types(Normed, NormedDifference, NormedDiffRatio, Zscore, RawCounts)
plugin.register_semantic_type_to_format(
        FeatureTable[Normed | NormedDifference | NormedDiffRatio | Zscore | RawCounts],
        BIOMV210DirFmt)