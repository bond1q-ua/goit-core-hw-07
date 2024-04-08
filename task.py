from collections import UserDict
from datetime import datetime, timedelta


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
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Не вірний формат дати. Введіть DD.MM.YYYY")


class AddressBook(UserDict):
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.values():
            if record.birthday:
                birthday_date = record.birthday.value.date().replace(year=today.year)
                if birthday_date < today:
                    birthday_date = birthday_date.replace(year=today.year + 1)
                days_until_birthday = (birthday_date - today).days

                if 0 <= days_until_birthday <= 7:
                    if birthday_date.weekday() >= 5:
                        birthday_date += timedelta(days=(7 - birthday_date.weekday()))
                    upcoming_birthdays.append({
                        'name': record.name.value,
                        'congratulation_date': birthday_date.strftime("%Y.%m.%d")
                    })

        return upcoming_birthdays


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

    def add_birthday(args, book):
        name, birthday = args
        if name not in book:
            return f"No record found for {name}."
        try:
            book[name].birthday = Birthday(birthday)
            return f"Birthday added for {name}."
        except ValueError as e:
            return str(e)

    def show_birthday(args, book):
        name = args[0]
        if name not in book:
            return f"No record found for {name}."
        if not book[name].birthday:
            return f"No birthday found for {name}."
        return f"Birthday of {name}: {book[name].birthday.value.strftime('%d.%m.%Y')}"

    def birthdays(args, book):
        upcoming_birthdays = book.get_upcoming_birthdays()
        if not upcoming_birthdays:
            return "No upcoming birthdays."
        return "Upcoming birthdays: " + ", ".join(
            f"{user['name']} ({user['congratulation_date']})" for user in upcoming_birthdays)

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

    def __str__(self):
        return f'Record(Name: {self.name} Phones: {self.phones})'

    def __repr__(self):
        return f'Record(Name: {self.name} Phones: {self.phones})'


class AddressBook(UserDict):
    def add_record(self, record: Record):
        name = record.name.value
        self.data.update({name: record})

    def find(self, name):
        return self.get(name)

    def delete(self, name):
        del self[name]


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
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(phone)

        elif command == "all":
            print(show_all(contacts))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


viktor = Record('Viktor')
viktor.add_phone('9999988812')

addressBook = AddressBook()
addressBook.add_record(viktor)

maria = Record('Maria')
maria.add_phone('8888877721')

addressBook.add_record(maria)

print(addressBook.find('Viktor'))
print(addressBook.find('Maria'))