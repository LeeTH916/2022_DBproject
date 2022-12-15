import requests
import json
import sqlite3
import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from datetime import datetime

conn = sqlite3.connect("C:/Users/LeeTaeHUn/OneDrive - inu.ac.kr/Study/3-2/데이터베이스/DBproject.db")
curs = conn.cursor()

key = "35147faa392b90af8e94027a1380bd601a2cf624a399a320b0449554ced86cb3"

Uiform = uic.loadUiType("DBproject.ui")[0]

def valiable_Recipe(ingredient):
    url = f"http://211.237.50.150:7080/openapi/{key}/json/Grid_20150827000000000227_1/1/10?IRDNT_NM={ingredient}"
    res = requests.get(url)
    return res

def RequiredIngredient(RecipeID):
    url = f"http://211.237.50.150:7080/openapi/{key}/json/Grid_20150827000000000227_1/1/10?RECIPE_ID={RecipeID}"
    res = requests.get(url)
    return res

def Recipe(RecipeID):
    url = f"http://211.237.50.150:7080/openapi/{key}/json/Grid_20150827000000000228_1/1/1000?RECIPE_ID={RecipeID}"
    res = requests.get(url)
    return res

def Menu_All():
    url = f"http://211.237.50.150:7080/openapi/{key}/json/Grid_20150827000000000226_1/1/1000"
    res = requests.get(url)
    return res


class MainWindow(QMainWindow,Uiform):

    def __init__(self,*args, obj= None, **kwrgs):
        super(MainWindow,self).__init__(*args,**kwrgs)
        self.setupUi(self)

        response=Menu_All()
        if (response.status_code == 200):
            self.MenuList=response.json()['Grid_20150827000000000226_1']['row']
        else:
            print(f'Error code : {response}')

        result = curs.execute("select 이름 from MyIngredient where 분류='주재료'")
        conn.commit()
        self.MainIngredient = [ingredient[0] for ingredient in result]
        self.comboBox.addItem('')
        for name in self.MainIngredient:
            self.comboBox.addItem(name)

        
        self.comboBox.currentIndexChanged.connect(self.comboBoxFunction)
        self.comboBox_2.currentIndexChanged.connect(self.comboBox_2Function)
        self.pushButton.clicked.connect(self.pushButtonFunction)
        self.pushButton_2.clicked.connect(self.pushButton_2Function)
        self.pushButton_3.clicked.connect(self.pushButton_3Function)
        self.pushButton_4.clicked.connect(self.pushButton_4Function)
        self.pushButton_5.clicked.connect(self.pushButton_5Function)

    def comboBoxFunction(self):
        
        response = valiable_Recipe(self.comboBox.currentText())
        if (response.status_code == 200):
            RecipeType=[item['RECIPE_ID'] for item in response.json()['Grid_20150827000000000227_1']['row']]
        else:
            print(f'Error code : {response}')
        
        self.RecipeName_ID={item['RECIPE_NM_KO'] : item['RECIPE_ID'] for item in self.MenuList if item['RECIPE_ID'] in RecipeType}

        self.comboBox_2.clear() 
        for key in self.RecipeName_ID:
            self.comboBox_2.addItem(key)
    
    def comboBox_2Function(self):
        self.Recipe_ID = self.RecipeName_ID[self.comboBox_2.currentText()]

        response = RequiredIngredient(self.Recipe_ID)
        if (response.status_code == 200):
            IngredientList = {item['IRDNT_NM'] : item['IRDNT_CPCTY'] for item in response.json()['Grid_20150827000000000227_1']['row']}
        else:
            print(f'Error code : {response}')
        
        self.textBrowser.clear()
        self.textBrowser.append('필요한 재료 목록 : ')
        for key in IngredientList:
            self.textBrowser.append(key)

        result = curs.execute("select 이름 from MyIngredient")
        conn.commit()
        MyIngredient = [ingredient[0] for ingredient in result]

        Ingredient_to_buy = [key for key in IngredientList if key not in MyIngredient]
        tmp_str='\n'.join(Ingredient_to_buy)
        print_str='\n현재 없는 재료 : \n' + tmp_str
        self.textBrowser.append(print_str)
    
    def pushButtonFunction(self):
        self.textBrowser.clear()

        response = Recipe(self.Recipe_ID)
        if (response.status_code == 200):
            CookingProcess = {item['COOKING_NO'] : item['COOKING_DC'] for item in response.json()['Grid_20150827000000000228_1']['row']}
        else:
            print(f'Error code : {response}')
        
        for key,value in CookingProcess.items():
            print_str=f"{key}. {value}"
            self.textBrowser.append(print_str)
    
    def pushButton_2Function(self):
        self.textBrowser.clear()

        result = curs.execute("select 이름 from MyIngredient")
        conn.commit()
        MyIngredient = [ingredient[0] for ingredient in result]
        tmp_str='\n'.join(MyIngredient)
        print_str='현재 있는 재료 : \n' + tmp_str
        self.textBrowser.append(print_str)

    def pushButton_3Function(self):
        self.textBrowser.clear()

        result = curs.execute("select 이름,유통기한 from MyIngredient where 유통기한 not null order by 유통기한")
        conn.commit()

 
        for row in result:
            now=datetime.now()
            expiration_date = datetime.strptime(str(row[1]),"%Y%m%d")
            remaining_date = expiration_date - now
            if remaining_date.days <= 7:
                self.textBrowser.append(f'{row[0]} : {remaining_date.days}일')

    def pushButton_4Function(self):
        curs.execute(f"insert into MyIngredient values ('{self.lineEdit.text()}','{self.lineEdit_2.text()}',{int(self.lineEdit_3.text())},{int(self.lineEdit_4.text())})")
        conn.commit()
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
    
    def pushButton_5Function(self):
        curs.execute(f"delete from MyIngredient where 이름 = '{self.lineEdit_5.text()}'")
        conn.commit()
        self.lineEdit_5.clear()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   w=MainWindow()
   w.show()
   app.exec_()
   conn.close()
