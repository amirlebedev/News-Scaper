from datetime import datetime


def get_database():
    database_data = []
    with open("database.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().split(" | ")
            database_data.append(line)
    return database_data


def get_database_links_from_list(database):
    list_links = []
    for data in database:
        list_links.append(data[2])
    return list_links


def get_database_links_from_file():
    database = get_database()
    list_links = get_database_links_from_list(database)
    return list_links


def convert_list_to_database_format(metadata):
    metadata_string = metadata[0] + " | " + metadata[1] + " | " + metadata[2] + " | " + metadata[3]
    metadata_string = metadata_string + " | " + metadata[4] + " | " + metadata[5]
    metadata_string = metadata_string + " | " + metadata[6] + " | " + metadata[7] + "\n"
    return metadata_string


def write_database(database):
    with open("database.txt", "w", encoding="utf-8") as f:
        for data in database:
            data_string = convert_list_to_database_format(data)
            f.write(data_string)


def write_database_backup(database):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    file_path = ".\\backup\\" + dt_string + ".txt"
    with open(file_path, "w", encoding="utf-8") as f:
        for data in database:
            data_string = convert_list_to_database_format(data)
            f.write(data_string)



def make_database_copy(database):
    database_copy = database[:]
    return database_copy


def write_database_website(database):
    with open("web.txt", "w", encoding="utf-8") as f:
        for data in database:
            data_string = convert_list_to_database_format(data)
            f.write(data_string)


def convert_to_html_view():
    database = get_database()
    database_copy = make_database_copy(database)

    line = 0
    for data in database:
        data[1].replace("|", " ")
        url = data[2]
        href_url = '<a href="' + url + '">Link</a>'
        database_copy[line][2] = href_url
        database_copy[line][7] = '<a href="' + data[7] + '">Archive</a>'
        line += 1
    write_database_website(database_copy)