from envparse import Env 

env = Env()

DATABASE_URL = env.str("DATABASE_URL", 
                       default ="sqlite+aiosqlite:///sqldb.db")

PROTOCOL_HEADER = "https://"
SITE_NAME = "game-ads"
DOMAIN_AREA = ".netlify.app"
BASE_WEB_ADDESS = f"{PROTOCOL_HEADER}{SITE_NAME}{DOMAIN_AREA}"


SECRET_KEY: str = env.str("SECRET_KEY", default = "secret_key")
ALHORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=60 * 24)