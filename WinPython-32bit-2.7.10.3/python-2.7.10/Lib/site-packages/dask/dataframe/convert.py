import pandas as pd
import numpy as np
from pandas.core.internals import create_block_manager_from_blocks, make_block
from pandas.core.index import _ensure_index


def to_blocks(df):
    blocks = [block.values for block in df._data.blocks]
    index = df.index.values
    return {'blocks': blocks,
            'index': index,
            'columns': df.columns,
            'placement': [ b.mgr_locs.as_array for b in df._data.blocks ]}


def from_blocks(blocks, index, columns, placement):
    blocks = [ make_block(b, placement=placement[i]) for i, b in enumerate(blocks) ]
    axes = [ _ensure_index(columns), _ensure_index(index) ]
    df = pd.DataFrame(create_block_manager_from_blocks(blocks, axes))
    return df


def test_blocks():
    N = 10000
    df = pd.DataFrame({'A' : np.arange(N),
                       'B' : np.random.randn(N),
                       'C' : pd.date_range('20130101',freq='s',periods=N),
                       'D' : np.random.randn(N) + 100, 'E' : 'foobar'})


    data = to_blocks(df)

    df2 = from_blocks(**data)

    assert list(df.columns) == list(df2.columns)
    assert [a.values.ctypes.data == b.values.ctypes.data
            for a, b in zip(df._data.blocks, df2._data.blocks)]
    assert df.index.values.ctypes.data == df2.index.values.ctypes.data
    assert df2.equals(df)

