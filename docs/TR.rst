-----------
TR Connect
-----------
.. _pyodbc: http://docs.continuum.io/iopro/pyodbc.html 
.. _TimeSeries: http://pandas.pydata.org/pandas-docs/stable/timeseries.html
.. _DataFrame: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.__init__.html


.. contents::
  :maxdepth: 2

The Thomson Reuters API provides a Pythonic interface to several Thomson Reuters databases.

 * The TR API is written in python and leverages Continuum IO's fast data
   loading module IOPro.  IOPro has built-in database support and is optimized
   for ODBC connections (see pyodbc_).

 * Data is returned as a Pandas TimeSeries_ or dictionary of TimeSeries_ which
   can then be manipulated in familiar ways, to easily construct novel analyses.

 * Instead of arduous and lengthy search queries common to many RDBMS, users
   define securities, measurements, and frequencies as arguments to a TR
   object.

Credentials
-----------
Just like with [SQLite](http://docs.python.org/2/library/sqlite3.html), the
user must first create a connection object.  Unlike SQLite, the connection occurs within 
the TR object (see below).  Users pass a dictionary of their credentials with the following keys:
**Uid**, **Pwd**, **Pwd**, **driver**, **server**.  We suggest defining a separate json file like so:

**trkeys.json**

    {
        "Uid":: "XXXXXXXX",

        "Pwd":: "XXXXXXXX",
        
        "driver":: "/usr/local/lib64/libsqlncli-11.0.so.1790.0",
        
        "server":: "XXX.XX.XXX.XXX,2866"
    }

TR Object
=========
The **TR** class is the main interface to both queries and searches. A TR object can
be created by supplying the credentials outlined above


**TR(creds)**
    
    >>> tr = TR(creds)
    
Whenever an query is executed, a **QueryObject** is returned.  It provides
convenience functions for manipulating data, including plot integration.

Queries
-------
The TR object has one general query method:

**tr.query(sec='security',meas='measurement',freq='frequency')**

    | sec - QAID string or list of strings ['IBM','APPL',...], often publicly used ticker symbol
    | meas - type of measurement to be returned. For daily closing data use the Datastream database: **ds.XXXXX**

            open, high, low, close, volume, vwap, bid, ask, mosttrdprc, consolvol, mosttrdvol

            or 

            ohlc, a shorthand for open, high, low, close

            frequency defaults to 'D'

            For WorldScope queries, meas can also be a list of measurements. (please refer to TR documentation for accepted keys): **ws.XXXX**

            1751, 2001, 3351, 3051

            which refer to: Net Income, Cash, Total Liabilities, Short Term Debt
    | freq - Daily 'D', Quarterly 'Q', etc.

    >>> ibm_ohlc =  tr.query('JNJ','ds.ohlc')
    >>> ibm_ni =  tr.query('IBM','ws.1751','Q')


Searching
---------

**find_id_gsec(search)**
    | search - string used to find QAID matching *XXXX* in the ID column of the foreign exchanges.
               Returns a dictionary of arrays of ID, Name, Country
**find_id_sec(search)**
    | search - string used to find QAID matching *XXXX* in the ID column of the US exchanges.
               Returns a dictionary of arrays of ID, Name, Country
**find_id(search)**
    | search - string used to find QAID matching *XXXX* in the ID column of the GSEC and SEC exchanges.
               Returns a dictionary of arrays of ID, Name, Country
**find_name_gsec(search)**
    | search - string used to find QAID matching *XXXX* in the NAME column of the foreign exchanges.
               Returns a dictionary of arrays of ID, Name, Country
**find_name_sec(search)**
    | search - string used to find QAID matching *XXXX* in the Nmae column of the US exchanges.
               Returns a dictionary of arrays of ID, Name, Country
**find_name(search)**
    | search - string used to find QAID matching *XXXX* in the NAME column of the GSEC and SEC exchanges.
               Returns a dictionary of arrays of ID, Name, Country

    >>> bmw_id = tr.find_id('BMW')
    >>> bmw_name = tr.find_name('Bayerische')


QueryObject
===========


Returned data object after query is successfully executed.

    >>> ibm_ohlc =  tr.query('JNJ','ds.ohlc')

Data Access
-----------
Data can be accessed with two methods: 

  **Pandas DataFrame**
  ibm_ohlc.df return the dataframe object

  **Keys**
  ibm_ohlc.data is a python dictionary ibm_ohlc.data.keys() returns keys 
  and ibm_ohlc.data['key'] returns values.  The value, is a Pandas TimeSeries_ or DataFrame_


Plotting
---------
Convenience function for plotting in Wakari

**plot(key,column=None,title=None)**

    | key - string key in data dictionary

    *Optional*
    | column - string column for dataframe
    | title - string for title of the plot


    >>> ibm_ohlc = tr.query('IBM','ds.ohlc')
    >>> ibm_ohlc.plot('ds.ohlc','open','Openings')

    or 

    >>> ibm = tr.query('IBM',['ws.1751','ws.2001','ws.3351'],'Q')
    >>> fig = ibm.plot('ws.1751','Net Income')

    



