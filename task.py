def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            return f"Error: {error}"
    return wrapper

@handle_errors
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

@handle_errors
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@handle_errors
def change_phone(args, book: AddressBook):
    name, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0].value, new_phone)
        return f"Phone number updated for {name}"
    else:
        return "Contact not found"

@handle_errors
def show_phone(args, book: AddressBook):
    name, = args
    record = book.find(name)
    if record and record.phones:
        return f"Phone number for {name}: {record.phones[0]}"
    else:
        return "Phone number not found"

@handle_errors
def show_all(book: AddressBook):
    if book:
        return "All contacts:\n" + '\n'.join([str(record) for record in book.values()])
    else:
        return "No contacts"

if __name__ == "__main__":
    main()
