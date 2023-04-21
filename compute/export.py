# pip install compute_rhino3d and rhino3dm
import compute_rhino3d.Util
import compute_rhino3d.Grasshopper as gh
import rhino3dm
import json
import csv

compute_rhino3d.Util.url = 'http://localhost:8081/'


def build_tree(b1, b2, b3 , b4):
    # create DataTree for each input
    input_trees = []
    tree = gh.DataTree("b1")
    tree.Append([0], [b1])
    input_trees.append(tree)

    tree = gh.DataTree("b2")
    tree.Append([0], [b2])
    input_trees.append(tree)

    tree = gh.DataTree("b3")
    tree.Append([0], [b3])
    input_trees.append(tree)

    tree = gh.DataTree("b4")
    tree.Append([0], [b4])
    input_trees.append(tree)

    return input_trees


all_data = []

common_range= range(9,11)

for i in common_range:
    for j in common_range:
        for k in common_range:
            for l in common_range:
                input_trees = build_tree(i,j,k,l)

                output = gh.EvaluateDefinition('C:\\Users\\david\\IAAC\\workshops\\iaac-cardiff-automation\\compute\\automate02.gh', input_trees)

                feat = {}
                feat["b1"] = i
                feat["b2"] = j
                feat["b3"] = k
                feat["b4"] = l
                feat["vol"] = l

                values = output['values']
                for value in values:
                    name = value['ParamName']
                    inner_tree = value['InnerTree']
                    for path in inner_tree:
                        values_at_path = inner_tree[path]
                        for value_at_path in values_at_path:
                            data = value_at_path['data']
                            if isinstance(data, str) and 'archive3dm' in data:
                                obj = rhino3dm.CommonObject.Decode(json.loads(data))
                                print(name, obj)
                            else:
                                # print(name, data)
                                data = data.replace("'", '').replace('"', '')
                                data = float(data)
                                feat[name] = float(data)

                all_data.append(feat)


print(all_data)



with open('data.csv', 'w') as f:

    writer = csv.writer(f)

    header = [ 'b1', 'b2', 'b3', 'b4', 'vol', 'ratio']
    print(header)
    writer.writerow(header)

    for d in all_data:
        print (d.values())
        writer.writerow(d.values())