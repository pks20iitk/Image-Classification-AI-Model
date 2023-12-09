from configparser import ConfigParser


def read_config(filename='postgres_database/config.ini', section='production'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        db = dict(parser.items(section))
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db
