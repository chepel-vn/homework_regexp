import re
import csv


def fix_errors(contact_list):
    """

    (list) -> list

    Function fix errors such as transposition of elements and translate to need value

    """
    # main replace
    pattern = r'^([А-Яа-я]+)[, ]([А-Яа-я]+)[, ]([А-Яа-я]*),,?,?([А-Яа-я]*),([А-Яa-zа-я –]*),(\+?\d?) ?\(?(\d?\d?\d?)'\
        r'\)?[ -]?(\d?\d?\d?)[ -]?(\d?\d?)[ -]*(\d?\d?)( *)\(*([доб.]*) *([\d{4}]*)\)*,([\da-zA-Z\.]*@*[a-z]*.*[a-z]*)'
    replacer = r'\1,\2,\3,\4,\5,\6(\7)\8-\9-\10\11\12\13,\14'

    # replace "8" to "+7" in phone number
    pattern8 = r'(,?)(8)([( ])'
    replacer8 = r'\1+7\3'

    # replace "()--" to ""
    pattern_empty_number = r'\(\)--'
    replacer_empty_number = r''

    result_all = list()
    for contact in contact_list[1::1]:
        prestr = ",".join(contact)
        result = re.sub(pattern8, replacer8, prestr)
        result = re.sub(pattern, replacer, result)
        result = re.sub(pattern_empty_number, replacer_empty_number, result)
        result_all.append(result)

    return result_all


def fix_double_records(contact_list):
    """

    (list) -> list

    Function union several records about one person to one record

    """
    result_all_string = ';'.join(contact_list)

    # Getting set of fio which have two and more records
    result_set = set()
    result_set_all = set()
    for item in contact_list:
        pattern_here = r'^([А-Яа-я]+[, ][А-Яа-я]+[, ][А-Яа-я]*)(.*)'
        replacer = r'\1'
        last_name = re.sub(pattern_here, replacer, item)
        found = re.findall(last_name, result_all_string)
        if len(found) > 1:
            result_set.add(last_name)
        result_set_all.add(last_name)

    # Union all repeated records to one record by one person and save it to result list
    result_records = []
    for item in result_set:
        pattern_here = item + r'[ a-zA-Zа-яА-Я,\+\d()-.@–]*'
        found = re.findall(pattern_here, result_all_string)
        person = ['', '', '', '', '', '', '']
        for found_item in found:
            found_item_split = re.split(',', found_item)
            result_set_all.discard(f"{found_item_split[0]},{found_item_split[1]},{found_item_split[2]}")

            for i in range(7):
                if len(person[i]) < len(found_item_split[i]):
                    person[i] = found_item_split[i]
        result_records.append(person)

    # Copy other records to result list
    for item in result_set_all:
        pattern_here = item + r'[ a-zA-Zа-яА-Я,\+\d()-.@–]*'
        found = re.findall(pattern_here, result_all_string)
        found_split = re.split(',', found[0])
        result_records.append(found_split)

    return result_records


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    contacts_list_fix = fix_errors(contacts_list)
    contacts_list_result = fix_double_records(contacts_list_fix)

    with open("phonebook_result.csv", "w", encoding="utf8", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows([contacts_list[0]])
        datawriter.writerows(contacts_list_result)
