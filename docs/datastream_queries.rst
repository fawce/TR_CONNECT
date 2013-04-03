-----------------------
Datastream Queries First Steps
-----------------------

Basic Usage
-----------

Create TR object with approved credentials::
    
    >>> import json
    >>> from tr_connect import TR
    >>> creds = json.load('trkeys.json')
    >>> tr = TR(creds)
    
At this point a TR object has been created and you are now able to query the various DBs for data::

    >>> ibm_open =  tr.query('IBM','ds.open')
    >>> ibm_open.df
    >>> ibm_open
        DataStream
        Securities: IBM Measurements: open Frequency: D

    >>> ibm_open.data
        {'ds.open': 1973-01-03    None
        1973-01-04    None
        1973-01-05    None
        1973-01-08    None
    ...
    >>> ibm_open.df.tail()
                   ds.open
        2013-03-25  212.54
        2013-03-26  211.77
        2013-03-27  210.96
        2013-03-28  209.83
        2013-04-01   212.8


The above can be repeated for standard daily closing measurements: open, high, low, close, volume, vwap, etc. 
There is also a convenience key for open, high, low, close: **ds.ohlc**
    

    >>> ibm_ohlc = tr.query('IBM','ds.ohlc')
    retrieving query:  IBM ds.ohlc

    >>> ibm_ohlc.df
    <class 'pandas.core.frame.DataFrame'>
    DatetimeIndex: 10151 entries, 1973-01-03 00:00:00 to 2013-04-01 00:00:00
    Data columns:
    close          10151  non-null values
    ISOCurrCode    10151  non-null values
    open           4928  non-null values
    high           10151  non-null values
    low            10151  non-null values
    dtypes: float64(4), object(1)


The library packages open, low, high, close, into a Pandas DataFrame indexed off the date.  

    >>> ibm_ohlc.df.ix['2013-03']
     
                     close ISOCurrCode        open        high         low
    marketdate
    2013-03-01  202.909988         USD  200.649994  202.939987  199.359985
    2013-03-04  205.189987         USD  202.589996  205.189987  202.549988
    2013-03-05  206.529999         USD  205.859985  207.699997  205.689987
    2013-03-06  208.379990         USD  207.029999  208.490005  206.659988
    2013-03-07  209.419998         USD  208.289993  209.600006  208.240005
    2013-03-08  210.379990         USD  209.850006  210.740005  209.429993
    2013-03-11  210.079987         USD  210.039993  210.199905  209.039993
    2013-03-12  210.549988         USD  209.399994  210.729996  209.089996
    2013-03-13  212.059998         USD  210.200089  212.359985  209.769989
    2013-03-14  215.799988         USD  212.149994  215.859985  212.149994
    2013-03-15  214.919998         USD  215.379990  215.899994  213.409988
    2013-03-18  213.210007         USD  212.899994  214.500000  212.639999
    2013-03-19  213.439987         USD  214.129990  215.119995  211.828995
    2013-03-20  215.059998         USD  214.759995  215.820007  214.299988
    2013-03-21  212.259995         USD  212.960007  213.000000  210.109985
    2013-03-22  212.079987         USD  212.210007  213.169998  211.618988
    2013-03-25  210.740005         USD  212.539993  212.809998  210.049988
    2013-03-26  212.359985         USD  211.769989  212.503998  211.500000
    2013-03-27  210.889999         USD  210.960007  212.159988  210.100006
    2013-03-28  213.299988         USD  209.829987  213.439987  209.734985

    