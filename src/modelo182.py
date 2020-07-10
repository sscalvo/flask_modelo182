#Code tells you how; Comments tell you why."
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import datetime

def saluda():
    print("hola")
    return "si"

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
    dfprev = pd.read_csv(r'.\modelo182\\' + filename, skiprows=1, header=None)
    dni = dfprev[0].str[17:26] # dni
    dana = (dfprev.iloc[:, 0].str[84:96]).astype(float) / 100 # donation
    aux = pd.concat([dni, dana], axis=1)
    aux.columns = columns
    return aux
    


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
DIR_DATOS                           = "modelo182"
FICHERO_CSV_ANIO_ACTUAL             = "calm4_dana_2019.csv"
FICHERO_EXPORTACION_ANIO_ANTERIOR   = "exportacion_2018.txt"
FICHERO_EXPORTACION_ANIO_ANTERIOR_2 = "exportacion_2017.txt"

# CONSTANTES
TIPO_REGISTRO = "1" 
MODELO_DECLARACION = "182"
TIPO_SOPORTE = "T" 
IMPORTE_DONATIVOS = '0' * 15                            # 15 carácteres
NUM_TOTAL_REGISTROS_DECLARADOS = '0' * 9                #  9 carácteres
BLANCOS = ' ' * 28
SELLO_ELECTRONICO = ' ' * 13

# Load files
# df = pd.read_csv(r".\modelo182\Calm4AdHocReport_279_1579686916.csv")
df = pd.read_csv('.\\' + DIR_DATOS + '\\' + FICHERO_CSV_ANIO_ACTUAL)
dfyear1 = extract_DNI_dana(FICHERO_EXPORTACION_ANIO_ANTERIOR, columns=["dni1", "dana1"])
dfyear2 = extract_DNI_dana(FICHERO_EXPORTACION_ANIO_ANTERIOR_2, columns=["dni2", "dana2"])


# ### REGISTRO TIPO 1 (pdf Hacienda, pág.2)


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


# REGISTROS TIPO 2 (pdf Hacienda, pág.9)
row_beginning = "2" + MODELO_DECLARACION + EJERCICIO + NIF_DECLARANTE

#Creacion e inicialización del DataFrame resultado
#TIPO_DE_REGISTRO + MODELO_DECLARACION + EJERCICIO + NIF_DECLARANTE
dfinal = pd.DataFrame(data=np.array([row_beginning] * count), columns=['Tipo2'], index=range(0,count))

# 18-26 NIF_DECLARADO
# @rosaura Poner dnis invalidos en blanco (' '*9)
# Antes de aplicar 'validateDNI_NIE', eliminar ruido y sanear:
dfaux = pd.DataFrame()
dfaux["tmp"] = df["National Id"].str.replace(r'[\.\-\s\_]+', '', regex=True)
dfaux["tmp"] = dfaux["tmp"].str.upper()
# Validar los DNIs..
dni_mask = dfaux["tmp"].apply(validate_DNI_NIE) 
# ..para poder poner los incorrectos en blanco
dfaux.loc[~dni_mask, ["tmp"]] = ' ' * 9
dfinal["Tipo2"] += dfaux["tmp"]
dfinal.loc[2, "Tipo2"]

# 25-37 NIF REPRESENTANTE LEGAL
dfinal["Tipo2"] += ' ' * 9

# 36-75 APELLIDOS Y NOMBRE 
dfaux["Tipo2"] = df["Family Name"].str.strip()  + ' ' + df["Given Name"].str.strip()
dfinal["Tipo2"] += ((dfaux["Tipo2"].str.upper()).str.ljust(40).str[:40])


# 76-77 CODIGO DE PROVINCIA
dfprov = pd.read_csv(r".\modelo182\provincias.tsv", sep='\t', dtype=str) # tab sepparated values
# MANY_TO_ONE MERGE
dfaux = df.merge(dfprov, how="left",left_on="Address State", right_on="Provincia")
mask_nan = pd.isna(dfaux["Codigo"])   
dfaux.loc[mask_nan, "Codigo"] = "99" # Codigo por defecto para extranjeros
#dfaux["Codigo"] = dfaux["Codigo"].astype(int) #merge ha dejado decimales '.0'
dfinal["Tipo2"]   += dfaux["Codigo"]

# 78 CLAVE
dfinal["Tipo2"]   += 'A'


# ### 79-83 PORCENTAJE DE DEDUCCION
# ![image.png](img\porcentaje_deduccion.png)

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
# Apicar CRITERIO % DEDUCCION segun Agencia  Tributaria
dfaux.loc[dfaux["dana0"] < 150, "deduc"] = "075"
dfaux.loc[dfaux["dana0"] >= 150, "deduc"] = "030"
dfaux.loc[mask_recurrentes, "deduc"] = "035"

dfinal["Tipo2"] += dfaux["deduc"] + "00"


# 84-96 IMPORTE (84-94 importe, 95-96 decimales)
dfinal["Tipo2"] += dfaux["dana0"].map(lambda x: '{0:011.0f}'.format(x))
dfinal["Tipo2"] += dfaux["dana0"].map(lambda x: '{0:.2f}'.format(x)[-2:])

# 97 EN ESPECIE
dfinal["Tipo2"] += " "


# 98-99 DEDUCCION COMUNIDAD AUTONOMA
# Buena explicacion de Rosaura para este campo y el siguiente
# https://mail.google.com/mail/u/0/#inbox/KtbxLzGSwSkKnwnKzTckLzHcrzvFnzMMJB
dfinal["Tipo2"] += "  "

# 100-104 % DEDUCCION COMUNIDAD AUTONOMA
dfinal["Tipo2"] += "     "

# 105 NATURALEZA DEL DECLARADO
dfinal["Tipo2"] += "F"

#106 REVOCACION (¿Siempre en blanco? SI)
dfinal["Tipo2"] += " "

#107-110 REVOCACION 
dfinal["Tipo2"] += "0000"

#111 TIPO DE BIEN
dfinal["Tipo2"] += " "

#112-131 IDENTIFICACION DEL BIEN
dfinal["Tipo2"] += " " * 20

#132 RECURRENCIA DONATIVOS
# Forzar conversion de bool --> 1 ó 2
dfinal["Tipo2"] += (mask_recurrentes * -1 + 2).astype(str)

#133-250 BLANCOS
dfinal["Tipo2"] += " " * 118


# ### Putting all together: Añadir ```linea1``` on top de ```dfinal```

dfinal.loc[-1] = [linea1]  # adding a row
dfinal.index = dfinal.index + 1  # shifting index
dfinal.sort_index(inplace=True)

# dfinal["Tipo2"] = dfinal["Tipo2"].astype(str)
dfinal.to_csv("lala.csv", header=None, columns=["Tipo2"], index=False, encoding="utf-8")

# ### Conversión a ISO-8859-1

# Pasar a python list
registros = dfinal.loc[:, "Tipo2"].astype(str).to_list()

from builtins import str
import unidecode
import codecs

usuarios_error = {}

def unidecode_fallback(e):
    part = e.object[e.start:e.end]
    usuarios_error[e.start //251 +1] = part
    # print('💔' + "se ha liado: " + str(e.start) + " " + part)
    replacement = str(unidecode.unidecode(part) or '?')
    return (replacement, e.start + len(part))

codecs.register_error('unidecode_fallback', unidecode_fallback)

registros = "\n".join(registros)
s = registros.encode('iso-8859-1', errors='unidecode_fallback')
#print(s.decode('iso-8859-1'))
resultado = s.decode('iso-8859-1')


# ### Guardar en fichero de texto

# In[234]:


date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
with open("modelo182-" + EJERCICIO + "-" + date + ".txt", 'w') as out:
    out.write(resultado)
    
print(usuarios_error)





