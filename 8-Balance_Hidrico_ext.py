import pandas as pd
#import scipy as sc
#import matplotlib as pb
#import tkinter as tk

#Funciona ademas para verificar logica operativa, ya sea continua o temporal segun precipitaciones
# === > parametros del sistema < ===
# se elige un sistema mas autonomo

#ASEGURESE DE USAR LA DIRECCION CORRECTA DE LOS ARCHIVOS!!!!
#ruta_csv = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_2\Mod_Precipi_Naranjo_Tidy.csv" #ORIGINAL
arch_entrada = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\lluvia_simulada-2.csv" # peor escenario, seria el esc-2
arch_salida = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\lluvia_simulada-2-ext.csv" #=>ext=extendida
#arch_entrada = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\Precipitacion_Naranjo_Original.csv" # original del IMN en anrajno
#arch_salida = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\Precipitacion_Naranjo_Original-ext.csv" #=>ext=extendida del original

efic_capt = 0.75
         #  ^^^ General y tecnicamente justificado
efic_escur = 0.30
         #   ^^^ Uso de tierra sin tratar
area_ha = 0.809 #hectarea
area_m2 = 8087.18 #metros cuadrados
#       # ^^^ area final modificada de captacion
dema_litros = 26715.89
dema_m3 = 26.72
#        ^^^ demanda del cafeto

# segun Araya, J. 2021 se debe usar 4 dias de frecuencia
# se hace el iniciador = 4 dias
racha_sequia = 4
fre_riego = 4
umbral_minimo = 0.2 #mm minimos capaces de medirse IMN
#         ^^^ datos elegidos segun IMN y el Inge Araya

#inicia dataframe
#df = pd.read_csv(arch_entrada, parse_dates=["Fecha"]) #otravez error del separador de decimales y lista
#df = df.sort_values("Fecha").reset_index(drop=1) #indice nuevo eliminado

#df = pd.read_csv(arch_entrada, sep=";", decimal =",")
#df = df.sort_values("Fecha").reset_index(drop=1)

#MOD DE ERROR
with open(arch_entrada, "r", encoding="utf-8") as f:
    primer_linea = f.readline()
separador = ";" if primer_linea.count(";") > primer_linea.count(",") else "," #=>vercual separadres usado
df = pd.read_csv(arch_entrada, sep = separador) #=>mejor solucionar la columna y limpiar:

#limpiar precipitacion
df["Precipitacion"] = (
    df["Precipitacion"]
    .astype(str)
    .str.replace(",", ",", regex = 0)
    .str.strip()
    ) #=>>>error
df["Precipitacion"] = pd.to_numeric(df["Precipitacion"], errors = "coerce").fillna(0.0) #errorfechas

#limpiar fechas
df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst = 0, errors="coerce") #.fillna(0.0)
#df = df.dropna(supset = ["Fecha"]) #error
df = df.dropna(subset = ["Fecha"])
df = df.sort_values("Fecha").reset_index(drop = 0)
# FIN DEL MOD DE ERROR

df["mm_netos"] = df["Precipitacion"]* efic_capt * efic_escur
df["m3_hectarea"] = df["mm_netos"] * 10
df["litros_m2"] = df["mm_netos"] #=>recordar equivalencias 1mm=1L/m2
df["produccion_m3"] = df["m3_hectarea"] * area_ha
df["produccion_litros"] = df["litros_m2"] * area_m2

#decision de diseño en logica del PLC
"""
se debe monitorear los dias consecutivos sin lluvia
defenir un detonador de dias secos que active el riego
una vez regada se deben contar los dias necesarios para volver hacerlo
evitar sobre riego si hay lluvias
"""

racha_sequia = 0 #dias
racha_ult_riego = fre_riego #inicia en riego

riego_activo = []
deman_diaria_L = []
deman_diaria_m3 = []

#df.iterrows
for i, fila in df.iterrows():
    llueve = fila["Precipitacion"] > umbral_minimo
    if llueve:
        racha_sequia = 0 #actualizar contador sequia
    else:
        racha_sequia += 1
    racha_ult_riego += 1

    if (racha_sequia >= fre_riego and racha_ult_riego >= fre_riego):
        riego_activo.append(True)
        deman_diaria_L.append(dema_litros)
        deman_diaria_m3.append(dema_m3)
        racha_ult_riego = 0 #reiniciar
        racha_sequia = 0
    else:
        #riego_activo.append(True) #=>mal
        riego_activo.append(False)
        deman_diaria_L.append(0.0)
        deman_diaria_m3.append(0.0)

df["riego_activo"] = riego_activo
df["demanda_litros"] = deman_diaria_L
df["demanda_m3"] = deman_diaria_m3

"""
logica del balance hidrico
si es poositivo la captacion supera la demanda
si es negativo lo cubre el tanque
"""

df["balance_litros"] = df["produccion_litros"] - df["demanda_litros"]
df["balance_m3"] = df["produccion_m3"] - df["demanda_m3"]

#imprimir todo
dias_regados = df["riego_activo"].sum()
total_dias = len(df)

print("=" * 20)
print(" Balance Hidrico en Finca Cirri Este ")
print("=" * 20)

print(" ")
print(f"    Periodo_Analizado: {df["Fecha"].min().date()} -->> {df["Fecha"].max().date()}")
print(f"    Total_Dias:        {total_dias}")
print(f"    Dias_Riego:        {dias_regados}")
print(f"    Dias_No_Riego:     {total_dias - dias_regados}")

print(" ")
print(" ======= Produccion Diaria, dias con lluvia =======") #ordenar concatenacion ojo
print(f"    Mediana_Produccion:         {df["produccion_litros"].median():.2f}   L/dia") #usando 2 digitos
print(f"    Promedio_Produccion:        {df["produccion_litros"].mean():.2f}     L/dia")

print(" ")
print(" ======= Balance Hidrico, dias con riego =======")
bal_riego = df.loc[df["riego_activo"], "balance_litros"]
print(f"    Mediana_Balance:              {bal_riego.median():.2f}   L")
print(f"    Promedio_Balance:            {bal_riego.mean():.2f}     L")
print(f"    Minimo_Balance:              {bal_riego.min():.2f}      L <<<<") #peor caso
print(f"    Maximo_Balance:              {bal_riego.max():.2f}      L")

print(" ")
print(" ======= Datos Criticos Seleccion ======= ")
mediana_deficit = abs(min(bal_riego.min(),0))
print(f"    Deficit_Max_Ciclo_Riego =  {mediana_deficit:.2f}   L")
print(f" ===> Se selecciona el peor escenario <===")
print("=" * 20)

#exportacion
columnas_exp = [
    "Fecha", "Precipitacion", 
    "mm_netos", "m3_hectarea", 
    "litros_m2", "produccion_m3", 
    "produccion_litros", "riego_activo", 
    "demanda_litros", "demanda_m3", #demanda_litros no demandaL
    "balance_litros", "balance_m3",]

df[columnas_exp].to_csv(arch_salida, index=0, float_format="%.4f")
print(f"\n Archivo Guardado:    {arch_salida}")