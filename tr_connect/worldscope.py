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

class WorldScope(object):

# GetWorldscope(cnxn, qaid, 2999,'Q')

    def __init__(self,conn,qaid,item,freq):
        self.conn = conn

        if isinstance(qaid,list):
            self.data = self.get_worldscope_list_qaids(qaid, item, freq)
        elif isinstance(item,int):
            self.data = self.get_worldscope(qaid, item, freq)
        elif isinstance(item,list):
            self.data = self.get_worldscope_list_items(qaid, item, freq)
        
    def get_worldscope_items(self):
        sql = '''select Number, Name from wsitem'''
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    
    def get_worldscope_currency(self, qaid):
        try:
            [seccode, region] = QADirect.get_sec_code_from_id(self.conn,qaid)
        except QADNotFound as e:
            print "Can't Find QAId:", e.value
            return
        
        if region == 'US':
            sql = '''select isoused 
                    from wscurr c join wsinfo i on c.natcode = i.country
                    join secmapx m on m.vencode = i.code and m.ventype = 10 and rank = 1
                    where seccode = ?'''
        elif region == 'G':
            sql = '''select isoused 
                    from wscurr c join wsinfo i on c.natcode = i.country
                    join gsecmapx m on m.vencode = i.code and m.ventype = 10 and rank = 1
                    where seccode = ?'''                
        cursor = self.conn.cursor()
        cursor.execute(sql, seccode)
        rows = cursor.fetchall()
        return rows[0][0]
                    
    def get_worldscope(self, qaid, item, freq):
        
        try:
            [seccode, region] = QADirect.get_sec_code_from_id(self.conn,qaid)
        except QADNotFound as e:
            print "Can't Find QAId:", e.value
            return
        if region == 'US':
            sql = '''select d.year_, d.seq, d.date_, value_, f.date_ from wsndata d
                    join secmapx m on m.ventype = 10 and m.vencode = d.code and rank = 1
                    left outer join wsfye f on f.code = d.code and f.year_ = d.year_
                    where m.seccode = ? and item = ? and freq = ?'''
        elif region == 'G':
            sql = '''select d.year_, d.seq, d.date_, value_, f.date_ from wsndata d
                    join gsecmapx m on m.ventype = 10 and m.vencode = d.code and rank = 1
                    left outer join wsfye f on f.code = d.code and f.year_ = d.year_
                    where m.seccode = ? and item = ? and freq = ?'''
        cursor = self.conn.cursor()
        cursor.execute(sql, seccode, item, freq)
        rows = cursor.fetchall()
        val = dict()
        if freq == 'Q':
            for row in rows:
                if row[2] is None and row[4] is not None:
                    if row[1] == 4:
                        row[2] = row[4]
                    elif row[1] == 3:
                        row[2] = row[4] + relativedelta(months=-3)
                    elif row[1] == 2:
                        row[2] = row[4] + relativedelta(months=-6)
                    elif row[1] == 1:
                        row[2] = row[4] + relativedelta(months=-9)
                    lastfy = row[4]
                elif row[2] is None and row[4] is None:
                    row[2] = lastfy + relativedelta(months=3*row[1])
                val[row[2]] = row[3]
        elif freq == 'A':
            for row in rows:
                if row[2] is None and row[4] is not None:
                    if row[1] == 1:
                        row[2] = row[4]
                val[row[2]] = row[3]

        #build dictionary to return
        series_dict = dict()
        series_dict['ws.'+str(item)] = pd.Series(val)
        return  series_dict
            

        
    
    def get_worldscope_list_items(self, qaid, item, freq):
            
            try:
                [seccode, region] = QADirect.get_sec_code_from_id(self.conn,qaid)
            except QADNotFound as e:
                print 'Can\'t Find QAId:', e.value
                return
            if region == 'US':
                sql = '''select d.year_, d.seq, d.date_, value_, f.date_ from wsndata d
                        join secmapx m on m.ventype = 10 and m.vencode = d.code and rank = 1
                        left outer join wsfye f on f.code = d.code and f.year_ = d.year_
                        where m.seccode = ? and item in (%s) and freq = ?'''
            elif region == 'G':
                sql = '''select d.year_, d.seq, d.date_, value_, f.date_ from wsndata d
                        join secmapx m on m.ventype = 10 and m.vencode = d.code and rank = 1
                        left outer join wsfye f on f.code = d.code and f.year_ = d.year_
                        where m.seccode = ? and item in (%s) and freq = ?'''
            
            #fill sql with ? to be replaced by list of qaid, measurements and 
            #freqency
            placeholder= '?' 
            placeholders= ', '.join(placeholder for unused in item)
            sql = sql % placeholders

            sql_items = copy.deepcopy(item)

            cursor = self.conn.cursor()

            #prepend with security code of qaid
            sql_items.insert(0,seccode)

            sql_items.append(freq)
            
            #define cursor for query
            cursor.execute(sql, sql_items)

            #query returned as big list.  need to pull out individual 
            #measurments change to fetchdictarray for more verbose indexing 
            rows = cursor.fetchall()
            
            #parse items based on inflection of date

            date = rows[0][0]
            qaid_pts = []
            
            series_dict = dict()
            
            val = dict()
            
            i = 0

            if freq == 'Q':
                for row in rows:
                    #date montonically increasing
                    if row[0] >= date:
                        date = row[0]

                    #inflection of date.  create series and store in dictionary
                    else:

                        #modify key for consistency with API usage
                        #+1 offset for prepended security id 
                        series_dict['ws.'+str(sql_items[i+1])] = pd.Series(val)
                        i += 1
                        val = dict()
                        date = row[0]
                    
                    if row[2] is None and row[4] is not None:
                        if row[1] == 4:
                            row[2] = row[4]
                        elif row[1] == 3:
                            row[2] = row[4] + relativedelta(months=-3)
                        elif row[1] == 2:
                            row[2] = row[4] + relativedelta(months=-6)
                        elif row[1] == 1:
                            row[2] = row[4] + relativedelta(months=-9)
                        lastfy = row[4]
                    elif row[2] is None and row[4] is None:
                        row[2] = lastfy + relativedelta(months=3*row[1])
                    val[row[2]] = row[3]
            elif freq == 'A':
                for row in rows:
                    if row[2] is None and row[4] is not None:
                        if row[1] == 1:
                            row[2] = row[4]
                    val[row[2]] = row[3]
            series_dict['ws.'+str(sql_items[i+1])] = pd.Series(val)
            
            return series_dict
            
    def get_worldscope_list_qaids(self, qaid, item, freq):
    
        seccodes = []
        regions = []

        series_dict_g = dict()
        series_dict_us = dict()

        for q in qaid:
            try:
                [seccode, region] = QADirect.get_sec_code_from_id(self.conn,q)
                seccodes.append(seccode)
                regions.append(region)
                print seccodes, regions
            except QADNotFound as e:
                print "Can't Find QAId:", e.value
                return

        #build dict of seccodes and qaid for series dict creation below
        seccode_dict = dict(zip(seccodes,qaid))

        if 'G' in regions:
            n_regions = np.array(regions)
            ii = np.where(n_regions == 'G')[0]
            qaids = list(seccodes[ii])
            for q in qaids:
                series_dict_g[q] = self.get_worldscope_region(q, item, freq,'G')

            
        elif 'US' in regions:
            indices = [i for i, x in enumerate(regions) if x == "US"]
            #pull out seccodes which match US
            s_codes = [seccodes[i] for i in indices]  
            for s in s_codes:
                series_dict_us[seccode_dict[s]] = self.get_worldscope_region(s, item, freq,'US')
            
        series_dict_us.update(series_dict_g)
        return series_dict_us
            
    def get_worldscope_region(self, seccode, item, freq,region):

        if region == 'US':
            sql = '''select d.year_, d.seq, d.date_, value_, f.date_ from wsndata d
                    join secmapx m on m.ventype = 10 and m.vencode = d.code and rank = 1
                    left outer join wsfye f on f.code = d.code and f.year_ = d.year_
                    where m.seccode = ? and item = ? and freq = ?'''
        elif region == 'G':
            sql = '''select d.year_, d.seq, d.date_, value_, f.date_ from wsndata d
                    join gsecmapx m on m.ventype = 10 and m.vencode = d.code and rank = 1
                    left outer join wsfye f on f.code = d.code and f.year_ = d.year_
                    where m.seccode = ? and item = ? and freq = ?'''

        cursor = self.conn.cursor()
        cursor.execute(sql, seccode, item, freq)
        rows = cursor.fetchall()
        val = dict()
        if freq == 'Q':
            for row in rows:
                if row[2] is None and row[4] is not None:
                    if row[1] == 4:
                        row[2] = row[4]
                    elif row[1] == 3:
                        row[2] = row[4] + relativedelta(months=-3)
                    elif row[1] == 2:
                        row[2] = row[4] + relativedelta(months=-6)
                    elif row[1] == 1:
                        row[2] = row[4] + relativedelta(months=-9)
                    lastfy = row[4]
                elif row[2] is None and row[4] is None:
                    row[2] = lastfy + relativedelta(months=3*row[1])
                val[row[2]] = row[3]
        elif freq == 'A':
            for row in rows:
                if row[2] is None and row[4] is not None:
                    if row[1] == 1:
                        row[2] = row[4]
                val[row[2]] = row[3]
        return pd.Series(val)
            

