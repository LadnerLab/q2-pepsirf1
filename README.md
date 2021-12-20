# q2-pepsirf
Qiime2 Plug-in for the use of pepsirf within qiime.

https://ladnerlab.github.io/pepsirf-q2-plugin-docs/

## Installation

### Qiime2 Installation:

Visit: https://docs.qiime2.org/2021.8/install/ for intallation documentation on Qiime2

### Pepsirf Installation:

Visit: https://github.com/LadnerLab/PepSIRF for installation documentation on PepSIRF

### q2-pepsirf installation:
#### Dependencies:
- `qiime2-2021.11 +`
- `PepSIRF`

#### Directions:

Visit: https://ladnerlab.github.io/pepsirf-q2-plugin-docs/Pepsirf_Plugins/q2-pepsirf1/ for installation documentation on q2-pepsirf.

#### Update q2-pepsirf:

Visit: https://ladnerlab.github.io/pepsirf-q2-plugin-docs/Pepsirf_Plugins/q2-pepsirf1/#updating for updating documentation on q2-pepsirf.

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
