#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'king-jojo'

import AST_Compare
from AST_Visualization import node_graph
from AST2JSON import to_json, to_dict, to_init_dict
from AST_Process import Node_extract
import sys
import os
import re
import json
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))

RE_AZ = re.compile(r'-(.*?) ')
RE_C = re.compile(r'/(.*?).c')

RE_MODULE1 = re.compile(r'from (.*?) to')
RE_MODULE2 = re.compile(r'to (.*)')

sel = True

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)>0:
        if args[0] == '--compare':
            if len(args[1:]) == 3:
                if args[3] != 'True' and args[3] != 'False':
                    raise SystemExit("Please use 'True' or 'False' to choose whether you need to remove the headers")
                else:
                    if args[3] == 'True':
                        sel = True
                    else:
                        sel = False
                if os.path.exists(args[1]) and os.path.exists(args[2]):
                    code_path_a = args[1]
                    code_path_b = args[2]
                    seq1 = AST_Compare.seq_process(code_path_a, sel)
                    seq2 = AST_Compare.seq_process(code_path_b, sel)
                    set = AST_Compare.Seqlist_compare(seq1, seq2)
                    node_graph(code_path_a, sel, set[0])
                    node_graph(code_path_b, sel, set[1])
                if not os.path.exists(args[1]) and os.path.exists(args[2]):
                    raise SystemExit("Error: Could not find the first h/c/c++ file")
                if not os.path.exists(args[2]) and os.path.exists(args[1]):
                    raise SystemExit("Error: Could not find the second h/c/c++ file")
                if not os.path.exists(args[1]) and not os.path.exists(args[2]):
                    raise SystemExit("Error: Could not find both two files")
            else:
                raise SystemExit("Usage: python main.py --compare c_file_dir1 c_file_dir2 True/False ")
        elif args[0] == '--view':
            if len(args[1:]) == 2:
                if args[2] != 'True' and args[2] != 'False':
                    raise SystemExit("Please use 'True' or 'False' to choose whether you need to remove the headers")
                else:
                    if args[2] == 'True':
                        sel = True
                    else:
                        sel = False
                if os.path.exists(args[1]):
                    code_path_a = args[1]
                    seq1 = AST_Compare.seq_process(code_path_a, sel)
                    node_graph(code_path_a, sel, None)
                else:
                    raise SystemExit("Error: Could not find h/c/c++ file")
            else:
                raise SystemExit("Usage: python main.py --view c_file_dir True/False ")
        elif args[0] == '--tojson':
            if len(args[1:]) == 2:
                if args[2] != 'True' and args[2] != 'False':
                    raise SystemExit("Please use 'True' or 'False' to choose whether you need to remove the headers")
                else:
                    if args[2] == 'True':
                        sel = True
                    else:
                        sel = False
                if os.path.exists(args[1]):
                    code_path = args[1]
                    code_path_list = []
                    names = []
                    json_files_dir = dir_path + '/jsons'
                    if not os.path.exists(json_files_dir):
                        os.mkdir(json_files_dir)
                    # json_file1 is a nested dict
                    json_file1 = json_files_dir + '/AST.json'
                    # json file2 is the trace of each node
                    json_file2 = json_files_dir + '/trace.json'
                    # json file3 restore the name of each module
                    json_file3 = json_files_dir + '/Module_names.json'
                    # json file4 restore the unnested dict
                    json_file4 = json_files_dir + '/uAST.json'
                    if '.c' in code_path or '.cpp' in code_path or '.h' in code_path or '.hpp' in code_path:
                        code_path_list.append(code_path)
                        node_list, name_all, node_list1 = Node_extract(code_path, sel)
                        node_list.insert(0, code_path)
                        names.append(name_all)
                        to_json(node_list, json_file1, False)
                        uAST = to_init_dict(node_list1, 0)[1]
                        print ('The total amount of the nodes is {}'.format(len(node_list1)))
                        with open(json_file3, 'w+') as f:
                            json.dump(names, f, ensure_ascii=False, indent=4)
                        f.close()
                        with open(json_file4, 'w+') as f1:
                            json.dump(uAST, f1, ensure_ascii=False, indent=4)
                        f1.close()
                        print ("The json file path: "+json_files_dir)
                    else:
                        json_list = []
                        AST_patch = []
                        node_len = 0
                        g = os.walk(code_path)
                        for path, di, filelist in g:
                            for filename in filelist:
                                k = os.path.join(path, filename)
                                suffix = os.path.splitext(k)[1]
                                if suffix == '.c' or suffix == '.cpp' or suffix == '.h' or suffix == '.hpp':
                                    code_path_list.append(k)
                        for i in range(len(code_path_list)):
                            node_list1, name_all, node_list = Node_extract(code_path_list[i], sel)
                            uAST = to_init_dict(node_list, i)[1]
                            AST_patch.append(uAST)
                            names.append(name_all)
                            name = code_path_list[i]
                            node_list1.insert(0, name)
                            json_list.append(node_list1)
                            node_len += len(node_list1)
                        print ('The total amount of the nodes is {}'.format(node_len))
                        with open(json_file3, 'w+') as f:
                            json.dump(names, f, ensure_ascii=False, indent=4)
                        f.close()
                        with open(json_file4, 'w+') as f1:
                            json.dump(AST_patch, f1, ensure_ascii=False, indent=4)
                        f1.close()
                        to_json(json_list, json_file1, True)
                        print ("The json file path: "+json_files_dir)
                    code_path_file = dir_path + "/jsons/file_path.json"
                    with open(code_path_file, 'w+') as f:
                        json.dump(code_path_list, f, ensure_ascii=False, indent=4)
                    f.close()
                else:
                    raise SystemExit("Error: Could not find h/c/c++ file")
            else:
                raise SystemExit("Usage: python main.py --tojson c_file_dir True/False")
        elif args[0] == '--multdir':
            if len(args[1:]) == 4:
                if args[4] != 'True' and args[4] != 'False':
                    raise SystemExit("Please use 'True' or 'False' to choose whether you need to remove the headers")
                else:
                    if args[4] == 'True':
                        sel = True
                    else:
                        sel = False
                json_files_dir = dir_path + '/jsons'
                # json_file1 is a nested dict
                json_file1 = json_files_dir + '/AST.json'
                # json file2 is the trace of each node
                json_file2 = json_files_dir + '/trace.json'
                # json file3 restore the name of each module
                json_file3 = json_files_dir + '/Module_names.json'
                # json file4 restore the unnested dict
                json_file4 = json_files_dir + '/uAST.json'
                json_list = []
                AST_patch = []
                code_path_list = []
                names = []
                count = 0
                node_len = 0
                for dir_index in range(len(args[1:4])):
                    if os.path.exists(args[1+dir_index]):
                        code_path = args[1+dir_index]
                        path_list = []
                        if not os.path.exists(json_files_dir):
                            os.mkdir(json_files_dir)
                        g = os.walk(code_path)
                        for path, di, filelist in g:
                            for filename in filelist:
                                k = os.path.join(path, filename)
                                suffix = os.path.splitext(k)[1]
                                if suffix == '.c' or suffix == '.cpp' or suffix == '.h' or suffix == '.hpp' or suffix == '.cc':
                                    path_list.append(k)
                        code_path_list += path_list
                        for i in range(len(path_list)):
                            node_list1, name_all, node_list = Node_extract(path_list[i], sel)
                            uAST = to_init_dict(node_list, count)[1]
                            count += 1
                            AST_patch.append(uAST)
                            names.append(name_all)
                            name = path_list[i]
                            node_list1.insert(0, name)
                            json_list.append(node_list1)
                            node_len += len(node_list1)
                    else:
                        raise SystemExit("Error: Could not find h/c/c++ file")
                print ('The total amount of the nodes is {}'.format(node_len))
                with open(json_file3, 'w+') as f:
                    json.dump(names, f, ensure_ascii=False, indent=4)
                f.close()
                with open(json_file4, 'w+') as f1:
                    json.dump(AST_patch, f1, ensure_ascii=False, indent=4)
                f1.close()
                to_json(json_list, json_file1, json_file2, True)
                print ("The json file path: "+json_files_dir)
                code_path_file = dir_path + "/jsons/file_path.json"
                with open(code_path_file, 'w+') as f:
                    json.dump(code_path_list, f, ensure_ascii=False, indent=4)
                f.close()
            else:
                raise SystemExit("Usage: python main.py --multdir c_file_dir1 c_file_dir2 c_file_dir3 True/False")
        elif args[0] == '--combine':
            if len(args[1:]) == 2:
                if args[2] != 'True' and args[2] != 'False':
                    raise SystemExit("Please use 'True' or 'False' to choose whether you need to remove the headers")
                else:
                    if args[2] == 'True':
                        sel = True
                    else:
                        sel = False
                if os.path.exists(args[1]):
                    code_path = args[1]
                    node_graph(code_path, sel, None)
                else:
                    raise SystemExit("Error: Could not find the file")
            else:
                raise SystemExit("Usage: python main.py --combine c_file_dir1 c_file_dir2 True/False ")
        elif args[0] == '--find_module':
            if len(args[1:]) == 2:
                if args[2] != 'True' and args[2] != 'False':
                    raise SystemExit("Please use 'True' or 'False' to choose whether you need to remove the headers")
                else:
                    if args[2] == 'True':
                        sel = True
                    else:
                        sel = False
                if len(args[1]) != 10:
                    raise SystemExit("Please use the right LINE_ID like 0000010001, for the first 6 characters represent the line number and the last 4 characters represent the file number")
                else:
                    if os.path.exists(dir_path + '/jsons/AST.json') and os.path.exists(dir_path + '/jsons/file_path.json'):
                        Input_id = args[1]
                        Input_line = int(Input_id[0:8])
                        Input_file = int(Input_id[8:16])
                        max = 0
                        count = 0
                        with open(dir_path + '/jsons/file_path.json') as f1:
                            file_path_list = json.load(f1)
                        f1.close()
                        if Input_file >= len(file_path_list):
                            raise SystemExit("The file number is too large")
                        file_name = file_path_list[Input_file]
                        node_list = Node_extract(file_name,sel)[2]
                        node_list_new = to_init_dict(node_list, Input_file)[1]
                        print ("###############The Result################")
                        print (str(file_name) + ":" + str(Input_line))
                        for i in range(1, len(node_list_new)):
                            line_range = node_list_new[i]['coord']
                            if line_range != 'null' :
                                if line_range[0] != 'null' and line_range[1] != 'null' :
                                    first_line = line_range[0]
                                    last_line = line_range[1]
                                    line_number1 = int(first_line[0:8])
                                    line_number2 = int(last_line[0:8])
                                    if line_number2 > max :
                                        max = line_number2
                                    if line_number1 != line_number2:
                                        if line_number1 <= Input_line and Input_line <= line_number2:
                                            print ("This module's node type is: %s "%(node_list_new[i]['_nodetype']))
                                            print ("This module's coordinate is: %s "%(node_list_new[i]['coord']))
                                            print ("This module's name is: %s "%(node_list_new[i]['node_name']))
                                            count = count + 1
                        if count == 0:
                            print ("No module satisfied")
                        if Input_line > max:
                            raise SystemExit("The line number is too large \n#########################################")
                        print ("#########################################")
                    else:
                        raise SystemExit("Please generate json files first with '--tojson' ")
            else:
                raise SystemExit("Usage: python main.py --find_module LINE_ID True/False")
        else:
            raise SystemExit("Usage: python main.py --compare c_file_dir1 c_file_dir2 True/False \n       python main.py --view c_file_dir True/False \n       python main.py --tojson c_file_dir True/False \n       python main.py --combine c_file_dir1 c_file_dir2 True/False \n       python main.py --find_module LINE_ID True/False \n       python main.py --multdir c_file_dir1 c_file_dir2 c_file_dir3 True/False  ")
    else:
        raise SystemExit("Usage: python main.py --compare c_file_dir1 c_file_dir2 True/False \n       python main.py --view c_file_dir True/False \n       python main.py --tojson c_file_dir True/False \n       python main.py --combine c_file_dir1 c_file_dir2 True/False \n       python main.py --find_module LINE_ID True/False \n       python main.py --multdir c_file_dir1 c_file_dir2 c_file_dir3 True/False  ")
