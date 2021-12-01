#!/usr/bin/env python
import qiime2.plugin.model as model
import os
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
InfoSNPN = SemanticType('InfoSNPN')
InfoSumOfProbes = SemanticType('InfoSumOfProbes')
EnrichThresh = SemanticType('EnrichThresh')

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
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        'TXT file is empty, not a '
                        'enriched peptides file.')

class EnrichmentFailureFmt(model.TextFileFormat):
    def _validate_( self, level='min'):
        pass

class EnrichedPeptideDirFmt(model.DirectoryFormat):
    pairwise = model.FileCollection(
        r'.+~.+_enriched\.txt',
        format=PeptideIDListFmt)
    @pairwise.set_path_maker
    def pairwise_pathmaker(self, a, b):
        return f'{a}~{b}_enriched.txt'
    
    failures = model.File(
        'failedEnrichment.txt',
        format=EnrichmentFailureFmt
    )

class ZscoreNanFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            for _, line in zip(range(1), fh):
                if not line.startswith('Probe name\t'):
                    raise model.ValidationError(
                        'nan does not contain "Probe name" as the first header. '
                        'Not a .nan file.')

ZscoreNanDirFmt = model.SingleFileDirectoryFormat(
    'ZscoreNanDirFmt',
    'nan-zscores.nan',
    ZscoreNanFormat)

class PeptideBinFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        'TSV is empty, not a bins file.')

PeptideBinDirFmt = model.SingleFileDirectoryFormat(
    'PeptideBinDirFmt',
    'bins.tsv',
    PeptideBinFormat)

class PepsirfInfoSNPNFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        'TSV is empty.')

PepsirfInfoSNPNDirFmt = model.SingleFileDirectoryFormat(
    'PepsirfInfoSNPNDirFmt',
    'SN.tsv',
    PepsirfInfoSNPNFormat)

class PepsirfInfoSumOfProbesFmt(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            for _, line in zip(range(1), fh):
                if not line.startswith('Sample name\t'):
                    raise model.ValidationError(
                        'TSV does not start with "Sample name"')


PepsirfInfoSumOfProbesDirFmt = model.SingleFileDirectoryFormat(
    'PepsirfInfoSumOfProbesDirFmt',
    'RC.tsv',
    PepsirfInfoSumOfProbesFmt)

class EnrichThreshFileFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        'TSV is empty.')

EnrichThreshFileDirFmt = model.SingleFileDirectoryFormat(
    'EnrichThreshFileDirFmt',
    '_thresh.tsv',
    EnrichThreshFileFormat)