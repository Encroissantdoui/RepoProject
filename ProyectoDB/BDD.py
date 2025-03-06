import sqlite3

def creartablas():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;") #forzar restricciones
    
    conexion.execute("""
        CREATE TABLE `Alumnes` (
            `AlumneID` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Nombre` TEXT NOT NULL,
            `Telefono` INTEGER,
            `Direccion` TEXT NOT NULL
            );
    """)

    conexion.execute("""
        CREATE TABLE `Autores` (
            `AutorId` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Nombre` TEXT NOT NULL
            );
    """)

    conexion.execute("""
        CREATE TABLE `Libros` (
            `LibroId` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Titulo` TEXT NOT NULL,
            `ISBN` INTEGER NOT NULL,
            `Editorial` TEXT NOT NULL,
            `Paginas` INTEGER
            );
    """)

    conexion.execute("""
        CREATE TABLE `Ejemplares` (
            `EjemplarId` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Localizacion` TEXT NOT NULL,
            `LibroId` INTEGER NOT NULL,
            FOREIGN KEY (`LibroId`) REFERENCES `Libros` (`LibroId`)
            ON UPDATE RESTRICT ON DELETE RESTRICT
            );
    """)

    conexion.execute("""
        CREATE TABLE `Escribe` (
            `EscribeId` INTEGER PRIMARY KEY AUTOINCREMENT,
            `AutorId` INTEGER NOT NULL,
            `LibroId` INTEGER NOT NULL,
            FOREIGN KEY (`AutorId`) REFERENCES `Autores` (`AutorId`)
            ON UPDATE RESTRICT ON DELETE RESTRICT,
            FOREIGN KEY (`LibroId`) REFERENCES `Libros` (`LibroId`)
            ON UPDATE RESTRICT ON DELETE RESTRICT
            );
    """)

    conexion.execute("""
        CREATE TABLE `Saca` (
            `PrestamoId` INTEGER PRIMARY KEY AUTOINCREMENT,
            `EjemplarId` INTEGER NOT NULL,
            `AlumneId` INTEGER NOT NULL,
            `FechaPrestamo` DATE NOT NULL,
            `FechaDevolucion` DATE NOT NULL,
            `HoraDevolucion` DATE,
            FOREIGN KEY (`EjemplarId`) REFERENCES `Ejemplares` (`EjemplarId`)
            ON UPDATE RESTRICT ON DELETE RESTRICT,
            FOREIGN KEY (`AlumneId`) REFERENCES `Alumnes` (`AlumneID`)
            ON UPDATE RESTRICT ON DELETE RESTRICT
            );
    """)


    conexion.commit()
    conexion.close()

def menu_de_gestion():
    while True:
        print("\nGestor Biblioteca")
        print("1. Gestion de libros")
        print("2. Gestion de personas")
        print("3. Gestion de prestamos")
        print("4. Gestion de autores")
        print("5. Gestion de ejemplares")
        print("6. Gestion de escribe")
        print("7. Lista de operaciones")
        print("8. Exit")
        choice = input("Enter: ")

        if choice == '1':
            gestion_libros()
        elif choice == '2':
            gestion_alumnos()
        elif choice == '3':
            gestion_saca()
        elif choice == '4':
            gestion_autores()
        elif choice == '5':
            gestion_ejemplares()
        elif choice == '6':
            gestion_escribe()
        elif choice == '7':
            lista_de_operaciones()
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalido")


def gestion_escribe():
    print("\nGestion de escribe")
    print("1. Suprimir escribe")
    print("2. Regresa")
    choice = input("Enter: ")

    if choice == '1':
        suprimir_escribe()
    elif choice == '2':
        print("Saliendo")
    else:
        print("Invalido")

def suprimir_escribe():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    nombre_autor = input("Introduce el nombre del autor: ")
    cursor.execute("""
        SELECT Autores.AutorId, Autores.Nombre
        FROM Autores
        WHERE Autores.Nombre = ?
    """, (nombre_autor,))
    autor = cursor.fetchone()
    if autor:
        autor_id = autor[0]
        cursor.execute("""
            SELECT Escribe.EscribeId, Libros.Titulo
            FROM Escribe
            JOIN Libros ON Escribe.LibroId = Libros.LibroId
            WHERE Escribe.AutorId = ?
        """, (autor_id,))
        escribe_list = cursor.fetchall()
        if escribe_list:
            for row in escribe_list:
                print(f"Escribe ID: {row[0]}, Titulo: {row[1]}")

                # f string para insercion directa

            escribe_id = input("Introduce el ID del escribe a eliminar: ")
            cursor.execute("DELETE FROM Escribe WHERE EscribeId = ?", (escribe_id,))
            conexion.commit()
            print("eliminado.")
        else:
            print("No se encontraron.")
    else:
        print("No se encontro un autor con ese nombre.")
    conexion.close()

def gestion_libros():
    print("\nGestion de libros")
    print("1. Nuevas copias de libros")
    print("2. Suprimir libros")
    print("3. Regresa a menu")
    choice = input("Enter: ")

    if choice == '1':
        nuevos_libros()
    elif choice == '2':
        suprimir_libros()
    elif choice == '3':
        print("Regresando")
    else:
        print("Invalido")

def nuevos_libros():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    titulo = input("Titulo: ")
    isbn = input("ISBN: ")
    editorial = input("Editorial: ")
    paginas = input("Paginas: ")
    autor_nombre = input("Nombre del autor: ")
    localizacion = input("Introduce la localización del ejemplar: ")

    cursor.execute("INSERT INTO Libros (Titulo, ISBN, Editorial, Paginas) VALUES (?, ?, ?, ?)", (titulo, isbn, editorial, paginas))
    libro_id = cursor.lastrowid

    cursor.execute("SELECT AutorId FROM Autores WHERE Nombre = ?", (autor_nombre,))
    autor = cursor.fetchone()
    if autor:
        autor_id = autor[0]
    else:
        cursor.execute("INSERT INTO Autores (Nombre) VALUES (?)", (autor_nombre,))
        autor_id = cursor.lastrowid

    cursor.execute("INSERT INTO Escribe (AutorId, LibroId) VALUES (?, ?)", (autor_id, libro_id))
    cursor.execute("INSERT INTO Ejemplares (Localizacion, LibroId) VALUES (?, ?)", (localizacion, libro_id))

    conexion.commit()
    conexion.close()
    print("Nuevo libro y ejemplar incorporados.")

def suprimir_libros():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    titulo = input("Introduce el titulo del libro a eliminar (Asegurar que el ejemplar esta eliminado primero): ")
    cursor.execute("SELECT LibroId, Titulo FROM Libros WHERE Titulo = ?", (titulo,))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, titulo: {row[1]}")
        libro_id = input("Introduce el ID del libro a eliminar: ")
        cursor.execute("DELETE FROM Libros WHERE LibroId = ?", (libro_id,))
        conexion.commit()
        print("Libro eliminado.")
    else:
        print("No se encontraron libros con ese titulo.")
    conexion.close()

    #REVIEWED

def gestion_alumnos():
    print("\ngestion de miembros")
    print("1. incorporar nuevos miembros")
    print("2. eliminar miembros")
    print("3. regresar al menu")
    choice = input("Enter: ")

    if choice == '1':
        nuevos_alumnos()
    elif choice == '2':
        suprimir_alumnos()
    elif choice == '3':
        print("Saliendo")
    else:
        print("Invalido")

def nuevos_alumnos():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    nombre = input("nombre del miembro: ")
    telefono = input("telefono del miembro: ")
    direccion = input("direccion del miembro: ")
    cursor.execute("INSERT INTO Alumnes (Nombre, Telefono, Direccion) VALUES (?, ?, ?)", (nombre, telefono, direccion))
    conexion.commit()
    conexion.close()
    print("nuevo miembro incorporado")

def suprimir_alumnos():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    nombre = input("Introduce el nombre del miembro: ")
    cursor.execute("SELECT AlumneID, Nombre FROM Alumnes WHERE Nombre = ?", (nombre,))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, Nombre: {row[1]}")
        alumne_id = input("Introduce el ID del miembro: ")
        cursor.execute("DELETE FROM Alumnes WHERE AlumneID = ?", (alumne_id,))
        conexion.commit()
        print("Miembro eliminado.")
    else:
        print("No se encontraron.")
    conexion.close()                                    


def gestion_saca():
    print("\ngestion de prestamos")
    print("1. registrar nuevo prestamo")
    print("2. registrar devolucion")
    print("3. suprimir saca")
    print("4. regresar al menu principal")
    choice = input("Enter: ")

    if choice == '1':
        nueva_saca()
    elif choice == '2':
        retorno()
    elif choice == '3':
        suprimir_saca()
    elif choice == '4':
        print("Saliendo")
    else:
        print("Invalido")

def nueva_saca():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    ejemplar_id = input("Introduce el ID del ejemplar (Si no sabes, utiliza lista de operaciones donde puedes buscar los libros disponibles): ")
    nombre_alumno = input("Introduce el nombre del miembro: ")
    cursor.execute("SELECT AlumneID FROM Alumnes WHERE Nombre = ?", (nombre_alumno,))
    alumno = cursor.fetchone()
    if alumno:
        alumne_id = alumno[0]
        fecha_prestamo = input("Introduce la fecha de prestamo (YYYY-MM-DD): ")
        fecha_devolucion = input("Introduce la fecha de devolución (YYYY-MM-DD): ")
        cursor.execute("INSERT INTO Saca (EjemplarId, AlumneId, FechaPrestamo, FechaDevolucion) VALUES (?, ?, ?, ?)", (ejemplar_id, alumne_id, fecha_prestamo, fecha_devolucion))
        conexion.commit()
        print("Nuevo prestamo registrado.")
    else:
        print("No se encontro un miembro con ese nombre.")
    
    conexion.close()

def retorno():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    
    ejemplar_id = input("Introduce el ID del ejemplar para registrar la devolución: ")
    
    cursor.execute("""
        SELECT Saca.PrestamoId
        FROM Saca
        WHERE EjemplarId = ? AND HoraDevolucion IS NULL
    """, (ejemplar_id,))
    
    results = cursor.fetchall()
    
    if results:
        for row in results:
            print(f"Prestamo ID: {row[0]}")
        
        prestamo_id = input("Introduce el ID del prestamo para registrar la devolución: ")
        hora_devolucion = input("Introduce la hora de devolución (YYYY-MM-DD): ")
        
        cursor.execute("UPDATE Saca SET HoraDevolucion = ? WHERE PrestamoId = ?", (hora_devolucion, prestamo_id))
        conexion.commit()
        print("Devolucion registrada.")
    else:
        print("No se encontraron prestamos pendientes para ese ejemplar.")
    
    conexion.close()

def libro_saca():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT Ejemplares.*
        FROM Ejemplares
        JOIN Saca ON Ejemplares.EjemplarId = Saca.EjemplarId
        WHERE Saca.HoraDevolucion IS NULL
    """)
    results = cursor.fetchall()
    for row in results:
        print("ID", row)
    conexion.close()

def alumnos_saca():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT Alumnes.*
        FROM Alumnes
        JOIN Saca ON Alumnes.AlumneID = Saca.AlumneId
        WHERE Saca.HoraDevolucion IS NULL
    """)
    results = cursor.fetchall()
    for row in results:
        print("ID", row)
    conexion.close()

def libros_no_saca():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT * FROM Ejemplares
        WHERE EjemplarId NOT IN (SELECT EjemplarId FROM Saca)
    """)
    results = cursor.fetchall()
    for row in results:
        print("ID", row)
    conexion.close()

def libros_mas_saca():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT Libros.Titulo, COUNT(Saca.EjemplarId) AS LoanCount
        FROM Libros
        JOIN Ejemplares ON Libros.LibroId = Ejemplares.LibroId
        JOIN Saca ON Ejemplares.EjemplarId = Saca.EjemplarId
        GROUP BY Libros.Titulo
        ORDER BY LoanCount DESC
    """)
    results = cursor.fetchall()
    for row in results:
        print(row)
    conexion.close()

    #REVIEWED SECTION ABOVE 2

def libros_disponibles():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT Ejemplares.EjemplarId, Ejemplares.Localizacion, Libros.Titulo
        FROM Ejemplares
        JOIN Libros ON Ejemplares.LibroId = Libros.LibroId
        WHERE Ejemplares.EjemplarId NOT IN (SELECT EjemplarId FROM Saca WHERE HoraDevolucion IS NULL)
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"ID: {row[0]}, Titulo: {row[2]}, Localizacion: {row[1]}")
    conexion.close()

def buscar_libros_por_localizacion():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    localizacion = input("Enter localizacion: ")
    cursor.execute("""
        SELECT Ejemplares.EjemplarId, Libros.Titulo, Ejemplares.Localizacion
        FROM Ejemplares
        JOIN Libros ON Ejemplares.LibroId = Libros.LibroId
        WHERE Ejemplares.Localizacion = ?
    """, (localizacion,))
    results = cursor.fetchall()
    for row in results:
        print(f"Ejemplar ID: {row[0]}, Titulo: {row[1]}, Localizacion: {row[2]}")
    conexion.close()

def gestion_autores():
    print("\nGestion Autores")
    print("1. Nuevos autores")
    print("2. Suprimir autores")
    print("3. Regresa")
    choice = input("Enter: ")

    if choice == '1':
        nuevos_autores()
    elif choice == '2':
        suprimir_autores()
    elif choice == '3':
        print("Saliendo")
    else:
        print("Invalido")

def nuevos_autores():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    nombre = input("Nombre Autor: ")
    cursor.execute("INSERT INTO Autores (Nombre) VALUES (?)", (nombre,))
    conexion.commit()
    conexion.close()
    print("Incorporado")

def suprimir_autores():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    nombre = input("Introduce el nombre del autor a eliminar: ")
    cursor.execute("SELECT AutorId, Nombre FROM Autores WHERE Nombre = ?", (nombre,))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, Nombre: {row[1]}")
        autor_id = input("Introduce el ID del autor a eliminar: ")
        cursor.execute("DELETE FROM Autores WHERE AutorId = ?", (autor_id,))
        conexion.commit()
        print("Autor eliminado.")
    else:
        print("No se encontraron.")
    conexion.close()

def gestion_ejemplares():
    print("\nGestion de ejemplares")
    print("1. Suprimir ejemplares")
    print("2. Regresa a menu")
    choice = input("Enter: ")

    if choice == '1':
        suprimir_ejemplares()
    elif choice == '2':
        print("Regresando")
    else:
        print("Invalido")

def suprimir_ejemplares():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    titulo = input("Introduce el titulo del libro del ejemplar a eliminar: ")
    cursor.execute("""
        SELECT Ejemplares.EjemplarId, Libros.Titulo, Ejemplares.Localizacion
        FROM Ejemplares
        JOIN Libros ON Ejemplares.LibroId = Libros.LibroId
        WHERE Libros.Titulo = ?
    """, (titulo,))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, titulo: {row[1]}, Localización: {row[2]}")
        ejemplar_id = input("Introduce el ID del ejemplar a eliminar: ")
        cursor.execute("DELETE FROM Ejemplares WHERE EjemplarId = ?", (ejemplar_id,))
        conexion.commit()
        print("Ejemplar eliminado.")
    else:
        print("No se encontraron ejemplares con ese titulo.")
    conexion.close()


def suprimir_saca():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    nombre_alumno = input("Introduce el nombre del alumno: ")
    cursor.execute("""
        SELECT Saca.PrestamoId, Ejemplares.Localizacion, Saca.FechaPrestamo, Saca.FechaDevolucion, Saca.HoraDevolucion
        FROM Saca
        JOIN Alumnes ON Saca.AlumneId = Alumnes.AlumneID
        JOIN Ejemplares ON Saca.EjemplarId = Ejemplares.EjemplarId
        WHERE Alumnes.Nombre = ?
    """, (nombre_alumno,))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"Prestamo ID: {row[0]}, Localizacion: {row[1]}, Fecha Prestamo: {row[2]}, Fecha Devolucion: {row[3]}, Hora devolucion: {row[4]}")
        prestamo_id = input("Introduce el ID del prestamo a eliminar: ")
        cursor.execute("DELETE FROM Saca WHERE PrestamoId = ?", (prestamo_id,))
        conexion.commit()
        print("Prestamo eliminado.")
    else:
        print("No se encontraron prestamos para ese alumno.")
    conexion.close()

def lista_de_operaciones():
    print("\nLista de operaciones")
    print("1. libros/ejemplares actualmente prestados")
    print("2. alumnos con ejemplares prestados")
    print("3. libros/ejemplares nunca prestados")
    print("4. libros/ejemplares mas solicitados")
    print("5. libros/ejemplares disponibles")
    print("6. buscar libros por localizacion")
    print("7. regresar al menu principal")
    choice = input("Enter: ")

    if choice == '1':
        libro_saca()
    elif choice == '2':
        alumnos_saca()
    elif choice == '3':
        libros_no_saca()
    elif choice == '4':
        libros_mas_saca()
    elif choice == '5':
        libros_disponibles()
    elif choice == '6':
        buscar_libros_por_localizacion()
    elif choice == '7':
        print("Saliendo")
    else:
        print("Invalido")

answer = input("Crear nueva base de datos? (y/n)")
if answer in ["y", "Y"]:
    creartablas()

else:
    print("pasa")
    
menu_de_gestion()

#REVIEW DONE, 06.03.2025

