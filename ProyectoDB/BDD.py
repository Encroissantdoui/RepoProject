import sqlite3

def creartablas():
    conexion = sqlite3.connect("Biblio.db")

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
        print("5. Exit")
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
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def gestion_libros():
    print("\nManage Books")
    print("1. Incorporate New Books/Copies")
    print("2. Delete Books/Copies")
    print("3. Back to Main Menu")
    choice = input("Enter your choice: ")

    if choice == '1':
        nuevos_libros()
    elif choice == '2':
        suprimir_libros()
    elif choice == '3':
        print("Returning to Main Menu...")
    else:
        print("Invalid choice. Please try again.")

def nuevos_libros():
    conexion = sqlite3.connect("Biblio.db")
    cursor = conexion.cursor()
    titulo = input("Enter book title: ")
    isbn = input("Enter book ISBN: ")
    editorial = input("Enter book editorial: ")
    paginas = input("Enter number of pages: ")
    autor_id = input("Enter author ID: ")
    localizacion = input("Enter copy location: ")
    cursor.execute("INSERT INTO Libros (Titulo, ISBN, Editorial, Paginas) VALUES (?, ?, ?, ?)", (titulo, isbn, editorial, paginas))
    libro_id = cursor.lastrowid
    cursor.execute("INSERT INTO Escribe (AutorId, LibroId) VALUES (?, ?)", (autor_id, libro_id))
    cursor.execute("INSERT INTO Ejemplares (Localizacion, LibroId) VALUES (?, ?)", (localizacion, libro_id))
    conexion.commit()
    conexion.close()
    print("New book and copy incorporated successfully.")

def suprimir_libros():
    conexion = sqlite3.connect("Biblio.db")
    cursor = conexion.cursor()
    libro_id = input("Enter book ID to delete: ")
    cursor.execute("DELETE FROM Libros WHERE LibroId = ?", (libro_id,))
    conexion.commit()
    conexion.close()
    print("Book deleted successfully.")

def gestion_alumnos():
    print("\nManage Members")
    print("1. Incorporate New Members")
    print("2. Deregister Members")
    print("3. Back to Main Menu")
    choice = input("Enter your choice: ")

    if choice == '1':
        nuevos_alumnos()
    elif choice == '2':
        suprimir_alumnos()
    elif choice == '3':
        print("Returning to Main Menu...")
    else:
        print("Invalid choice. Please try again.")

def nuevos_alumnos():
    conexion = sqlite3.connect("Biblio.db")
    cursor = conexion.cursor()
    nombre = input("Enter member name: ")
    telefono = input("Enter member phone: ")
    direccion = input("Enter member address: ")
    cursor.execute("INSERT INTO Alumnes (Nombre, Telefono, Direccion) VALUES (?, ?, ?)", (nombre, telefono, direccion))
    conexion.commit()
    conexion.close()
    print("New member incorporated successfully.")

def suprimir_alumnos():
    conexion = sqlite3.connect("Biblio.db")
    cursor = conexion.cursor()
    alumne_id = input("Enter member ID to deregister: ")
    cursor.execute("SELECT * FROM Saca WHERE AlumneId = ? AND FechaDevolucion IS NULL", (alumne_id,))
    if cursor.fetchone():
        print("Cannot deregister member with active loans.")
    else:
        cursor.execute("DELETE FROM Alumnes WHERE AlumneID = ?", (alumne_id,))
        conexion.commit()
        print("Member deregistered successfully.")
    conexion.close()

def gestion_saca():
    print("\nManage Loans")
    print("1. Register New Loan")
    print("2. Register Return")
    print("3. Books/Copies Currently on Loan")
    print("4. Students with Copies on Loan")
    print("5. Books/Copies Never Loaned")
    print("6. Most Requested Books/Copies")
    print("7. Back to Main Menu")
    choice = input("Enter your choice: ")

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
        print("Returning to Main Menu...")
    else:
        print("Invalid choice. Please try again.")

def nueva_saca():
    conexion = sqlite3.connect("Biblio.db")
    cursor = conexion.cursor()
    ejemplar_id = input("Enter copy ID: ")
    alumne_id = input("Enter member ID: ")
    fecha_prestamo = input("Enter loan date (YYYY-MM-DD): ")
    fecha_devolucion = input("Enter return date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO Saca (EjemplarId, AlumneId, FechaPrestamo, FechaDevolucion) VALUES (?, ?, ?, ?)", (ejemplar_id, alumne_id, fecha_prestamo, fecha_devolucion))
    conexion.commit()
    conexion.close()
    print("New loan registered successfully.")

def retorno():
    conexion = sqlite3.connect("Biblio.db")
    cursor = conexion.cursor()
    prestamo_id = input("Enter loan ID to register return: ")
    fecha_devolucion = input("Enter return date (YYYY-MM-DD): ")
    hora_devolucion = input("Enter return time (YYYY-MM-DD): ")
    cursor.execute("UPDATE Saca SET HoraDevolucion = ? WHERE PrestamoId = ?", (hora_devolucion, prestamo_id))
    conexion.commit()
    conexion.close()
    print("Return registered successfully.")

def libro_saca():
    conexion = sqlite3.connect("Biblio.db")
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

def gestion_autores():
    print("\nManage Authors")
    print("1. Incorporate New Author")
    print("2. Back to Main Menu")
    choice = input("Enter your choice: ")

    if choice == '1':
        nuevos_autores()
    elif choice == '2':
        print("Returning to Main Menu...")
    else:
        print("Invalid choice. Please try again.")

def nuevos_autores():
    conexion = sqlite3.connect("Biblio.db")
    cursor = conexion.cursor()
    nombre = input("Enter author name: ")
    cursor.execute("INSERT INTO Autores (Nombre) VALUES (?)", (nombre,))
    conexion.commit()
    conexion.close()
    print("New author incorporated successfully.")

answer = input("Crear nueva base de datos? (y/n)")
if answer in ["y", "Y"]:
    creartablas()

else:
    print("pasa")
    
menu_de_gestion()

