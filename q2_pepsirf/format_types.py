#!/usr/bin/env python
import qiime2.plugin.model as model
from qiime2.plugin import SemanticType

from q2_types.feature_table import FeatureTable


Normed = SemanticType('Normed', variant_of=FeatureTable.field['content'])
NormedDifference = SemanticType('NormedDifference', variant_of=FeatureTable.field['content'])
NormedDiffRatio = SemanticType('NormedDiffRatio', variant_of=FeatureTable.field['content'])
NormedRatio = SemanticType('NormedRatio', variant_of=FeatureTable.field['content'])
NormedSized = SemanticType('NormedSized', variant_of=FeatureTable.field['content'])
Zscore = SemanticType('Zscore', variant_of=FeatureTable.field['content'])
RawCounts = SemanticType('RawCounts', variant_of=FeatureTable.field['content'])

PairwiseEnrichment = SemanticType('PairwiseEnrichment')
ZscoreNan = SemanticType('ZscoreNan')
PeptideBins = SemanticType('PeptideBins')


class PepsirfContingencyTSVFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            for _, line in zip(range(1), fh):
                if not line.startswith('Sequence name\t'):
                    raise model.ValidationError(
                        'TSV does not start with "Sequence name"')


PepsirfContingencyTSVDirFmt = model.SingleFileDirectoryFormat(
    'PepsirfContingencyTSVDirFmt',
    'pepsirf-table.tsv',
    PepsirfContingencyTSVFormat)

class PeptideIDListFmt(model.TextFileFormat):
    def _validate_(self, level='min'):
        pass

class EnrichedPeptideDirFmt(model.DirectoryFormat):
    pairwise = model.FileCollection(
        r'.+~.+_enriched\.txt',
        format=PeptideIDListFmt)

class ZscoreNanFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        pass

ZscoreNanDirFmt = model.SingleFileDirectoryFormat(
    'ZscoreNanDirFmt',
    'nan-zscores.nan',
    ZscoreNanFormat)

class PeptideBinFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        pass

PeptideBinDirFmt = model.SingleFileDirectoryFormat(
    'PeptideBinDirFmt',
    'bins.tsv',
    PeptideBinFormat)