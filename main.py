import sqlite3

def crear_conexion():
    #creo base de dato y conexion 
    try:
        conn = sqlite3.connect('gestion_biblioteca.db')
        cur = conn.cursor()
        return conn, cur
    
    except sqlite3.Error as error:
        print("Algo salió mal creando la conexion, revisá el codigo", error)

def cerrar_conexion(conn):
    conn.close()

#menu principal
def menu_principal():
    #Saludo principal
    print("Bienvenido a BookHub V.23.12."
          "\nMenú principal\n"
          "\nPor favor seleccioná una opcion: ")
    
    while True:
        
        #solicito opcion al usuario
        opcion = int(input(
                        "\n1. Libros"
                        "\n2. Lectores"
                        "\n3. Bibliotecarios"
                        "\n4. Acerca del sistema"
                        "\n5. Salir del programa"
                        "\n>>>"))
        
        if opcion == 1:
            menu_libros()
            break
                    
        elif opcion == 2:
            menu_lectores()
            break
                    
        elif opcion == 3:
            menu_bibliotecarios()
            break
                    
        elif opcion == 4:
            print("BookHub V.23.12")
            input("Presiona Enter para salir...")
            break

        elif opcion == 5:
            print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
            break 

        else:
            print("Por favor selecciona una opcion valida: ")
            continue

#DESDE AQUI LIBROS
#menu libros
def menu_libros():

    #saludo del menu
    print("**BookHub - MENU LIBROS **")
    print("")
    print("Por favor elegí una opcion: ")

    while True:
        #solicito opcion al usuario
        opcion = int(input(
                        "\n1. Registrar libro nuevo"
                        "\n2. Prestar libro"
                        "\n3. Devolver libro"
                        "\n4. Buscar Libro"
                        "\n5. Historial"
                        "\n6. Menu Principal"
                        "\n7. Salir del programa"                       
                        "\n>>>"))
        

        if opcion == 1:
            registrar_libro()
            break

        elif opcion == 2:
            prestar_libro()
            break
        
        elif opcion == 3:
            devolver_libro()
            break
            
        elif opcion == 4:
            buscar_libro()
            break
            
        elif opcion == 5:
            print("opcion aun no programada")
            break

        elif opcion == 6:
            menu_principal()
            break
        
        elif opcion == 7:
            print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
            break 
        else:
            print("Opcion invalida, por favor intentalo otra vez.")
            continue

#registrar libro
def registrar_libro():
    conn, cur = crear_conexion()

    #saludo incial del menu
    print("\nBookHub ---> REGISTRAR NUEVO LIBRO\n")

    #solicitar datos al usuario:
    titulo = input("Ingresá el titulo del libro: ")
    autor = input("Ingresa el nombre del autor: ")
    genero = input("Ingresá el género del libro: ")
    disponibles = int(input("¿Cuantos hay disponibles?: "))

    #almaceno los datos ingresados en la variable datos_libro
    datos_libro = (None,None,titulo,autor,genero,disponibles)

    #seteo la consulta SQL
    sql = "INSERT INTO libros VALUES (?,?,?,?,?,?)"

    #ejecuto la consulta
    try:
        cur.execute(sql,datos_libro)
        conn.commit()
        conn.close()
        print("El libro fue cargado exitosamente!")
        submenu_registrar_libro()
        return datos_libro
    except sqlite3.Error as e:
        print("no se cargo el libro, ",e)

#submenu registrar libro
def submenu_registrar_libro():
    
    #saludo incial del menu
    print("\nBookHub ---> SUBMENU REGISTRAR LIBRO\n")
    print("Por favor ingresá una opcion:")

    while True:
        opcion = int(input(
            ".1 Agregar otro libro"
            "\n.2 Menu principal"
            "\n.3 Menu libros"
            "\n.4 salir"
            "\n>>>"))
        

        if opcion == 1:
            registrar_libro()
            break
        
        elif opcion == 2:
            menu_principal()
            break
                
        elif opcion == 3:
            menu_libros()
            break
        
        elif opcion == 4:
            print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
            break 

        else:
            print("Por favor selecciona una opcion valida: ")
            continue

#prestar libro
def prestar_libro():
    #creo la conexion y cursor
    conn, cursor = crear_conexion()

    #saludo inicial menu
    print("\nBookHub ---> PRESTAR LIBRO\n")

    while True:
    
        #solicito datos al usuario
        dni_lector = input("Por favor ingresa el DNI del lector: ")
        titulo_libro = input("Por favor ingresa el titulo del libro: ")


        #convertir titulo a minusculas
        titulo_libro = titulo_libro.lower()

        #sentencia SELECT LIBRO
        sql_buscar_libro = """SELECT ID_libro FROM libros WHERE LOWER (titulo) = LOWER(?)"""

        #sentencia SELECT LECTOR
        sql_buscar_lector = """SELECT ID_lector FROM lectores WHERE dni = ?"""
        
        #ejecuto la consulta SELECT
        try:
            cursor.execute(sql_buscar_libro, (titulo_libro,))
            resultado_libro = cursor.fetchone()
                    
            if resultado_libro:
                print("ID de libro encontrado: ",resultado_libro[0])
            
            else: 
                print("Libro no encontrado, intentalo otra vez!")
                return None
        
        except sqlite3.Error as e:
            print("Algo no salió bien, llama al help desk y "
                "dales el sieguiente codigo de error: ", e)
            return None
        
        if resultado_libro:
            id_libro = resultado_libro[0]

            #restar cantidad DISPONIBLES
            sql_restar = """UPDATE libros SET disponibles = disponibles -1 WHERE ID_libro = ?"""
            
            #ejecutar SQL_RESTAR
            cursor.execute(sql_restar, (id_libro,))
            conn.commit()

        #buscar el ID_lector por DNI

            cursor.execute(sql_buscar_lector,(dni_lector,))
            resultado_lector = cursor.fetchone()
            
            if resultado_lector:
                id_lector = resultado_lector[0]
                

                # Asignar el libro prestado al lector actualizando 
                # el ID_libro en la tabla lectores
                sql_asignar_libro = """UPDATE lectores SET ID_libro = ? WHERE ID_lector = ?"""
                
                cursor.execute(sql_asignar_libro,(id_libro, id_lector))
                conn.commit()
                print("Se presto el libro: ", titulo_libro, " al lector: ", dni_lector,)
                print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
                break
            
            else:
                print("No se encontro el lector, por favor intentalo otra vez")
        else:
            print("no se encontro el libro, por favor intentalo otra vez.")
            break         

#devolver libro
def devolver_libro():
    conn, cursor = crear_conexion()

    #saludo inicial menu
    print("\nBookHub ---> DEVOLVER LIBRO\n")
    
    #pedir datos al usuario:
    dni_lector = int(input("Por favor ingresá el DNI del lector: "))
    titulo = input("Por favor ingresa el titulo del libro: ")

    #buscar lector por DNI:
    sql_buscar_lector = """SELECT ID_lector FROM lectores WHERE dni = ?"""

    #DESDE AQUI APARTADO PARA EL LIBRO    
    #convertir titulo a LOWER
    titulo = titulo.lower()

    #buscar titulo de libro
    sql_buscar_titulo = """SELECT ID_libro FROM libros WHERE LOWER (titulo) = LOWER (?) """

    #ejecutar CONSULTA LIBRO
    cursor.execute(sql_buscar_titulo, (titulo,))
    id_libro = cursor.fetchone()
    print("ID de libro: ", id_libro[0])

    #sumar DISPONIBLES
    sql_sumar = """UPDATE libros SET disponibles = disponibles +1 WHERE ID_libro = ?"""

    #ejecutar SENTENCIA DISPONIBLES
    try:
        cursor.execute(sql_sumar, id_libro)
        conn.commit()
    except sqlite3.Error as e:
        print("Algo salió mal, llama a Help Desk y dales el siguinte codigo de error: ",e)


    #DESDE AQUI APARTADO PARA EL LECTOR

    #SENTENCIA buscar LECTOR
    cursor.execute(sql_buscar_lector,(dni_lector,))
    id_lector = cursor.fetchone()

    #DES-ASIGNAR LIBRO AL LECTOR
    while True:
        if id_lector:
            if id_libro:
                sql_desasignar = """UPDATE lectores SET ID_libro = NULL WHERE ID_libro = ?"""

                #ejecutar SENTENCIA DESASINAR
                try:
                    cursor.execute(sql_desasignar, id_libro)
                    conn.commit()
                    print("Se devolvio el libro: ", titulo, " del usuario: ", dni_lector)
                    print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
                    break
                except sqlite3.Error as e:
                    print("Comunicate con HelpDesk y dales el siguiente codigo: ", e)

            else:
                print("No se encontró el libro, por favor intentalo otra vez.")
                break
        
        else:
            print("El lector no existe, por favor intenta nuevamente")
            
        break

#buscar libro
def buscar_libro():
    conn, cur = crear_conexion()
    print("\nBookHub ---> BUSCAR LIBRO\n")

    #solicitar datos al usuario:
    titulo = input("Ingresá el titulo del libro: ")
    
    #convertir titulo a minuscula
    titulo = titulo.lower()

    #Buscar ID con titulo
    sql_datos_titulo = """SELECT * FROM libros WHERE LOWER (titulo) = LOWER (?)"""

    #EJECUTAR CONSULTA
    cur.execute(sql_datos_titulo,(titulo,))
    id_libro = cur.fetchone()

    if id_libro:
        print("Los datos del libro son: ", id_libro)
    else:
        print("libro no encontrado")


#DESDE AQUI LECTORES
#menu lectores
def menu_lectores():
    print("\nBookHub ---> **MENU LECTORES**\n")
    print("")
    print("Por favor elegí una opcion: ")
    while True:
        opcion = int(input(
                       "\n1. Registrar lector nuevo"
                       "\n2. Modificar lector"
                       "\n3. Buscar lector"
                       "\n4. Ver historial"
                       "\n5. Menu Principal"
                       "\n6. Salir del programa"
                       "\n>>> "))

        if opcion == 1:
            registrar_lector()
            break

        if opcion == 2:
            modificar_lector()
            break
        
        if opcion == 3:
            buscar_lector()
            break
            
        if opcion == 4:
            print("opcion aun no programada")
            
        if opcion == 5:
            menu_principal()
            break

        if opcion == 6:
            print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
            break

        else:
            print("Opcion invalida, por favor intentalo otra vez.")
            continue        

#registrar lector
def registrar_lector():
    #creo conexion y cursor
    conn, cur = crear_conexion()

    #saludo incial menu
    print("\nBookHub ---> REGISTRAR NUEVO LECTOR\n")

    #solicitud de datos al usuario
    nombre = input("Ingresá el nombre: ")
    apellido = input("Ingresá el apellido: ")
    direccion = input("Ingresá la direccion: ")
    telefono = input("Ingresá el telefono: ")
    dni = input("Ingresá el DNI: ")
    email = input("Ingresá el correo electronico: ")
    
    #almaceno los datos ingresados en la variable "datos_usuario"
    datos_usuario = (None,None,nombre,apellido,direccion,telefono,dni,email)
    
    #almaceno consulta SQL
    sql = "INSERT INTO lectores VALUES (?,?,?,?,?,?,?,?)"
  

    try:
        #ejecuto la consulta
        cur.execute(sql,datos_usuario)
        conn.commit()

        #imprimo y retorno los resultados para ser reutilizados
        print("El lector ",nombre, " ", apellido, " fue agregado correctamente")
        
        #llamado al submenu_lectores
        submenu_registrar_lector()
        return nombre, apellido          
    
    except sqlite3.Error as e:
        #imprimo y retorno los resultados para ser reutilizados
        print("Ocurrio un error al registrar el lector. Llama al Help Desk y dales el siguiente "
            "codigo de error: ", e)
        return e
    
    finally:
        #cierro la conexion
        conn.close

#submenulectores
def submenu_registrar_lector():
    
    #saludo incial menu
    print("\nBookHub --->SUBMENU REGISTRAR NUEVO LECTOR\n")
    print("Por favor seleccioná una opcion:")
    
    while True:

        #almaceno la seleccion del usuario
        opcion = int(input(
                        "\n.1 Agregar otro lector"
                        "\n.2 Ir a Menu lectores"
                        "\n.3 Ir al Menu Principal"
                        "\n.4 Salir del programa"
                        "\n>>>"
                        ))
        
        if opcion == 1:
            registrar_lector()

        elif opcion == 2:
            menu_lectores()
        
        elif opcion == 3:
            menu_principal()
        
        elif opcion == 4:
            print(
                "Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!"
                )
            break 
    
        else:
            print(
                "Por favor selecciona una opcion valida: "
                  )
        continue   

#buscar lector
def buscar_lector():
    conn, cursor = crear_conexion()
    
    #mensaje de bienvenida
    print("\nBookHub ---> **BUSCAR LECTOR**\n")
    while True:
        

        #solicitud datos
        dni_lector = int(input("Por favor ingresa el DNI del lector: "))

        #sentencia SQL
        sql_buscar_lector = """SELECT * FROM lectores WHERE dni = ?"""

        #ejecutar BUSCAR LECTOR
        try:
            cursor.execute(sql_buscar_lector,(dni_lector,))
            #almacenar el resultado
            resultado_lector = cursor.fetchone()

            if resultado_lector: 
                #imprimir RESULTADO
                print("Los datos del lector en busqueda son: ", resultado_lector)
                submenu_buscar_lector()
                            
            else:
                print("El usuario ingresado no existe, por favor volvé a intentarlo: ")
                buscar_lector()
        
        except sqlite3.Error as e:
            print("Algo no salio bien, llamá al HelpDesk y dales el siguiente codigo de error: ", e)

        
        finally:
            conn.close()
        break

#submenu buscar lector
def submenu_buscar_lector():

    #saludo incial menu
    print("\nBookHub --->SUBMENU BUSCAR LECTOR\n")
    print("Por favor seleccioná una opcion:")

    while True:
        opcion = int(input(
            "\n1. Buscar otro lector"
            "\n2. Ir al menu principal"
            "\n3. Ir al menu lectores"
            "\n4. Salir del programa"
            "\n>>>"
            ))
        
        if opcion == 1:
            buscar_lector()
            break

        elif opcion == 2:
            menu_principal()
            break

        elif opcion == 3:
            menu_lectores()
            break

        elif opcion == 4:
            print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
            break

        else:
            print("Por favor intentalo otra vez: ")
            continue

#modificar lector
def modificar_lector():
    conn, cur = crear_conexion()

    #mensaje de bienvenida
    print("\nBookHub ---> **MODIFICAR LECTOR**\n")

    while True:

        #solicitud al usuario
        dni_viejo = int(input("Por favor ingresa el DNI anterior del lector: "))
        dni_nuevo =int(input("Ahora ingresa el DNI nuevo: "))

        #Sentencias SQL
        sql_modificar_lector = """UPDATE lectores SET dni = ? WHERE dni = ?"""
        sql_mostrar_cambios = """SELECT * FROM lectores WHERE dni = ?"""

        #EJECUTAR SQL MODIFICAR
        try:
            cur.execute(sql_modificar_lector, (dni_nuevo, dni_viejo,))
            conn.commit()

            #EJECUTAR SQL MOSTRAR NUEVO DNI
            try:
                cur.execute(sql_mostrar_cambios, (dni_nuevo,))
                #almacenar resultados
                resultados_cambio_lector = cur.fetchone()
                
                if resultados_cambio_lector[6] == dni_nuevo:
                    #imprimir resultados
                    print("Se modificó el lector, estos son los datos actuales: \n", resultados_cambio_lector)
                    submenu_modificar_lector()
                    break

                else:
                    print("no se realizo el cambio solicitado.\n")
                    modificar_lector()
            
            except sqlite3.Error as e:
                print("Algo no salio bien, llama a HelpDesk y dales el siguiente mensaje de error: ",e)


        except sqlite3.Error as e:
            print("Algo no salio bien, llama a HelpDesk y dales el siguiente mensaje de error: ",e)

        finally:
            conn.close()
            break
        
#submenu modificar lector
def submenu_modificar_lector():

    #saludo incial menu
    print("\nBookHub ---> **SUBMENU MODIFICAR LECTOR**\n")
    print("Por favor ingresa una opcion: ")

    while True:
        #solicitar opcion al usuario
        opcion = int(input(            
                        "\n1. Modificar otro lector"
                        "\n2. Ir al menu principal"
                        "\n3. Ir al menu lectores"
                        "\n4. Salir del programa"
                        "\n>>>"
                        ))
        
        if opcion == 1:
            modificar_lector()
            break

        elif opcion == 2:
            menu_principal()
            break

        elif opcion == 3:
            menu_lectores()
            break
            

        elif opcion == 4:
            print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
            break 



#DESDE AQUI BIBLIOTECARIOS
#menu bibliotecarios        
def menu_bibliotecarios():

    #saludo inicial menu
    print("\nBookHub ---> **MENU BIBLIOTECARIOS**\n")
    print("")
    print("Por favor elegí una opcion: ")
    while True:    
        
        #solicito opcion al usuario
        opcion = int(input(
                       "\n1. Registrar bibliotecario nuevo"
                       "\n2. Buscar bibliotecario"
                       "\n3. Modificar bibliotecario"
                       "\n4. Eliminar bibliotecario"
                       "\n5. Menu Principal"
                       "\n6. Salir del programa"
                       "\n>>>"
                       ))
    


        if opcion == 1:
            registrar_bibliotecario()
            break
        
        elif opcion == 2:
            buscar_bibliotecario()
            break

        elif opcion == 3:
            modificar_biblio()
            break

        elif opcion == 4:
            eliminar_bibliotecario()
            break

        elif opcion == 5:
            menu_principal()
            break

        if opcion == 6:
            print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
            break
        
        else:
            print("Opcion invalida, por favor intentalo otra vez.")
            continue      

#registrar bibliotecario
def registrar_bibliotecario():
    #creo conexion y cursor
    conn, cursor = crear_conexion()

    #saludo inicial menu
    print("\nBookHub ---> *CREAR BIBLIOTECARIO**\n")

    while True:
        #solicitar los datos al usuario:
        nombre = input("Ingresá el nombre del bibliotecario nuevo: ")
        apellido = input("Ingresá el apellido del nuevo bibliotecario: ")
        telefono = (input("Ingresá el telefono del nuevo bibliotecario: "))
        email = input("Ingresá el correo electronico del nuevo bibliotecario: ")

        #almaceno los datos solicitados
        datos_bibliotecario = (None, nombre, apellido, telefono, email)

        #almaceno consulta SQL
        sql = "INSERT INTO bibliotecarios VALUES(?,?,?,?,?)"

        try:
            #ejecuto la consulta:
            cursor.execute(sql, datos_bibliotecario)
            conn.commit()

            #imprimo resultados y restorno para ser reutilizados
            print("El bibliotecario", nombre, " ",apellido, " fue registrado correctamente")
        
        except sqlite3.Error as e:
            print("Algo salió mal, comunicate con HelpDesk y dales el siguiente codigo: ",e)

        finally:
            conn.close()
            break     

#submenu  REGISTRAR bibliotecario
def submenu_bibliotecario():
    while True:
        print("\nBookHub ---> **SUBMENU REGISTRAR BIBLIOTECARIO**\n")
        print("Por favor selecciona una opcion: ")
        opcion = int(input(
                "\n1.Registrar otro bibliotecario"
                "\n2.Menu bibliotecarios"
                "\n3.Menu principal"
                "\n4.salir"
                "\n>>> "))
  
        if opcion == 1:
            registrar_bibliotecario()
            break

        elif opcion ==2:
            menu_bibliotecarios()
            break

        elif opcion == 3:
            menu_principal()
            break

        elif opcion == 4:
            print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
            break 
        
        else:
            print("Por favor selecciona una opcion valida: "
                  )
            continue

#buscar bibliotecario
def buscar_bibliotecario():
    conn, cur = crear_conexion()

    #saludo inicial menu
    print("\nBookHub ---> **MENU BUSCAR BIBLIOTECARIO**\n")
    print("")

    while True:
        #solicitud datos al usuario
        nombre = input("Por favor ingresa el nombre del bibliotecario: ")
        apellido = input("Ahora ingresa el apellido del bibliotecario: ")

        #convertir datos a minusculas
        nombre = nombre.lower()
        apellido = apellido.lower()

        #sentencia consulta SQL
        sql_buscar_bibliotecario = """SELECT * FROM bibliotecarios WHERE nombre = LOWER(?) AND apellido = LOWER(?)"""

        #EJECUTAR sql
        try:
            cur.execute(sql_buscar_bibliotecario, (nombre, apellido))
            resultado_bibliotecario = cur.fetchall()

            #chequear resultados para imprimirlos
            if resultado_bibliotecario:
                print("Los datos del bibliotecario son: ", resultado_bibliotecario)
                submenu_buscar_biblio()
                break
            
            else:
                print("El bibliotecario ingresado no existe, por favor intentalo otra vez.")
                buscar_bibliotecario()
                break
        
        except sqlite3.Error as e:
            print("BookHub tuvo un error buscando el bibliotecario, comunicate "
                "con HelpDesk y dales el siguiente codigo: ",e)
        
        finally:
            conn.close()
            break
    
#submenu BUSCAR bibliotecario
def submenu_buscar_biblio():

    #saludo incial menu
    print("\nBookHub --->SUBMENU BUSCAR BIBLIOTECARIO\n")
    print("Por favor seleccioná una opcion:")

    while True:
        opcion = int(input(
            "\n1. Buscar otro bibliotecario"
            "\n2. Ir al menu principal"
            "\n3. Ir al menu bibliotecarios"
            "\n4. Salir del programa"
            "\n>>>"
            ))
        
        if opcion == 1:
            buscar_bibliotecario()
            break

        elif opcion == 2:
            menu_principal()
            break

        elif opcion == 3:
            menu_bibliotecarios()
            break

        elif opcion == 4:
            print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
            break

        else:
            print("Por favor intentalo otra vez: ")
            continue

#modificar bibliotecario
def modificar_biblio():
    conn, cur = crear_conexion()

    #saludo inicial menu
    print("\nBookHub ---> **MENU MODIFICAR BIBLIOTECARIO**\n")
    print("")

    while True:
        #solicitud datos
        nombre = input("Por favor ingresá el nombre del bibliotecario: ")
        apellido = input("Por favor ingresá el apellido del bibliotecario: ")
        telefono = int(input("Por favor ingresa el nuevo numero telefonico: "))

        #cambiar datos ingresados a minuscula
        nombre = nombre.lower()
        apellido = apellido.lower()

        #sentencia SQL
        sql_modifcar_biblio = """UPDATE bibliotecarios SET telefono = ? WHERE nombre = LOWER(?) AND apellido = LOWER(?)"""

        #EJECUTAR sentencia
        try:
            cur.execute(sql_modifcar_biblio, (telefono, nombre, apellido))
            conn.commit()

        except sqlite3.DatabaseError as e:
            print("Algo salió mal, cominicate con HelpDesk y dales el siguiente codigo: ",e)
        
        #sentencia SQL mostrar cambios
        sql_mostrar_cambios = """SELECT * FROM bibliotecarios WHERE nombre = LOWER(?) AND apellido = (?)"""

        #EJECUTAR SQL
        try:
            cur.execute(sql_mostrar_cambios, (nombre, apellido ))
            resultado_cambio_biblio = cur.fetchall()

            if resultado_cambio_biblio:
                print("Se realizo la modificacion en el bibliotecario ", nombre, apellido)
                print("Los nuevos datos del bibliotecario son: ", resultado_cambio_biblio)
                submenu_modificar_biblio()
                break                    
            
            else:
                print("No se realizo ningun cambio")
        
        except sqlite3.DatabaseError as e:
            print("Algo salió mal, cominicate con HelpDesk y dales el siguiente codigo: ",e)

#submenu MODIFICAR bibliotecario
def submenu_modificar_biblio():

    #saludo incial menu
    print("\nBookHub --->SUBMENU MODIFICAR BIBLIOTECARIO\n")
    print("Por favor seleccioná una opcion:")

    while True:
        opcion = int(input(
            "\n1. MODIFICAR otro bibliotecario"
            "\n2. Ir al menu principal"
            "\n3. Ir al menu bibliotecarios"
            "\n4. Salir del programa"
            "\n>>>"
            ))
        
        if opcion == 1:
            modificar_biblio()
            break

        elif opcion == 2:
            menu_principal()
            break

        elif opcion == 3:
            menu_bibliotecarios()
            break

        elif opcion == 4:
            print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
            break

        else:
            print("Por favor intentalo otra vez: ")
            continue

#eliminar bibliotecario
def eliminar_bibliotecario():

    #cursor y conexion
    conn, cur = crear_conexion()

    while True:
        #solicitud de datos al usuario
        nombre = input(
            "Por favor ingresa el nombre del bibliotecario que deseas eliminar: "
        )
        
        apellido = input(
            "Ahora ingresá el apellido del bibliotecario: "
        )

        #convertir datos a minuscula
        nombre = nombre.lower()
        apellido = apellido.lower()

        #secuencia SQL
        sql_eliminar_biblio = """DELETE FROM bibliotecarios WHERE nombre = LOWER(?) AND apellido = LOWER(?);"""

        #EJECUTAR sentencia SQL
        try:
            cur.execute(sql_eliminar_biblio, (nombre, apellido))
            conn.commit()
            print("Se eliminó el bibliotecario: ",nombre, apellido,".")
            submenu_eliminar_biblio()
            
        
        except sqlite3.Error as e:
            print("Algo salio mal, comunicate con HelpDesk y dales el siguiente codigo: ",e)
        
        finally:
            conn.close()
            break

#submenu ELIMINAR bibliotecario
def submenu_eliminar_biblio():

    #saludo incial menu
    print("\nBookHub --->SUBMENU ELIMINAR BIBLIOTECARIO\n")
    print("Por favor seleccioná una opcion:")

    while True:
        opcion = int(input(
            "\n1. ELIMINAR otro bibliotecario"
            "\n2. Ir al menu principal"
            "\n3. Ir al menu bibliotecarios"
            "\n4. Salir del programa"
            "\n>>>"
            ))
        
        if opcion == 1:
            eliminar_bibliotecario()
            break

        elif opcion == 2:
            menu_principal()
            break

        elif opcion == 3:
            menu_bibliotecarios()
            break

        elif opcion == 4:
            print("Muchas gracias por utilizar BookHub V.23.12, te esperamos la proxima!")
            break

        else:
            print("Por favor intentalo otra vez: ")
            continue
        
menu_principal()