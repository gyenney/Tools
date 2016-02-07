# try:
#     import blaze
# except ImportError:
#     pass
# else:
#     from multipledispatch import halt_ordering, restart_ordering
#     halt_ordering()
#     from .core import blaze_
#     restart_ordering()


import numbers
from datetime import date, datetime

from blaze.dispatch import dispatch, namespace
from blaze.expr import Projection, Field, BinOp, UnaryOp, Not, USub, Expr
import datashape
from multipledispatch import Dispatcher
import numpy as np
from datashape import Record, dshape

import xray
from xray.core.groupby import GroupBy

base = (numbers.Number, basestring, date, datetime)


@dispatch(xray.Dataset)
def discover(ds):
    def var_dshape(v):
        return datashape.from_numpy(v.shape, v.dtype)

    return Record([(k, var_dshape(v)) for k, v in ds.items()])


@dispatch(xray.DataArray)
def discover(data):
    return datashape.from_numpy(data.shape, data.dtype)


xray_types = (xray.Dataset, xray.DataArray)
base_types = (np.ndarray, base)


@dispatch(Projection, xray.Dataset)
def compute_up(t, ds, **kwargs):
    return ds[list(t.fields)]


@dispatch(Field, xray.Dataset)
def compute_up(t, ds, **kwargs):
    assert len(t.fields) == 1
    return ds[t.fields[0]]


@dispatch(BinOp, xray_types, xray_types + base_types)
def compute_up(t, lhs, rhs, **kwargs):
    return t.op(lhs, rhs)


@dispatch(BinOp, xray_types, GroupBy)
def compute_up(t, lhs, rhs, **kwargs):
    return t.op(lhs, rhs)


@dispatch(BinOp, GroupBy, xray_types)
def compute_up(t, lhs, rhs, **kwargs):
    return t.op(lhs, rhs)


@dispatch(BinOp, xray_types)
def compute_up(t, data, **kwargs):
    if isinstance(t.lhs, Expr):
        return t.op(data, t.rhs)
    else:
        return t.op(t.lhs, data)


@dispatch(BinOp, base_types, xray_types)
def compute_up(t, lhs, rhs, **kwargs):
    return t.op(lhs, rhs)


@dispatch(UnaryOp, xray.Dataset)
def compute_up(t, x, **kwargs):
    return x.apply(getattr(np, t.symbol))


@dispatch(UnaryOp, xray.DataArray)
def compute_up(t, x, **kwargs):
    return getattr(np, t.symbol)(x)


@dispatch(Not, xray_types)
def compute_up(t, x, **kwargs):
    return ~x


@dispatch(USub, xray_types)
def compute_up(t, x, **kwargs):
    return -x



math_names = '''abs sqrt sin cos tan sinh cosh tanh acos acosh asin asinh atan atanh
exp log expm1 log10 log1p radians degrees ceil floor trunc isnan'''.split()

reduction_names = '''any all sum min max mean var std'''.split()


# types = {builtins: object,
#          np: (np.ndarray, np.number),
#          pymath: Number,
#          blazemath: Expr,
#          reductions: Expr}

types_mapping = {
    xray.Dataset: lambda func: lambda ds: ds.apply(func),
    xray.DataArray: lambda func: func,
}


for funcname in math_names:  # sin, sqrt, ceil, ...
    d = namespace[funcname]
    for typ, create_func in types_mapping.items():
        if hasattr(np, funcname):
            d.add((typ,), create_func(getattr(np, funcname)))
    locals()[funcname] = d


for funcname in reduction_names:  # any, all, sum, max, ...
    d = namespace[funcname]
    for typ, _ in types_mapping.items():
        if hasattr(np, funcname):
            d.add((typ,), lambda obj: getattr(obj, funcname)())
    locals()[funcname] = d
#     for module, typ in types.items():
#         if hasattr(module, funcname):
#             d.add((typ,), getattr(module, funcname))

#     namespace[funcname] = d
#     locals()[funcname] = d
