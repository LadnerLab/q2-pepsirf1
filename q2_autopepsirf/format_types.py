import os

import qiime2.plugin.model as model
from qiime2.plugin import SemanticType
from q2_types.feature_table import FeatureTable

rawCounts = SemanticType('rawCounts', variant_of=FeatureTable.field['content'])
