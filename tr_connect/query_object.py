'''Object which stores query results and provides convenience functions for 
plotting.  May build out for common financial computations'''

import sys
from StringIO import StringIO
import pandas as pd

class QueryObject(object):

    def __init__(self,qaid,item,freq,data,db_type,currency='US Dollars'):
        self.qaid = qaid
        self.item = item
        self.freq = freq
        self.data = data
        self.keys = data.keys()
        self.db_type = db_type
        self.currency = currency

        #build dataframe:
        self.df = self.build_dataframe()
        
    #borrow from pandas frame.py
    def __repr__(self):
        """
        Return a string representation for a particular Query Object
        """
        return self.__unicode__()

    def __unicode__(self):
        
        buf = StringIO(u"")
        self.info()

        value = buf.getvalue()

        return value
    
    def info(self):
        """
        Concise summary of a TR Query Object.

        """

        print self.db_type 
        print 'Securities: %s Measurements: %s Frequency: %s' % (self.qaid,self.item,self.freq)

    #DataFrame Construction
    def build_dataframe(self):
        """function which construction dataframe from query.  (convenience function)"""
        
        data = self.data[self.data.keys()[0]]
        
        if isinstance(data,pd.core.series.TimeSeries):
            return pd.DataFrame(self.data)
        else:
            return self.data[self.data.keys()[0]]

    #plotting functions
    def plot(self,key,column=None,title=None):
        '''Convenience plotting with Wakari'''
        from webplot import p

        p.use_doc('TR Plots')

        
        p.figure()
        data = self.data[key]
        if isinstance(data,pd.core.series.TimeSeries):
            dates = data.index.values.astype('datetime64[ms]').astype('int64')
            fig = p.plot_dates(dates,data.values,title=title,width=500,height=300)
        else:
            dates = data.index.values.astype('datetime64[ms]').astype('int64')
            fig = p.plot_dates(dates,data[column].values,title=title,width=500,height=300)
        return fig

    #financial computation functions
    #Coming Soon


