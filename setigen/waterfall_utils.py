import sys
import numpy as np
from blimpy import read_header, Waterfall


def max_freq(waterfall):
    """
    Returns central frequency of the highest-frequency bin in a .fil file.

    Parameters
    ----------
    waterfall : str or Waterfall
        Name of filterbank file or Waterfall object

    Returns
    -------
    fmax : float
        Maximum frequency in data
    """
    if isinstance(waterfall, str):
        waterfall = Waterfall(waterfall, load_data=False)
    elif not isinstance(waterfall, Waterfall):
        sys.exit('Invalid fil file!')

    return waterfall.container.f_stop


def min_freq(waterfall):
    """
    Returns central frequency of the lowest-frequency bin in a .fil file.

    Parameters
    ----------
    waterfall : str or Waterfall
        Name of filterbank file or Waterfall object

    Returns
    -------
    fmin : float
        Minimum frequency in data
    """
    if isinstance(waterfall, str):
        waterfall = Waterfall(waterfall, load_data=False)
    elif not isinstance(waterfall, Waterfall):
        sys.exit('Invalid data file!')

    return waterfall.container.f_start


def get_data(waterfall, use_db=False):
    """
    Gets time-frequency data from filterbank file as a 2d NumPy array.

    Note: when multiple Stokes parameters are supported, this will have to
    be expanded.

    Parameters
    ----------
    waterfall : str or Waterfall
        Name of filterbank file or Waterfall object

    Returns
    -------
    data : ndarray
        Time-frequency data
    """
    if isinstance(waterfall, str):
        waterfall = Waterfall(waterfall)
    elif not isinstance(waterfall, Waterfall):
        sys.exit('Invalid data file!')

    if use_db:
        return 10 * np.log10(waterfall.data[:, 0, :])

    return waterfall.data[:, 0, :]


def get_fs(waterfall):
    """
    Gets frequency values from filterbank file.

    Parameters
    ----------
    waterfall : str or Waterfall
        Name of filterbank file or Waterfall object

    Returns
    -------
    fs : ndarray
        Frequency values
    """
    if isinstance(waterfall, str):
        fch1 = read_header(waterfall)[b'fch1']
        df = read_header(waterfall)[b'foff']
        fchans = read_header(waterfall)[b'nchans']
    elif isinstance(waterfall, Waterfall):
        fch1 = waterfall.header[b'fch1']
        df = waterfall.header[b'foff']
        fchans = waterfall.header[b'nchans']
    else:
        sys.exit('Invalid data file!')

    return np.arange(fch1, fch1 + fchans * df, df)


def get_ts(waterfall):
    """
    Gets time values from filterbank file.

    Parameters
    ----------
    waterfall : str or Waterfall
        Name of filterbank file or Waterfall object

    Returns
    -------
    ts : ndarray
        Time values
    """
    if isinstance(waterfall, str):
        tsamp = read_header(waterfall)[b'tsamp']
    elif isinstance(waterfall, Waterfall):
        tsamp = waterfall.header[b'tsamp']
    else:
        sys.exit('Invalid fil file!')

    if isinstance(waterfall, str):
        fch1 = read_header(waterfall)[b'fch1']
        df = read_header(waterfall)[b'foff']
    else:
        fch1 = waterfall.header[b'fch1']
        df = waterfall.header[b'foff']

    waterfall0 = Waterfall(waterfall, f_start=fch1, f_stop=fch1 + df)

    try:
        tchans = get_data(waterfall0).shape[0]
    except Exception as e:
        sys.exit('No data in filterbank file!')

    return np.arange(0, tchans * tsamp, tsamp)
