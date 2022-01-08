# sscalvo@gmail.com
# 05/08/2020
#Code tells you how; Comments tell you why."
#Esto proviene de un cuaderno jupyter alojado en https://github.com/sscalvo/jupyter_modelo182
import pandas as pd
import numpy as np
import datetime

from builtins import str
import unidecode
import codecs
import os
import json
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


# Global dict usado para gestión de errores en callback 'unidecode_fallback'
usuarios_error = {}
# Global stats para almacenar informacion a mostrar
stats = {}

# Debe ejecutarse primero, por que los demas metodos hacen uso de esas CONSTANTES:
def load_form_fields(form):

    params = {
        "EJERCICIO"                                : str(form.ejercicio.data),
        "NIF_DECLARANTE"                           : form.NIF.data,
        "DENOMINACION_DECLARANTE"                  : form.denominacion.data,
        "PERSONA_CONTACTO"                         : form.persona.data,
        "TELEFONO_CONTACTO"                        : str(form.telefono.data),
        "NUMERO_JUSTIFICANTE_DECLARACION"          : str(form.justificante.data),
        "ID_DECLARACION_ANTERIOR"                  : str(form.idAnterior.data),
        "DECLARACION_COMPLEMENTARIA_O_SUSTITUTIVA" : form.tipoDeclaracion.data.replace('X',' '),
        "FICHERO_COMUNIDADES_AUTONOMAS"            : "cautonomas.csv",
        "FICHERO_PROVINCIAS"                       : "provincias.tsv", #tab separated values
        "TIPO_REGISTRO"                            : '1',
        "MODELO_DECLARACION"                       : '182',
        "TIPO_SOPORTE"                             : 'T',
        "IMPORTE_DONATIVOS"                        : '0' * 15,         # 15 carácteres
        "NUM_TOTAL_REGISTROS_DECLARADOS"           : '0' * 9,          #  9 carácteres
        "BLANCOS"                                  : ' ' * 28,
        "SELLO_ELECTRONICO"                        : ' ' * 13,
        "NATURALEZA_DECLARANTE"                    : '1',              #  1 carácteres
        "NIF_TITULAR_PATRIMONIO"                   : ' ' * 9,
        "APELLIDOS_NOMBRE_TITULAR_PATRIMONIO"      : ' ' * 40,
    }

    return params

# Load files
def load_uploaded_files(paths, params, recurrencias):
    df = pd.read_csv(paths[0])  # Before PATCH '001A'
    ####### PARCHE '001A' : CAMBIO de CABECERAS nativo en CALM (detectado en Sept 2020)
    # Viejas cabeceras:   ["National Id","Family Name","Given Name","Address State","Donation Amount","Currency"]
    # Nuevas cabeceras:   ["Documento nacional de identidad","Apellido","Nombre","Estado fiscal","Cantidad para donación","Moneda"]
    #######
    keep_using_old_cabeceras = ["National Id","Family Name","Given Name","Address State","Donation Amount","Currency"]
    current_cabeceras = list(df.columns)
    #df = pd.read_csv(paths[0], names=keep_using_old_cabeceras, header=0) # After PATCH '001A'
    if current_cabeceras != keep_using_old_cabeceras:
        df.rename(columns = dict(zip(current_cabeceras, keep_using_old_cabeceras)) , inplace = True)

    dfyear1, dfyear2 = None, None
    # print(df.columns)
    if recurrencias:
        dfyear1 = extract_DNI_dana(paths[1], columns=["dni1", "dana1"])
        dfyear2 = extract_DNI_dana(paths[2], columns=["dni2", "dana2"])
    return (df, dfyear1, dfyear2)

def load_local_dataframes(path, params): # + os.path.sep + 'mod182' + os.path.sep + 'probando.tsv'
    # print('load_local_dataframes(): ', path)
    dfprov = pd.read_csv(os.path.join(path, 'mod182' + os.path.sep + params['FICHERO_PROVINCIAS']), sep='\t', dtype=str) # tab sepparated values
    dfca = pd.read_csv(os.path.join(path, 'mod182' + os.path.sep + params['FICHERO_COMUNIDADES_AUTONOMAS']), dtype=str) # tab sepparated values
    return (dfprov, dfca)

# ### REGISTRO TIPO 1 (pdf Hacienda, pág.2)

# In[17]:


def reg_tipo1(df, p):
    # Algunos campos necesitan ser calculados
    count = df.shape[0]
    NUM_TOTAL_REGISTROS_DECLARADOS = '{0:0>9}'.format(count)
    IMPORTE_DONATIVOS = df["Donation Amount"].str[:-2].str.replace(".","").str.replace(",", ".").astype(float).sum()

    linea1  = p["TIPO_REGISTRO"] + p["MODELO_DECLARACION"] + p["EJERCICIO"] + p["NIF_DECLARANTE"]
    linea1 += '{0:<40}'.format(p["DENOMINACION_DECLARANTE"])
    linea1 += p["TIPO_SOPORTE"] + '{0:<9}'.format(p["TELEFONO_CONTACTO"]) + '{0:<40}'.format(p["PERSONA_CONTACTO"])
    linea1 += '{0:<13}'.format(p["NUMERO_JUSTIFICANTE_DECLARACION"]) + p["DECLARACION_COMPLEMENTARIA_O_SUSTITUTIVA"]
    linea1 += p["ID_DECLARACION_ANTERIOR"] + NUM_TOTAL_REGISTROS_DECLARADOS
    linea1 += '{0:013.0f}'.format(IMPORTE_DONATIVOS) + '{0:.2f}'.format(IMPORTE_DONATIVOS)[-2:]
    linea1 += p["NATURALEZA_DECLARANTE"] + p["NIF_TITULAR_PATRIMONIO"] + p["APELLIDOS_NOMBRE_TITULAR_PATRIMONIO"]
    linea1 += p["BLANCOS"] + p["SELLO_ELECTRONICO"]

    add_stats("NUMERO DONACIONES", count, "Numero total de donaciones")
    add_stats("IMPORTE TOTAL", IMPORTE_DONATIVOS, "Suma de todas las donaciones")

    return linea1


# ### REGISTROS TIPO 2 (pdf Hacienda, pág.9)

# In[21]:


def reg_tipo2(charts, df, dfyear1, dfyear2, dfprov, dfca, p, hay_recurrencias):
    count = df.shape[0]
    # REGISTROS TIPO 2 (pdf Hacienda, pág.9)
    row_beginning = "2" + p["MODELO_DECLARACION"] + p["EJERCICIO"] + p["NIF_DECLARANTE"]

    #Creacion e inicialización del DataFrame resultado
    #TIPO_DE_REGISTRO + MODELO_DECLARACION + EJERCICIO + NIF_DECLARANTE
    dflineas2 = pd.DataFrame(data=np.array([row_beginning] * count), columns=['Tipo2'], index=range(0,count))

    # 18-26 NIF_DECLARADO
    # @rosaura: Poner dnis invalidos en blanco (' '*9)
    # Antes de aplicar 'validateDNI_NIE', eliminar ruido y sanear:
    dfaux = pd.DataFrame()
    dfaux["dni"] = df["National Id"].str.replace(r'[\.\-\s\_]+', '', regex=True)
    dfaux["dni"] = dfaux["dni"].str.upper()

    # @@@ GRAFICO   !!LINEA POSICIONAL: Necesita dfaux sin el apply(validate_DNI_NIE) !!
    charts.append(get_json_plot_num_donaciones_persona(dfaux, p)) #no modifica dfaux

    # Validar los DNIs..
    mask_dni = dfaux["dni"].apply(validate_DNI_NIE)
    
    # Para sacar un listado de aquellos DNI que se han eliminado (en realidad mantenido pero puesto en blanco) 
    # aa = df[~mask_dni].to_html()
    # print(aa)
    # with open("eliminados.txt", "w", encoding='utf-8') as f:
        # f.write(aa)

    # @@@ GRAFICO   !!LINEA POSICIONAL: Necesita el apply(validate_DNI_nie)
    charts.append( get_json_plot_identificacion(mask_dni, dfaux, p) )
    # print(charts)
    # # # # # # # # # # # # # # # # # # # # # # # # #  print("fin reg_tipo2")

    # ..para poder poner los incorrectos en blanco
    dfaux.loc[~mask_dni, ["dni"]] = ' ' * 9
    dflineas2["Tipo2"] += dfaux["dni"]


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
    # import random
    # import time
    # from matplotlib import cm

    # dfbydana = dfaux.merge(dfca, how="left",on="cod_ca")
    # dfbydana = dfbydana.groupby(["comunidad"])["donacion"].sum().reset_index()
    # dfbydana = dfbydana.sort_values(by = ['donacion'], ascending=[False]).reset_index(drop=True)
    # xkcd_row = random.randint(0,len(dfbydana)-1)
    # xkcd_ca, xkcd_dana = dfbydana.loc[xkcd_row, ["comunidad", "donacion"]]
    #plt.xkcd()

    # color = cm.plasma_r(np.linspace(.4, .8, 30))
    # x = [{i: dfbydana.loc[i,'donacion']} for i in range(len(dfbydana))]
    # BAR plot: Por 'Provincia' SIN extanjero
    # dfplot = pd.DataFrame(x)
    # ax = dfplot.plot(kind='bar',figsize=(12, 10), legend=True, fontsize=12, stacked=True ,color=color)
    #ax = dfxx.plot(kind='bar',figsize=(15, 10), legend=True, fontsize=12, stacked=True ,color=color)
    # plt.xticks(range(0,len(dfbydana.comunidad)), dfbydana.comunidad, rotation=75)
    # ax.set_xlabel("Comunidad Autónoma", fontsize=14)
    # ax.set_ylabel("Donacion (eur)", fontsize=14)
    # ax.set_title(p["EJERCICIO"] + "\nDonaciones agrupadas por COMUNIDADES AUTONOMAS")
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # plt.legend(["Donacion (eur)"])
    # plt.annotate('DONANTE ANONIMO\nDE ' + xkcd_ca.upper() + '...  GRACIAS!', xy=(xkcd_row, xkcd_dana // 2), arrowprops=dict(arrowstyle='->'), xytext=(10, 80000))
    # TODO: Decidir que nombre ponerle al fichero
    ######## 17/09/2020 NO DEBERIAMOS ESCRIBIR MAS IMAGENES EN EL SERVER-SIDE ##########plt.savefig(os.path.join(path_img, 'foo.png'), bbox_inches='tight')
    # plt.close(None)
    #os.rename(img_path, img_path + "?" + str(time.time()))
    # #############################################################

    # 78 CLAVE
    dflineas2["Tipo2"]   += 'A'

    # 79-83 PORCENTAJE DE DEDUCCION
    mask_recurrentes = pd.Series([False] * len(df)) # Declare mask as Falses (in case there are no recurrencias)
    if hay_recurrencias:
        # La formula corregida =IF((B4>=C4)AND(C4>=D4)AND(D4>0),1,0)
        # Donantes que donaron este año y año anterior
        dfaux = df.merge(dfyear1, how="left",left_on="National Id", right_on="dni1")
        # Donantes que donaron este año y hace 2 años
        dfaux = dfaux.merge(dfyear2, how="left",left_on="dni1", right_on="dni2")
        # Limpiar "Donation Amount"
        dfaux["dana0"] = dfaux["Donation Amount"].str[:-2].str.replace(".","").str.replace(",", ".").astype(float)
        # Donantes recurrentes (este añe & año pasado & hace 2 años
        mask_recurrentes = (~pd.isna(dfaux["dni2"])) & (dfaux["dana0"] >= dfaux["dana1"]) & (dfaux["dana1"] >= dfaux["dana2"]) & (dfaux["dana2"] > 0)
        if len(mask_recurrentes.value_counts()) > 1:
            add_stats("NUMERO RECURRENTES", mask_recurrentes.value_counts()[1], "Número de personas que han donado este año y los dos anteriores")
        # Apicar CRITERIO % DEDUCCION segun Agencia  Tributaria
        dfaux.loc[dfaux["dana0"] < 150, "deduc"] = "080"  # Updated jan 2021 "075"
        dfaux.loc[dfaux["dana0"] >= 150, "deduc"] = "035" # Updated jan 2021 "030"
        dfaux.loc[mask_recurrentes, "deduc"] = "040"      # Updated jan 2021 "035"
        dflineas2["Tipo2"] += dfaux["deduc"] + "00"
    else:
        dfaux["dana0"] = df["Donation Amount"].str[:-2].str.replace(".","").str.replace(",", ".").astype(float)
        dflineas2["Tipo2"] += "03500"

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
    #print(type(registros))
    s = registros.encode('iso-8859-1', errors='unidecode_fallback')
    #print(s.decode('iso-8859-1'))
    resultado = s.decode('iso-8859-1')
    return resultado

def get_json_plot_identificacion(mask_dni, dfbydni, p):
    '''
    Estructura del json generada:
        {
            "labels": ["ID Valido\\n(NACIONAL)", "Id Invalido\\n(EXTRANJERO ?)", "En BLANCO\\n(Anonimo)"],
            "percent":   [66.2, 30.2, 3.6],
            "values":    [2058.0, 940.0, 112.0]
            "descriptions":    ["Con DNI/NIE", "Documento malformado o no reconocido", "Campo en blanco (no relleno)"]
            "tooltips":    ["2058 donantes (54%)", "940 donantes (23%)", "112 donantes (5%)"]
        }
    '''
    # conceptualmente no eliminamos los duplicados, pues al fin y al cabo son tambien donaciones
    # bydni = bydni.drop_duplicates(subset='dni') #eliminar dups
    # bydni = bydni[(~bydni.duplicated()) | (bydni['dni'].isnull())] # alternativa a drop_dups manteniendo  NaN
    # TIPOS DE DONANTES: A)Con ID valido  B)Con ID invalido (¿extranjeros?)  C)anonimos (originalmente NaN)
    # Los NaN, que serán catalogados como "anonimo"
    num_donantes = len(dfbydni);
    mask_C = pd.isna(dfbydni["dni"])
    mask_A = mask_dni
    mask_B = ~(mask_A | mask_C)  # element-wise NOR
    # Vamos a verbalizarlo..
    dfbydni.loc[mask_A, "Identificacion"] = "ID Valido"
    dfbydni.loc[mask_B, "Identificacion"] = "Id Invalido"
    dfbydni.loc[mask_C, "Identificacion"] = "En BLANCO"
    # Porcentajes
    dfflat = (dfbydni["Identificacion"].value_counts()).to_list();
    dfnorm = (dfbydni["Identificacion"].value_counts(normalize=True) * 100).round(decimals=1).to_list();
    result_json = { 'labels': ['VALIDO', 'INVALIDO', 'ANONIMO' ],
         'percent': dfnorm,
         'values': dfflat,
         'descriptions': ["Con DNI/NIE\n(Nacional)", "Documento malformado o no reconocido", "En blanco (sin rellenar)"]}
    result_json['title'] =   "¿Cómo se identifican los donantes?"
    result_json['tooltips'] =   [  str(x[0]) + " donantes (" + str(x[1])  + "%)" for x in zip(dfflat, dfnorm) ]

    if len(dfnorm) > 1:
        result_json['description'] = "De las " + str(len(dfbydni)) + " donaciones recibidas durante en el año " + p["EJERCICIO"] + ", el " + str(dfnorm[1]) + "% se ha identificado con un documento no reconocido (documento extranjero, DNI escrito incorrectamente, etc)";
    result_json['label_yAxes'] = "Número de personas"
    result_json['label_xAxes'] = "Identificación"
    result_json['custom_yAxes_type'] = 'linear'
    # print(result_json)
    return result_json

def get_json_plot_num_donaciones_persona(dfbydni, p):
    bydni = dfbydni.groupby("dni")["dni"].count().sort_values(ascending=False).reset_index(name="num. donaciones");
    num_donantes = len(bydni);
    bydni = bydni.groupby("num. donaciones")["num. donaciones"].count().sort_values(ascending=False).reset_index(name="personas")
    list_donaciones = bydni["num. donaciones"].to_list()
    list_personas = bydni["personas"].to_list()
    list_porcentaje = (100. * bydni["personas"] / bydni["personas"].sum()).round(2).to_list()
    result_json = { 'tooltips': [ "(" + str(x) + "%)" for x in list_porcentaje ],
         'donaciones': list_donaciones,
         'values': list_personas,
         'descriptions': [  str(x[1]) + (" persona donó " if x[1] == 1 else " personas donaron ")  + str(x[0])  + " ve" + ("z" if x[0] == 1 else "ces") for x in zip(list_donaciones, list_personas) ]
    }
    result_json['title'] =   "Donantes reincidentes en " + p["EJERCICIO"] + " (escala LOGARITMICA)"
    result_json['labels'] =  list_donaciones
    result_json['label_yAxes'] = "Personas (LOGARITMICA)"
    result_json['label_xAxes'] = "Número de donaciones"
    result_json['custom_yAxes_type'] = 'logarithmic'


    if len(list_personas) > 1 :
        result_json['description'] = "Durante el año " + p["EJERCICIO"] + " hubo un total de <b>" +  str(len(dfbydni)) + " donaciones</b> provenientes de <b>" + str(num_donantes) + " donantes</b>." \
        " Es decir, hay personas que donan más de una vez (donantes reincidentes). Esta gráfica refleja esa reincidencia, mostrando cuanta gente donó diferentes veces." \
        " Por ejemplo, en la segunda columna, podemos ver que " + str(list_personas[1]) + " personas, (es decir, el " + str(list_porcentaje[1])  + " % de los donantes) donaron " + \
        str(list_donaciones[1]) + " veces."
    else:
        result_json['description'] = "Durante el año " + p["EJERCICIO"] + " el 100% de los donantes (es decir, " + str(list_personas[0])  + " personas) donaron " \
        + str(list_donaciones[0]) + " vez."
    # print(result_json)
    return result_json

def save_to_file(DIR_DOWNLOADS, texto, p, user_id):
    ### Guardar en fichero de texto
    # date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    date = datetime.datetime.now().strftime("%H%M%S")
    filename = "modelo182-" + p["EJERCICIO"] + "-" + date + "-" + user_id + ".txt"
    path = os.path.join(DIR_DOWNLOADS, filename)

    with open(path, 'w') as out:
        out.write(texto)
        out.close()

    # print(usuarios_error)
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




