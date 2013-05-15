TR CONNECT
======

Thomson Reuters Python API provides a pythonic interface into several Thomson Reuters DBs.

 * Worldscope Fundamentals
 * Datastream Equity Pricing


Currently, Worldscope and Datastream are supported with I/B/E/S support coming soon.

Requirements
------------

* numpy 1.7
* pandas 0.10+
* iopro 1.4.2+
* Valid TR Credentials:
 * User ID
 * Password
 * Driver Path
 * Server



Installation
============

The package is not yet designed for installation.  Users can load the package by including the root level package directory path into their python scripts.

Usage
=====
We recommend storing credentials in a json file (see basic_test.py and trkey.json for an example).

Example
------------------
```python
    >>> from tr_connect import TR

    >>> #define or load credentials
    >>> creds = {"Uid": "XXXXXXXX", "Pwd": "XXXXXXXX", \
                "driver": "/usr/local/lib64/libsqlncli-11.0.so.1790.0", \
                "server": "XXX.XX.XXX.XXX,XXXX"}



    >>> #create tr  object
    >>> tr = TR(creds)

    >>> #single security-single measurement of 
    >>> ibm =  tr.query('IBM','ws.1751','Q')

    #Data Access
    >>>ibm.df #or ibm.data['ws.1751']
                       ws.1751
        1998-03-31  1031000000
        1998-06-30  1447000000
        1998-09-30  1489000000
        1998-12-31  2341000000
        1999-03-31  1465000000
        1999-06-30  2386000000

```

Queries
-------
Queries to the Worldscope and Datastream DBs are prepended with **ws.** and **ds.** respectively.

#Datastream
tr.query('security','ds.measure')

*The Datastream DB stores daily open, high, low, close, etc.  as such, frequency defaults to 'D'*

Available measures from Datastream are (all measures are fully adjusted):

* high
* low
* open
* close
* volume
* bid
* ask
* vwap
 * the volume-weighted average price for the day
* mosttrdprc
 * the most-traded price
* consolvol
 * the consolidated volume
* mosttrdvol
 * the most-traded volume
* totalreturn
 * the total return of the security, including dividends, distributions, and spinoffs.
* ohlc 
 * a convenience measure which returns open, high, low, and close



#Worldscope
tr.query('security','ws.measure','frequency')
The measures available for Worldscope are found in the wsitem_data.csv file distributed with the library. The measure is a four digit number corresponding to the description found in the wsitem_data.csv file. 

Example:

tr.query('IBM', 'ws.1001', 'Q') retrieves the Net Sales or Revenues for IBM, on a quarterly basis.


Searching for IDs
-----------------
QA Direct maintains a list of internal symbols for securities: **QAIDs**.  Often these overlap with public ticker names but not always.  We have provided basic search functionality for finding the **QAIDs** by searching QA Direct's ID and Name Columns.

#search id for like BMW
tr.find_id('BMW') 

#search for Names like Bayerische
tr.find_name('Bayerische')

In both instances a dictionary of arrays of QAID, Country, and Name are returned

Design
======
Class Names are CamelCase
Function Names are lower_case_underscore
