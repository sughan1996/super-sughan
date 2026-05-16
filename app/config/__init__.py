import os

if not os.environ.get("developer"):
    runtime = 'console'
    log_level = os.getenv('log_level', 'INFO').upper()
    username = os.getenv('username')
    password = os.getenv('password')
    database = os.getenv('database')
    host = os.getenv('host')
    port = int(os.getenv('port', 5432))
else:
    from decouple import config
    runtime = 'developer'
    log_level = config('log_level', default='INFO').upper()
    print(f"Log level set to: {log_level}")
    username = config('username')
    password = config('password')
    database = config('database')
    host = config('host')
    port = config('port', cast = int)