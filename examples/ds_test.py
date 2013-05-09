'''
TR Connect Datastream example

Query DB for Open, High, Low, Close, etc.
Demonstrate search functionality to find proper QAID

Securities:
BMW:
JNJ: Johnson & Johnson

Measurements:
1751: Net Income 
2001: Cash
3351: total liabilities
3051: short term debt
'''

import os, json,sys
from tr_connect import TR

tr_creds = None

if tr_creds == None:
    try:
        from wakaridata.trdata import *
    except:
        print 'Valid TR tr_credentials unavailable'

tr = TR(tr_creds)

print 'Total Return Unitless'
totalreturn = tr.query('JNJ','ds.totalreturn')

print 'GET DF of OHLC'
ohlc =  tr.query('JNJ','ds.ohlc')

print 'Get TimeSeries of Singular Metric'
jnj_vwap =  tr.query('JNJ','ds.vwap')
jnj_high =  tr.query('JNJ','ds.high')
jnj_low =  tr.query('JNJ','ds.low')
jnj_close =  tr.query('JNJ','ds.close')
jnj_volume =  tr.query('JNJ','ds.volume')
jnj_bid =  tr.query('JNJ','ds.bid')
jnj_ask =  tr.query('JNJ','ds.ask')
jnj_vwap =  tr.query('JNJ','ds.vwap')
jnj_mosttrdprc =  tr.query('JNJ','ds.mosttrdprc')
jnj_consolvol =  tr.query('JNJ','ds.consolvol')
jnj_mosttrdvol =  tr.query('JNJ','ds.mosttrdvol')

print 'Try and find BMW in SEC and GSEC DBs'
bmw_id = tr.find_id('BMW')
bmw_name = tr.find_name('Bayerische')
