import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#configuracion del navegador
options = webdriver.ChromeOptions()
options.add_argument("--starts-maximized")

#iniciamos el driver de Chrome con las opciones
driver = webdriver.Chrome(options=options)
#creamos un diccionario vacio para guardar los productos
todos_productos = []
url = "https://www.celudmovil.com.co/collections/coleccion-de-apple/apple"

try:
    print("cargando pagina...")
    driver.get(url)

    #configuramos un tiempo de espera para que cargue el navegador
    wait =  WebDriverWait(driver, 20)

    #esperamos que un elemento este en la pagina
    wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='grid-product__meta']"))

    )

    #buscamos todos los contenedores principales de los productos
    productos = driver.find_elements(By.XPATH,".//div[@class= 'grid-product__content']" )


    for producto in productos:
        try:
            #extraemos el titulo del texto dentro de la tarjerta
            titulo = producto.text.strip()
            tarjeta = producto.find_element(By.XPATH, ".//div[@class='grid-product__title']")

            #bucle para buscar el enlace del producto
            link = "N/A"
            for nivel in range(1,7):
                try:
                    enlace = producto.find_elements(By.XPATH, ".//a[@href]")

                    if enlace:
                        link = enlace[0].get_attribute("href")
                        break

                except Exception:
                    continue

            #extraccion del precio
            precio = "N/A"
            precios = producto.find_elements(By.XPATH, ".//span[contains(@class, 'sale-price')]")

            if precios:
                precio = precios[0].text.strip()


            #guardamos toda la informacion en el diccionario vacio
            todos_productos.append({
                "titulo": titulo,
                "precio": precio,
                "link":link
            })

        except Exception as e:
            print("error procesando los productos", e)

finally:
    #cerramos el navegador 
    driver.quit()

#creamos el dataFrame
df_apple = pd.DataFrame(todos_productos)
#mostramos las primeras filas del resultado
print(df_apple.head(10))    
