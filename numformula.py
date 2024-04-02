# モデルを数式に変換して、ウィンドウ上に表示する
# どのような形のモデルにも対応できるように変換する必要がある
# model -> latex -> png -> display(main.py)
# 数式を画像に変換して、main.pyに画像のpathを渡す
import matplotlib.pyplot as plt


class Numeric_Formula:
    
    def tex_to_png():
        fig = plt.figure()
        ax = fig.add_subplot()

        fig.subplots_adjust(top=0.85)

        ax.axis([0, 10, 0, 10])
        ax.invert_yaxis()
        ax.axis("off")

        ax.text(0, 0, r'$E=mc^2$', style='italic',
            bbox={'facecolor': '#fff', 'alpha': 0.5, 'pad': 10})

        ax.text(0, 2, r'$E=mc^2$', style='italic',
            bbox={'facecolor': '#fff', 'alpha': 0.5, 'pad': 10})

        return fig
    
    
    
        