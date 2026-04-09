from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

from prisma import Prisma

db = Prisma()
