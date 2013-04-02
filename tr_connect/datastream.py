import iopro.pyodbc
from dateutil.relativedelta import relativedelta
import datetime as dt
import time
import pandas as pd
import copy
import numpy as np

    
from errors import NoData, QADNotFound, QADMultipleFound
from stdqad import QADirect

__all__ = (
        "NoData",
        "QADNotFound",
        "QADMultipleFound",
        "QADirect"
        )

class DataStream(object):

# GetWorldscope(cnxn, qaid, 2999,'Q')

    def __init__(self,qaid,query,conn):
        self.conn = conn

        if query == 'ohlc':
            self.data  = self.get_pricing_item_list(qaid,['Open_', 'high', 'low', 'Close_'])
        
        elif query == 'totalreturn':
            self.data = self.get_total_return(qaid)

        elif query in ['open', 'high', 'low', 'close', 'volume', 'bid', 'ask', 'vwap', 'mosttrdprc','consolvol', 'mosttrdvol']:
            self.data  = self.get_pricing_item(qaid,query)
        
    
    def get_total_return(self, qaid):
        [seccode, region] = QADirect.get_sec_code_from_id(self.conn,qaid)
        
        if region == 'US':
            sql = '''select marketdate, ri 
                from Ds2PrimQtRI q join secmapx m on 
                m.vencode = q.infocode and m.ventype = 33 and rank = 1 and q.marketdate 
                between m.startdate and m.enddate
                where m.seccode = ?'''
        elif region == 'G':
            sql = '''select marketdate, ri 
                from Ds2PrimQtRI q join gsecmapx m on 
                m.vencode = q.infocode and m.ventype = 33 and rank = 1 and q.marketdate 
                between m.startdate and m.enddate
                where m.seccode = ?'''
        
        cursor = self.conn.cursor()
        cursor.execute(sql, seccode)
        rows = cursor.fetchall()
        s = QADirect.rows_to_series(rows)
        #build dictionary to return
        totalreturn_dict = dict()
        totalreturn_dict['ds.totalreturn'] = s
        
        return totalreturn_dict


    def get_pricing_item(self, qaid, query):

        #temp variable for switching below
        item = query
        try:
            [seccode, region] = QADirect.get_sec_code_from_id(self.conn,qaid)
        except QADNotFound as e:
            print "Can't Find QAId: ", e.value
            return
        if item == 'close':
            item = 'Close_'
        elif item == 'open':
            item = 'Open_'
        if query in ['volume','consolvol', 'mosttrdvol']:
            adjuster = '/CumAdjFactor'
        else:
            adjuster = "*CumAdjFactor * case when priceunit  = 'E+02' then 100 else 1 end"
        if region == 'US':
            sql = '''select marketdate, ''' + item + adjuster + ''', q.ISOCurrCode
                from Ds2PrimQtPrc q join secmapx m on 
                m.vencode = q.infocode and m.ventype = 33 and rank = 1 
                    and q.marketdate between m.startdate and m.enddate
                join ds2Adj a on a.infocode = q.infocode 
                    and q.marketdate between adjdate and isnull(endadjdate, '2079-06-06') and AdjType = 2
                join ds2exchqtinfo e on e.infocode = q.infocode 
                    and e.startdate < q.marketdate and q.exchintcode = e.exchintcode
                where m.seccode = ?'''
        elif region == 'G':
            sql = '''select marketdate, ''' + item + adjuster + ''', q.ISOCurrCode
                from Ds2PrimQtPrc q join gsecmapx m on 
                m.vencode = q.infocode and m.ventype = 33 and rank = 1 
                    and q.marketdate between m.startdate and m.enddate
                join ds2Adj a on a.infocode = q.infocode 
                    and q.marketdate between adjdate and isnull(endadjdate, '2079-06-06') and AdjType = 2
                join ds2exchqtinfo e on e.infocode = q.infocode 
                    and e.startdate < q.marketdate and q.exchintcode = e.exchintcode
                where m.seccode = ?'''
        
        cursor = self.conn.cursor()
        cursor.execute(sql, seccode)
        rows = cursor.fetchall()
        s = QADirect.rows_to_series(rows)
        
        #build dictionary to return
        pricingitem_dict = dict()
        pricingitem_dict['ds.'+str(query)] = s
        
        return pricingitem_dict

    def get_pricing_item_list(self, qaid, query):
        
        [seccode, region] = QADirect.get_sec_code_from_id(self.conn,qaid)
        
        if region == 'US':
            sql = '''select marketdate, ''' + ' ,'.join(query) + '''*CumAdjFactor * case when priceunit  = 'E+02' then 100 else 1 end, q.ISOCurrCode
                    from Ds2PrimQtPrc q join secmapx m on 
                    m.vencode = q.infocode and m.ventype = 33 and rank = 1 
                        and q.marketdate between m.startdate and m.enddate
                    join ds2Adj a on a.infocode = q.infocode 
                        and q.marketdate between adjdate and isnull(endadjdate, '2079-06-06') and AdjType = 2
                    join ds2exchqtinfo e on e.infocode = q.infocode 
                        and e.startdate < q.marketdate and q.exchintcode = e.exchintcode
                    where m.seccode = ?'''
        elif region == 'G':
            sql = '''select marketdate, ''' + ' ,'.join(query) + '''*CumAdjFactor * case when priceunit  = 'E+02' then 100 else 1 end, q.ISOCurrCode
                    from Ds2PrimQtPrc q join gsecmapx m on 
                    m.vencode = q.infocode and m.ventype = 33 and rank = 1 
                        and q.marketdate between m.startdate and m.enddate
                    join ds2Adj a on a.infocode = q.infocode 
                        and q.marketdate between adjdate and isnull(endadjdate, '2079-06-06') and AdjType = 2
                    join ds2exchqtinfo e on e.infocode = q.infocode 
                        and e.startdate < q.marketdate and q.exchintcode = e.exchintcode
                    where m.seccode = ?'''


        cursor = self.conn.cursor()
        cursor.execute(sql, seccode)
        
        rows = cursor.fetchdictarray()

        df = pd.DataFrame(rows)
        
        #Close_ column not listed
        df = df.rename(columns={'':'close'})
        df = df.rename(columns={'Open_':'open'})
        
        df = df.set_index('marketdate')

        #build dictionary to return
        pricingitem_dict = dict()

        pricingitem_dict['ds.'+'ohlc'] = df
        
        return pricingitem_dict
