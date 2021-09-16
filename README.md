# ScrapyNewsBot
## Table of Contents
1. [Info General](#info-general)
2. [Instalacion](#instalacion)
3. [Uso del Bot](#uso-del-bot)

### Info General 
***
Trabajo realizado para la catedra [Taller de Python y Aplicaciones](http://taller-de-python-y-aplicaciones.alumnos.exa.unicen.edu.ar/) de la Facultad de Ciencias Exactas - UNCPBA

Enlace al bot : https://t.me/ScrapyNews_bot

## Instalacion
***
El primer paso será instalar Python y algunas herramientas más:

* Python a partir de la versión 3.4
* El gestor de paquetes pip para Python
* El módulo venv
Para la instalación de Python es necesario seguir el siguiente link https://www.python.org/downloads/ e instalar segun sistema operativo.
```
# En la carpeta de nuestro proyecto 
# Crear entorno virtual
virtualenv venv
# Activar entorno virtual
source venv/bin/activate
# Instalar paquetes
pip install -r requirements.txt
```
Luego ejecutamos
```
# Para el Scraping
python scrap.py
# Para levantar el Bot
python scrapyBot.py
```
Si queremos que el scrapeo sea automatico podemos utilizar el administrador regular de procesos en segundo plano CRON que ejecuta procesos o guiones a intervalos regulares.
Cron existe para Sistemas Operativos Unix.
```
# Ejecutamos 
crontab -e
# Nos va a ofrecer un menu para seleccionar un editor de texto (VIM-Nano). Elegimos el que nos guste
# Debajo del documento escribimos
*/20 * * * * DirBinarioPython DirScrap/scrap.py
```
Lo que estamos haciendo es ejecutar cada 20 minutos el script python.
La direccion python, es la direccion donde esta el binario Python. Ejemplo: "/usr/bin/python"
Si queremos usar el entorno virtual la direccion de Python estará el CarpetaProyecto/venv/bin/python. Ejemplo "home/NombreUser/ScrapyNewsBot/venv/bin/python". Además es necesario agregar en el tope del archivo scrap.py. Siguiendo el ejemplo:
```
#!home/NombreUser/ScrapyNewsBot/venv/bin/python
```


## Uso del Bot
***
1. En Telegram buscamos ScrapyNews. El userName es @ScrapyNews_bot. Sino directamente desde el link: https://t.me/ScrapyNews_bot
2. Ponemos **/start** ó Iniciar(esta opción esta la primera vez que hay contacto con el bot en la version mobile) 
3. El bot da la bienvenida y da una breve explicación de uso del bot.
4. En caso de necesitar más información escribir el comando **/help**
5. Para usarlo es necesario escribir: sitio seccion. Sitios: Clarin Nacion Pagina - Secciones: Politica Economia Deportes Mundo
6. Podemos agregar una cantidad de noticias que queremos que van de 1 a 10. Si se inserta cualquier otra cantidad, el bot por default entrega solo una. Por ejemplo: Pagina Deportes 3 -> Entregara las ultimas 3 noticias de Deportes de Pagina12
