import pandas as pd

# === parametros del sistema ===
# se debe usar el CSV extesndido generado por el script 8-Balance_Hidrico_ext.py
# datoos importantes => produccion_litros, demanda_litros y balance_litros calculados
#este script agrega la dimension del tiedmpo: simula el llenado y vaciado real del tanque

#ASEGURESE DE USAR LA DIRECCION CORRECTA DE LOS ARCHIVOS!!!!
#arch_entrada = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\lluvia_simulada-2-ext.csv" # peor escenario aprobado por KS
#arch_salida  = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\lluvia_simulada-2-tanque.csv" #=>tanque=simulacion acumulada

#ruta_csv = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_2\Mod_Precipi_Naranjo_Tidy.csv" #ORIGINAL
#arch_entrada = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\lluvia_simulada-2.csv" # peor escenario, seria el esc-2
#arch_salida = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\lluvia_simulada-2-ext.csv" #=>ext=extendida

arch_entrada = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\Precipitacion_Naranjo_Original-ext.csv" # original del IMN en anrajno
arch_salida = r"E:\1-Archi-Temp\2_CASA-TEC\_111AAA_EXECUTE_TFG\Scripts_Python_3\Precipitacion_Naranjo_Original-tanque.csv" #=>ext=extendida del original


# === > parametros del tanque < ===
# segun el balance hidrico del script 8, el deficit maximo por ciclo de riego es 26715.89 L
# segun Araya J. 2021 y Valverde J. 2022 se recomienda autonomia de 4 dias
# 4 tanques Ecotank Poseidon de 27000 L cada uno = 108000 L total =>ojo con esto relacionado segun autonomia propuesta
num_tanques   = 4 #modificar si es necesario segun conclusion
cap_tanque_L  = 27000.0
#              ^^^ capacidad comercial del modelo Poseidon segun ficha tecnica de La Casa del Tanque
cap_total_L   = num_tanques * cap_tanque_L
#              ^^^ capacidad maxima de la bateria de vasos comunicantes en paralelo

# se inicia el tanque a la mitad para no partir de un supuesto optimista ni pesimista
# simula un estado de operacion normal al comienzo del periodo analizado
vol_inicial_L = cap_total_L * 0.50
#              ^^^ se puede cambiar a 0.0 para ver el peor caso de arranque en seco

# === > lectura del CSV extendido < ===
# MOD DE ERROR: el mismo detector de separador que en el script 8
with open(arch_entrada, "r", encoding="utf-8") as f:
    primer_linea = f.readline()
separador = ";" if primer_linea.count(";") > primer_linea.count(",") else ","
df = pd.read_csv(arch_entrada, sep=separador)

# limpiar fecha por si viene como string
df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=0, errors="coerce")
df = df.dropna(subset=["Fecha"])
df = df.sort_values("Fecha").reset_index(drop=True)

# limpiar columnas numericas clave por si el CSV trae comas en decimales
for col in ["produccion_litros", "demanda_litros", "balance_litros", "riego_activo"]:
    if df[col].dtype == object:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", ".", regex=False).str.strip(),
            errors="coerce"
        ).fillna(0.0)

# riego_activo puede venir como True/False o como 1/0 segun el CSV
# se normaliza a booleano igual que en el script 9
df["riego_activo"] = df["riego_activo"].astype(str).str.strip().str.lower().isin(["true", "1"])

# === > simulacion dia a dia del tanque < ===
"""
logica del tanque acumulativo:
cada dia el tanque recibe el agua captada por lluvia (produccion_litros)
si ese dia hay riego activo se descuenta la demanda (demanda_litros)
si hay superavit de lluvia el tanque sube, con tope en la capacidad maxima
si hay deficit el tanque baja, con piso en cero (no puede tener volumen negativo)
los dias en que el tanque llega a cero y hay demanda se registra como fallo critico
"""

vol_actual = vol_inicial_L  # estado inicial del tanque en litros

vol_inicio_dia  = []  # volumen al comienzo de cada dia
entrada_dia     = []  # litros que entran por lluvia ese dia
salida_dia      = []  # litros que salen por riego ese dia
desborde_dia    = []  # litros que se pierden por desborde (tanque lleno)
vol_fin_dia     = []  # volumen al final del dia
fallo_dia       = []  # True si el tanque se vacio y habia demanda activa

for i, fila in df.iterrows():
    entrada   = fila["produccion_litros"]   # agua captada ese dia
    demanda   = fila["demanda_litros"]      # agua requerida si hay riego

    vol_inicio_dia.append(vol_actual)

    # primero entra el agua de lluvia
    vol_con_lluvia = vol_actual + entrada

    # si supera la capacidad se pierde el exceso por desborde
    desborde = max(0.0, vol_con_lluvia - cap_total_L)
    vol_con_lluvia = min(vol_con_lluvia, cap_total_L)

    # luego sale el agua de riego si el PLC lo activo ese dia
    vol_despues_riego = vol_con_lluvia - demanda

    # el tanque no puede quedar en negativo
    # si queda negativo es un fallo: no habia suficiente agua para regar
    if vol_despues_riego < 0.0:
        fallo = True
        vol_despues_riego = 0.0  # se seco el tanque
    else:
        fallo = False

    entrada_dia.append(entrada)
    salida_dia.append(demanda)
    desborde_dia.append(desborde)
    vol_fin_dia.append(vol_despues_riego)
    fallo_dia.append(fallo)

    vol_actual = vol_despues_riego  # el estado de hoy es el inicio de manana

# agregar columnas al dataframe
df["tanque_inicio_L"]  = vol_inicio_dia
df["tanque_entrada_L"] = entrada_dia
df["tanque_salida_L"]  = salida_dia
df["tanque_desborde_L"]= desborde_dia
df["tanque_fin_L"]     = vol_fin_dia
df["tanque_fallo"]     = fallo_dia

# columnas derivadas utiles para graficar
df["tanque_fin_m3"]     = df["tanque_fin_L"]     / 1000.0
df["tanque_fin_pct"]    = df["tanque_fin_L"]     / cap_total_L * 100.0
#                         ^^^ porcentaje de llenado del dia

# === > calculos de resumen < ===
dias_riego     = df["riego_activo"].sum()
dias_fallo     = df["tanque_fallo"].sum()
total_dias     = len(df)

# dias en que el tanque estuvo por encima del 75% de capacidad
dias_lleno     = (df["tanque_fin_pct"] >= 75.0).sum()
# dias en que el tanque estuvo por debajo del 25% de capacidad
dias_critico   = (df["tanque_fin_pct"] <= 25.0).sum()

vol_min        = df["tanque_fin_L"].min()
vol_max        = df["tanque_fin_L"].max()
vol_promedio   = df["tanque_fin_L"].mean()
vol_mediana    = df["tanque_fin_L"].median()

total_desborde = df["tanque_desborde_L"].sum()
total_entrada  = df["tanque_entrada_L"].sum()
total_salida   = df["tanque_salida_L"].sum()

# si hubo fallos, buscar la fecha del primero y del ultimo
if dias_fallo > 0:
    fecha_primer_fallo = df.loc[df["tanque_fallo"], "Fecha"].min().date()
    fecha_ultimo_fallo = df.loc[df["tanque_fallo"], "Fecha"].max().date()
else:
    fecha_primer_fallo = "Sin fallos"
    fecha_ultimo_fallo = "Sin fallos"

# === > imprimir resultados en terminal < ===
print("=" * 40)
print("   Simulacion de Tanque - Finca Cirri Este   ")
print("=" * 40)

print(" ")
print(f"    Periodo_Analizado:  {df['Fecha'].min().date()} -->> {df['Fecha'].max().date()}")
print(f"    Total_Dias:         {total_dias}")
print(f"    Inicio_Tanque:      {vol_inicial_L:.0f}   L  ({vol_inicial_L/cap_total_L*100:.0f}% de capacidad)")

print(" ")
print(" ======= Configuracion de la Bateria ======= ")
print(f"    Num_Tanques:        {num_tanques}   unidades")
print(f"    Cap_Tanque:         {cap_tanque_L:.0f}   L  por unidad")
print(f"    Cap_Total:          {cap_total_L:.0f}   L  en paralelo")
print(f"    Cap_Total_m3:       {cap_total_L/1000:.1f}     m3")

print(" ")
print(" ======= Balance de Entradas y Salidas ======= ")
print(f"    Total_Captado:      {total_entrada:.0f}   L  en todo el periodo")
print(f"    Total_Regado:       {total_salida:.0f}      L  en todo el periodo")  #ordenar concatenacion ojo
print(f"    Total_Desbordado:   {total_desborde:.0f}   L  perdidos por tanque lleno") #usar mismo que anteriores
print(f"    Dias_Con_Riego:     {dias_riego}")

print(" ")
print(" ======= Estado del Tanque en el Tiempo ======= ")
print(f"    Volumen_Minimo:     {vol_min:.0f}      L  ({vol_min/cap_total_L*100:.1f}% de capacidad)")
print(f"    Volumen_Maximo:     {vol_max:.0f}   L  ({vol_max/cap_total_L*100:.1f}% de capacidad)")
print(f"    Volumen_Promedio:   {vol_promedio:.0f}   L  ({vol_promedio/cap_total_L*100:.1f}% de capacidad)")
print(f"    Volumen_Mediana:    {vol_mediana:.0f}   L  ({vol_mediana/cap_total_L*100:.1f}% de capacidad)")
print(f"    Dias_Tanque_Lleno:  {dias_lleno}   dias sobre el 75% de capacidad")
print(f"    Dias_Tanque_Bajo:   {dias_critico}   dias bajo el 25% de capacidad")

print(" ")
print(" ======= Analisis de Fallos Criticos ======= ")
print(f"    Dias_Fallo_Total:   {dias_fallo}   dias en que el tanque se vacio con demanda activa")
if dias_fallo > 0:
    print(f"    Primer_Fallo:       {fecha_primer_fallo}   <<<<")
    print(f"    Ultimo_Fallo:       {fecha_ultimo_fallo}   <<<<")
    print(f" ===> ATENCION: hubo dias sin agua suficiente para regar <===")
else:
    print(f"    Primer_Fallo:       {fecha_primer_fallo}")
    print(f"    Ultimo_Fallo:       {fecha_ultimo_fallo}")
    #print(f" === OK: el tanque nunca se vacio en dias de riego activo ===") #error de logfix

print(" ")

#conclusiond e dimencionamiento debe estar en resumen en el trabajo escrito
#print(" ======= Conclusion de Dimensionamiento ======= ") #esta logica seria correcta si el tanque trabajara todos los dias
#if dias_fallo == 0:
#    print(f"    La bateria de {num_tanques} tanques de {cap_tanque_L:.0f} L ({cap_total_L:.0f} L total)")
#    print(f"    es SUFICIENTE para cubrir la demanda del cafeto en el Escenario 2")
#    print(f"    Autonomia validada con datos de precipitacion aprobados por KS")
#else:
#    pct_fallo = dias_fallo / dias_riego * 100
#    print(f"    La bateria de {num_tanques} tanques de {cap_tanque_L:.0f} L ({cap_total_L:.0f} L total)")
#    print(f"    tuvo FALLOS en {dias_fallo} dias de riego ({pct_fallo:.1f}% de los eventos de riego)")
#    print(f"    Se recomienda revisar el numero de tanques o el volumen inicial")
# para una operacion continua no esta dando, pero para fechas especificas segun la teoria sí lo hace
print("=" * 40)

# === > exportacion del CSV con simulacion del tanque < ===
columnas_exp = [
    "Fecha", "Precipitacion",
    "produccion_litros", "riego_activo",
    "demanda_litros", "balance_litros",
    "tanque_inicio_L", "tanque_entrada_L",
    "tanque_salida_L", "tanque_desborde_L",
    "tanque_fin_L", "tanque_fin_m3",
    "tanque_fin_pct", "tanque_fallo",]

df[columnas_exp].to_csv(arch_salida, index=False, float_format="%.4f")
print(f"\n Archivo Guardado:    {arch_salida}")