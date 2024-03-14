from configparser import ConfigParser

DB_INIT_FILE = 'database.ini'
section = 'postgresql'
parser = ConfigParser()
parser.read(DB_INIT_FILE)
if parser.has_section(section):
    params = parser.items(section)
    db = {param[0]: param[1] for param in params}
else:
    raise Exception(f'Section {section} not found in the {DB_INIT_FILE} file')

POSTGRES_URI = f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"

EMBEDDING_LENGTH = 512
