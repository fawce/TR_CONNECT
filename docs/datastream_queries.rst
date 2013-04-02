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



