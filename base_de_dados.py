import mysql.connector

def get_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='dudu1605',
        database='trabalho_bd',
        buffered=True,
        charset='utf8mb4'
    )
    return conn

def testar_conexao():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        print("Conexão bem-sucedida!")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return False

if __name__ == "__main__":
    testar_conexao()