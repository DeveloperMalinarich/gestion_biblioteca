#importo libreria
import sqlite3


def crear_conexion():
    #creo base de dato y conexion 
    try:
        conn = sqlite3.connect('gestion_biblioteca.db')
        cur = conn.cursor()
        return conn, cur
    
    except sqlite3.Error as error:
        print("Algo salió mal creando la conexion, revisá el codigo", error)

def crear_tablas():
    #creo variables que llaman a "crear_conexion"
    conn, cur = crear_conexion()

    #creo variable de script de ejecucion SQL
    sql = """
    CREATE TABLE IF NOT EXISTS libros
    (
        ID_libro INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_lector INTEGER,
        titulo VARCHAR(20) NOT NULL,
        autor VARCHAR(20) NOT NULL,
        genero VARCHAR(20) NOT NULL,
        disponibles INTEGER NOT NULL,
        FOREIGN KEY(ID_lector) REFERENCES lectores(ID_lector)
    ); 

    CREATE TABLE IF NOT EXISTS bibliotecarios
    (
        ID_bibliotecario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(20) NOT NULL,
        apellido VARCHAR(20) NOT NULL,
        telefono INTEGER NOT NULL,
        email VARCHAR(20) NOT NULL
    ); 
    
    CREATE TABLE IF NOT EXISTS lectores
    (
        ID_lector INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(20) NOT NULL,
        apellido VARCHAR(20) NOT NULL,
        direccion VARCHAR(20) NOT NULL,
        telefono INTEGER NOT NULL,
        dni INTEGER UNIQUE NOT NULL,
        email VARCHAR(20) NOT NULL,
        ID_libro INTEGER,
        titulo VARCHAR(20),
        FOREIGN KEY (ID_libro) REFERENCES libros(ID_libro)
    );
    """

    try:
        cur.executescript(sql)
        print("Se crearon las tablas correctamente !")
        conn.commit()

    except Exception as e:
        print("Algo salio mal: ",e)
    
    finally:
        conn.close()

crear_conexion()

crear_tablas()

