# in local connect to postgresql
# db_host_ip = '127.0.0.1'
# POSTGRES_URI = f"postgresql+psycopg2://testuser:testpwd@{db_host_ip}:9876/vectordb"

# in docker container connect to postgresql
db_host_ip = 'db'
POSTGRES_URI = f"postgresql+psycopg2://testuser:testpwd@{db_host_ip}:5432/vectordb"

