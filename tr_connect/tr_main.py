from worldscope import WorldScope
from query_object import QueryObject
import pandas
import iopro.pyodbc
import parser


class TR(QueryObject):
    """ Represents a connection to a Thomson Reuters database """

    def __init__(self,creds):
        """
        conn: Data source; can be file name, file object, or StringIO object.
        parser: Type of parser for parsing text. Valid parser types are 'csv',
        'fixed width', and 'regex'
        """
        try:
            print 'connecting to TR Database'
            self.conn = iopro.pyodbc.connect('Driver={%s};Server={%s};Database=qai;Uid={%s};Pwd={%s}'%(creds['driver'],creds['server'],creds['Uid'],creds['Pwd']))
        except:
            raise Exception("Error connecting to TR Database.  Please makes sure you are using a json dictionary\nwith driver,server,Uid,and Pwd defined.")
        self.df_ws = pandas.read_csv('../data/wsitem_data.csv',sep='\t')

    def get_ws(self):
        """ Returns dataframe of Worldscope names and IDs """
        return self.df_ws
        # tr_connect = client(self.conn,self.driver)
    
        
    def query(self,qaid,item,freq='Q'):
        """Function which defines pythonic sql-query and returns a QueryObject"""
        
        print 'retrieving query: ', qaid, item
        if isinstance(item,str):
            db_prefix, meas = item.split('.')

        if isinstance(item,list):
            db_prefix, meas = item[0].split('.')

        #World Scope Query
        if db_prefix == 'ws':
            df = self.get_ws()
            
            #Parse Query and Return Query Object
            return parser.parse_ws(df,qaid,item,freq,self.conn)

        #World Scope Query
        if db_prefix == 'ds':
            return parser.parse_ds(qaid,meas,self.conn)
         


    #SEARCH FUNCTION
    def find_id_gsec(self,search):
        """ Returns an array of vaild qaid and Full Names Ids based on ID from GSEC DB"""

        cursor = self.conn.cursor()
        sql = "select Id,Name,Country from gsecmstrx where id like '%%%s%%'"
        cursor.execute(sql % str(search) )
        
        rows_gsec = cursor.fetchdictarray()

        return rows_gsec

    def find_id_sec(self,search):
        """ Returns an Dictonary of vaild qaid Ids and Full Names based on ID from SEC DB"""

        cursor = self.conn.cursor()
        sql = "select Id,Name,Country from secmstrx where id like '%%%s%%'"
        cursor.execute(sql % str(search) )
        
        rows_sec = cursor.fetchdictarray()

        return rows_sec
    
    def find_id(self,search):
        """ Returns a dictionary of vaild qaid Ids based on ID.  Indexs SEC and GSEC"""

        search_dict = {}
        search_dict['GSEC'] = self.find_id_gsec(search)
        search_dict['SEC'] = self.find_id_sec(search)

        return search_dict
    
    def find_name_gsec(self,search):
        """ Returns an array of vaild qaid and Full Names Ids based on NAME from GSEC DB"""

        cursor = self.conn.cursor()
        sql = "select Id,Name,Country from gsecmstrx where NAME like '%%%s%%'"
        cursor.execute(sql % str(search) )
        
        rows_gsec = cursor.fetchdictarray()

        return rows_gsec

    def find_name_sec(self,search):
        """ Returns an Dictonary of vaild qaid Ids and Full Names based on ID from SEC DB"""

        cursor = self.conn.cursor()
        sql = "select Id,Name,Country from secmstrx where NAME like '%%%s%%'"
        cursor.execute(sql % str(search) )
        
        rows_sec = cursor.fetchdictarray()

        return rows_sec
    
    def find_name(self,search):
        """ Returns a dictionary of vaild qaid Ids based on NAME.  Indexs SEC and GSEC"""

        search_dict = {}
        search_dict['GSEC'] = self.find_name_gsec(search)
        search_dict['SEC'] = self.find_name_sec(search)

        return search_dict
