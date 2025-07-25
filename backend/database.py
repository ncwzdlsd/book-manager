import pymysql
from pymysql.cursors import DictCursor

# データベース設定
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "111111",
    "database": "library-all",
    "charset": "utf8mb4",
    "cursorclass": DictCursor
}

def get_db_connection():
    """データベース接続を取得"""
    return pymysql.connect(**DB_CONFIG)

def execute_query(query, params=None):
    """クエリを実行して結果を返す"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
    finally:
        conn.close()

def execute_single_query(query, params=None):
    """クエリを実行して単一の結果を返す"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result
    finally:
        conn.close()

def execute_update(query, params=None):
    """更新操作を実行"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
            # 影響を受けた行数を返す（lastrowidではなく）
            return cursor.rowcount
    finally:
        conn.close() 