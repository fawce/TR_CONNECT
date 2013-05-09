'''
Worldscope DB Example

Securities:
IBM: IBM
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
        print 'Valid TR credentials unavailable'

tr = TR(tr_creds)

print 'single security-single measurement'
jnj =  tr.query('JNJ','ws.1751','Q')

print jnj

print 'single security-multiple measurements'
# ibm = tr.query('IBM',1751,'Q']
ibm = tr.query('IBM',['ws.1751','ws.2001','ws.3351'],'Q')

print ibm
print ibm.data.keys()

print 'multiple securities-single measurments'
ni_secs = tr.query(['IBM','APPL','GOOG'],'ws.1751','Q')

print ni_secs
print ni_secs.data.keys()


