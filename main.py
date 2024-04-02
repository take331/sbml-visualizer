import PySimpleGUI as sg
import tkinter as tk
from utils import layout, check_exist, info_holder, convert_file
from draw_network import NetworkDrawer
from numformula import Numeric_Formula
import os

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import igraph as ig



# GUIがぼやける現象を防ぐ
def make_dpi_aware():
    import ctypes
    import platform
    if int(platform.release()) >= 10:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
make_dpi_aware()


# sg.theme('LightBlue6')
layout = layout.get_layouts()
window = sg.Window('SBML Visualizer', layout, no_titlebar=True)
# window.maximize()

#TODO: アプリの解像度を上げる関数を実行するとウィンドウサイズがおかしくなる
# finalizeをfalseにすると解決するが、ウィンドウサイズを最大化することが出来ない

##### ----- elements ----- #####
fpbox_elem = window['-filepath_box-']
canvas_elem = window['network_canvas']
table_elem = window['-model_catalog-']
item_elem = window['-selected_item_name-']
value_elem = window['-change_value-']
formula_elem = window['-formula-']
graph_elem = window['graph']
ROW_DATA = None
file_path = None

# 描画用関数
def draw_canvas(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both')
    return figure_canvas_agg

def graph(g):
    fig = plt.Figure(figsize=(2,2))
    instance=fig.subplots()
    ig.plot(g, 
            vertex_size=30, 
            vertex_label=['C', 'M', 'X'],
            vertex_color = "white",
            target=instance)
    return fig

# イベントループ
while True:
    event, values = window.read()
    print(event)
    
    
    # =====================================
    #   browseボタンをクリックした際の処理 
    # =====================================
    if event == 'open_browse':
        file_path = tk.filedialog.askopenfilename()
        fpbox_elem.update(file_path, text_color='#000')

    # event = tree
    if event == '-TREE-':
        # クリックしたファイルのパスが欲しい
        file_path = values['-TREE-'][0]
        fpbox_elem.update(file_path, text_color='#000')
        # print(values['-TREE-'][0])



    # ===============================
    #   Importボタンを押した際の処理
    # ===============================
    if event == 'file_import':

        ### === importしたファイルの形式を確認 === ###
        if not check_exist.is_sbml_file(file_path):
            sg.popup('Not SBML File')
        
        # sbmltoodepyでモデルを変換 
        file_name = os.path.splitext(os.path.basename(file_path))[0] # file_pathからファイル名だけを抽出
        search_file_path = './converted/' + file_name
        # - 変換済みでない場合のみモデルを変換 - # 
        if not check_exist.check_exist(search_file_path):
            convert_file.Converter.file_convert(file_path)
            sg.popup("conversion success!")

        # - 変換したファイルのpath - #
        module_path = 'converted.' + file_name + '.pythonfile'
        json_file_path = './converted/' + file_name + '/jsonfile.json'
        
        ### --- 変換したファイルからデータを抽出して、Tableを更新 --- ###
        model_instance = info_holder.InfoHolder(module_path, json_file_path) # InfoHolderをインスタンス化(1回目)
        ROW_DATA = model_instance.insert_table_values()
        table_elem.update(ROW_DATA)

        # 数式の表示
        # formulas, assignments = info_holder.InfoHolder.get_formula(model_instance)
        formulas = info_holder.InfoHolder.get_formula(model_instance)
        for key in formulas.keys():
            formulas[key] = ' + '.join(formulas[key])
        
        formula_elem.update('\n'.join(formulas.values()))
        # formula_elem.update(('<reactions>\n' + '\n'.join(formulas) ) + '\n' + '\n<assignments>\n' + '\n'.join(assignments))

        fig2 = Numeric_Formula.tex_to_png()
        draw_canvas(window['graph'].TKCanvas, fig2)

        # ネットワーク図を表示
        g = NetworkDrawer(model_instance).draw_network()
        figure_canvas_agg = FigureCanvasTkAgg(graph(g), master=canvas_elem.TKCanvas)
        figure_canvas_agg.get_tk_widget().pack()

        

    # ===============================
    #   Updateボタンを押した際の処理
    # ===============================
    # TODO: 空の表を選択した際のエラー 
    if event == '-model_catalog-' and values['-model_catalog-'] != []:
        selected_row = values['-model_catalog-'] #選択した行を取得
        print(selected_row)
        selected_row_name =ROW_DATA[int(selected_row[0])][0] #選択した行のnameの値を取得
        selected_row_value = ROW_DATA[int(selected_row[0])][2]
        item_elem.update(selected_row_name)
        value_elem.update(selected_row_value)

    if event == '-UPDATE_VALUES-':
        print(values['-selected_item_name-'])
        print(values['-model_catalog-'])

        new_name = values['-selected_item_name-'] 
        new_value = values['-change_value-']
        default_type = ROW_DATA[int(selected_row[0])][1]
        update_data = [new_name, default_type, new_value]
        ROW_DATA[values['-model_catalog-'][0]] = update_data
        
        table_elem.update(values=ROW_DATA, select_rows=values['-model_catalog-'])
    
    # =================================
    #   Simulateボタンを押した際の処理
    # =================================
    '''
    # Tableデータを使ってシミュレーションを行い、アニメーションを作成
    # ネットワーク図からノードの座標を受け取って、反映させる
    if event == 'simulate':
    '''
    
    def make_win2():
        layout = [[sg.Text('This is the second window')],
                  [sg.Button('Exit')]]
        return sg.Window('second Window', layout, finalize=True)
    
    # =====================
    #   Usageボタンの処理
    # =====================
    if event == 'usage':
        window2 = make_win2()

    # ========================
    #  アプリケーションの終了
    # ========================
    if event == sg.WIN_CLOSED:
        break

    if event == 'exit':
        break

window.close()