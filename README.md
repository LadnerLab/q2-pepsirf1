# q2-pepsirf
Qiime2 Plug-in for the use of pepsirf within qiime.

## Installation

### Qiime2 Installation:

### Pepsirf Installation:

### q2-pepsirf installation:

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
| Zscore Thresholds | ZscoreThreshFileFormat | 'ZscoreThresh' |
| Num. of Samples | PepsirfInfoSNPNFormat | 'InfoSNPN' |
| Num. of Peptides | PepsirfInfoSNPNFormat | 'InfoSNPN' |
| Sum of Probes | PepsirfInfoSumOfProbesFmt | 'InfoSumOfProbes' | 

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
| Zscore Thresholds | ZscoreThreshFileFormat |
| Num. of Samples | PepsirfInfoSNPNFormat |
| Num. of Peptides | PepsirfInfoSNPNFormat |
| Sum of Probes | PepsirfInfoSumOfProbesFmt |
| Enrichment Directory | EnrichedPeptideDirFmt |
