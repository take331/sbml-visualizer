import PySimpleGUI as sg
import tkinter as tk
import os

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'
# ツリーデータ作成用関数
def get_tree_data(parent, dirname):
    treedata = sg.TreeData()

    # https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Tree_Element.py#L26
    def add_files_in_folder(parent, dirname):

        files = os.listdir(dirname)
        for f in files:
            fullname = os.path.join(dirname, f)
            if os.path.isdir(fullname):
                treedata.Insert(parent, fullname, f, values=[], icon=folder_icon)
                add_files_in_folder(fullname, fullname)
            else:

                treedata.Insert(parent, fullname, f, values=[
                                os.stat(fullname).st_size], icon=file_icon)

    add_files_in_folder(parent, dirname)

    return treedata

# TODO: 機能を編集しやすいように、分割する
def get_layouts():
    # ============================-===
    #   function : back layout list
    #   layout structure : header_frame
    #                      operation_frame
    #                      main_frame
    # ================================

    # == option == #
    item_box_size = (5, None)
    value_box_size = (20, None)

    # == headers == #
    model_formula_header = [sg.Text("Model Formula", font=('', 10,'bold'))]
    model_catalog_header =  [sg.Text("Model Items", font=('', 10,'bold'))]
    network_header = [sg.Text("Network", font=('', 10, 'bold'))]
    graph_header = [sg.Text("Graph", font=('', 10, 'bold'))]
    animation_header = [sg.Text("Animation", font=('', 10, 'bold'))]
    tree_header = [sg.Text("Folder Tree", font=('', 10, 'bold'))]
    oprating_header = [sg.Text("Operating", font=('', 10, 'bold'))]
    tx1 = [sg.Text("change Items")]
    tx2 = [sg.Text("change Times")]

    # == header frame  == #
    header_elements = [
                        [sg.Image('assets\logo1.png', pad=((30, 70),(0,0))), 
                         sg.Input('import SBML file', key='-filepath_box-', text_color='#979897', disabled=True, size=(70, 1)),
                         sg.Button('Browse', key='open_browse', pad=(0,0)), 
                         sg.Button('Import', key='file_import', pad=(0,0)),
                         sg.Button('Submit', key='-submit-', pad=(0,0)),
                         sg.Button('Downloads', pad=(0,0)),
                         sg.Button('Usage', key='usage', pad=(0,0)),
                         sg.Button('Options',key='options', pad=(0,0)),
                         sg.Button('Exit', key='exit', pad=(0,0))],
                        [sg.HorizontalSeparator()]
                      ] 
    header_frame = sg.Frame("", header_elements, relief="flat", expand_x=True)

    cwd = os.getcwd()
    chdir = cwd + '\\' + 'inputs_model'
    print(chdir)
    tree_folder = [sg.Tree(data=get_tree_data("", chdir),
                headings=[],
                auto_size_columns=True,
                num_rows=24,
                col0_width=30,
                key="-TREE-",
                show_expanded=False,
                enable_events=True)]
    
    tree_frame_layout = [tree_header, tree_folder]
    
    tree_frame = sg.Frame("", tree_frame_layout, pad=(10,0), relief='flat')

    # operating frame
    # -- Change Value Box -- #
    change_item = [
                    sg.Input("", key='-selected_item_name-', disabled=False, size=item_box_size), 
                    sg.Spin("", key='-change_value-', disabled=False, size=value_box_size),
                    sg.Button('Update', key='-UPDATE_VALUES-', pad=(0,0))
                  ]
    operating_layout = [oprating_header, change_item]
    operating_frame = sg.Frame("", operating_layout, relief='flat', pad=((0,0), (0, 110)))

    # setting frame 
    setting_frame_layout = [[tree_frame],[operating_frame]]
    setting_frame = sg.Frame("", setting_frame_layout)
    
    # -- model formula -- #
    # num_formula = [sg.Image(size=(300, 150), key="-formula-", background_color='#F7F4F4')]
    num_formula = [sg.Multiline('<reactions>\n\n<assignments>', size=(40, 8), key="-formula-", disabled=True)]

    # --  Value Table -- #
    COL_HEADINGS = ["name", "type", "value"]
    ROW_DATA = [[]]
    model_catalog = [sg.Table(ROW_DATA, COL_HEADINGS, auto_size_columns=False, key='-model_catalog-', enable_events=True)]
    
    change_time = [
                    sg.Input("", key='-start-', disabled=False, size=item_box_size),
                    sg.Text("~"),
                    sg.Input("", key='-end-', disabled=False, size=item_box_size),
                  ]
    
    network_frame = [sg.Canvas(size=(300, 200), key="network_canvas", background_color='white')]
    
    # == operation frame == #
    operation_frame_layout = [
                            model_formula_header,
                            num_formula, 
                            model_catalog_header,
                            model_catalog,
                            network_header,
                            network_frame
                           ]

    operation_frame = sg.Frame("", operation_frame_layout, pad=0, element_justification="center")

    graph_frame = [sg.Canvas(size=(500, 280), key="graph", background_color='white')]
    animation_frame = [sg.Canvas(size=(500, 280), key="animation", background_color='white')]

    main_frame_layout = [
                           graph_header,
                           graph_frame, 
                           animation_header,
                           animation_frame
                        ]
    
    main_frame = sg.Frame("", main_frame_layout, expand_x=True, pad=(30,0), element_justification='center')

    layout = [
              [header_frame],
              [setting_frame, operation_frame, main_frame]
             ]

    return layout
