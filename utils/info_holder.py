# psg_main.pyのImportイベント発生時に動作
# 変換されたファイルから必要な情報を抽出して、ひとまとめにする
# Tableの更新やネットワークの作成に必要なすべての情報を保持する

import importlib
import json
import re


def instance_class(module_path, calss_name):
    # クラスをインスタンス化
    module = importlib.import_module(module_path)
    my_class = getattr(module, calss_name)
    instance = my_class()

    return instance

def load_json(json_file_path):
    with open(json_file_path) as jfp:
        di = json.load(jfp)
    return di

class InfoHolder:
    def __init__(self, module_name, json_file_path):
        # 変換したファイルのクラスをインスタンス化
        self.model_instance = instance_class(module_name, "ModelName")
        self.species = [s for s in self.model_instance.s.keys()]
        self.parameters = [p for p in self.model_instance.p.keys()]
        self.reactions = [r for r in self.model_instance.r.keys()]

        self.di = load_json(json_file_path)

        # assignmentRulesの取得
        self.assignment_num = len(self.di["assignmentRules"])
        self.assignment_dict = dict()
        for a in range(1, self.assignment_num+1):
            self.assignment_dict[self.di["assignmentRules"][str(a)]["variable"]] = self.di["assignmentRules"][str(a)]["math"] # ex.{V1:"C * VM1 * (C + Kc)^-1"}

        self.nodes = self.species
        self.edges = []

    def insert_table_values(self):
        # Importした際にTableに挿入する値を返す
        # model_instance = instance_class(module_name, "ModelName")
        info_array = []
        
        # species
        # s_names = [s for s in self.model_instance.s.keys()]
        for i in self.species:
            tmp  =[i, "species", self.model_instance.s[i].amount]
            info_array.append(tmp)

        # prameters
        # p_names = [p for p in self.model_instance.p.keys()]
        for i in self.parameters:
            tmp = [i, "parameter", self.model_instance.p[i].value]
            info_array.append(tmp)

        return info_array
    
    def get_node(self):
        return self.nodes
    
    def get_edge(self):
        for i in self.reactions:
            species = [s for s in self.species]
            reactants = self.di["reactions"][i]["reactants"]
            ratelaw = self.di["reactions"][i]["rateLaw"] # 項
            pnm = reactants[0][0] # 1.0 or -1.0
            reactant = reactants[0][1] # 反応分子

            react_idx = species.index(reactant)
            species.pop(react_idx) # 調べる項の分子以外のリストを作る

            for i, j in self.assignment_dict.items():
                pattern = re.compile(i)
                match = pattern.search(ratelaw)
                if match:
                    ratelaw = re.sub(i, j, ratelaw)

            # ratelaw = self.deep_law(ratelaw, self.assignment_dict)
            for j in species:
                if j in ratelaw:
                    self.edges.append([j, reactant])
    
        return self.edges
    
    def get_formula(self):
        formula = []
        assignment = []
        reactants = dict()

        for i in self.species:
            reactants[i] = []
        
        """
        for r in self.reactions:
            formula.append(self.di["reactions"][str(r)]["rateLaw"])
        for a in range(1, self.assignment_num+1):
            assignment.append(self.di["assignmentRules"][str(a)]["math"])
        return formula, assignment
        """
        for r in self.reactions:
            pm = self.di["reactions"][str(r)]["reactants"][0][0]
            parent = self.di["reactions"][str(r)]["reactants"][0][1]
            
            if pm < 0:
                reactants[parent].append('-1.0 * ' + self.di["reactions"][str(r)]["rateLaw"])
            else:
                reactants[parent].append(self.di["reactions"][str(r)]["rateLaw"])
            
        return reactants
