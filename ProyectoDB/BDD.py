import sqlite3

def creartablas():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    
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

    conexion.execute("CREATE INDEX IF NOT EXISTS idx_ejemplares_libro_id ON Ejemplares (LibroId);")
    conexion.execute("CREATE INDEX IF NOT EXISTS idx_escribe_autor_id ON Escribe (AutorId);")
    conexion.execute("CREATE INDEX IF NOT EXISTS idx_escribe_libro_id ON Escribe (LibroId);")
    conexion.execute("CREATE INDEX IF NOT EXISTS idx_saca_ejemplar_id ON Saca (EjemplarId);")
    conexion.execute("CREATE INDEX IF NOT EXISTS idx_saca_alumne_id ON Saca (AlumneId);")

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
        print("6. Gestion de saca")
        print("7. Exit")
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
            gestion_saca_records()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalido")

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
    autor_id = input("ID del autor: ")
    localizacion = input("Ingrese la localización del ejemplar: ")
    cursor.execute("INSERT INTO Libros (Titulo, ISBN, Editorial, Paginas) VALUES (?, ?, ?, ?)", (titulo, isbn, editorial, paginas))
    libro_id = cursor.lastrowid
    cursor.execute("INSERT INTO Escribe (AutorId, LibroId) VALUES (?, ?)", (autor_id, libro_id))
    cursor.execute("INSERT INTO Ejemplares (Localizacion, LibroId) VALUES (?, ?)", (localizacion, libro_id))
    conexion.commit()
    conexion.close()
    print("Nuevo libro y ejemplar incorporados.")

def suprimir_libros():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    titulo = input("Ingrese el título del libro a eliminar: ")
    cursor.execute("SELECT LibroId, Titulo FROM Libros WHERE Titulo LIKE ?", ('%' + titulo + '%',))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, Título: {row[1]}")
        libro_id = input("Ingrese el ID del libro a eliminar: ")
        cursor.execute("DELETE FROM Libros WHERE LibroId = ?", (libro_id,))
        conexion.commit()
        print("Libro eliminado exitosamente.")
    else:
        print("No se encontraron libros con ese título.")
    conexion.close()

def gestion_alumnos():
    print("\ngestion de miembros")
    print("1. incorporar nuevos miembros")
    print("2. dar de baja miembros")
    print("3. regresar al menu principal")
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
    nombre = input("Ingrese el nombre del miembro a dar de baja: ")
    cursor.execute("SELECT AlumneID, Nombre FROM Alumnes WHERE Nombre LIKE ?", ('%' + nombre + '%',))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, Nombre: {row[1]}")
        alumne_id = input("Ingrese el ID del miembro a dar de baja: ")
        cursor.execute("SELECT * FROM Saca WHERE AlumneId = ? AND FechaDevolucion IS NULL", (alumne_id,))
        if cursor.fetchone():
            print("No se puede dar de baja al miembro con préstamos activos.")
        else:
            cursor.execute("DELETE FROM Alumnes WHERE AlumneID = ?", (alumne_id,))
            conexion.commit()
            print("Miembro dado de baja exitosamente.")
    else:
        print("No se encontraron miembros con ese nombre.")
    conexion.close()

def gestion_saca():
    print("\ngestion de prestamos")
    print("1. registrar nuevo prestamo")
    print("2. registrar devolucion")
    print("3. libros/ejemplares actualmente prestados")
    print("4. alumnos con ejemplares prestados")
    print("5. libros/ejemplares nunca prestados")
    print("6. libros/ejemplares mas solicitados")
    print("7. libros/ejemplares disponibles")
    print("8. buscar libros por localizacion")
    print("9. regresar al menu principal")
    choice = input("Enter: ")

    if choice == '1':
        nueva_saca()
    elif choice == '2':
        retorno()
    elif choice == '3':
        libro_saca()
    elif choice == '4':
        alumnos_saca()
    elif choice == '5':
        libros_no_saca()
    elif choice == '6':
        libros_mas_saca()
    elif choice == '7':
        libros_disponibles()
    elif choice == '8':
        buscar_libros_por_localizacion()
    elif choice == '9':
        print("Saliendo")
    else:
        print("Invalido")

def nueva_saca():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    ejemplar_id = input("Ingresa el ID del ejemplar: ")
    alumne_id = input("Ingresa el ID del miembro: ")
    fecha_prestamo = input("Ingresa la fecha de préstamo (YYYY-MM-DD): ")
    fecha_devolucion = input("Ingresa la fecha de devolución (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO Saca (EjemplarId, AlumneId, FechaPrestamo, FechaDevolucion) VALUES (?, ?, ?, ?)", (ejemplar_id, alumne_id, fecha_prestamo, fecha_devolucion))
    conexion.commit()
    conexion.close()
    print("Nuevo préstamo registrado exitosamente.")

def retorno():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    prestamo_id = input("Ingresa el ID del préstamo para registrar la devolución: ")
    hora_devolucion = input("Ingresa la hora de devolución (YYYY-MM-DD): ")
    cursor.execute("UPDATE Saca SET HoraDevolucion = ? WHERE PrestamoId = ?", (hora_devolucion, prestamo_id))
    conexion.commit()
    conexion.close()
    print("Correcto")

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
        print(row)
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
        print(row)
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
        print(row)
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
        print(f"ID: {row[0]}, Title: {row[2]}, Location: {row[1]}")
    conexion.close()

def buscar_libros_por_localizacion():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    localizacion = input("Enter location: ")
    cursor.execute("""
        SELECT Libros.Titulo, Ejemplares.Localizacion, 
               CASE WHEN Saca.HoraDevolucion IS NULL THEN 'On Loan' ELSE 'Available' END AS Status
        FROM Ejemplares
        JOIN Libros ON Ejemplares.LibroId = Libros.LibroId
        LEFT JOIN Saca ON Ejemplares.EjemplarId = Saca.EjemplarId AND Saca.HoraDevolucion IS NULL
        WHERE Ejemplares.Localizacion = ?
    """, (localizacion,))
    results = cursor.fetchall()
    for row in results:
        print(f"Title: {row[0]}, Location: {row[1]}")
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
    nombre = input("Ingrese el nombre del autor a eliminar: ")
    cursor.execute("SELECT AutorId, Nombre FROM Autores WHERE Nombre LIKE ?", ('%' + nombre + '%',))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, Nombre: {row[1]}")
        autor_id = input("Ingrese el ID del autor a eliminar: ")
        cursor.execute("DELETE FROM Autores WHERE AutorId = ?", (autor_id,))
        conexion.commit()
        print("Autor eliminado exitosamente.")
    else:
        print("No se encontraron autores con ese nombre.")
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
    ejemplar_id = input("Ingrese el ID del ejemplar a eliminar: ")
    cursor.execute("SELECT EjemplarId FROM Ejemplares WHERE EjemplarId = ?", (ejemplar_id,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM Ejemplares WHERE EjemplarId = ?", (ejemplar_id,))
        conexion.commit()
        print("Ejemplar eliminado exitosamente.")
    else:
        print("No se encontró el ejemplar con ese ID.")
    conexion.close()

def gestion_saca_records():
    print("\nGestion de saca")
    print("1. Suprimir saca")
    print("2. Regresa a menu")
    choice = input("Enter: ")

    if choice == '1':
        suprimir_saca()
    elif choice == '2':
        print("Regresando")
    else:
        print("Invalido")

def suprimir_saca():
    conexion = sqlite3.connect("Biblio.db")
    conexion.execute("PRAGMA foreign_keys = ON;")
    cursor = conexion.cursor()
    prestamo_id = input("Ingrese el ID del préstamo a eliminar: ")
    cursor.execute("SELECT PrestamoId FROM Saca WHERE PrestamoId = ?", (prestamo_id,))
    if cursor.fetchone():
        cursor.execute("SELECT * FROM Ejemplares WHERE EjemplarId IN (SELECT EjemplarId FROM Saca WHERE PrestamoId = ?)", (prestamo_id,))
        if cursor.fetchone():
            print("No se puede eliminar el préstamo porque hay ejemplares asociados.")
        else:
            cursor.execute("DELETE FROM Saca WHERE PrestamoId = ?", (prestamo_id,))
            conexion.commit()
            print("Préstamo eliminado exitosamente.")
    else:
        print("No se encontró el préstamo con ese ID.")
    conexion.close()

answer = input("Crear nueva base de datos? (y/n)")
if answer in ["y", "Y"]:
    creartablas()

else:
    print("pasa")
    
menu_de_gestion()

