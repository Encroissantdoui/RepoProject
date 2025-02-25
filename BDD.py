import sqlite3

def create_tables():
    con = sqlite3.connect("Biblio.db")

    con.execute("""
        CREATE TABLE `Alumnes` (
            `AlumneID` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Nombre` TEXT NOT NULL,
            `Telefono` INTEGER,
            `Direccion` TEXT NOT NULL
            );
    """)

    con.execute("""
        CREATE TABLE `Autores` (
            `AutorId` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Nombre` TEXT NOT NULL
            );
    """)

    con.execute("""
        CREATE TABLE `Libros` (
            `LibroId` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Titulo` TEXT NOT NULL,
            `ISBN` INTEGER NOT NULL,
            `Editorial` TEXT NOT NULL,
            `Paginas` INTEGER
            );
    """)

    con.execute("""
        CREATE TABLE `Ejemplares` (
            `EjemplarId` INTEGER PRIMARY KEY AUTOINCREMENT,
            `Localizacion` TEXT NOT NULL,
            `LibroId` INTEGER NOT NULL,
            FOREIGN KEY (`LibroId`) REFERENCES `Libros` (`LibroId`)
            ON UPDATE RESTRICT ON DELETE RESTRICT
            );
    """)

    con.execute("""
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

    con.execute("""
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

    con.commit()
    con.close()

def display_menu():
    while True:
        print("\nGestor Biblioteca")
        print("1. Gestion de libros")
        print("2. Gestion de personas")
        print("3. Gestion de prestamos")
        print("4. Gestion de autores")
        print("5. Exit")
        choice = input("Enter: ")

        if choice == '1':
            manage_books()
        elif choice == '2':
            manage_members()
        elif choice == '3':
            manage_loans()
        elif choice == '4':
            manage_authors()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def manage_books():
    print("\nManage Books")
    print("1. Incorporate New Books/Copies")
    print("2. Delete Books/Copies")
    print("3. Back to Main Menu")
    choice = input("Enter your choice: ")

    if choice == '1':
        incorporate_new_book()
    elif choice == '2':
        delete_book()
    elif choice == '3':
        print("Returning to Main Menu...")
    else:
        print("Invalid choice. Please try again.")

def incorporate_new_book():
    con = sqlite3.connect("Biblio.db")
    cursor = con.cursor()
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
    con.commit()
    con.close()
    print("New book and copy incorporated successfully.")

def delete_book():
    con = sqlite3.connect("Biblio.db")
    cursor = con.cursor()
    libro_id = input("Enter book ID to delete: ")
    cursor.execute("DELETE FROM Libros WHERE LibroId = ?", (libro_id,))
    con.commit()
    con.close()
    print("Book deleted successfully.")

def manage_members():
    print("\nManage Members")
    print("1. Incorporate New Members")
    print("2. Deregister Members")
    print("3. Back to Main Menu")
    choice = input("Enter your choice: ")

    if choice == '1':
        incorporate_new_member()
    elif choice == '2':
        deregister_member()
    elif choice == '3':
        print("Returning to Main Menu...")
    else:
        print("Invalid choice. Please try again.")

def incorporate_new_member():
    con = sqlite3.connect("Biblio.db")
    cursor = con.cursor()
    nombre = input("Enter member name: ")
    telefono = input("Enter member phone: ")
    direccion = input("Enter member address: ")
    cursor.execute("INSERT INTO Alumnes (Nombre, Telefono, Direccion) VALUES (?, ?, ?)", (nombre, telefono, direccion))
    con.commit()
    con.close()
    print("New member incorporated successfully.")

def deregister_member():
    con = sqlite3.connect("Biblio.db")
    cursor = con.cursor()
    alumne_id = input("Enter member ID to deregister: ")
    cursor.execute("SELECT * FROM Saca WHERE AlumneId = ? AND FechaDevolucion IS NULL", (alumne_id,))
    if cursor.fetchone():
        print("Cannot deregister member with active loans.")
    else:
        cursor.execute("DELETE FROM Alumnes WHERE AlumneID = ?", (alumne_id,))
        con.commit()
        print("Member deregistered successfully.")
    con.close()

def manage_loans():
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
        register_new_loan()
    elif choice == '2':
        register_return()
    elif choice == '3':
        books_on_loan()
    elif choice == '4':
        students_with_loans()
    elif choice == '5':
        books_never_loaned()
    elif choice == '6':
        most_requested_books()
    elif choice == '7':
        print("Returning to Main Menu...")
    else:
        print("Invalid choice. Please try again.")

def register_new_loan():
    con = sqlite3.connect("Biblio.db")
    cursor = con.cursor()
    ejemplar_id = input("Enter copy ID: ")
    alumne_id = input("Enter member ID: ")
    fecha_prestamo = input("Enter loan date (YYYY-MM-DD): ")
    fecha_devolucion = input("Enter return date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO Saca (EjemplarId, AlumneId, FechaPrestamo, FechaDevolucion) VALUES (?, ?, ?, ?)", (ejemplar_id, alumne_id, fecha_prestamo, fecha_devolucion))
    con.commit()
    con.close()
    print("New loan registered successfully.")

def register_return():
    con = sqlite3.connect("Biblio.db")
    cursor = con.cursor()
    prestamo_id = input("Enter loan ID to register return: ")
    fecha_devolucion = input("Enter return date (YYYY-MM-DD): ")
    hora_devolucion = input("Enter return time (YYYY-MM-DD): ")
    cursor.execute("UPDATE Saca SET HoraDevolucion = ? WHERE PrestamoId = ?", (hora_devolucion, prestamo_id))
    con.commit()
    con.close()
    print("Return registered successfully.")

def books_on_loan():
    con = sqlite3.connect("Biblio.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT Ejemplares.*
        FROM Ejemplares
        JOIN Saca ON Ejemplares.EjemplarId = Saca.EjemplarId
        WHERE Saca.HoraDevolucion IS NULL
    """)
    results = cursor.fetchall()
    for row in results:
        print(row)
    con.close()

def students_with_loans():
    con = sqlite3.connect("Biblio.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT Alumnes.*
        FROM Alumnes
        JOIN Saca ON Alumnes.AlumneID = Saca.AlumneId
        WHERE Saca.HoraDevolucion IS NULL
    """)
    results = cursor.fetchall()
    for row in results:
        print(row)
    con.close()

def books_never_loaned():
    con = sqlite3.connect("Biblio.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT * FROM Ejemplares
        WHERE EjemplarId NOT IN (SELECT EjemplarId FROM Saca)
    """)
    results = cursor.fetchall()
    for row in results:
        print(row)
    con.close()

def most_requested_books():
    con = sqlite3.connect("Biblio.db")
    cursor = con.cursor()
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
    con.close()

def manage_authors():
    print("\nManage Authors")
    print("1. Incorporate New Author")
    print("2. Back to Main Menu")
    choice = input("Enter your choice: ")

    if choice == '1':
        incorporate_new_author()
    elif choice == '2':
        print("Returning to Main Menu...")
    else:
        print("Invalid choice. Please try again.")

def incorporate_new_author():
    con = sqlite3.connect("Biblio.db")
    cursor = con.cursor()
    nombre = input("Enter author name: ")
    cursor.execute("INSERT INTO Autores (Nombre) VALUES (?)", (nombre,))
    con.commit()
    con.close()
    print("New author incorporated successfully.")

answer = input("Crear nueva base de datos? (y/n)")
if answer in ["y", "Y"]:
    create_tables()

else:
    print("pasa")
    
display_menu()

