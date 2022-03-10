# q2-pepsirf
Qiime2 Plug-in for the use of pepsirf within qiime.

https://ladnerlab.github.io/pepsirf-q2-plugin-docs/

## Installation

### Qiime2 Installation:

Visit: https://docs.qiime2.org/2022.2/install/ for intallation documentation on Qiime2

### Pepsirf Installation:

Visit: https://github.com/LadnerLab/PepSIRF for installation documentation on PepSIRF

### q2-pepsirf installation:

#### Directions:

Visit: https://ladnerlab.github.io/pepsirf-q2-plugin-docs/Pepsirf_Plugins/q2-pepsirf1/ for installation documentation on q2-pepsirf.

#### Update q2-pepsirf:

Visit: https://ladnerlab.github.io/pepsirf-q2-plugin-docs/Pepsirf_Plugins/q2-pepsirf1/#updating for updating documentation on q2-pepsirf.

## Tutorial

Visit: https://ladnerlab.github.io/pepsirf-q2-plugin-docs/tutorials/pepsirf-tutorial/ for a tutorial on select modules.

## Qiime Import
#### Raw Data Example:
```
qiime tools import --input-path rawData.tsv \
--input-format PepsirfContingencyTSVFormat \
--type 'FeatureTable[RawCounts]' \
--output-path rawData.qza
```

#### Format-Types:
| Type of Data | --input-format arg | --type arg |
| --- | --- | --- |
| Raw Data | PepsirfContingencyTSVFormat | 'FeatureTable[RawCounts]' |
| Normalized Col-sum | PepsirfContingencyTSVFormat | 'FeatureTable[Normed]' |
| Normalized Difference | PepsirfContingencyTSVFormat | 'FeatureTable[NormedDifference]' |
| Normalized Difference Ratio | PepsirfContingencyTSVFormat | 'FeatureTable[NormedDiffRatio]' |
| Normalized Ratio | PepsirfContingencyTSVFormat | 'FeatureTable[NormedRatio]' |
| Normalized Sized | PepsirfContingencyTSVFormat | 'FeatureTable[NormedSized]' |
| Zscores | PepsirfContingencyTSVFormat | 'FeatureTable[Zscore]' |
| Zscores Nan | ZscoreNanFormat | 'ZscoreNan' |
| Bins | PeptideBinFormat | 'PeptideBins' |
| Enrich Thresholds | EnrichThreshFileFormat | 'EnrichThresh' |
| Num. of Samples | PepsirfInfoSNPNFormat | 'InfoSNPN' |
| Num. of Peptides | PepsirfInfoSNPNFormat | 'InfoSNPN' |
| Sum of Probes | PepsirfInfoSumOfProbesFmt | 'InfoSumOfProbes' | 
| Multi-File | SubjoinMultiFileFmt | 'MultiFile' |
| Protein Fasta | ProteinFastaFmt | 'ProteinFasta' |
| Peptide Fasta | PeptideFastaFmt | 'PeptideFasta' |
| Link Output | PepsirfLinkTSVFormat | 'Link' |
| Enriched Dir | EnrichedPeptideDirFmt | 'PairwiseEnrichment' |
| Enriched Peptide List | PeptideIDListFmt | 'PeptideIDList' |
| .DMP file | PepsirfDMPFormat | 'PepsirfDMP' |
| Deconv Singluar | PepsirfDeconvSingularFormat | 'DeconvSingular' |
| Deconv Batch Dir | PepsirfDeconvBatchDirFmt | 'DeconvBatch' |
| Score Per Round (Deconv) | ScorePerRoundDirFmt | 'ScorePerRound' |
| Peptide Assignment Map (Deconv) | PeptideAssignMapDirFmt | 'PeptideAssignmentMap' |
| fif file (Demux) | PepsirfDemuxFifFmt | 'DemuxFif' |
| Sample List (Demux) | PepsirfDemuxSampleListFmt | 'DemuxSampleList' |
| Index (Demux) | PepsirfDemuxIndexFmt | 'DemuxIndex' |
| Library (Demux) | PepsirfDemuxLibraryFmt | 'DemuxLibrary' |
| FASTQ file (Demux) | PepsirfDemuxFastqFmt | 'DemuxFastq' |
| Diagnostic file (Demux) | PepsirfDemuxDiagnosticFormat | 'DemuxDiagnostic' |
| Protein Alignment (proteinHeatmap) | ProteinAlignmentFormat | 'ProteinAlignment' |


## Qiime Export
#### Raw Data Example:
```
qiime tools export --input-path rawData.qza \
--output-path rawData.tsv \
--output-format PepsirfContingencyTSVFormat
```

#### Format-Types:
| Type of Data | --output-format arg |
| --- | --- |
| Raw Data | PepsirfContingencyTSVFormat |
| Normalized Col-sum | PepsirfContingencyTSVFormat |
| Normalized Difference | PepsirfContingencyTSVFormat |
| Normalized Difference Ratio | PepsirfContingencyTSVFormat |
| Normalized Ratio | PepsirfContingencyTSVFormat |
| Normalized Sized | PepsirfContingencyTSVFormat |
| Zscores | PepsirfContingencyTSVFormat |
| Zscores Nan | ZscoreNanFormat |
| Bins | PeptideBinFormat |
| Enrich Thresholds | EnrichThreshFileFormat |
| Num. of Samples | PepsirfInfoSNPNFormat |
| Num. of Peptides | PepsirfInfoSNPNFormat |
| Sum of Probes | PepsirfInfoSumOfProbesFmt |
| Enrichment Directory | EnrichedPeptideDirFmt |
| Multi-File | SubjoinMultiFileFmt |
| Protein Fasta | ProteinFastaFmt |
| Peptide Fasta | PeptideFastaFmt |
| Link Output | PepsirfLinkTSVFormat |
| Enriched Peptide List | PeptideIDListFmt |
| .DMP file | PepsirfDMPFormat |
| Deconv Singluar | PepsirfDeconvSingularFormat |
| Deconv Batch Dir | PepsirfDeconvBatchDirFmt |
| Score Per Round (Deconv) | ScorePerRoundFmt |
| Peptide Assignment Map (Deconv) | PeptideAssignMapDirFmt |
| fif file (Demux) | PepsirfDemuxFifFmt |
| Sample List (Demux) | PepsirfDemuxSampleListFmt |
| Index (Demux) | PepsirfDemuxIndexFmt |
| Library (Demux) | PepsirfDemuxLibraryFmt |
| FASTQ file (Demux) | PepsirfDemuxFastqFmt |
| Diagnostic file (Demux) | PepsirfDemuxDiagnosticFormat |
| Protein Alignment (proteinHeatmap) | ProteinAlignmentFormat |
