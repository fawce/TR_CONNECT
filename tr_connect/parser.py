from worldscope import WorldScope
from datastream import DataStream
from query_object import QueryObject

def parse_ws(df,qaid,item,freq,conn):

    #list of securities requested      
    if isinstance(qaid,list):
        
        if isinstance(item,list):
            raise Exception("Invalid Query: Can't parse list of Securities and list of Measurements")
           
        if isinstance(item,str):
            result = df[df['VALUE'] == int(item.split('.')[1])]
                
            if result.empty:
                raise Exception("Key not in WSITEM DB")
            
            else:
                #need to convert to int 
                #pyodbc.ProgrammingError: ('Invalid parameter type.  param-index=1 param-type=numpy.int64', 'HY105')
                num_id = int(result.VALUE.values[0])
                
                #Build WorldScope Object
                ws = WorldScope(conn,qaid,num_id,freq)
                return QueryObject(qaid,item,freq,ws.data,'World Scope DB: Multiple Securities')   

         
    #user wants multiple measurements for one qaid
    if isinstance(item,list):
        
        #fist check measurements:
        if isinstance(item[0],str):
            result =  [df[df['VALUE'] == int(i.split('.')[1])] for i in item]
        
        #check if results are empty
        for r in result:
            if r.empty:
                raise Exception("Key not in WSITEM DB")
    
        num_ids = [int(i.split('.')[1]) for i in item]
        ws = WorldScope(conn,qaid,num_ids,freq)
        return QueryObject(qaid,item,freq,ws.data,'World Scope List')   
    
              

    #user wants one qaid one measurement 
    if isinstance(item,str):
        result = df[df['VALUE'] == int(item.split('.')[1])]
   
    if result.empty:
        raise Exception("Key not in WSITEM DB")

    else:
        #need to convert to int 
        #pyodbc.ProgrammingError: ('Invalid parameter type.  param-index=1 param-type=numpy.int64', 'HY105')
        num_id = int(result.VALUE.values[0])
        
        #Build WorldScope Object
        ws = WorldScope(conn,qaid,num_id,freq)

        #Build and return Query Object
        return QueryObject(qaid,item,freq,ws.data,'World Scope')   


def parse_ds(qaid,meas,conn):
    
    #Build DataStream Object
    ds = DataStream(qaid,meas,conn)

    #Build and return Query Object
    #Total Returns Frequency = 'D' (Trading Daily)
    return QueryObject(qaid,meas,'D',ds.data,'DataStream')   

