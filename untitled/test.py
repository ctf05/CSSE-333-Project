phone = "317-123-4567"
print(len(phone))

def check_phone(number):
    length = len(number) == 10 or len(number) == 12

    if length == 12:
        pass