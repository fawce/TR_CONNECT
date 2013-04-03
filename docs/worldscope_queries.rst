-----------------------
Worldscope Queries First Steps
-----------------------

Basic Usage
-----------

Create TR object with approved credentials::
    
    >>> import json
    >>> from tr_connect import TR
    >>> creds = json.load('trkeys.json')
    >>> tr = TR(creds)
    
At this point a TR object has been created and you are now able to query the various DBs for data::

    >>> ibm =  tr.query('IBM','ws.1751','Q')
    >>> ibm
    Securities: IBM Measurements: ws.1751 Frequency: Q
    >>> ibm.data
    {'ws.1751': 1998-03-31    1031000000
    1998-06-30    1447000000
    1998-09-30    1489000000
    1998-12-31    2341000000
    1999-03-31    1465000000
    ...
    >>> ibm.df
                       ws.1751
        1998-03-31  1031000000
        1998-06-30  1447000000
        1998-09-30  1489000000
        1998-12-31  2341000000

We can also create more complex queries such as requesting multiple measurement for 
the same security:

    >>> ibm = tr.query('IBM',['ws.1751','ws.2001','ws.3351'],'Q')
    retrieving query:  IBM ['ws.1751', 'ws.2001', 'ws.3351']

    >>> ibm
    World Scope List
    Securities: IBM Measurements: ['ws.1751', 'ws.2001', 'ws.3351'] Frequency: Q

    >>> ibm.df
                   ws.1751      ws.2001      ws.3351
    1998-03-31  1031000000   5889000000  59079000000
    1998-06-30  1447000000   5471000000  58535000000
    1998-09-30  1489000000   5869000000  61084000000
    1998-12-31  2341000000   5768000000  63746000000

Or query for mutliple securities with same measurement:

    >>> ni_secs = tr.query(['IBM','AAPL','HP'],'ws.1751','Q')
    retrieving query:  ['IBM', 'AAPL', 'HP'] ws.1751
                                                                                                                                                               
    >>> ni_secs.df 
    <class 'pandas.core.frame.DataFrame'>
    DatetimeIndex: 142 entries, 1997-12-25 00:00:00 to 2012-12-31 00:00:00
    Data columns:
    AAPL    61  non-null values
    HP      57  non-null values
    IBM     60  non-null values
    dtypes: float64(3)

