from datetime import datetime, timedelta
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name=None):
        if name is None:
            raise ValueError
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        if len(phone) != 10:
            raise ValueError
        super().__init__(phone)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        raise ValueError

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f'Record(Name: {self.name}, Phones: {self.phones}, Birthday: {self.birthday})'


class AddressBook(UserDict):
    def add_record(self, record: Record):
        name = record.name.value
        self.data.update({name: record})

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self[name]

    def get_upcoming_birthdays(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []
        for record in self.values():
            if record.birthday is not None:
                if today < record.birthday.value < next_week:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays


def parse_input(user_input):
    return user_input.split()


def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}"
    else:
        return "Contact not found"


def show_birthday(args, book):
    name, = args
    record = book.find(name)
    if record and record.birthday:
        return f"Birthday for {name}: {record.birthday}"
    else:
        return "Birthday not found"


def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "Upcoming birthdays:\n" + '\n'.join([str(record) for record in upcoming_birthdays])
    else:
        return "No upcoming birthdays"


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


def change_phone(args, book: AddressBook):
    name, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0].value, new_phone)
        return f"Phone number updated for {name}"
    else:
        return "Contact not found"


def show_phone(args, book: AddressBook):
    name, = args
    record = book.find(name)
    if record and record.phones:
        return f"Phone number for {name}: {record.phones[0]}"
    else:
        return "Phone number not found"


def show_all(book: AddressBook):
    if book:
        return "All contacts:\n" + '\n'.join([str(record) for record in book.values()])
    else:
        return "No contacts"


if __name__ == "__main__":
    main()
