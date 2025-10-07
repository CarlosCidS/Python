import csv                   
import requests               
from bs4 import BeautifulSoup #obtener info mas especifica

def extraccion_html(url):
    #primero estraer contenido de una url
    #args: la url a descargar
    #returns: el contenido html de la pagina

    try:
        #configuracion User-Agent para evitar bloqueos
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Geko) Chrome/91.0.4472.124 Safari/537.36'
        }
        #Peticion GET
        respuesta = requests.get(url, headers=headers, timeout=10)

        if respuesta.status_code == 200:
            return respuesta.text
        else:
            print(f'Error al obtener la página: código de estado: {respuesta.status_code}')
            return None
    
    except Exception as e:
        print(f'Error en la obtención de la página: {e}')
        return None


def extraccion_titulares(html):
    #Crear el objeto BeautifulSoup para anlizar el html
    soup = BeautifulSoup(html, 'html.parser')
    titulos = []

    for heading in soup.find_all(['h1','h2','h3']):
        #Filtrar los que parecen ser titulares
        if heading.text.strip() and len(heading.text.strip()) > 15:
            titulos.append(heading.text.strip())
    #Elementos con clases comunes, que suelen usarse para titulos
    for elemento in soup.select('.title, .headline, .article-title, .news-title'):
        if elemento.text.strip() and elemento.text.strip() not in titulos:
            titulos.append(elemento.text.strip())

    return titulos


def extraccion_articulos(html):
    #Crear el objeto BeautifulSoup para analizar el html
    soup = BeautifulSoup(html, 'html.parser')
    articulos = []     

    #Elementos con clases comunes, que podrian ser articulos
    for articulo_elem in soup.select('article, .article, .post, .nes-item'):
        articulo = {}

        #Extraccion titulo
        titulo_elem = articulo_elem.find(['h1','h2','h3']) or articulo_elem.select_one('.title, .headline')
        if titulo_elem:
            articulo['titulo'] = titulo_elem.text.strip()
        else:
            continue  

        #Extraccion fecha 
        fecha_elem = articulo_elem.select_one('.date, .time, .published, .timestamp')
        articulo['fecha'] = fecha_elem.text.strip() if fecha_elem else ""

        #extraccion resumen
        resumen_elem = articulo_elem.select_one('.sumary, .excerpt, .description, .snippet, p')
        articulo['resumen'] = resumen_elem.text.strip() if resumen_elem else ""

        #Añadir a la lista de artiulos
        articulos.append(articulo)

    return articulos 


def guardar_csv(datos, nombre_archivo):
    try:
        if not datos:
            print('No se encontraron datos para almacenar.')
            return False
        
        #Obtencion de nombres de las columnas
        columnas = datos[0].keys()

        #escribir en el csv
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
            writer = csv.DictWriter(archivo_csv, fieldnames=columnas)
            writer.writeheader()        #escribir encabezados
            writer.writerows(datos)     #escribir fila datos

        print(f'Se guardo correctamente en {nombre_archivo}')
        return True
    
    except Exception as e:
        print(f'Error al guardar CSV: {e}')
        return False




def main():
    #funcion principal
    url = input('Ingresa la url que quieres consultar:')

    #Obtencion html de la pagina
    print(f'Descargando contenido de {url} ...')
    html = extraccion_html(url)

    if not html:
        print('Error. no se pudo obtener contenido')
        return
    print('Descarga Exitosa')

    #Menu opciones
    print('\nOpciones:')
    print('1. Extraer titulos de noticias')
    print('2. Extraer articulos completos')

    opcion = input('\nSelecciona opcion (1-2)')

    if opcion == '1':
        #extraccion titulos
        print('\nExtrayendo titulos...')
        titulos = extraccion_titulares(html)

        print(f'\nSe encontraron {len(titulos)} titulos:')
        for i, titulo in enumerate(titulos, 1):
            print(f'{i}. {titulo}')

        #guardar en CSV
        if titulos and input('\n ¿Desea Guardar titulos en archivo CSV? (s/n)').lower() == 's':
            #Convertir la lista de titulos a una lista de diccionarios
            datos = [{'numero': i, 'titulo':titulo} for i, titulo in enumerate(titulos, 1)]
            guardar_csv(datos, 'titulos_noticias.csv')

    elif opcion == '2':
        #extraer articulos
        print('\nExtrayendo articulos ...')
        articulos = extraccion_articulos(html)

        print(f'\nSe encontraron {len(articulos)} articulos.')
        for i, articulo in enumerate(articulos, 1):
            print(f'\n{i}. {articulo.get('titulo', 'Sin titulo')}')
            if articulo.get('fecha'):
                print(f'    Fecha: {articulo['fecha']}')
            if articulo.get('resumen'):
                print(f'    Resumen: {articulo['resumen'][:100]}...')

        #guardar en csv
        if articulos and input('\nDesea guardar articulos en archivo csv? (s/n)').lower():
            guardar_csv(articulos, 'articulos.csv')

    else:
        print('Opcion no encontrada')

if __name__ == '__main__':
    main()



