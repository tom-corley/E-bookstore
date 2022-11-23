#===Imports/Setup===
import sqlite3
db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()

#===Functions===

# Adds a user inputted new book to virtual book store
def add_book():
    # Getting user input for new book
    print("\nEnter book selected: ")
    new_book = [
        max(ids)+1,
        input("Enter title: "),
        input("Enter author: "),
        int(input("Enter quantity in stock: "))
    ]

    # Updating local books array
    books.append(new_book)

    # Updating database
    cursor.execute('''INSERT INTO books (id, Title, Author, Qty)
        VALUES(?,?,?,?)''', \
            (new_book[0], new_book[1], new_book[2], new_book[3]))
    db.commit()

# Updates a book of users choice
def update_book():
    print("\nUpdate a book selected: ")

    # Case where no books are available to update
    if len(books) == 0:
        print("\nNo books to update, please add some, returning to menu...")
        return

    # Show user available books to update
    print("Books on record: \n")
    for i, book in enumerate(books):
        print(str(i+1)+". "+book[1])

    # Get user book choice
    book_to_update = int(input("\nEnter number of book to update: "))

    if 0 <= book_to_update-1 and book_to_update <= len(books):
        # Output to user, and getting user choice for what to change
        print("You have selected: "+str(books[book_to_update-1]))
        ans = input("Enter 1,2,3 to change title, author or quantity"\
            +" respectively, otherwise enter 0 to make no changes: ")

        # Setting new/keeping same values based on user answer
        if ans == "1":
            new_title = input("What is the new title: ")
            new_auth = books[book_to_update-1][2]
            new_quant = books[book_to_update-1][3]
        elif ans == "2":
            new_title = books[book_to_update-1][1]
            new_auth = input("Who is the new author: ")
            new_quant = books[book_to_update-1][3]
        elif ans == "3":
            new_title = books[book_to_update-1][1]
            new_auth = books[book_to_update-1][2]
            new_quant = input("What is the new quantity: ")
        else:
            new_title = books[book_to_update-1][1]
            new_auth = books[book_to_update-1][2]
            new_quant = books[book_to_update-1][3]
        
        # Updating database
        cursor.execute('''UPDATE books 
            SET Title = ?, Author = ?, Qty = ?
            WHERE id = ? ''',\
                (new_title,new_auth,new_quant,books[book_to_update-1][0]))
        db.commit()


        # Updating list
        books[book_to_update-1][1] = new_title
        books[book_to_update-1][2] = new_auth
        books[book_to_update-1][3] = new_quant

# Deletes a book of users choice
def delete_book():
    print("\nDelete a book selected: ")

    # Case where no books are available to update
    if len(books) == 0:
        print("\nNo books to delete, please add some, returning to menu...")
        return

    # Show user available books to delete
    print("Books on record: \n")
    for i, book in enumerate(books):
        print(str(i+1)+". "+book[1])

    # Get user book choice
    book_to_delete = int(input("\nEnter number of book to delete: "))

    # Check if selection is valid
    if 0 <= book_to_delete-1 and book_to_delete <= len(books):#
        print("Valid choice of book. deleting...\n")

        # Delete book from database
        cursor.execute('''DELETE FROM books
            WHERE id=?
        ''',(books[book_to_delete-1][0],))
        db.commit()

        # Delete from local list, reference variable so deletes it everywhere
        del books[book_to_delete-1]
    

# Searches for a user inputted book, is case sensitive
def search_book():
    print("\nSearch for book selected: ")

    # Case where no books are available to update
    if len(books) == 0:
        print("\nNo books to find, please add some, returning to menu...")
        return
    # Get user input for search type
    srch_type = input("Enter 0 or 1 to search by title or author: ")

    # Title Search
    if srch_type == "0":

        # Retrieve book from database if it exists
        s_title = input("Enter title: ")
        cursor.execute(''' SELECT * FROM books
        WHERE Title = ?''',(s_title,))
        found = cursor.fetchone()

        # If no such book is found, inform user
        if found == None:
            print("\nNo such book found, returning to menu...")
            return

        # If book is found, display book information to user
        print("\nBook found, Information about book:\n"\
            +"Book ID: "+str(found[0])
            +"\nTitle: "+found[1]
            +"\nAuthor: "+found[2]
            +"\nQuantity in stock: "+str(found[3]))
    
    # Author Search, may return several books
    elif srch_type == "1":
        # Retrieve book from database if it exists
        s_auth = input("Enter author: ")
        cursor.execute(''' SELECT * FROM books
        WHERE Author = ?''',(s_auth,))
        founds = cursor.fetchall()

        # If no such book is found, inform user
        if len(founds) == 0:
            print("\nNo such book found, returning to menu...")
            return

        # If book is found, display book information to user
        for found in founds:
            print("\nBook found, Information about book:\n"\
                +"Book ID: "+str(found[0])
                +"\nTitle: "+found[1]
                +"\nAuthor: "+found[2]
                +"\nQuantity in stock: "+str(found[3]))

    else:
        print("\nInvalid response, returning to menu...\n")
        
#===Creating and populating Database===

# Creating table
# In try-except in case table already exists
try:
    cursor.execute('''
    CREATE TABLE books (
        id int,
        Title varchar(70),
        Author varchar(40),
        Qty int,
        PRIMARY KEY (id)
    );
''')
    db.commit()
except Exception as e:
    pass

# Storing values in lists and creating local books array
ids = [3001,3002,3003,3004,3005]
qtys = [30,40,25,37,12]
titles = [
    'A Tale of Two Cities',
    'Harry Potter and the Philosopher\'s stone',
    'The Lion, the Witch, and the Wardrobe',
    'The Lord of the Rings',
    'Alice in Wonderland'
]
authors = [
    'Charles Dickens',
    'J.K. Rowling',
    'C.S. Lewis',
    'J.R.R Tolkien',
    'Lewis Carrol'
]

# Populating database with values, in try-except in case already populated.
try:
    for i in range(5):
        cursor.execute('''INSERT INTO books (id, Title, Author, Qty)
            VALUES(?,?,?,?)''', (ids[i], titles[i], authors[i],qtys[i]))
    db.commit()
except Exception as e:
    pass

# Populating local list for convenient use
cursor.execute('''SELECT * FROM books''')
books = [[i[0], i[1], i[2], i[3]] for i in cursor.fetchall()]

#===Main Menu===
while True:
    menu = input('''\nSelect one of the following Options below:
    1. Enter book
    2. Update book
    3. Delete Book
    4. Search books
    0. Exit
    : ''').lower()

    # Enter Option
    if menu == '1':
        add_book()

    # Update Option
    elif menu == '2':
        update_book()
    
    # Delete Option
    elif menu == '3':
        delete_book()

    # Search Option
    elif menu == '4':
        search_book()
    
    # Exit Option
    elif menu == '0':
        print('Goodbye!!!')
        db.close()
        exit()

    # Feedback to user when input invalid
    else:
        print("You have made a wrong choice, Please Try again")