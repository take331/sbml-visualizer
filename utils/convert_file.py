# get_values.pyが受け取ったファイルが存在しない場合に動作
# sbmltoode@yを使ってファイルを変換

import sbmltoodepy
from utils import make_dir as mk
import os

class Converter:
    def file_convert(file_path):
        # convertedディレクトリが存在しない場合のみ作成
        mk.convdir()    
        # converted下に、ファイル名のディレクトリを作成
        dir_name = os.path.splitext(os.path.basename(file_path))[0]
        mk.anydir(dir_name)

        ifp = file_path
        pfp = "./converted/" + dir_name + "/pythonfile.py"
        cn = "ModelName"
        jfp = "./converted/" + dir_name + "/jsonfile.json"
        sbmltoodepy.ParseAndCreateModel(ifp, outputFilePath=pfp, className = cn, jsonFilePath=jfp)