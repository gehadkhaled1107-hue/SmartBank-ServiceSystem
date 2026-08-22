import time
import copy

user_data = [
    {
        "id": 1,
        "profile": {
            "name": "Amr",
            "phone": "01011111111",
            "email": "amr@test.com",
            "gender": "male",
            "age": 22,
            "city": "Cairo",
            "account_type": "business"
            },
        "security": {
            "password": "1234",
            "failed_attempts": 0,
            "is_locked": False
            },
        "wallet": {
            "balance_egp": 6000
            },
        "transactions": [],
        "settings": {
            "emergency_contact": []
            },
        "login_attempts": []
    },
    {
        "id": 2,
        "profile": {
            "name": "Gehad",
            "phone": "01022222222",
            "email": "gehad@test.com",
            "gender": "female",
            "age": 22,
            "city": "Giza",
            "account_type": 
            "personal"
            },
        "security": {
            "password": "1234",
            "failed_attempts": 0,
            "is_locked": False
        },
        "wallet": {
            "balance_egp": 1500
            },
        "transactions": [],
        "settings": {
            "emergency_contact": []
            },
        "login_attempts": []
    },
    {
        "id": 3,
        "profile": {
            "name": "Raghd",
            "phone": "01033333333",
            "email": "raghd@test.com",
            "gender": "female",
            "age": 22,
            "city": "Alexandria",
            "account_type": "personal"
            },
        "security": {
            "password": "1234",
            "failed_attempts": 0,
            "is_locked": False
            },
        "wallet": {
            "balance_egp": 200
            },
        "transactions": [],
        "settings": {
            "emergency_contact": []
            },
        "login_attempts": []
    },
]


next_user_id = 4

main_menu = "*************** SIC SMART BANK SYSTEM ***************\n\
If you already have an account, enter login\n\
If you do not have an account, enter register\n\
To close the system, enter exit\n"




while True:
    print(f"\n{main_menu}\n")
    current_user = None
    failed_attempts = 0

    operation = input("> ").lower().replace(" ", "")
    if operation not in ["login", "register", "exit"]:
        print("Invalid operation")
        continue

    # Login by ID
    if operation == "login":
        is_login_canceled = False

        while True:
            login_method = input("Login by ID or Email or Exit > (or type 'exit' to cancel) > ").lower().replace(" ", "")

            if login_method == "exit":
                print("Returning to main menu...")
                break

            elif login_method == "id":
                while failed_attempts != 3:
                    user_id = input("Enter your account id > ")

                    if user_id.lower() == "exit":
                        print("Returning to main menu...")
                        is_login_canceled = True
                        break

                    try:
                        user_id = int(user_id)
                    except ValueError:
                        print("Invalid input! ID must be a number.")
                        failed_attempts+=1
                        continue

                    for user in user_data:
                        if user["id"] == user_id:
                            current_user = user
                            break

                    if current_user != None:
                        print(f"Account found: {current_user['profile']['name']}")
                        break
                    else:
                        failed_attempts+=1
                        if failed_attempts < 3:
                            trials = input("Invalid account id\n Want to try again (yes/no) > ").strip().lower()
                            if trials in ["n", "no"]:
                                print("You exit successfully")
                                is_login_canceled = True
                                break
                        else:
                            print("Too many failed attempts!")
                            is_login_canceled = True
                            break

            # Login by Email
            elif login_method == "email":
                while failed_attempts != 3:
                    user_email = input("Enter your account email > ").lower().replace(" ", "")

                    if user_email == "exit":
                        print("Returning to main menu...")
                        is_login_canceled = True
                        break

                    for user in user_data :
                        if user_email == user["profile"]["email"]:
                            current_user = user
                            break

                    if current_user != None:
                        print(f"Account found: {current_user['profile']['name']}")
                        break
                    else:
                        failed_attempts+=1
                        if failed_attempts < 3:
                            trials = input("Invalid account email\n Want to try again (yes/no) > ").strip().lower()
                            if trials in ["n", "no"]:
                                print("You exit successfully")
                                is_login_canceled = True
                                break
                        else:
                            print("Too many failed attempts!")
                            is_login_canceled = True
                            break
            else:
                print("Invalid choice! Please type 'id' or 'email'.")

            if is_login_canceled:
                break

            # Password
            if current_user != None:
                if current_user["security"]["is_locked"] == True:
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    current_user["login_attempts"].append(f"Login Denied (Account Locked) at {current_time}")
                    print("Your account is locked")
                    is_login_canceled = True
                else:
                    while failed_attempts != 3:
                        user_password = input("Enter your account password > (or type 'exit' to cancel) >").strip()

                        if user_password.lower() == "exit":
                            print("Returning to main menu...")
                            is_login_canceled = True
                            break

                        if current_user["security"]["password"] == user_password:
                            current_user["security"]["failed_attempts"] = 0
                            print(f"Logged in seccessfully {current_user['profile']['name']}\n")
                            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                            current_user["login_attempts"].append(f"Success Login at {current_time}")

                            recent_attempts = current_user["login_attempts"][-3:]
                            print(f"Recent Login History: {recent_attempts}")

                            while True:

                                """
                                TODO: Wallet&Transactions menu options go here

                                ### Note for Wallet & Reports :
                                - The post-login session inside `main.py` is currently using a **temporary placeholder/stub menu** (Option 1). 
                                - Shared global state variables used: `user_data`, `next_user_id`, and `current_user`.
                                - You can plug your Wallet & Transactions loop directly into this post-login section.

                                """

                                user_action = input("Logged in Menu -> Type 'logout' to exit session: ").strip().lower()
                                if user_action == "logout":
                                    print("Logged out successfully.")
                                    is_login_canceled = True
                                    break
                                else:
                                    print("Invalid option. Type 'logout' to exit.")
                            break

                        else:
                            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                            current_user["login_attempts"].append(f"Failed Login at {current_time}")
                            failed_attempts+=1
                            current_user["security"]["failed_attempts"] = failed_attempts
                            if failed_attempts < 3:
                                trials = input("Wrong password\n Want to try again (yes/no) > ").strip().lower()
                                if trials in ["n", "no"]:
                                    print("You exit successfully")
                                    is_login_canceled = True
                                    break
                            else:
                                print("Too many failed attempts!")
                                is_login_canceled = True
                                current_user["security"]["is_locked"] = True
                if is_login_canceled:
                    break


    elif operation == "register":
        is_canceled = False

        # Name
        while True:
            user_name = input("Enter your name (or type 'exit' to cancel): ").strip()
            if user_name.lower() == "exit":
                is_canceled = True
                break

            if user_name:
                break
            print("Name cannot be empty!")

        if is_canceled:
            print("Registration canceled.")
            continue
        
        # Password
        while True:
            user_password = input("Please enter your password > ").strip()
            if user_password.lower() == "exit":
                is_canceled = True
                break

            if not user_password:
                print("Password cannot be empty!")
                continue

            if len(user_password) < 6:
                print("Password too short! Must be at least 6 characters long.")
                continue
            break


        if is_canceled:
            print("Registration canceled.")
            continue

        # Phone 
        while True:
            user_phone = input("Please enter your phone number (or type 'exit' to cancel) > ").strip().lower()
            
            if user_phone == "exit":
                is_canceled = True
                break


            try:
                int(user_phone)
                if len(user_phone) == 11 and user_phone.startswith("01"):
                    break
                else:
                    print("Invalid phone number!")
            except ValueError:
                print("Invalid phone number! Must contain digits only.")

        if is_canceled:
            print("Registration canceled.")
            continue

        # Email
        while True:
            user_email = input("Please enter your email (or type 'exit' to cancel) > ").strip().lower()
            
            if user_email == "exit":
                is_canceled = True
                break
                
            if user_email.count("@") == 1:
                domain = user_email.split("@")[1]
                if "." in domain and not domain.startswith(".") and not domain.endswith("."):
                    break
                else:
                    print("Invalid email domain format!")
            else:
                print("Invalid email! Email must contain exactly one '@' symbol.")

        if is_canceled:
            print("Registration canceled.")
            continue

        # Gender
        while True:
            user_gender = input("Please enter your gender (male/female) (or type 'exit' to cancel) > ").strip().lower()
            
            if user_gender == "exit":
                is_canceled = True
                break
                
            if user_gender in ["male", "female"]:
                break
            else:
                print("Invalid choice! Choose 'male' or 'female'.")

        if is_canceled:
            print("Registration canceled.")
            continue

        # Age
        while True:
            age_input = input("Please enter your age (or type 'exit' to cancel) > ").strip().lower()
            
            if age_input == "exit":
                is_canceled = True
                break
                
            try:
                user_age = int(age_input)
                if 18 <= user_age <= 100:
                    break
                else:
                    print("Please enter a valid age between 18 and 100.")
            except ValueError:
                print("Invalid age!")

        if is_canceled:
            print("Registration canceled.")
            continue

        # City
        while True:
            user_city = input("Please enter your city > ").strip()
            
            if user_city.lower() == "exit":
                is_canceled = True
                break

            if user_city:
                user_city = user_city.title()
                break
            print("City cannot be empty!")

        if is_canceled:
            print("Registration canceled.")
            continue

        # Account Type
        while True:
            account_type = input("Please enter account type (personal/business) (or type 'exit' to cancel) > ").strip().lower()
            if account_type == "exit":
                is_canceled = True
                break

            if account_type in ["personal", "business"]:
                break
            else:
                print("Invalid choice! Choose 'personal' or 'business'.")

        if is_canceled:
            print("Registration canceled.")
            continue

        # Check duplication for phone and email 
        is_duplicate = False
        for user in user_data:
            if user_phone == user["profile"]["phone"] and user_email == user["profile"]["email"]:
                print("This account already exist try to login")
                is_duplicate = True
                break
            elif user_phone == user["profile"]["phone"]:
                print("This phone number already exist try to login")
                is_duplicate = True
                break
            elif user_email == user["profile"]["email"]:
                print("This email already exist try to login")
                is_duplicate = True
                break

        # Update User Data
        if not is_duplicate:
            new_user = {
                "id": next_user_id,
                "profile": {
                    "name": user_name,
                    "phone": user_phone,
                    "email": user_email,
                    "gender": user_gender,
                    "age": user_age,
                    "city": user_city,
                    "account_type": account_type
                },
                "security": {
                    "password": user_password,
                    "failed_attempts": 0,
                    "is_locked": False
                },
                "wallet": {
                    "balance_egp": 0.0
                },
                "transactions": [],
                "settings": {
                    "emergency_contact": []
                },
                "login_attempts": []
            }

            """
            Using deepcopy to create an independent copy of the user dictionary, 
            ensuring that nested objects/data inside new_user are completely isolated 
            from future modifications when stored in user_data.
            """
            final_user_record = copy.deepcopy(new_user)

            user_data.append(final_user_record)

            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Sign up successful at {current_time} ! Your ID is {next_user_id}")

            next_user_id += 1

    elif operation == "exit":
        break

    else:
        print("Invalid input please choose\n\
        (login - register - exit)\n")


