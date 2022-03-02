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
MultiFile = SemanticType('MultiFile')
ProteinFasta = SemanticType('ProteinFasta')
PeptideFasta = SemanticType('PeptideFasta')
Link = SemanticType('Link')
PeptideIDList = SemanticType('PeptideIDList')
PepsirfDMP = SemanticType('PepsirfDMP')
DeconvSingluar = SemanticType('DeconvSingluar')
ScorePerRound = SemanticType('ScorePerRound')
DeconvBatch = SemanticType('DeconvBatch')
PeptideAssignmentMap = SemanticType('PeptideAssignmentMap')
DemuxFif = SemanticType('DemuxFif')
DemuxSampleList = SemanticType('DemuxSampleList')
DemuxIndex = SemanticType('DemuxIndex')
DemuxLibrary = SemanticType('DemuxLibrary')
DemuxFastq = SemanticType('DemuxFastq')
DemuxDiagnostic = SemanticType('DemuxDiagnostic')
ProteinAlignment = SemanticType('ProteinAlignment')

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
        r'.+_+.+\.txt',
        format=PeptideIDListFmt)
    @pairwise.set_path_maker
    def pairwise_pathmaker(self, comparisons, suffix):
        return f'{"~".join(comparisons)}_{suffix}.txt'
    
    failures = model.File(
        'failedEnrichment.txt',
        format=EnrichmentFailureFmt
    )

PeptideIDListDirFmt = model.SingleFileDirectoryFormat(
    'PeptideIDListDirFmt',
    'samp_A~samp_B.txt',
    PeptideIDListFmt)

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

class SubjoinMultiFileFmt(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        '.txt file is empty.')

SubjoinMultiFileDirFmt = model.SingleFileDirectoryFormat(
    'SubjoinMultiFileDirFmt',
    'multifile.txt',
    SubjoinMultiFileFmt)

class ProteinFastaFmt(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        '.fasta file is empty.')

ProteinFastaDirFmt = model.SingleFileDirectoryFormat(
    'ProteinFastaDirFmt',
    'protein_file.fasta',
    ProteinFastaFmt)

class PeptideFastaFmt(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        '.faa file is empty.')

PeptideFastaDirFmt = model.SingleFileDirectoryFormat(
    'PeptideFastaDirFmt',
    'peptide_file.faa',
    PeptideFastaFmt)

class PepsirfLinkTSVFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            for _, line in zip(range(1), fh):
                if not line.startswith('Peptide Name\t'):
                    raise model.ValidationError(
                        'TSV does not start with "Peptide Name"')


PepsirfLinkTSVDirFmt = model.SingleFileDirectoryFormat(
    'PepsirfLinkTSVDirFmt',
    'link_output.tsv',
    PepsirfLinkTSVFormat)

class PepsirfDMPFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        'TSV is empty, not a .dmp file.')

PepsirfDMPDirFmt = model.SingleFileDirectoryFormat(
    'PepsirfDMPDirFmt',
    'file.dmp',
    PepsirfDMPFormat)

class PepsirfDeconvSingularFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            for _, line in zip(range(1), fh):
                if not line.startswith('Species Name\t'):
                    raise model.ValidationError(
                        'TSV does not start with "Species Name"')

PepsirfDeconvSingularDirFmt = model.SingleFileDirectoryFormat(
    'PepsirfDeconvSingularDirFmt',
    'singular_mode.tsv',
    PepsirfDeconvSingularFormat)

class PepsirfDeconvBatchDirFmt(model.DirectoryFormat):
    batch = model.FileCollection(
        r'.+_+.+\.txt',
        format=PepsirfDeconvSingularFormat)
    @batch.set_path_maker
    def batch_pathmaker(self, comparisons, suffix):
        return f'{"~".join(comparisons)}_{suffix}.txt'

class ScorePerRoundFmt(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            for _, line in zip(range(1), fh):
                if not line.startswith('Species ID\t'):
                    raise model.ValidationError(
                        'round file does not start with "Species ID"')

class ScorePerRoundDirFmt(model.DirectoryFormat):
    score = model.FileCollection(
        r'round_.+',
        format=ScorePerRoundFmt)
    @score.set_path_maker
    def score_pathmaker(self, round):
        return f'round_{round}'

class PeptideAssignMapFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            for _, line in zip(range(1), fh):
                if not line.startswith('Peptide\t'):
                    raise model.ValidationError(
                        '.map does not start with "Peptide"')

class PeptideAssignMapDirFmt(model.DirectoryFormat):
    batch = model.FileCollection(
        r'.+_.+\.map',
        format=PeptideAssignMapFormat)
    @batch.set_path_maker
    def batch_pathmaker(self, comparisons, suffix):
        return f'{"~".join(comparisons)}_{suffix}.map'

class PepsirfDemuxFifFmt(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        'TSV is empty, not a demux fif file.')

PepsirfDemuxFifDirFmt = model.SingleFileDirectoryFormat(
    'PepsirfDemuxFifDirFmt',
    'demux_fif.tsv',
    PepsirfDemuxFifFmt)

class PepsirfDemuxSampleListFmt(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        'TSV is empty, not a demux sample list file.')

PepsirfDemuxSampleListDirFmt = model.SingleFileDirectoryFormat(
    'PepsirfDemuxSampleListDirFmt',
    'demux_index.tsv',
    PepsirfDemuxSampleListFmt)

class PepsirfDemuxIndexFmt(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        '.fa is empty, not a demux index file.')

PepsirfDemuxIndexDirFmt = model.SingleFileDirectoryFormat(
    'PepsirfDemuxIndexDirFmt',
    'demux_index.fa',
    PepsirfDemuxIndexFmt)

class PepsirfDemuxLibraryFmt(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        '.fna is empty, not a demux library file.')

PepsirfDemuxLibraryDirFmt = model.SingleFileDirectoryFormat(
    'PepsirfDemuxLibraryDirFmt',
    'demux_library.fna',
    PepsirfDemuxLibraryFmt)

class PepsirfDemuxFastqFmt(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            line = list(zip(range(1), fh))
            if line == [] :
                raise model.ValidationError(
                        '.fna is empty, not a demux library file.')

PepsirfDemuxFastqDirFmt = model.SingleFileDirectoryFormat(
    'PepsirfDemuxFastqDirFmt',
    'demux.fastq',
    PepsirfDemuxFastqFmt)

class PepsirfDemuxDiagnosticFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            for _, line in zip(range(1), fh):
                if not line.startswith('Sample name\t'):
                    raise model.ValidationError(
                        'TSV does not start with "Sample name"')


PepsirfDemuxDiagnosticDirFmt = model.SingleFileDirectoryFormat(
    'PepsirfDemuxDiagnosticDirFmt',
    'diagnostic_output.tsv',
    PepsirfDemuxDiagnosticFormat)

class ProteinAlignmentFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        with self.open() as fh:
            for _, line in zip(range(1), fh):
                if not line.startswith('ProtName\t'):
                    raise model.ValidationError(
                        'TSV does not start with "ProtName"')


PrtoeinAlignmentDirFmt = model.SingleFileDirectoryFormat(
    'PrtoeinAlignmentDirFmt',
    'protein_alignment.tsv',
    ProteinAlignmentFormat)