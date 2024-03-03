# モデルを数式に変換して、ウィンドウ上に表示する
# どのような形のモデルにも対応できるように変換する必要がある
# model -> latex -> png -> display(main.py)
# 数式を画像に変換して、main.pyに画像のpathを渡す
import matplotlib.pyplot as plt
import numpy as np

class Numeric_Formula:
    def convert_tex(formula_str):
        
        return 
    
    def tex_to_png(formula_str):
        fig = plt.figure()
        plt.axes("off")
        formula_tex = self.convert_tex(formula_str)
        plt.text(0.5, 0.5, f"${formula_tex}$", size=50, ha="center", va="center")

        png_path = "./converted/formula/result.png"
        plt.savefig(png_path, format="png", bbox_inches="tight", pad_inches=0.4)
        plt.close(fig)

        return png_path
    
        