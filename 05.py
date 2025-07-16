import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# Your file paths
user_path = "user.csv"
book_path = "books.csv"
borrow_path = "borrow.csv"
requests_path = "requests.csv"



class Admin:
    def __init__(self):
        self.user_path = user_path
        self.book_path = book_path
        self.borrow_path = borrow_path
        self.requests_path = requests_path

    def menu(self):
        while True:
            print("Admin menu: ")
            print("1: Book availability by book ID")
            print("2: Remove User")
            print("3: Add new book to library")
            print("4: Increase book")
            print("5: Decrease book")
            print("6: Update monthly bill of all users")
            print("0: To exit.")

            try:
                choice = int(input("Enter ur choice: "))
            except ValueError:
                print("Enter a number pls from above.")
                continue
            
            if choice == 1:
                book_id = int(input("Enter Book ID: "))
                self.books_and_availability(book_id)
            elif choice == 2:
                user_id = int(input("Enter user id:"))
                self.remove_user(user_id)
            elif choice == 3:
                self.new_book_add_to_library()
            elif choice == 4:
                self.increase_book()
            elif choice == 5:
                book_id = int(input("Enter book id: "))
                count = int(input("Enter no. of books: "))
                self.decrease_book(book_id, count)
            elif choice == 6:
                self.monthly_bill_calculator()
            elif choice == 0:
                print("✅ Logged out from Admin menu.")
                break
            else:
                print("❌ Invalid choice. Try again.")




    def books_and_availability(self, id: int):
        book = pd.read_csv(self.book_path, index_col='ID')

        try:
            print(f"The ID is {id} and number of available books are {book.loc['Availability']}")
        except KeyError:
            print("No such id")


    def remove_user(self, user_id: int):
        df = pd.read_csv(self.user_path, index_col="ID")
        try:
            if df.loc[user_id, "Monthly_bill"] != 0:
                print("User cannot be removed, fine must be paid.")
            else:
                df = df.drop(user_id)
                df.to_csv(self.user_path)
                print("User removed.")
        except KeyError:
            print("No such user!!!")


    def sort_dataframe(self):
        df = pd.read_csv(self.user_path, index_col="ID")
        df.sort_index(inplace=True)
        df.to_csv(self.user_path)

        df = pd.read_csv(self.book_path, index_col="ID")
        df.sort_index(inplace=True)
        df.to_csv(self.book_path)

        df = pd.read_csv(self.borrow_path, index_col="ID")
        df.sort_index(inplace=True)
        df.to_csv(self.borrow_path)

        df = pd.read_csv(self.requests_path, index_col="book_id")
        df.sort_index(inplace=True)
        df.to_csv(self.requests_path)



    def unoccupied_id_for_book(self):
        self.sort_dataframe()
        df = pd.read_csv(self.book_path)
        arr = df["ID"].to_numpy()

        starting = arr[0]
        if starting != 1:
            return 1
        elif starting + 1 != arr[1]:
            return 2
        else:
            i = 2
            while i < len(arr):
                if arr[i-1] + 1 != arr[i]:
                    return arr[i-1] + 1
                elif i == len(arr) - 1:
                    return arr[i] + 1
                else:
                    i += 1


    def new_book_add_to_library(self):
        df = pd.read_csv(self.book_path, index_col="ID")
        title = input("Enter title of book: ")
        author = input("Enter author: ")
        publishers = input("Enter publisher of book: ")
        pages = input("Enter number of pages: ")
        availability = input("Enter number of books: ")

        place = self.unoccupied_id_for_book()

        df.loc[place] = [title, author, publishers, pages, availability]
        df.to_csv(self.book_path)
        self.sort_dataframe()



    def increase_book(self,count: int):
        df_books = pd.read_csv(self.book_path, index_col="ID")
        df_request =  pd.read_csv(self.requests_path)
        try:
            book_id = df_request.loc[0, "book_id"]
            df_books.loc[book_id, "Availability"] += count
            df_request = df_request.drop(0)
            df_books.to_csv(self.book_path)
            df_request.to_csv(self.requests_path,index=False)

        except KeyError:
            book_id = int(input("Enter the book id: "))
            try:
                df_books.loc[book_id, "Availability"] += count
                df_books.to_csv(self.book_path)
            except KeyError:
                print("No such book ID found.")




    def decrease_book(self, book_id: int, count: int):
        df = pd.read_csv(self.book_path, index_col="ID")
        df.loc[book_id, "Availability"] -= count
        df.to_csv(self.book_path)



    def monthly_bill_calculator(self):
        df_borrow = pd.read_csv(self.borrow_path, index_col="ID")
        df_user = pd.read_csv(self.user_path, index_col="ID")

        current_time = datetime.today().date()

        for user_id in df_borrow.index:
            expiry_date = df_borrow.loc[user_id, "final_date"]
            expiry_date_int = datetime.strptime(expiry_date, "%d/%m/%Y").date()
            days = (current_time - expiry_date_int).days
            if days > 0:
                amount = days * 5
                df_user.loc[user_id, "Monthly_bill"] += amount

        df_user.to_csv(self.user_path)





class User:
    def __init__(self):
        self.user_path = user_path
        self.book_path = book_path
        self.borrow_path = borrow_path
        self.requests_path = requests_path

    def menu(self):
        while True:
            print("1: Book availability by book ID")
            print("2: Register as a new user")
            print("3: Borrow book")
            print("4: Return book")
            print("5: Request book")
            print("6: Search a book")
            print("7: Forgot user id")
            print("0: Exit")
        
            try:
                choice = int(input("Enter ur choice: "))
            except ValueError:
                print("Invalid")
                continue

            if choice == 1:
                book_id = int(input("Enter Book ID: "))
                self.books_and_availability(book_id)
            elif choice == 2:
                self.new_user_info_collect()
            elif choice == 3:
                self.borrow_book()
            elif choice == 4:
                user_id = int(input("Enter your user ID: "))
                book_id = int(input("Enter book ID: "))
                self.return_book_by_user(user_id, book_id)
            elif choice == 5:
                user_id = int(input("Enter your id: "))
                self.requested_books(user_id)
            elif choice == 6:
                title = input("Enter the name: ")
                self.search_book_by_name(title)
            elif choice == 7:
                self.find_user_id_by_info()
            elif choice == 0:
                print("Logged out from User menu.")
                break
            else:
                print("❌ Invalid choice. Try again.")
            




    def books_and_availability(self, id: int):
        book = pd.read_csv(self.book_path, index_col='ID')

        try:
            print(f"The ID is {id} and number of available books are {book.loc['Availability']}")
        except KeyError:
            print("No such id")



    def unoccupied_id_for_user(self):
        self.sort_dataframe()
        df = pd.read_csv(self.user_path)
        arr = df["ID"].to_numpy()

        starting = arr[0]
        if starting != 1:
            return 1
        elif starting + 1 != arr[1]:
            return 2
        else:
            i = 2
            while i < len(arr):
                if arr[i-1] + 1 != arr[i]:
                    return arr[i-1] + 1
                elif i == len(arr) - 1:
                    return arr[i] + 1
                else:
                    i += 1



    def new_user_info_collect(self):
        df = pd.read_csv(self.user_path, index_col="ID")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")
        address = input("Enter your address: ")
        contact_number = input("Enter your contact number: ")

        start_date = datetime.today()
        expiry_date = start_date + timedelta(days=30)
        expiry_date_str = expiry_date.strftime('%d/%m/%Y')

        place = self.unoccupied_id_for_user()

        df.loc[place] = [first_name, last_name, email, address, contact_number, expiry_date_str, 0]
        df.to_csv(self.user_path)
        self.sort_dataframe()



    def sort_dataframe(self):
        df = pd.read_csv(self.user_path, index_col="ID")
        df.sort_index(inplace=True)
        df.to_csv(self.user_path)

        df = pd.read_csv(self.book_path, index_col="ID")
        df.sort_index(inplace=True)
        df.to_csv(self.book_path)

        df = pd.read_csv(self.borrow_path, index_col="ID")
        df.sort_index(inplace=True)
        df.to_csv(self.borrow_path)

        df = pd.read_csv(self.requests_path, index_col="book_id")
        df.sort_index(inplace=True)
        df.to_csv(self.requests_path)




    def borrow_book(self):
        df_user = pd.read_csv(self.user_path, index_col="ID")
        df_book = pd.read_csv(self.book_path, index_col="ID")
        df_borrow = pd.read_csv(self.borrow_path, index_col="ID")


        user_id = int(input("Enter your ID: "))
        if user_id not in df_user.index:
                print("❌ Invalid user ID.")
                return
        
        title = input("Enter name of the book: ")
        self.search_book_by_name(title)
        book_id = int(input("Enter book ID or enter 0 to exit to menu: "))
        if book_id == 0:
            return self.menu()
        if book_id not in df_book.index:
                print("❌ Invalid book ID.")
                return
        

        today = datetime.today().date()
        end_time = today + timedelta(days=21)

        if df_book.loc[book_id, "Availability"] < 5:
            print("Sorry, book cannot be borrowed for now, returning you to request side.")
            return self.requested_books(user_id)
        else:
            df_book.loc[book_id, "Availability"] -= 1
            df_borrow.loc[user_id] = [
                book_id,
                f"{df_user.loc[user_id, 'first_name']} {df_user.loc[user_id, 'last_name']}",
                df_book.loc[book_id, "Title"],
                end_time.strftime("%d/%m/%Y")
            ]

        df_borrow.to_csv(self.borrow_path)
        self.sort_dataframe()
        # print(df_borrow)


    def search_book_by_name(self, title: str):
        df_book = pd.read_csv(self.book_path, index_col="ID")
        needed_id = []

        words = title.lower().split()

        for book_id in df_book.index:
            book_title = df_book.loc[book_id, "Title"].lower()
            if any(word in book_title for word in words):
                needed_id.append(book_id)

        if df_book.loc[needed_id].empty is False:
            print(df_book.loc[needed_id])
        else:
            print("No such book currently available")



    def requested_books(self, user_id: int):
        df_user = pd.read_csv(self.user_path, index_col="ID")
        df_book = pd.read_csv(self.book_path, index_col="ID")
        df_requests = pd.read_csv(self.requests_path, index_col="book_id")
        
        try:
            name = str(input("Enter the book name you want to request: "))
            self.search_book_by_name(name)
            book_id = int(input("Enter book id from above: "))

            if user_id not in df_user.index:
                print("❌ Invalid user ID.")
                return
            if book_id not in df_book.index:
                print("❌ Invalid book ID.")
                return
            
            df_requests.loc[book_id] = [df_book.loc[book_id, "Title"], df_user.loc[user_id, "first_name"] + " " +
                            df_user.loc[user_id, "last_name"] ]

            df_requests.to_csv(self.requests_path)
            self.sort_dataframe()
            print("Book request submitted successfully.")

        except ValueError:
            print("Enter valid user id and book id.")






    def return_book_by_user(self, user_id: int, book_id: int):
        df_borrow = pd.read_csv(self.borrow_path)
        matches = df_borrow[(df_borrow["ID"] == user_id) & (df_borrow["BookID"] == book_id)]
        if matches.empty:
            print("❌ No matching record found for this user and book.")
        else:
            df_borrow = df_borrow.drop(matches.index)
            df_borrow.to_csv(self.borrow_path, index=False)
            print("✅ Book successfully returned.")




    def find_user_id_by_info(self):
        email = input("Enter your email address: ").lower()
        mobile_number = int(input("Enter your mobile number: "))
        df = pd.read_csv(self.user_path, index_col="ID")
        self.sort_dataframe()

        for i in range(1, df.index.max() + 1):
            if email == df.loc[i, "email"] and mobile_number == df.loc[i, "phone"]:
                print(f"Your ID number is {i}")
                return
        else:
            print("No user found.")


    def subcription_checker(user_id :int):
        positive = 1
        df = pd.read_csv(user_path, index_col="ID")
        expiry_date = df.loc[user_id, "subscription_status"]
        exp_date = datetime.strptime(expiry_date, "%d/%m/%Y")   #it convert date to int format from str

        today = datetime.today().date()    #get todays date
        today_new = today.strftime("%d/%m/%Y")        #remove time from date and format is d/m/y
        current_date = datetime.strptime(today_new, "%d/%m/%Y")    #convert date to readable int from str

        if current_date < exp_date:
            # print("User is member.")
            return positive
        else:
            # print("Buy subscription")
            positive = 0
            return positive



# user = User()
# user.menu()




class Mainmenu:
    def __init__(self):
        self.password = "dementor#021"


    def menu(self):
        tries = 0
        while True:
            print("Menu: ")
            print("1: User Menu")
            print("2: Admin Menu")
            print("3: Exit")
            

            choice = int(input("Enter your choice."))

            if choice == 1:
                user = User()
                user.menu()
            elif choice == 2 and tries < 3:
                for i in range(3):
                    key = input("Enter the password: ")
                    if key == self.password:
                        admin = Admin()
                        admin.menu()
                        break
                    else:
                        tries += 1
                        if tries == 3:
                            print("Admin login blocked, restart if needed")

            elif choice == 3:
                print("Session terminated")
                break

            else:
                ("Invalid choice.")


    
menu = Mainmenu()
menu.menu()

