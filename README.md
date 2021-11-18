# q2-pepsirf
Qiime2 Plug-in for the use of pepsirf within qiime.

## Installation

### Qiime2 Installation:

Visit: https://docs.qiime2.org/2021.8/install/ for intallation documentation on Qiime2

### Pepsirf Installation:

Visit: https://github.com/LadnerLab/PepSIRF for installation documentation on PepSIRF

### q2-pepsirf installation:
#### Dependencies:
- `qiime2`
- `PepSIRF`

#### Directions:
Make sure your Qiime2 conda environment is activated by running the command:
  
```
conda activate qiime2-2021.8
```

You can replace `qiime2-2021.8` above with whichever version of QIIME 2 you have currently installed.

Now you are ready to install q2-pepsirf. Run the following commands:

```
pip install git+https://github.com/LadnerLab/q2-pepsirf1.git
```

Run `qiime info` to check for a successful installation. If installation was successful, you should see `pepsirf: version` in the list of installed plugins.

#### Update q2-pepsirf:

To update q2-pepsirf, run the following command:

```
pip install -U git+https://github.com/LadnerLab/q2-pepsirf1.git
```

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
