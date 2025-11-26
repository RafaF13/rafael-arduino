import psycopg2
import os

def get_connection():
    return psycopg2.connect(host=os.environ.get("DB_HOST"), database=os.environ.get("DB_NAME"), user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASSWORD"))

def get_data_field(field, limit):

    data = []
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Ordenar do mais antigo para o mais e recente e obter as primeiras 10 linhas
                # e dps voltar a ordenar do mais antigo para o mais recent
                cur.execute("SELECT * FROM (SELECT * FROM arduino_data WHERE field = %s ORDER BY date_time DESC LIMIT %s) AS dados_desc ORDER BY date_time ASC", [field, limit])
                for tuple in cur.fetchall():
                    reg = {
                        "id": tuple[0],
                        "field": tuple[1],
                        "value": tuple[2],
                        "date_time": tuple[3].strftime("%m-%d %H:%M")
                    }
                    data.append(reg)
                    
    except (Exception, psycopg2.Error) as error:
        pass
    finally:
        if(conn):
            cur.close()
            conn.close()

    return data


def get_arduino_info():

    info = {}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, current_field, temp_max_value, temp_min_value, temp_measures_30s, dist_max_value, dist_min_value, dist_measures_30s FROM arduino_info")
                tuple = cur.fetchone()
                info = {
                    "id": tuple[0],
                    "current_field": tuple[1],
                    "temp_max_value": tuple[2],
                    "temp_min_value": tuple[3],
                    "temp_measures_30s": tuple[4],
                    "dist_max_value": tuple[5],
                    "dist_min_value": tuple[6],
                    "dist_measures_30s": tuple[7]
                }
                    
    except (Exception, psycopg2.Error) as error:
        pass
    finally:
        if(conn):
            cur.close()
            conn.close()

    return info

def get_field_stats(field):

    info = {}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*), ROUND(AVG(value), 2), MAX(value), MIN(value) FROM arduino_data WHERE field = %s", [field])
                tuple = cur.fetchone()
                info = {
                    "count": tuple[0],
                    "avg": tuple[1],
                    "max": tuple[2],
                    "min": tuple[3]
                }
                    
    except (Exception, psycopg2.Error) as error:
        pass
    finally:
        if(conn):
            cur.close()
            conn.close()

    return info


def insert_data(data):
    
    status = True
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO arduino_data (field, value, date_time) VALUES (%s, %s, NOW())", [data["field"], data["value"]])
    except (Exception, psycopg2.Error) as error:
        status = error
    finally:
        if(conn):
            cur.close()
            conn.close()
    
    return status


def update_arduino_info(data):

    status = True
    # este json apenas vai ter um param
    # a key do json vai ser a coluna a atualizar
    # e o valor da key vai ser o novo valor a atualizar
    column = list(data.keys())[0] 
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE arduino_info SET " + column + " = %s WHERE id = 1", [data[column]])
    except (Exception, psycopg2.Error) as error:
        status = error
    finally:
        if(conn):
            cur.close()
            conn.close()
    
    return status
