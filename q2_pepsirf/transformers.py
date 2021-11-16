#!/usr/bin/env python
from q2_pepsirf.plugin_setup import plugin
from q2_pepsirf.format_types import PepsirfContingencyTSVFormat, PepsirfInfoSumOfProbesFmt, EnrichedPeptideDirFmt, PeptideIDListFmt

from q2_types.feature_table import BIOMV210Format

import pandas as pd
import biom


# Then BIOMV210Format -> BIOMV210DirFmt
@plugin.register_transformer
def _0(ff: PepsirfContingencyTSVFormat) -> BIOMV210Format:
    result = BIOMV210Format()

    dataframe = pd.read_csv(str(ff), sep='\t', index_col=0)
    table = biom.Table(dataframe.values, observation_ids=dataframe.index,
                       sample_ids=dataframe.columns)

    with result.open() as fh:
        table.to_hdf5(fh, generated_by="q2-pepsirf for pepsirf")

    return result



@plugin.register_transformer
def _1(ff: BIOMV210Format) -> PepsirfContingencyTSVFormat:
    result = PepsirfContingencyTSVFormat()

    with ff.open() as fh:
        table = biom.Table.from_hdf5(fh)
    df = table.to_dataframe(dense=True)
    df.index.name = "Sequence name"
    df.to_csv(str(result), sep='\t')

    return result

@plugin.register_transformer
def _2(ff: PepsirfInfoSumOfProbesFmt) -> pd.DataFrame:
    result = pd.read_csv(str(ff), sep='\t')
    return result

@plugin.register_transformer
def _3(ff: EnrichedPeptideDirFmt ) -> pd.DataFrame:
    pairwiseDict = {}
    for relpath, series in ff.pairwise.iter_views(pd.Series):
        pairwiseDict[relpath] = series
    df = pd.DataFrame(pairwiseDict)
    df = df.fillna(False)
    return df

@plugin.register_transformer
def _4(ff: PeptideIDListFmt) -> pd.Series:
    with ff.open() as fh:
        ids = [id.strip() for id in fh.readlines()]
    return pd.Series(True, index = ids)