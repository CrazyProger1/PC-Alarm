from app.utils.config import *

env = ENVConfig.load('env/local.env')

env.save('env/local2.env')
