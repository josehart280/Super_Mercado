"""Heatmap Hora x Dia - SuperAmerica - Optimizado"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Rutas
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
REPORTES_DIR = SCRIPT_DIR # El script ya está dentro de la carpeta reportes

DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
ARCHIVOS = {'Enero': os.path.join(PROJECT_ROOT, 'datos', 'Ventas_Enero.xlsx'),
            'Febrero': os.path.join(PROJECT_ROOT, 'datos', 'Ventas_Febrero.xlsx')}

os.makedirs(REPORTES_DIR, exist_ok=True)

#cargar datos
def cargar_datos():
    return {mes: pd.read_excel(arch) for mes, arch in ARCHIVOS.items()}
#procesar datos
def procesar(df):
    df = df.copy()
    df['Hora'] = pd.to_datetime(df['Hora'], errors='coerce').dt.hour
    df['Dia'] = pd.to_datetime(df['Fecha'], errors='coerce').dt.dayofweek
    df = df[(df['Hora'] >= 7) & (df['Hora'] <= 21)]
    return df

#crear heatmap con matplotlib y seaborn
def crear_heatmap(data, titulo, archivo):
    matriz = data.pivot_table(index='Dia', columns='Hora', values='ID_Compra', aggfunc='count', fill_value=0)
    matriz.index = [DIAS[d] for d in matriz.index]
    plt.figure(figsize=(16, 8))
    sns.heatmap(matriz, annot=True, fmt='d', cmap='YlOrRd', linewidths=0.5, cbar_kws={'label': 'Transacciones'})
    plt.title(f'Heatmap: Transacciones por Hora y Día\nSuperAmerica - {titulo}', fontsize=16, fontweight='bold')
    plt.xlabel('Hora del Día')
    plt.ylabel('Día de la Semana')
    plt.tight_layout()
    #Crear el heatmap
    path_img = os.path.join(REPORTES_DIR, archivo)
    path_csv = os.path.join(REPORTES_DIR, archivo.replace(".png", ".csv"))
    
    plt.savefig(path_img, dpi=150, bbox_inches='tight')
    matriz.to_csv(path_csv)
    plt.close()

def main():
    #cargar datos
    datos = {k: procesar(v) for k, v in cargar_datos().items()}
    #combinar datos
    datos['Combinado'] = pd.concat(datos.values())
    #crear heatmap
    for nombre, df in datos.items():
        crear_heatmap(df, nombre, f'heatmap_hora_dia_{nombre.lower()}.png')
    #hora pico
    hc = datos['Combinado'].pivot_table(index='Dia', columns='Hora', values='ID_Compra', aggfunc='count', fill_value=0)
    print(f"Hora pico: {hc.mean(axis=0).idxmax()}:00 | Día más ocupado: {DIAS[hc.sum(axis=1).idxmax()]}")

if __name__ == '__main__':
    main()