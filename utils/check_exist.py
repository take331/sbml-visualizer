# ファイルやディレクトリが既に存在しているかを判定

import os
import xml.etree.ElementTree as ET

def is_sbml_file(file_path):
    # is import file type sbml
    # return -> exist：True / not exist：Fales
    # first method -> judge of endswith()
    # second method -> judge of getroot()

    if file_path == None:
        return False

    if file_path.endswith(".xml"):
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                return 'sbml' in root.tag
        
        
        except ET.ParseError:
            return False
        except UnicodeDecodeError:
            return False
        

    else:
        return False
    

def check_exist(path):
    # ディレクトリが存在するか判定
    # converted and any directory
    # return -> True(exist) / Fales(not exist)
    if not os.path.exists(path):
        return False
    else:
        return True