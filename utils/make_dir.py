import os
from utils import check_exist as ch
    
def convdir():
    # make 'converted' dir
    # SBMLtoNetwork
    # |- converted

    path = './converted'
    if not ch.check_exist(path): 
        os.mkdir(path)

def anydir(dir_name):
    # make 'anyname' dir 
    # SBMLtoNetwork
    # |- converted
    # |  |- anyname dir
    # |  |- formula

    path = "./converted/" + dir_name
    if not ch.check_exist(path):
        os.mkdir(path)
        os.mkdir(path + "/formula")
