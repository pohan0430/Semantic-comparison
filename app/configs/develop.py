docker_host_ip = '172.20.0.2'

POSTGRES_URI = f"postgresql+psycopg2://testuser:testpwd@{docker_host_ip}:5432/vectordb"
