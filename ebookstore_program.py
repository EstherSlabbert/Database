import sqlite3 # imports SQLLite3 module

# creates or opens a database called 'ebookstore'
db = sqlite3.connect('ebookstore')

# creates a cursor object to exectue SQL statements
cursor = db.cursor()

# creates a table called 'books'
cursor.execute('''
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY, 
    Title TEXT, 
    Author TEXT, 
    Qty INTEGER
    );
''')

# saves changes to database
db.commit()

list_books = [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30), 
    (3002, 'Harry Potter and the Philosophers Stone', 'J.K. Rowling', 40), 
    (3003, 'The Lion, The Witch and the Wardrobe', 'C.S. Lewis', 25), 
    (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37), 
    (3005, 'Alice in Wonderland', 'Lewis Carrol', 12)
    ]
# selects all data in database    
cursor.execute('''SELECT * FROM books''')

if cursor.fetchone() == None:
    # Inserts books from 'list_books' into 'books' table if table empty
    cursor.executemany('''INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?);''', list_books)
    db.commit()
else:
    pass

###MAIN PROGRAM###
while True:
    menu = input('''
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit
Please enter your selected option number: ''')
    # options
    if menu == '1': # Allows user to enter a new book to database
        # Gets information to enter into database from user input
        while True:
            try:
                book_id = int(input("Book ID: "))
                break
            except ValueError:
                print("Book ID is an integer. Please enter the correct number id.")
        title = input("Book name: ")
        author = input("Author: ")
        while True:
            try:
                qty = int(input("Quantity in stock: "))
                break
            except ValueError:
                print("Please enter the correct quantity of books as an integer.")
        while True:
            try:
                # Adds book to database
                cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
                VALUES(?,?,?,?)''', (book_id, title, author, qty))
                break
                
            except sqlite3.IntegrityError:
                print("Please enter a unique Book ID.")
                while True:
                    try:
                        book_id = int(input("Book ID: "))
                        break
                    except ValueError:
                        print("Book ID is an integer. Please enter the correct number id.")
        # saves added book to database
        db.commit()
        
        # outputs message of success
        print("You have successfully added a book to the database!")
    
    elif menu == '2': # Allows user to update Qty information of a book to database
        # assigns temporary values to variable
        result = None

        # selects a book using book id ensuring entry of book id exists in database   
        while True:
            if result == None:
                
                while True:
                    try:
                        book_id = int(input("Book ID: "))
                        break
                    except ValueError:
                        print("Book ID is an integer. Please enter the correct number id.")
                cursor.execute('''SELECT id FROM books WHERE id = ?''', (book_id,))
                result = cursor.fetchone()

            else:
                print(f"Book ID: {book_id}, is in the database and has been selected to be updated.")
                break

        # get new quantity number    
        while True:
            try:
                quantity = int(input("New quantity: "))
                break
            except ValueError:
                print("The quantity of books is an integer. Please enter the correct number of books in stock.")

        # updates quantity of selected book in database
        cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''', (quantity, book_id))
        
        # saves update to database
        db.commit()

        # displays message of success of update
        print("You have successfully updated the information on the book in the database!")
    
    elif menu == '3': # Allows user to remove a book from database
        # assigns temporary values to variable
        result = None

        # selects a book using book id ensuring entry of book id exists in database   
        while True:
            if result == None:
                
                while True:
                    try:
                        book_id = int(input("Book ID you wish to delete information of: "))
                        break
                    except ValueError:
                        print("Book ID is an integer. Please enter the correct number id.")
                cursor.execute('''SELECT id FROM books WHERE id = ?''', (book_id,))
                result = cursor.fetchone()

            else:
                print(f"Book ID: {book_id}, is in the database and has been selected to be deleted.")
                break
        
        # deletes selected row from database using book id
        cursor.execute('''DELETE FROM books WHERE id = ?''', (book_id,))
        
        # saves changes to database
        db.commit()
        
        # outputs message of success
        print(f"You have successfully deleted the book with Book ID: {book_id} and its information from the database!")

    elif menu == '4': # Allows user to search for book by id in the database and display its info
        # collects user input of book id
        while True:
            try:
                book_id = int(input("To search for the book please enter the Book ID: "))
                break
            except ValueError:
                print("Book ID is an integer. Please enter the correct number id.")

        # selects appropriate data from books table to display
        cursor.execute('''SELECT id, Title, Author, Qty FROM books WHERE id = ?;''', (book_id,))
        book_info = cursor.fetchall()

        if book_info == []: # Displays that no items were found for the searched book id
            print("No results for your search were found in the database.")
        else: # Displays book information for chosen book id
            print("\nDisplay Format: [(BOOK_ID, TITLE, AUTHOR, QUANTITY)]\n\nBook information:")
            print(book_info)

    elif menu == '0': # Exits program
        print("Goodbye!") # farewell display
        db.close() # closes database
        quit() # exit

    else: # Lets user know their input was invalid
        print("You have not selected a valid option. Try again.")