  
import requests
import json
import pandas as pd
from openpyxl import load_workbook
import os
import sys


#Pass as argument the filename of the txt containing the ids

excel_columns = ['MalwareType', 'Family', 'ID', 'T1001','T1002','T1003','T1004','T1005','T1006','T1007','T1008','T1009','T1010','T1011','T1012','T1013','T1014','T1015','T1016','T1017','T1018','T1019','T1020','T1021','T1022','T1023','T1024','T1025','T1026','T1027','T1028','T1029','T1030','T1031','T1032','T1033','T1034','T1035','T1036','T1037','T1038','T1039','T1040','T1041','T1042','T1043','T1044','T1045','T1046','T1047','T1048','T1049','T1050','T1051','T1052','T1053','T1054','T1055','T1056','T1057','T1058','T1059','T1060','T1061','T1062','T1063','T1064','T1065','T1066','T1067','T1068','T1069','T1070','T1071','T1072','T1073','T1074','T1075','T1076','T1077','T1078','T1079','T1080','T1081','T1082','T1083','T1084','T1085','T1086','T1087','T1088','T1089','T1090','T1091','T1092','T1093','T1094','T1095','T1096','T1097','T1098','T1099','T1100','T1101','T1102','T1103','T1104','T1105','T1106','T1107','T1108','T1109','T1110','T1111','T1112','T1113','T1114','T1115','T1116','T1117','T1118','T1119','T1120','T1121','T1122','T1123','T1124','T1125','T1126','T1127','T1128','T1129','T1130','T1131','T1132','T1133','T1134','T1135','T1136','T1137','T1138','T1139','T1140','T1141','T1142','T1143','T1144','T1145','T1146','T1147','T1148','T1149','T1150','T1151','T1152','T1153','T1154','T1155','T1156','T1157','T1158','T1159','T1160','T1161','T1162','T1163','T1164','T1165','T1166','T1167','T1168','T1169','T1170','T1171','T1172','T1173','T1174','T1175','T1176','T1177','T1178','T1179','T1180','T1181','T1182','T1183','T1184','T1185','T1186','T1187','T1188','T1189','T1190','T1191','T1192','T1193','T1194','T1195','T1196','T1197','T1198','T1199','T1200','T1201','T1202','T1203','T1204','T1205','T1206','T1207','T1208','T1209','T1210','T1211','T1212','T1213','T1214','T1215','T1216','T1217','T1218','T1219','T1220','T1221','T1222','T1223','T1480','T1482','T1483','T1484','T1485','T1486','T1487','T1488','T1489','T1490','T1491','T1492','T1493','T1494','T1495','T1496','T1497','T1498','T1499','T1500','T1501']


key = ""
headers = {"Authorization": "Bearer " + key}

def main():

    path = sys.argv[1]
    with open(path) as f:
        contents = f.readlines()
    base = os.path.basename(path)
    filename = os.path.splitext(base)[0]

    name = filename.split("_")

    i=0
    for s_id in contents:
        s_id = s_id.strip('\n')
        excel_final = load_workbook("./dataset.xlsx")
        # Select First Worksheet
        sheet = excel_final.worksheets[0]
        new_row = [0]*247
        #The elements are stored by Family
        new_row[0] = name[0]
        new_row[1] = name[1]
        #The elements are also stored by ID
        with open('./sample_ids.txt') as f:
            if (s_id in f.read()):
                found_id = 0
                print(s_id + " Already in excel sheet")
            else:
                found_id = 1
                with open('./sample_ids.txt', 'a') as f:
                    f.write(s_id + '\n')
        if(found_id == 1):
            print (s_id  + " Added")
            new_row[2] = s_id
            #Request the data of that specific ID
            url ='https://api.tria.ge/v0/samples/'+ s_id  +'/overview.json'
            print(url)
            response = requests.get(url, headers=headers).json()

            for value1, content in response.items():
                if(value1 == "signatures"):
                    for dicts_signatures in content:
                        for ttps, number in dicts_signatures.items():
                            if (ttps == "ttp"):
                                for ttp_number in number:
                                    if ttp_number in excel_columns:
                                        new_row[excel_columns.index(ttp_number)] = 1

            sheet.append(new_row)
            excel_final.save("./dataset.xlsx")
            i=i+1;


if __name__ == "__main__":
    main()