from phonenumbers import NumberParseException, PhoneNumber, PhoneNumberFormat, format_number, is_possible_number, parse


def format_phone(phone: str):
    phone_number: PhoneNumber = parse(phone)
    # res = [f'{phone.country_code[1:]}{phone.number}' for phone in phones if phone.country_code and phone.number]
    res = format_number(phone_number, PhoneNumberFormat.E164)
    return res


if __name__ == '__main__':
    # +7 (998) 999-00-00
    # 79608675036
    format_phone('+7 (998) 999-00-00')
