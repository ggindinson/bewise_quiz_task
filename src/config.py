from environs import Env

env = Env()
env.read_env()

DB_USER: str = env.str("DB_USER")
DB_NAME: str = env.str("DB_NAME")
DB_PASSWORD: str = env.str("DB_PASSWORD")
DB_HOST: str = env.str("DB_HOST")
