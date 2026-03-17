"""
Heatmap Hora x Dia - SuperAmerica
Análisis de horas pico para optimizar staffing y reabastecimiento
Genera 3 heatmaps: Enero, Febrero, y Combinado
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#config
ARCHIVOS_VENTAS = {
    'Enero': 'datos/Ventas_Enero.xlsx',
    'Febrero': 'datos/Ventas_Febrero.xlsx'
}


# LEER DATOS

dfs = {}
for mes, archivo in ARCHIVOS_VENTAS.items():
    try:
        df = pd.read_excel(archivo)
        dfs[mes] = df
        print(f"  - {mes}: {len(df):,} transacciones")
    except Exception as e:
        print(f"  - Error leyendo {mes}: {e}")




# PROCESAR DATOS
def procesar_dataframe(df, mes_nombre):
    """Procesa un DataFrame y retorna datos para heatmap"""
    df = df.copy()

    # Intentar parsear hora de diferentes formatos por multipliples formatos
    try:
        df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S', errors='coerce')
    except:
        try:
            df['Hora'] = pd.to_datetime(df['Hora'], format='%I:%M:%S %p', errors='coerce')
        except:
            df['Hora'] = pd.to_datetime(df['Hora'], errors='coerce')

    df['Hora_num'] = df['Hora'].dt.hour
    df['Dia_semana'] = pd.to_datetime(df['Fecha'], errors='coerce').dt.dayofweek

    # Mapa de días en español
    dias = {
        0: 'Lunes',
        1: 'Martes',
        2: 'Miércoles',
        3: 'Jueves',
        4: 'Viernes',
        5: 'Sábado',
        6: 'Domingo'
    }
    df['Dia_nombre'] = df['Dia_semana'].map(dias)

    # Filtrar horas de operación (7:00 - 21:00)
    df = df[(df['Hora_num'] >= 7) & (df['Hora_num'] <= 21)]

    return df

# Procesar cada mes
datos_procesados = {}
for mes, df in dfs.items():
    datos_procesados[mes] = procesar_dataframe(df, mes)
    print(f"  {mes} - Transacciones en horario válido (7-21): {len(datos_procesados[mes]):,}")

# Crear DataFrame combinado
df_combinado = pd.concat(datos_procesados.values(), ignore_index=True)
datos_procesados['Combinado'] = df_combinado
print(f"\nTotal combinado: {len(df_combinado):,} transacciones")



# CREAR HEATMAPS
def crear_heatmap(data, titulo, nombre_archivo):
    """Genera un heatmap para los datos dados"""
    # Crear matriz pivote
    heatmap_data = data.pivot_table(
        index='Dia_nombre',
        columns='Hora_num',
        values='ID_Compra',
        aggfunc='count',
        fill_value=0
    )

    # Ordenar días de la semana
    orden_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    heatmap_data = heatmap_data.reindex(orden_dias)

    # Generar visualización
    plt.figure(figsize=(16, 8))
    sns.set(font_scale=1.2)

    ax = sns.heatmap(
        heatmap_data,
        annot=True,
        fmt='d',
        cmap='YlOrRd',
        linewidths=0.5,
        cbar_kws={'label': 'Transacciones'}
    )

    plt.title(f'Heatmap: Transacciones por Hora y Día de la Semana\nSuperAmerica - {titulo}', fontsize=16, fontweight='bold')
    plt.xlabel('Hora del Día', fontsize=12)
    plt.ylabel('Día de la Semana', fontsize=12)
    plt.xticks(rotation=0)

    # Guardar imagen
    plt.tight_layout()
    plt.savefig(f'reportes/{nombre_archivo}', dpi=150, bbox_inches='tight')
    plt.close()

    # Guardar CSV
    heatmap_data.to_csv(f'reportes/{nombre_archivo.replace(".png", ".csv")}')

    return heatmap_data


# GENERAR CADA HEATMAP
print("\n" + "="*60)
print("GENERANDO HEATMAPS")
print("="*60)

for nombre, data in datos_procesados.items():
    titulo = nombre
    archivo = f'heatmap_hora_dia_{nombre.lower()}.png'

    heatmap_data = crear_heatmap(data, titulo, archivo)
    print(f"\n{titulo}:")
    print(f"  - Imagen: reportes/{archivo}")
    print(f"  - CSV: reportes/{archivo.replace('.png', '.csv')}")

    # Análisis de insights por mes
    if nombre != 'Combinado':
        hora_pico = heatmap_data.mean(axis=0).idxmax()
        transacciones_hora_pico = heatmap_data.mean(axis=0).max()
        dia_pico = heatmap_data.sum(axis=1).idxmax()
        transacciones_dia_pico = heatmap_data.sum(axis=1).max()

        print(f"  - Hora pico: {hora_pico}:00 (~{transacciones_hora_pico:.0f} trans/hora)")
        print(f"  - Día más ocupado: {dia_pico} ({transacciones_dia_pico:,} trans)")


# ANÁLISIS COMBINADO
print("\n" + "="*60)
print("ANÁLISIS COMBINADO (Enero + Febrero)")
print("="*60)

heatmap_combinado = datos_procesados['Combinado'].pivot_table(
    index='Dia_nombre',
    columns='Hora_num',
    values='ID_Compra',
    aggfunc='count',
    fill_value=0
).reindex(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])

# Hora pico promedio
hora_pico = heatmap_combinado.mean(axis=0).idxmax()
transacciones_hora_pico = heatmap_combinado.mean(axis=0).max()
print(f"\nHora pico promedio: {hora_pico}:00 ({transacciones_hora_pico:.0f} transacciones)")

# Día más ocupado
dia_pico = heatmap_combinado.sum(axis=1).idxmax()
transacciones_dia_pico = heatmap_combinado.sum(axis=1).max()
print(f"Día más concurrido: {dia_pico} ({transacciones_dia_pico:,} transacciones)")

# Top 3 horas pico
print("\nTop 3 Horas Pico:")
for hora, count in heatmap_combinado.mean(axis=0).sort_values(ascending=False).head(3).items():
    print(f"  {hora}:00 - {count:.0f} transacciones promedio")

# Distribución por período
manana = heatmap_combinado[[7, 8, 9, 10, 11]].sum().sum()
tarde = heatmap_combinado[[12, 13, 14, 15, 16, 17]].sum().sum()
noche = heatmap_combinado[[18, 19, 20, 21]].sum().sum()
total = manana + tarde + noche

print(f"\nDistribución por período:")
print(f"  Mañana (7-11):  {manana:,} ({manana/total*100:.1f}%)")
print(f"  Tarde (12-17):  {tarde:,} ({tarde/total*100:.1f}%)")
print(f"  Noche (18-21):  {noche:,} ({noche/total*100:.1f}%)")

# Hora más tranquila
hora_baja = heatmap_combinado.mean(axis=0).idxmin()
print(f"\nHora más tranquila: {hora_baja}:00")


print("ARCHIVOS GENERADOS:")
print("  - reportes/heatmap_hora_dia_enero.png")
print("  - reportes/heatmap_hora_dia_febrero.png")
print("  - reportes/heatmap_hora_dia_combinado.png")
