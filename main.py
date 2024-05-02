from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime
import pathlib , time , json , os , requests , random


BASE_DIR = pathlib.Path( __file__ ).parent.absolute()


def get_games_Steam( driver , max_games ):

	try:
		driver.get( "https://store.steampowered.com/search/" )
		#input("Espera...")
		div_result_search = driver.find_element( By.XPATH , './/div[@id="search_results"]' )
		
		list_results_games = []
		while max_games > len(list_results_games):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(3)
			list_results_games = div_result_search.find_elements( By.XPATH , '//a[contains(@class,"search_result_row")]' )
			print(f'Maximo Juegos: {max_games} ; Cantidad Obtenida: { len(list_results_games) }')

		Lista_Games_Validos = []
		for data_game in list_results_games:
			
			try:	
				nombre = data_game.find_element( By.XPATH , './/div[contains(@class," search_name ")]' ).text
				if len( nombre ) > 0:
					
					precio = data_game.find_element( By.XPATH , './/div[@class="discount_final_price"]' ).text
					try:
						porcentaje_descuento = data_game.find_element( By.XPATH , './/div[@class="discount_pct"]' ).text
					except:
						porcentaje_descuento = '-0%'
					url = data_game.get_attribute('href')
					
					precio = precio.replace("USD","").replace("$","").replace(" ","")
					precio = float(precio)
					
					meta_game = {
						"nombre":nombre,
						"precion":precio,
						"porcentaje_descuento":porcentaje_descuento,
						"url": url
						}
					Lista_Games_Validos.append( meta_game )
			except:
				pass
				
		return Lista_Games_Validos[0:max_juegos]

	except Exception as error:
		print( error )
		raise error


def get_games_Microsoft_Store( driver , max_games ):

	try:
		driver.get( "https://store.steampowered.com/search/" )
		#input("Espera...")
		div_result_search = driver.find_element( By.XPATH , './/div[@id="search_results"]' )
		
		list_results_games = []
		while max_games > len(list_results_games):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(3)
			list_results_games = div_result_search.find_elements( By.XPATH , '//a[contains(@class,"search_result_row")]' )

		Lista_Games_Validos = []
		for data_game in list_results_games:
			
			try:	
				nombre = data_game.find_element( By.XPATH , './/div[contains(@class," search_name ")]' ).text
				if len( nombre ) > 0:
					
					precio = data_game.find_element( By.XPATH , './/div[@class="discount_final_price"]' ).text
					try:
						porcentaje_descuento = data_game.find_element( By.XPATH , './/div[@class="discount_pct"]' ).text
					except:
						porcentaje_descuento = '-0%'
					url = data_game.get_attribute('href')
					
					precio = precio.replace("USD","").replace("$","").replace(" ","")
					precio = float(precio)
					
					meta_game = {
						"nombre":nombre,
						"precion":precio,
						"porcentaje_descuento":porcentaje_descuento,
						"url": url
						}
					Lista_Games_Validos.append( meta_game )
			except:
				pass
				
		return Lista_Games_Validos[0:max_juegos]

	except Exception as error:
		print( error )
		raise error


if __name__ == "__main__":

	# Config --->>>
	max_juegos = 3000
	# ---------->>>

	driver = webdriver.Chrome()
	
	try:
		list_juegos = get_games_Steam( driver , max_juegos )
	except:
		pass

	driver.quit()
		
	with open( f'Games/{str(datetime.now())[0:19].replace(":","_").replace(" ","__")}~Steam.json' , "w") as archivo:
		json.dump( list_juegos , archivo, indent=4 )
	