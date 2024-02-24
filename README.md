#  Extracción de datos de la página web del CHIP: Consolidador de Hacienda e Información Pública

## Descripción:
Este proyecto automatiza la extracción de datos de recaudo del portal web del CHIP (Consolidador de Hacienda e Información Pública). El script utiliza Selenium para interactuar con el navegador web y BeautifulSoup para analizar el HTML de la página.

## Funcionalidades:
- Permite seleccionar la entidad territorial de interés.
- Filtra por categoría, periodo y formulario.
- Extrae los datos de recaudo en diferentes formatos:
    Tabla HTML: Se guarda en la variable tabla_html.
    DataFrame de Pandas: Se guarda en la variable df_final.
    Lista de filas: Se guarda en la variable lista_filas.

Tener en cuenta que el archivo de cod_entidades.xlsx es el que permite hacer el ciclo y llenar el filtro de entidad, donde hay más de 1000 entidades.

## Requisitos:
- Python 3.8 o superior
- Librerías:
  Selenium
  BeautifulSoup
  Pandas
  NumPy

## Limitaciones:
- El script solo funciona para el portal web del CHIP de Colombia.
- Es posible que el script no funcione correctamente si el diseño del portal web cambia.

## Contacto:
Si tienes preguntas o sugerencias, puedes contactarme a través de la plataforma de GitHub.
