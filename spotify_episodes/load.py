# load.py
# load transformed dataframe into database
import extract
import transform
from sqlalchemy import create_engine
import psycopg2
import time

def check_table_postgres(connection_string):
    '''
    check for tables in postgres
    '''
    # create table if necessary
    sql1 = '''
    CREATE TABLE IF NOT EXISTS episodes (
    ID VARCHAR(200),
    name VARCHAR(200),
    description VARCHAR(200),
    duration_ms BIGINT,
    release_date DATE
    )
    '''

    pg_conn = None
    try:
        #connect to postgres
        pg_conn = psycopg2.connect(connection_string)
        cursor = pg_conn.cursor()

        #run sql
        start_time = time.time()
        cursor.execute(sql1)
        print("execute sql1 duration: {} seconds".format(time.time() - start_time))

        #close connection and commit changes
        cursor.close()
        print('close connection to database')
        pg_conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    if pg_conn is not None:
        pg_conn.close()

def load_df_postgres(df, connection_string, destination):
    conn = None
    try:
        #connect to postgres
        db = create_engine(connection_string)
        conn = db.connect()

        #upload dataframe
        start_time = time.time()
        df.to_sql(destination, con=conn, if_exists = 'replace', index = False)
        print("to_sql duration: {} seconds".format(time.time() - start_time))

        #commit and close connection
        conn.commit()
        conn.close()
        print('close connection to database')
    except:
        raise Exception('connection or to_sql error')
    
    if conn is not None:
        conn.close()


if __name__ == '__main__':
    client_id = '4cb9bf88a1844329886f8ab395c9dea0'
    client_secret = 'e934c0e875434659b5efe6f4023c11dc'
    base_url = 'https://api.spotify.com/v1/shows/'
    show_id = '07SjDmKb9iliEzpNcN2xGD' #bill simmons podcast
    # extract data
    json_file = extract.get_request_results(client_id, client_secret, base_url, show_id)
    # convert json_file to dataframe
    load_df = transform.return_dataframe(json_file)
    # quality check dataframe
    if(transform.quality_check(load_df) == False):
        raise Exception('dataframe failed quality check')

    # postgres location
    conn_string = 'postgresql://localhost/mikeaguenza'

    # check if table needs to be made or not
    try:
        check_table_postgres(conn_string)
    except:
        raise Exception('connection or table error')
    
    #load to postgress
    load_df_postgres(load_df, conn_string, 'episodes')