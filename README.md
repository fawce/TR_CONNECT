TR CONNECT
======

Thomson Reuters Python API provides a pythonic interface into several Thomson Reuters DBs.

 * Worldscope Fundamentals
 * Datastream Equity Pricing
 * I/B/E/S

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

#Worldscope
tr.query('security','ws.measure','frequency')


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
