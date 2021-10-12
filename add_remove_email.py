# takes a backup of the ids to a new file
def backup_id():
    with open('authorized_emails.csv', 'r') as f:
        text = f.read()
        with open('authorized_emails_bak.csv', 'w') as f_bak:
            f_bak.write(text)

# reads the authorised contacts from csv
def read_authorised_id():
    with open('authorized_emails.csv', 'r') as f:
        text = f.read()

    list = []

    # This takes the mail ids from csv and appends to the list
    for item in text.split('\n'):
        if len(item) != 0:
            list.append(item)
    print(list)
    return list


# Adds the email ID
def add_id(id_in_mailbody):
    backup_id()
    list = read_authorised_id()
    old_list = read_authorised_id()

    if id_in_mailbody in list:
        print(id_in_mailbody + ': Email ID already in the list.')
    else:
        list.append(id_in_mailbody)
        with open('authorized_emails.csv', 'w') as f:
            for item in list:
                f.write(item + '\n')

    new_list = read_authorised_id()
    return old_list, new_list, id_in_mailbody


# Removes the email ID
def remove_id(id_in_mailbody):
    backup_id()
    old_list = read_authorised_id()

    if id_in_mailbody not in old_list:
        print(id_in_mailbody + ': Email ID not in the list')
    else:
        with open('authorized_emails.csv', 'w') as f:
            for item in old_list:
                if item != id_in_mailbody:
                    f.write(item + '\n')

    new_list = read_authorised_id()

    return old_list, new_list, id_in_mailbody

# print(remove_id("abc@xyz.com"))
# print(add_id("abc@xyz.com"))
# print(read_authorised_id())