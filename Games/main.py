# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime

import Convertidor , json

if __name__ == "__main__":
    
    
    list_data = json.load( open("2024-04-29__23_26_33~Steam.json","r") )
    #print( list_data )
    '''
    list_data = []
    list_data.append({"nombre":"Diego","DNI":155116015})
    list_data.append({"nombre":"Licandropo","DNI":555})
    list_data.append({"nombre":"River Plate","CUIL":8977856})
    list_data.append({"nombre":"Zapato","CUIT":666789113258,"Correo":["diego.xmen123@gmail.com"]})
    list_data.append({"nombre":"Ventilador","CUIT":4448911312,"Correo":"diego.xmen123@gmail.com","estudiante":True})
    list_data.append({"nombre":"Indeterminado","estudiante":False})
    '''
    obj_convert = Convertidor.Converter()
    obj_convert.converter_json_to_sqlite3( list_data , f'new_db.sqlite3' )