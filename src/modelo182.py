#!/usr/bin/env python
# coding: utf-8

# <div align="center">
# 
# <h1><font color='#fd7317'>Generación del modelo 182 a partir de los datos del fichero CSV de CALM</font></h1>
# <h3><font color='#999999'>(para la FPV)</font></h3>
# <img  width="100" src="https://www.hacienda.gob.es/es-ES/Prensa/En%20Portada/2020/PublishingImages/20181307_AEAT.jpg" />
# </div>

# ### Imports

# In[14]:


#Code tells you how; Comments tell you why."
#Esto es un cuaderno jupyter alojado en https://github.com/sscalvo/jupyter_modelo182
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import datetime

from builtins import str
import unidecode
import codecs
import os
from matplotlib import cm

# ### Definicion de Funciones propias ```validate_DNI_NIE()``` ```extract_DNI_dana()```

# Ojo! Verificar que los ficheros pasados a ```extract_DNI_dana()``` no tienen malformaciones: 
# <img src="img\error1.png" width="800">

# In[15]:


def validate_DNI_NIE(dni):
    '''
   Valida el documento, tanto extranjero como nacional

   :param: str filename: file name of the exported mod182 file 
   :return: True si es un fichero válido, False en caso contrario
   '''
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    dig_ext = "XYZ"
    reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
    numeros = "1234567890"
    dni = str(dni)
    dni = dni.upper()
    if len(dni) == 9:
        dig_control = dni[8]
        dni = dni[:8]
        if dni[0] in dig_ext:
            dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
        return len(dni) == len([n for n in dni if n in numeros])             and tabla[int(dni)%23] == dig_control
    return False


def extract_DNI_dana(filename, columns=["dni", "dana"]):
    '''
   Extracts DNI and dana from an 'oficial' modelo182 file

   :param str filename: file name of the exported mod182 file 
   :return: dataframe with columns ["dni", "dana"]
   '''
    dfprev = pd.read_csv(filename, skiprows=1, header=None)
    dni = dfprev[0].str[17:26] # dni
    dana = (dfprev.iloc[:, 0].str[84:96]).astype(float) / 100 # donation
    aux = pd.concat([dni, dana], axis=1)
    aux.columns = columns
    return aux
    

def unidecode_fallback(e):
    part = e.object[e.start:e.end]
    usuarios_error[e.start //251 +1] = part
    # print('💔' + "se ha liado: " + str(e.start) + " " + part)
    replacement = str(unidecode.unidecode(part) or '?')
    return (replacement, e.start + len(part))
    
# interaccion con FLASK:
def populate_CONSTS_from_request(request):
  EJERCICIO                       = request.form["ejercicio"]
  NIF_DECLARANTE                  = request.form["nif"]
  DENOMINACION_DECLARANTE         = request.form["denominacion"]
  PERSONA_CONTACTO                = request.form["persona"] 
  TELEFONO_CONTACTO               = request.form["telefono"]
  NUMERO_JUSTIFICANTE_DECLARACION = request.form["justificante"]
  ID_DECLARACION_ANTERIOR         = request.form["idAnterior"] 
 
  DECLARACION_COMPLEMENTARIA_O_SUSTITUTIVA = request.form["tipoDeclaracion"].replace("X"," ")


# ### Lectura de los CSV y Declaracion de CONSTANTES

# CONSTANTES anuales (actualizar cada año)
EJERCICIO = "2019"
NIF_DECLARANTE = "G17572108"
DENOMINACION_DECLARANTE = "FUNDACION PRIVADA VIPASSANA" # 40 carácteres
PERSONA_CONTACTO = "KARMASS MOHAMED"                    # 40 carácteres
TELEFONO_CONTACTO = "972426090"                         #  9 carácteres
NUMERO_JUSTIFICANTE_DECLARACION = "1822628017603"       # 13 carácteres
DECLARACION_COMPLEMENTARIA_O_SUSTITUTIVA = "  "         #  2 carácteres
ID_DECLARACION_ANTERIOR = '0' * 13                      # 13 carácteres
NATURALEZA_DECLARANTE = '1'                             #  1 carácteres
NIF_TITULAR_PATRIMONIO = ' ' * 9
APELLIDOS_NOMBRE_TITULAR_PATRIMONIO = ' ' * 40


# PATHs
FICHERO_CSV_ANIO_ACTUAL             = "calm4_dana_2019.csv"
FICHERO_EXPORTACION_ANIO_ANTERIOR   = "exportacion_2018.txt"
FICHERO_EXPORTACION_ANIO_ANTERIOR_2 = "exportacion_2017.txt"
FICHERO_COMUNIDADES_AUTONOMAS       = "cautonomas.csv"
FICHERO_PROVINCIAS                  = "provincias.tsv" #tab separated values

# CONSTANTES
TIPO_REGISTRO = "1" 
MODELO_DECLARACION = "182"
TIPO_SOPORTE = "T" 
IMPORTE_DONATIVOS = '0' * 15                            # 15 carácteres
NUM_TOTAL_REGISTROS_DECLARADOS = '0' * 9                #  9 carácteres
BLANCOS = ' ' * 28
SELLO_ELECTRONICO = ' ' * 13

# Global dict usado para gestión de errores en callback 'unidecode_fallback'
usuarios_error = {}   
# Global stats para almacenar informacion a mostrar
stats = {}

# Load files
def load_uploaded_files(paths):
    df = pd.read_csv(paths[0])
    dfyear1 = extract_DNI_dana(paths[1], columns=["dni1", "dana1"])
    dfyear2 = extract_DNI_dana(paths[2], columns=["dni2", "dana2"])
    return (df, dfyear1, dfyear2)

def load_local_dataframes(path):
    dfprov = pd.read_csv('.\\' + path + '\\' + FICHERO_PROVINCIAS, sep='\t', dtype=str) # tab sepparated values
    dfca = pd.read_csv('.\\' + path + '\\' + FICHERO_COMUNIDADES_AUTONOMAS, dtype=str)
    return (dfprov, dfca)
    
# ### REGISTRO TIPO 1 (pdf Hacienda, pág.2)

# In[17]:


def reg_tipo1(df):
    # Algunos campos necesitan ser calculados
    count = df.shape[0] 
    NUM_TOTAL_REGISTROS_DECLARADOS = '{0:0>9}'.format(count)
    IMPORTE_DONATIVOS = df["Donation Amount"].str[:-2].str.replace(".","").str.replace(",", ".").astype(float).sum()

    linea1  = TIPO_REGISTRO + MODELO_DECLARACION + EJERCICIO + NIF_DECLARANTE + '{0:<40}'.format(DENOMINACION_DECLARANTE)
    linea1 += TIPO_SOPORTE + '{0:<9}'.format(TELEFONO_CONTACTO) + '{0:<40}'.format(PERSONA_CONTACTO)
    linea1 += '{0:<13}'.format(NUMERO_JUSTIFICANTE_DECLARACION) + DECLARACION_COMPLEMENTARIA_O_SUSTITUTIVA
    linea1 += ID_DECLARACION_ANTERIOR + NUM_TOTAL_REGISTROS_DECLARADOS 
    linea1 += '{0:013.0f}'.format(IMPORTE_DONATIVOS) + '{0:.2f}'.format(IMPORTE_DONATIVOS)[-2:]
    linea1 += NATURALEZA_DECLARANTE + NIF_TITULAR_PATRIMONIO + APELLIDOS_NOMBRE_TITULAR_PATRIMONIO
    linea1 += BLANCOS + SELLO_ELECTRONICO
    
    add_stats("NUMERO DONACIONES", count, "Numero total de donaciones")
    add_stats("IMPORTE TOTAL", IMPORTE_DONATIVOS, "Suma de todas las donaciones")
    
    return linea1


# ### REGISTROS TIPO 2 (pdf Hacienda, pág.9)

# In[21]:


def reg_tipo2(path_downloads, df, dfyear1, dfyear2, dfprov, dfca):
    count = df.shape[0] 
    # REGISTROS TIPO 2 (pdf Hacienda, pág.9)
    row_beginning = "2" + MODELO_DECLARACION + EJERCICIO + NIF_DECLARANTE

    #Creacion e inicialización del DataFrame resultado
    #TIPO_DE_REGISTRO + MODELO_DECLARACION + EJERCICIO + NIF_DECLARANTE
    dflineas2 = pd.DataFrame(data=np.array([row_beginning] * count), columns=['Tipo2'], index=range(0,count))

    # 18-26 NIF_DECLARADO
    # @rosaura Poner dnis invalidos en blanco (' '*9)
    # Antes de aplicar 'validateDNI_NIE', eliminar ruido y sanear:
    dfaux = pd.DataFrame()
    dfaux["tmp"] = df["National Id"].str.replace(r'[\.\-\s\_]+', '', regex=True)
    dfaux["tmp"] = dfaux["tmp"].str.upper()
    # Validar los DNIs..
    dni_mask = dfaux["tmp"].apply(validate_DNI_NIE) 
    
    add_stats("DNI INVALIDOS", dni_mask.value_counts()[False], "Documentos de identidad NO válidos")
    add_stats("DNI VALIDOS", dni_mask.value_counts()[True], "Documentos de identidad válidos")
    
    # ..para poder poner los incorrectos en blanco
    dfaux.loc[~dni_mask, ["tmp"]] = ' ' * 9
    dflineas2["Tipo2"] += dfaux["tmp"]
    dflineas2.loc[2, "Tipo2"]

    # 25-37 NIF REPRESENTANTE LEGAL
    dflineas2["Tipo2"] += ' ' * 9

    # 36-75 APELLIDOS Y NOMBRE 
    dfaux["Tipo2"] = df["Family Name"].str.strip()  + ' ' + df["Given Name"].str.strip()
    dflineas2["Tipo2"] += ((dfaux["Tipo2"].str.upper()).str.ljust(40).str[:40])

    # 76-77 CODIGO DE PROVINCIA
    # MANY_TO_ONE MERGE
    dfaux = df.merge(dfprov, how="left",left_on="Address State", right_on="provincia")
    add_stats("MONEDA", pd.DataFrame(dfaux["Currency"].value_counts()).to_html(), "Distintos tipos de divisas usadas")
    dfaux["donacion"] = df["Donation Amount"].str[:-2].str.replace(".","").str.replace(",", ".").astype(float)
    # borrar: mask_nan = pd.isna(dfaux["Codigo"])   

    # Extranjeros: Sustituir NaN por valores que permitan agrupar y trabajar con ellos 
    dfaux.loc[ pd.isna(dfaux.cod_prov), ["provincia", "cod_prov", "cod_ca"]] = ["NO RESIDENTE", "99", "99"]
    
    dflineas2["Tipo2"]   += dfaux["cod_prov"]
    
    # ################################## PLOT #####################
    # PLOT Dana x Provincia: Preparar el dataset (limpiar 'dana', agrupar y sumar por CA, ordenar por dana decreciente)
    dfbydana = dfaux.merge(dfca, how="left",on="cod_ca")
    dfbydana = dfbydana.groupby(["comunidad"])["donacion"].sum().reset_index()
    dfbydana = dfbydana.sort_values(by = ['donacion'], ascending=[False]).reset_index(drop=True)

    color = cm.plasma_r(np.linspace(.4, .8, 30))
    x = [{i: dfbydana.loc[i,'donacion']} for i in range(len(dfbydana))]
    # BAR plot: Por 'Provincia' SIN extanjero
    dfplot = pd.DataFrame(x)
    ax = dfplot.plot(kind='bar',figsize=(12, 10), legend=True, fontsize=12, stacked=True ,color=color)
    #ax = dfxx.plot(kind='bar',figsize=(15, 10), legend=True, fontsize=12, stacked=True ,color=color)
    plt.xticks(range(0,len(dfbydana.comunidad)), dfbydana.comunidad, rotation=75)
    ax.set_xlabel("Provincia", fontsize=14)
    ax.set_ylabel("Donacion (eur)", fontsize=14)
    ax.set_title(EJERCICIO + "\nDonaciones agrupadas por Comunidades Autónomas", fontsize=14)
    plt.legend(["Donación (eur)"])
    plt.savefig('.\\' + path_downloads + '\\' + 'foo.png', bbox_inches='tight')
    # #############################################################

    # 78 CLAVE
    dflineas2["Tipo2"]   += 'A'

    # 79-83 PORCENTAJE DE DEDUCCION 
    # La formula corregida =IF((B4>=C4)AND(C4>=D4)AND(D4>0),1,0) 
    # Donantes que donaron este año y año anterior
    dfaux = df.merge(dfyear1, how="left",left_on="National Id", right_on="dni1")
    # Donantes que donaron este año y ahace 2 años
    dfaux = dfaux.merge(dfyear2, how="left",left_on="dni1", right_on="dni2")
    # Limpiar "Donation Amount"
    dfaux["dana0"] = dfaux["Donation Amount"].str[:-2].str.replace(".","").str.replace(",", ".").astype(float)
    # Donantes recurrentes (este añe & año pasado & hace 2 años
    mask_recurrentes = (~pd.isna(dfaux["dni2"])) & (dfaux["dana0"] >= dfaux["dana1"]) & (dfaux["dana1"] >= dfaux["dana2"]) & (dfaux["dana2"] > 0)
    add_stats("NUMERO RECURRENTES", mask_recurrentes.value_counts()[1], "Número de personas que han donado este año y los dos anteriores")
    # Apicar CRITERIO % DEDUCCION segun Agencia  Tributaria
    dfaux.loc[dfaux["dana0"] < 150, "deduc"] = "075"
    dfaux.loc[dfaux["dana0"] >= 150, "deduc"] = "030"
    dfaux.loc[mask_recurrentes, "deduc"] = "035"

    dflineas2["Tipo2"] += dfaux["deduc"] + "00"

    # 84-96 IMPORTE (84-94 importe, 95-96 decimales)
    dflineas2["Tipo2"] += dfaux["dana0"].map(lambda x: '{0:011.0f}'.format(x))
    dflineas2["Tipo2"] += dfaux["dana0"].map(lambda x: '{0:.2f}'.format(x)[-2:])

    # 97 EN ESPECIE
    dflineas2["Tipo2"] += " "

    # 98-99 DEDUCCION COMUNIDAD AUTONOMA
    # Buena explicacion de Rosaura para este campo y el siguiente
    # https://mail.google.com/mail/u/0/#inbox/KtbxLzGSwSkKnwnKzTckLzHcrzvFnzMMJB
    dflineas2["Tipo2"] += "  "

    # 100-104 % DEDUCCION COMUNIDAD AUTONOMA
    dflineas2["Tipo2"] += "     "

    # 105 NATURALEZA DEL DECLARADO
    dflineas2["Tipo2"] += "F"

    #106 REVOCACION (¿Siempre en blanco? SI)
    dflineas2["Tipo2"] += " "

    #107-110 REVOCACION 
    dflineas2["Tipo2"] += "0000"

    #111 TIPO DE BIEN
    dflineas2["Tipo2"] += " "

    #112-131 IDENTIFICACION DEL BIEN
    dflineas2["Tipo2"] += " " * 20

    #132 RECURRENCIA DONATIVOS
    # Forzar conversion de bool --> 1 ó 2
    dflineas2["Tipo2"] += (mask_recurrentes * -1 + 2).astype(str)

    #133-250 BLANCOS
    dflineas2["Tipo2"] += " " * 118
    return dflineas2
    
def unir(linea1, dflineas2):
    ### Putting all together: Añadir ```linea1``` on top de ```dfinal```
    dflineas2.loc[-1] = [linea1]  # adding a row
    dflineas2.index = dflineas2.index + 1  # shifting index
    dflineas2.sort_index(inplace=True)

    # dflineas2["Tipo2"] = dflineas2["Tipo2"].astype(str)
    #dflineas2.to_csv("lala.csv", header=None, columns=["Tipo2"], index=False, encoding="utf-8")
    return dflineas2

def convertir_iso8859(dfinal):
    ### Conversión a ISO-8859-1
    # Pasar a python list
    registros = dfinal.loc[:, "Tipo2"].astype(str).to_list()

    codecs.register_error('unidecode_fallback', unidecode_fallback)

    registros = "\n".join(registros)
    print(type(registros))
    s = registros.encode('iso-8859-1', errors='unidecode_fallback')
    #print(s.decode('iso-8859-1'))
    resultado = s.decode('iso-8859-1')
    return resultado

def save_to_file(texto):
    ### Guardar en fichero de texto
    date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "modelo182-" + EJERCICIO + "-" + date + ".txt"
    with open(filename, 'w') as out:
        out.write(texto)

    print(usuarios_error)
    return filename

def add_stats(key, value, description):
    stats[key] = (value, description)

def get_stats():
    return stats
    
# In[22]:


# df, dfyear1, dfyear2 = load_files()
# linea1    = reg_tipo1()
# dflineas2 = reg_tipo2()
# dfinal    = unir(linea1, dflineas2)
# errores   = convertir_iso8859(dfinal)


# In[ ]:




