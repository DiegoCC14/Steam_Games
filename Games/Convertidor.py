# -*- coding: utf-8 -*-

import sqlite3


class Data_Columna():

    def __init__( self ):
        self.tipo_columna = None
        self.nivel_tipo_columna = 0 #Comenzamos por el tipo mas basico
        self.flujo = (-1) # int_float_string = 0 ; Booleano_string = 1
        self.lista_nivel_tipo_columna = [ [int,float,str] , [ bool , str ] ] #flujo 0 es pos=0, flujo 1 es pos=1

    def cambiar_tipo_dato_columna( self , tipo_dato ):

        if self.flujo==(-1):
            if type( tipo_dato ) == bool: # Se define el Flujo solo al principio
                self.flujo = 1 #Flujo bool -> string
            else: # no es bool entonces pasa a flujo int , float , string
                self.flujo = 0 #Flujo int -> float -> string

        lista_flujo = self.lista_nivel_tipo_columna[ self.flujo ] #Accedemos al flujo
        
        tipo_dato_fue_seleccionado = False
        for pos , nivel_tipo in enumerate( lista_flujo ):
            if type(tipo_dato) == nivel_tipo:
                if self.nivel_tipo_columna <= pos:
                    self.tipo_columna = nivel_tipo
                    self.nivel_tipo_columna = pos
                tipo_dato_fue_seleccionado = True
                break
        
        if tipo_dato_fue_seleccionado == False:
            self.nivel_tipo_columna = pos
            self.tipo_columna = nivel_tipo

    def get_tipo_columna( self ):
        return self.tipo_columna


class Converter():

    def __init__( self ):
        pass

    def __data_is_json_or_list_json( self , data ):
        
        if isinstance( data , dict ):
            return dict
        elif isinstance( data , list ):
            for item in data:
                if not( isinstance( item , dict ) ):
                    raise Exception("'data_json' is not of type json or list of valid json for method 'converter_json_to_sqlite3'")
            return list
        else:
            raise Exception("'data_json' is not of type json or list of valid json for method 'converter_json_to_sqlite3'")
    
    def __get_columns_and_type_to_list_json( self , list_json ):
        dicc_columns = {}
        for item in list_json:
            for key in item.keys():
                if str(key) not in dicc_columns:
                    dicc_columns[ str(key) ] = Data_Columna() #Instanciamos objeto columna

                obj_columna = dicc_columns[ str(key) ]
                obj_columna.cambiar_tipo_dato_columna( item[key] )

        for key , value in dicc_columns.items():
            dicc_columns[key] = value.get_tipo_columna()

        return dicc_columns

    def __creando_tabla( self , cursor , conexion , dicc_columnas ):
        SQL_Query = f'CREATE TABLE json_to_db ('
        for key,value in dicc_columnas.items():
            
            SQL_Query += f'{str(key)}'

            if value == str:
                SQL_Query += f' TEXT,'
            elif value == int:
                SQL_Query += f' INTEGER,'
            elif value == float:
                SQL_Query += f' REAL,'
            elif value == bool:
                SQL_Query += f' BLOB,'
        SQL_Query = SQL_Query[0:len(SQL_Query)-1] + ')'
        
        cursor.execute( SQL_Query )

    def __ingresando_registros_a_tabla( self , cursor , conexion , dicc_columnas , data_json ):

        SQL_Query = f'INSERT INTO json_to_db ('
        for key,value in dicc_columnas.items():
            SQL_Query += f'{key},'
        SQL_Query = SQL_Query[0:len(SQL_Query)-1] + ')'
        
        SQL_Query += ' VALUES '
        for data in data_json:
            
            SQL_Query += '('
            
            for key_columnas , value_columnas in dicc_columnas.items():
                
                data_columna_encontrado = False
                
                for key_data , value_data in data.items():

                    if str(key_data) == str(key_columnas):

                        if value_columnas == str:
                            if '"' in value_data:
                                value_data = value_data.replace('"',"'")
                                print( value_data )
                            SQL_Query += f'"{value_data}",'
                        elif value_columnas == int:
                            SQL_Query += f'{int(value_data)},'
                        elif value_columnas == float:
                            SQL_Query += f'{float(value_data)},'
                        elif value_columnas == bool:
                            SQL_Query += f'{bool(value_data)},'
                        
                        data_columna_encontrado = True
                        break

                if data_columna_encontrado == False:
                    SQL_Query += f'null,'

            SQL_Query = SQL_Query[0:len(SQL_Query)-1] + '),'

        SQL_Query = SQL_Query[0:len(SQL_Query)-1]
        #print( SQL_Query )
        cursor.execute( SQL_Query )
        conexion.commit()

    def converter_json_to_sqlite3( self , data_json , dir_outputh ):
        
        try:
            type_data = self.__data_is_json_or_list_json( data_json )    
            
            if type_data == dict:
                data_json = [ data_json ]

            dicc_columnas = self.__get_columns_and_type_to_list_json( data_json )
            
            conexion = sqlite3.connect( dir_outputh )
            cursor = conexion.cursor()
            
            self.__creando_tabla( cursor , conexion , dicc_columnas )
            
            self.__ingresando_registros_a_tabla( cursor , conexion , dicc_columnas , data_json )
            
            conexion.commit()
            conexion.close()
            
        except Exception as error:
            raise error

