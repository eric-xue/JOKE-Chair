import json
from collections import OrderedDict
import xml.etree.ElementTree as ET


def pmmlToJson(pmmlFilePath, jsonFilePath):
    data_dict = OrderedDict()
    data_dict["PMML"] = OrderedDict()

    tree = ET.parse(pmmlFilePath)
    root = tree.getroot()
    data_dict['PMML']['version'] = root.attrib['version']
    data_dict['PMML']['x-baseVersion'] = root.attrib['version']
    for child in root:
        if child.tag == '{http://www.dmg.org/PMML-4_4}Header':
            for a in child:
                if a.tag == '{http://www.dmg.org/PMML-4_4}Application':
                    name = a.attrib['name']
                    version = a.attrib['version']
                if a.tag == '{http://www.dmg.org/PMML-4_4}Timestamp':
                    timestamp = a.text
            data_dict['PMML']['Header'] = OrderedDict({
                "Application": {
                    "name": name,
                    'version': version
                },
                "Timestamp": {
                    "content": [
                        timestamp
                    ]
                }
            })

        if child.tag == '{http://www.dmg.org/PMML-4_4}DataDictionary':
            data_field = []
            for a in child:
                entry = OrderedDict()
                for attrib in a.attrib:
                    entry[attrib] = a.attrib[attrib]
                if a.attrib['name'] == 'y':
                    entry["Value"] = []
                    for value_entry in a:
                        entry['Value'].append({
                            "value": value_entry.attrib['value']
                        })
                data_field.append(entry)
            data_dict['PMML']['DataDictionary'] = OrderedDict({
                "DataField": data_field
            })

        if child.tag == '{http://www.dmg.org/PMML-4_4}RegressionModel':
            regression_model = OrderedDict()
            for attrib in child.attrib:
                regression_model[attrib] = child.attrib[attrib]
            regression_model['MiningSchema'] = OrderedDict({
                "MiningField": []
            })
            regression_model['Output'] = OrderedDict({
                "OutputField": []
            })
            regression_model['RegressionTable'] = []
            for a in child:
                if a.tag == '{http://www.dmg.org/PMML-4_4}MiningSchema':
                    for entry in a:
                        mining_field = OrderedDict()
                        for attrib in entry.attrib:
                            mining_field[attrib] = entry.attrib[attrib]
                        regression_model['MiningSchema']['MiningField'].append(mining_field)
                if a.tag == '{http://www.dmg.org/PMML-4_4}Output':
                    for entry in a:
                        output_field = OrderedDict()
                        for attrib in entry.attrib:
                            output_field[attrib] = entry.attrib[attrib]
                        regression_model['Output']['OutputField'].append(output_field)
                if a.tag == '{http://www.dmg.org/PMML-4_4}RegressionTable':
                    regression_table = OrderedDict()
                    for attrib in a.attrib:
                        if attrib == 'intercept':
                            regression_table[attrib] = float(a.attrib[attrib])
                        else:
                            regression_table[attrib] = a.attrib[attrib]
                    regression_table['NumericPredictor'] = []
                    for entry in a:
                        numeric_predictor = OrderedDict()
                        for attrib in entry.attrib:
                            if attrib == 'coefficient':
                                numeric_predictor[attrib] = float(entry.attrib[attrib])
                            else:
                                numeric_predictor[attrib] = entry.attrib[attrib]
                        regression_table['NumericPredictor'].append(numeric_predictor)
                    regression_model['RegressionTable'].append(regression_table)
            data_dict['PMML']['Model'] = [{
                "RegressionModel": regression_model
            }]

    with open(jsonFilePath, 'w') as fp:
        json.dump(data_dict, fp)
    print(jsonFilePath + " created")


# pmmlToJson("lr.pmml", "lr.json")
