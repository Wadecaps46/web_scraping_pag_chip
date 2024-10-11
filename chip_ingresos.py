from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

import time 
import timeit
from IPython.display import clear_output
import glob
import os

# Configuración del servicio y opciones para el navegador Chrome
path = "El archivo chromedriver a instalar"
service = Service(path)
options = webdriver.ChromeOptions()

# Ruta de la carpeta que contiene los archivos a recorrer
path_carpeta = 'La ruta donde estan los archivos'
path_guardado = 'La ruta donde se guardaran cuando se termine el scraping'

files_ciclos = os.listdir(path_carpeta)
files_guardar = os.listdir(path_guardado)

# Verificar si el archivo ya ha sido procesado
def archivo_procesado(nombre_archivo):
    nombre_archivo_salida = f"{nombre_archivo.split('.')[0]}_ingresos_0406.csv"
    return nombre_archivo_salida in os.listdir(path_guardado)

columnas_de_interes = ['CODIGO', 'NOMBRE', 'codigo_fut', 'CIUDAD','RECAUDO VIGEN ACTUAL SIN FONDOS(Pesos)', 'RECAUDO VIGEN ACTUAL CON FONDOS(Pesos)', 'RECAUDO VIGEN ANTERIOR SIN FONDO(Pesos)', 'RECAUDO VIGEN ANTERIOR CON FONDO(Pesos)', 'TOTAL RECAUDO(Pesos)']
columnas_final = ['CODIGO', 'NOMBRE', 'codigo_fut','RECAUDO VIGEN ACTUAL SIN FONDOS(Pesos)', 'RECAUDO VIGEN ACTUAL CON FONDOS(Pesos)', 'RECAUDO VIGEN ANTERIOR SIN FONDO(Pesos)', 'RECAUDO VIGEN ANTERIOR CON FONDO(Pesos)', 'TOTAL RECAUDO(Pesos)']

periodo_interes = ["JUN A JUN - 2024"]

columna_tipo = "INGRESOS"
columna_year = "2024"
columna_periodo = "0406"
columna_orden = 0


# Inicialización del navegador Chrome y navegación a la página web
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
driver.get("https://www.chip.gov.co/schip_rt/index.jsf")

# Esperar hasta que se cargue el elemento y damo click para ir a la pág de filtros
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#j_idt105\:InformacionEnviada')))
pag_informacion_ciudadano = driver.find_element(By.CSS_SELECTOR, '#j_idt105\:InformacionEnviada')
pag_informacion_ciudadano.click()

# Inicio del contador de ciclos
contar_ciclos = 0

# Inicia el temporizador
inicio = timeit.default_timer()

# Donde se almacenara todas las filas de las entidades por ciclo
lista_filas = []

for file in files_ciclos:
    if os.path.isfile(os.path.join(path_carpeta, file)) and file.lower().endswith(".csv"):
        if not archivo_procesado(file):
            print(f"Procesando archivo: {file}")
            df_entidad = pd.read_csv(os.path.join(path_carpeta, file))
            if df_entidad.shape[0] <= 130: 
                for codigo in df_entidad['codigo_chip']:
                    for periodo in periodo_interes: 
                        contar_intentos = 0

                        # Filtro entidad, esperar a que aparezca y llenarlo 
                        while True:
                            try:
                                filtro_entidad = driver.find_element(By.CSS_SELECTOR, '#frm1\:SelBoxEntidadCiudadano_input')
                                filtro_entidad.clear() 
                                break
                            except Exception as e:
                                print(f"Elemento no encontrado: {e}")
                                time.sleep(6)
                        
                        # while True:
                        #     try:
                        #         filtro_entidad = driver.find_element(By.CSS_SELECTOR, '#frm1\:SelBoxEntidadCiudadano_input')
                        #         filtro_entidad.clear()
                        #         filtro_entidad.send_keys(codigo)
                        #         filtro_entidad.send_keys(Keys.ENTER)
                        #         break
                        #     except Exception as e:
                        #         print(f"Elemento no encontrado: {e}")
                        #         time.sleep(5)
                        while True:
                            try:
                                filtro_entidad = driver.find_element(By.CSS_SELECTOR, '#frm1\:SelBoxEntidadCiudadano_input')
                                
                                # Verificar si el campo de filtro está habilitado
                                if filtro_entidad.is_enabled():
                                    filtro_entidad.clear()
                                    filtro_entidad.send_keys(codigo)
                                    filtro_entidad.send_keys(Keys.ENTER)
                                    break
                                else:
                                    print("El campo de filtro de entidad está deshabilitado. Intentando de nuevo...")
                                    time.sleep(6)
                            except Exception as e:
                                print(f"Elemento no encontrado: {e}")
                                time.sleep(6)

                        # Filtro de categorias que es de elección, esperamos y seleccionamos
                        while True:
                            try:
                                filtro_categorias = Select(driver.find_element(By.CSS_SELECTOR, '#frm1\:SelBoxCategoria'))
                                filtro_categorias.select_by_visible_text(". : : Seleccione : : .")
                                break
                            except Exception as e:
                                print(f"Elemento no encontrado: {e}")
                                time.sleep(6)

                        while True:
                            try:
                                filtro_categorias = Select(driver.find_element(By.CSS_SELECTOR, '#frm1\:SelBoxCategoria'))
                                filtro_categorias.select_by_visible_text(". : : Seleccione : : .")
                                filtro_categorias.select_by_visible_text("CUIPO - CATEGORIA UNICA DE INFORMACION DEL PRESUPUESTO ORDINARIO")
                                break
                            except Exception as e:
                                print(f"Elemento no encontrado: {e}")
                                time.sleep(5)

                        # Filtro de periodo que es de elección, esperamos y seleccionamos    
                        while True:
                            try:
                                filtro_periodo = Select(driver.find_element(By.CSS_SELECTOR, '#frm1\:SelBoxPeriodo')) 
                                filtro_periodo.select_by_visible_text(". : : Seleccione : : .")
                                break
                            except Exception as e:
                                print(f"Elemento no encontrado: {e}")
                                time.sleep(5)

                        while True:
                            try:
                                trimestre = False
                                contar_intentos+=1
                                print(contar_intentos)
                                filtro_periodo = Select(driver.find_element(By.CSS_SELECTOR, '#frm1\:SelBoxPeriodo'))
                                filtro_periodo.select_by_visible_text(periodo)
                                break
                            except Exception as e:
                                print(f"Elemento no encontrado: {e}")
                                time.sleep(5)
                                trimestre = True
                            if contar_intentos >= 5:
                                contar_intentos = 0
                                driver.get("https://www.chip.gov.co/schip_rt/index.jsf")
                                driver.refresh()
                                time.sleep(6)
                                break

                        # Filtro de formulario que es de elección, esperamos y seleccionamos
                        if not trimestre:
                            while True:
                                try:
                                    print(filtro_periodo)
                                    filtro_formulario = Select(driver.find_element(By.CSS_SELECTOR, '#frm1\:SelBoxForma'))
                                    filtro_formulario.select_by_index(2)
                                    break
                                except Exception as e:
                                    print(f"Elemento no encontrado: {e}")
                                    time.sleep(4)

                            # Boton generar, para obtener la tabla
                            while True:
                                try:
                                    boton_consultar = driver.find_element(By.CSS_SELECTOR, '#frm1\:BtnConsular')
                                    boton_consultar.click()
                                    break
                                except Exception as e:
                                    print(f"Error: {e}")
                                    time.sleep(4)

                            # Elegir el nivel para que me muestre toda la tabla en esa página
                            while True:
                                try:
                                    nivel = Select(driver.find_element(By.CSS_SELECTOR, '#frm1\:SelBoxNivel'))
                                    total_opciones = len(nivel.options)
                                    nivel.select_by_index(total_opciones - 1)
                                    break
                                except Exception as e:
                                    print(f"Elemento no encontrado: {e}")
                                    time.sleep(4)

                            # Extraemos html de la tabla y convertimos a un objeto bs
                            while True:                                           
                                tabla_html = driver.find_element(By.CSS_SELECTOR, '#frm1\:j_idt222').get_attribute("outerHTML")
                                soup = BeautifulSoup(tabla_html, "html.parser")
                                filas = soup.find_all('tr')
                                if len(filas) > 3:
                                    break

                            # Extraemos columnas y filas
                            headers = [th.text.strip() for th in soup.find_all('th')]
                            rows = []
                            for tr in soup.find_all('tr'):
                                cells = [td.text.strip() for td in tr.find_all('td')]
                                rows.append(cells)

                            # Creamos dataframe para ver como salieron los datos con las columnas y filas
                            df_temp = pd.DataFrame(rows, columns=headers)
                            df_temp = df_temp.drop(0)
                            df_temp['codigo_fut'] = codigo
                            df_temp["CIUDAD"] = df_entidad.loc[df_entidad["codigo_chip"] == codigo, "Entidad"].values[0]

                            print(df_temp.shape)

                            # Revisamos si el el daframe cuenta con las columnas que queremos
                            columnas_dataframe = set(df_temp.columns)
                            columnas_de_interes = set(columnas_de_interes)
                            columnas_faltantes = columnas_de_interes - columnas_dataframe
                            print(columnas_faltantes)

                            if not columnas_faltantes:
                                df_temp = df_temp[columnas_final]
                            else:
                                for columna in columnas_faltantes:
                                    df_temp[columna] = np.nan
                                df_temp = df_temp[columnas_final]

                            lista_filas.extend(df_temp[columnas_final].to_numpy().tolist())

                            # Volvemos a la página para generar otra tabla
                            boton_volver = driver.find_element(By.CSS_SELECTOR, '#frm1\:j_idt148')
                            boton_volver.click()

                            contar_ciclos+=1
                            clear_output() 
                
                # Transformaciones
                df_final = pd.DataFrame(lista_filas, columns=columnas_final)
                print(df_final.shape)

                # Agregamos nuevas columnas necesarias
                df_final["tipo"] = columna_tipo
                df_final["anno"] = columna_year
                df_final["periodo"] = columna_periodo
                df_final['orden'] = columna_orden
                
                # Eliminamos las comas y puntos de las columnas para poder cambiar el tipo de dato 
                columnas_recaudo = ['RECAUDO VIGEN ACTUAL SIN FONDOS(Pesos)', 'RECAUDO VIGEN ACTUAL CON FONDOS(Pesos)', 
                    'RECAUDO VIGEN ANTERIOR SIN FONDO(Pesos)', 'RECAUDO VIGEN ANTERIOR CON FONDO(Pesos)', 
                    'RECAUDO VIGEN ANTERIOR CON FONDO(Pesos)', 'TOTAL RECAUDO(Pesos)']

                for col in columnas_recaudo:
                    df_final[col] = df_final[col].str.replace('[,. ]+', '', regex=True).replace('', '0')

                # Cmbiamos el tipo de datos int    
                for col in columnas_recaudo:
                    df_final[col] = pd.to_numeric(df_final[col], errors='coerce').fillna(0).astype('int64')
                    
                # Creaos 2 nuevas columnas, valor_actual (suma de recaudos actuales)  y valor_anterior (suma de reccaudos anteriores)
                df_final["valor_actual"] = df_final['RECAUDO VIGEN ACTUAL SIN FONDOS(Pesos)'] + df_final['RECAUDO VIGEN ACTUAL CON FONDOS(Pesos)']
                df_final["valor_anterior"] = df_final['RECAUDO VIGEN ANTERIOR SIN FONDO(Pesos)'] + df_final['RECAUDO VIGEN ANTERIOR CON FONDO(Pesos)']
                
                # Renombramos las columnas necesarias como nos indican
                df_final.rename(columns={'NOMBRE': 'Nombre', 'CODIGO': 'cuipo', 'TOTAL RECAUDO(Pesos)': 'valor'}, inplace=True)
                
                df_final = df_final.loc[:, ['tipo', 'codigo_fut', 'anno', 'periodo', 'cuipo', 'orden', 'Nombre', 'valor', 'valor_actual', 'valor_anterior']]
                
                nombre_archivo = file.split('.')[0]
                nuevo = f"{nombre_archivo}_ingresos_0406.csv"
                df_final.to_csv(f"{path_guardado}/{nuevo}", index=False)
                
                lista_filas.clear()
                df_final = pd.DataFrame()
        else:
            print(f"El archivo {file} ya ha sido procesado, se omite.")

driver.quit()
clear_output() 
                
# Fin del temporizador
fin = timeit.default_timer()
tiempo_ejecucion = fin - inicio
print(f"Tiempo de ejecución: {tiempo_ejecucion} segundos")
print(f'Hizo {contar_ciclos} ciclos')