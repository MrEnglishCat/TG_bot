import os
from pprint import pprint

from environs import Env

env = Env()
env.read_env()
print(env('BOT_TOKEN'))
pprint(os.environ)