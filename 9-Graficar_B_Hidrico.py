#ASEGURESE DE USAR LA DIRECCION CORRECTA DE LOS ARCHIVOS!!!!
#import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
#      ^^^ libreria principal para graficar de python
import matplotlib.patches as mpatches
#      ^^^ para crear leyendas manuales con colores
import seaborn as sns
#      ^^^ libreria de graficas de estadisticas sobre matplotlib
#quitar tkinter mejor
#def ruta del csv extendido
#ruta_csv = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_2\Mod_Precipi_Naranjo_Tidy.csv" #ORIGINAL
#ruta_csv = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_2\lluvia_simulada-8.csv" #ESCENARIO.
#ruta_csv = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\lluvia_simulada-2-ext.csv" #=>>>usar extendido
#              ^^^^^^^^^^^^^^^^^ USAR ESTE ESTOCASTICO Y EXTENDIDO

arch_entrada = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\Precipitacion_Naranjo_Original.csv" # original del IMN en anrajno
ruta_csv = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\Precipitacion_Naranjo_Original-ext.csv" #=>ext=extendida del original 
#             ^^^^^^^^^^^^^^^^^^^^^USAR ESTE HISTORICO Y EXTENDIDO

df = pd.read_csv(ruta_csv)
#    ^ carga el CSV extendido con todas las columnas extras del BH

if "Fecha" in df.columns:
    df["Fecha"] = pd.to_datetime(df["Fecha"])
#                 ^ convertir fecha de str a fecha real para matplotlib

# columna bool: True/False => int 0/1 para poder filtrar y graficar
df["riego_activo"] = df["riego_activo"].astype(str).str.strip().str.lower() == "1" #=>corregir
#  ^ a veces pandas lee True/False como strings segun el CSV

# separar dias con y sin riego para graficas focalizadas
df_riego   = df[df["riego_activo"] == 1].copy()
#            ^ solo los dias en que el PLC activo el riego
df_sin_riego = df[df["riego_activo"] == 0].copy()

sns.set_style("whitegrid")
#   ^ estilo visual de fondo blanco, igual que en el codigo original

#figura1 ========================================
#plt.figure(figsize=(14, 4))

#plt.plot(
#    df["Fecha"],
#    df["Precipitacion"],
#    linewidth=0.5,
#    color="steelblue",
#    label="Precipitacion (mm)"
#)
#   ^ serie de precipitacion diaria;;;;corregir linea fina para ver densidad

# diferneciar dias
#for fecha in df_riego["Fecha"]:
#    plt.axvline(x=fecha, color="red", linewidth=2)
#   plt.axvline(x=fecha, color="red", alpha=1, linewidth=2)
#               ^^^ linea vertical por cada dia que se activo el riego
#nose aprecia bien cambar alpha y color

#plt.xlabel("Fecha")
#plt.ylabel("Precipitacion_mm")
#plt.title("Precipitacion_Diaria_Y_Dias_Riego_Activado")

#linea_prec  = mpatches.Patch(color="steelblue", label="Precipitacion_mm")
#linea_riego = mpatches.Patch(color="red", label="Dia_Riego_PLC")
#plt.legend(handles=[linea_prec, linea_riego])

#plt.tight_layout()
#plt.show()

#figurea2========================
plt.figure(figsize=(14, 4))

plt.plot(
    df["Fecha"],
    df["produccion_litros"],
    linewidth=0.5,
    color="steelblue",
    label="Produccion_captada_Litros"
)

plt.plot(
    df["Fecha"],
    df["demanda_litros"],
    linewidth=1.2,
    color="red",
    label="Demanda_riego_Litros"
)
#   ^ cambiar el formato de demanda

plt.xlabel("Fecha")
plt.ylabel("Litros")
plt.title("Produccion_Captada_VS_Demanda_Riego")
plt.legend()
plt.tight_layout()
plt.show()


#figura 3 ===============================
plt.figure(figsize=(14, 4))

# color segun areade balance
plt.fill_between(
    df["Fecha"],
    df["balance_litros"],
    0,
    where=(df["balance_litros"] >= 0),
    color="green",
    alpha=0.5,
    label="Superavit con captacion > demanda)"
)
plt.fill_between(
    df["Fecha"],
    df["balance_litros"],
    0,
    where=(df["balance_litros"] < 0),
    color="red",
    alpha=0.5,
    label="Deficit_cubierto por tanque"  #ordenar concatenacion ojo
)
#   ^ fill_between: colorea el area entre la curva y el eje Y=0 :funti

plt.axhline(y=0, color="black", linewidth=0.8, linestyle="--")
#           ^ linea de referencia en cero

plt.xlabel("Fecha")
plt.ylabel("Balance en Litros ")
plt.title("Balance Hidrico Diario - Superavit y Deficit")
plt.legend()
plt.tight_layout()
plt.show()

#figura de caja e histograma se descartan no dan info importante