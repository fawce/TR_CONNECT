from errors import NoData, QADNotFound, QADMultipleFound
from pandas import Series

__all__ = (
        "NoData",
        "QADNotFound",
        "QADMultipleFound"
        "QADirect"
        )


class QADirect(object):
    '''
    qa direct data access class.  
    '''

    @staticmethod
    def rows_to_series(rs):
        t = zip(*rs)
        try:
            index = t[0]
            data = t[1]
            s = Series(data, index)
            return s
        except:
            print 'Bad Data to Series'


    @staticmethod
    def get_sec_code_from_id(conn, qaid):
        cursor = conn.cursor()
        sql = 'select seccode from secmstrx where id = ?'

        cursor.execute(sql,qaid)
        
        rows = cursor.fetchall()
        if len(rows) > 0: 
            # it's a North American ID, so get data from the NA tables
            # (ibesestl* and secmapx)
            seccode = rows[0][0]
            region = 'US'
        else: 
            # It's global so get data from the global tables (ibgsestl* and
            # gsecmapx)
            sql = 'select seccode from gsecmstrx where id = ?'
            cursor.execute(sql,qaid)
            rows = cursor.fetchall()
            if len(rows) > 0: #it's valid
                seccode = rows[0][0]    
                region = 'G'
            else:
                raise QADNotFound(qaid)
        return [seccode, region]
            
    