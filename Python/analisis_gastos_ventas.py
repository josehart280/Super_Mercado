import pandas as pd
import os

# Rutas porque este es el proyecto a presentar no en el que trabaje
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
REPORTES_DIR = os.path.join(SCRIPT_DIR, 'reportes')

# Asegurar que existe la carpeta reportes
os.makedirs(REPORTES_DIR, exist_ok=True)


print('ANÁLISIS DE GASTOS ENERO 2025\n')


# Cargar datos - Usando datosCrudos 
gastos_path = os.path.join(PROJECT_ROOT, 'datosCrudos', 'Resumen contable mensual 2025 completo.xlsx')
gastos = pd.read_excel(gastos_path, sheet_name='Gastos', header=1)

print(gastos)

# Filtrar 
tipos_validos = ['Decoración', 'Suministros Oficina', 'Servicio de Agua', 'Otros Gastos Empleados',
                 'Mantenimiento local', 'Articulos de Limpieza', 'Servicios Tecnicos',
                 'Mantenimiento vehiculo', 'Servicio Telefono', 'Servicio Electrico',
                 'Telecomunicaciones', 'Combustible', 'Equipo computo', 'Servicios Legales',
                 'Hielo', 'Servicios Contables', 'Seguros', 'Gastos de Representacion',
                 'uniforme', 'Mantenimiento equipo', 'Material de Empaque', 'Mantenimiento Local']

gastos_filtrado = gastos[gastos['Tipo Gasto'].isin(tipos_validos)]

# Ingresos enero 2025 
ingresos_enero = 33810196

# Gastos por tipo
gastos_tipo = gastos_filtrado.groupby('Tipo Gasto')['Total'].sum().sort_values(ascending=False)
total_gastos = gastos_tipo.sum()
ratio_gasto_ingreso = (total_gastos / ingresos_enero) * 100

print(f'\nTotal Gastos: {total_gastos:,.0f} CRC')
print(f'Ingresos Enero: {ingresos_enero:,.0f} CRC')
print(f'Ratio Gasto/Ingreso: {ratio_gasto_ingreso:.1f}%')

# JASEC 
jasec = gastos_filtrado[gastos_filtrado['Nombre'].str.contains('JASEC|ELECTRICO', case=False, na=False)]['Total'].sum()
ratio_jasec = (jasec / ingresos_enero) * 100
print(f'Gasto Electrico (JASEC): {jasec:,.0f} CRC ({ratio_jasec:.2f}%)')

# Top 10 proveedores
gastos_proveedor = gastos_filtrado.groupby('Nombre')['Total'].sum().sort_values(ascending=False).head(10)
top3_total = gastos_proveedor.head(3).sum()
ratio_top3 = (top3_total / total_gastos) * 100
print(f'Concentración Top 3: {ratio_top3:.1f}%')

# Crear CSV de gastos
gastos_data = []
for tipo, monto in gastos_tipo.items():
    pct = (monto / ingresos_enero) * 100
    gastos_data.append({'Categoria': tipo, 'Monto_Colones': monto, 'Porcentaje_Ingreso': f'{pct:.2f}%'})

# Agregar totales
gastos_data.append({'Categoria': 'TOTAL', 'Monto_Colones': total_gastos, 'Porcentaje_Ingreso': f'{ratio_gasto_ingreso:.2f}%'})

print(gastos_data)

#guardar csv
df_gastos = pd.DataFrame(gastos_data)
output_gastos = os.path.join(REPORTES_DIR, 'gastos_enero_2025.csv')
df_gastos.to_csv(output_gastos, index=False, encoding='utf-8')
print(f'\n[OK] Guardado: {output_gastos}')


 #VENTAS FEBRERO 2025


print('\nANÁLISIS DE VENTAS FEBRERO 2025')


# Cargar ventas febrero 
ventas_path = os.path.join(PROJECT_ROOT, 'datos', 'Ventas_Febrero.xlsx')
ventas = pd.read_excel(ventas_path)

print(ventas)

# Limpiar nombres de columnas
ventas.columns = [c.strip().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') for c in ventas.columns]
print(f'Transacciones: {len(ventas)}')

# KPIs
col_total = [c for c in ventas.columns if 'Total' in c][0]
col_descuento = [c for c in ventas.columns if 'Descuento' in c][0]
col_id = 'ID_Compra'
col_desc = 'Descripcion'

ticket_promedio = ventas[col_total].sum() / ventas[col_id].nunique()
items_por_ticket = len(ventas) / ventas[col_id].nunique()
tasa_descuento = (ventas[col_descuento].sum() / ventas[col_total].sum()) * 100

print(f'\nTicket Promedio: {ticket_promedio:,.0f} CRC (objetivo: >2,500)')
print(f'Items por Ticket: {items_por_ticket:.2f} (objetivo: >1.8)')
print(f'Tasa Descuento: {tasa_descuento:.2f}% (objetivo: <5%)')

# Top 10 productos
top_productos = ventas.groupby(col_desc)[col_total].sum().sort_values(ascending=False).head(10)
print('\nTop 10 Productos:')
for prod, monto in top_productos.items():
    print(f'  {str(prod)[:40]:<40} {monto:>10,.0f} CRC')

# Hora pico - procesar hora
ventas['Hora'] = pd.to_datetime(ventas['Hora'], format='%H:%M:%S', errors='coerce')
ventas['Hora_num'] = ventas['Hora'].dt.hour
hora_pico = ventas['Hora_num'].value_counts().idxmax()
print(f'\nHora Pico: {hora_pico}:00')

# Guardar CSV de ventas
ventas_data = [
    {'Metrica': 'Ticket Promedio (ATV)', 'Valor': f'{ticket_promedio:,.0f} CRC', 'Objetivo': '> 2,500 CRC',
     'Estado': 'OK' if ticket_promedio > 2500 else 'ALERTA'},
    {'Metrica': 'Items por Ticket', 'Valor': f'{items_por_ticket:.2f}', 'Objetivo': '> 1.8',
     'Estado': 'OK' if items_por_ticket > 1.8 else 'ALERTA'},
    {'Metrica': 'Tasa de Descuento', 'Valor': f'{tasa_descuento:.2f}%', 'Objetivo': '< 5%',
     'Estado': 'OK' if tasa_descuento < 5 else 'ALERTA'},
    {'Metrica': 'Hora Pico', 'Valor': f'{hora_pico}:00', 'Objetivo': '-', 'Estado': '-'},
    {'Metrica': 'Total Transacciones', 'Valor': f'{ventas[col_id].nunique():,}', 'Objetivo': '-', 'Estado': '-'},
    {'Metrica': 'Total Ingresos', 'Valor': f'{ventas[col_total].sum():,.0f} CRC', 'Objetivo': '-', 'Estado': '-'},
]

# Agregar top 10 productos
ventas_data.append({'Metrica': '', 'Valor': '', 'Objetivo': '', 'Estado': ''})
ventas_data.append({'Metrica': '--- TOP 10 PRODUCTOS ---', 'Valor': '', 'Objetivo': '', 'Estado': ''})
for i, (prod, monto) in enumerate(top_productos.items(), 1):
    ventas_data.append({'Metrica': f'{i}. {str(prod)[:50]}', 'Valor': f'{monto:,.0f} CRC', 'Objetivo': '', 'Estado': ''})

# Oportunidades de mejora
ventas_data.append({'Metrica': '', 'Valor': '', 'Objetivo': '', 'Estado': ''})
ventas_data.append({'Metrica': '--- OPORTUNIDADES DE MEJORA ---', 'Valor': '', 'Objetivo': '', 'Estado': ''})

# Evaluar condiciones
if ratio_jasec > 2:
    ventas_data.append({'Metrica': 'Optimizacion Energetica',
                        'Valor': f'JASEC = {ratio_jasec:.2f}% de ingresos',
                        'Objetivo': '< 2%', 'Estado': 'OPORTUNIDAD'})
else:
    ventas_data.append({'Metrica': 'Gasto Electrico',
                        'Valor': f'{ratio_jasec:.2f}%',
                        'Objetivo': '< 2%', 'Estado': 'OK'})

if items_por_ticket < 1.5:
    ventas_data.append({'Metrica': 'Cross-Selling',
                        'Valor': f'Items/ticket = {items_por_ticket:.2f}',
                        'Objetivo': '> 1.5', 'Estado': 'MEJORA'})
else:
    ventas_data.append({'Metrica': 'Cross-Selling',
                        'Valor': f'{items_por_ticket:.2f} items/ticket',
                        'Objetivo': '> 1.5', 'Estado': 'OK'})

if ratio_gasto_ingreso > 70:
    ventas_data.append({'Metrica': 'Ratio Gasto/Ingreso',
                        'Valor': f'{ratio_gasto_ingreso:.1f}%',
                        'Objetivo': '< 70%', 'Estado': 'ALERTA'})

if tasa_descuento > 5:
    ventas_data.append({'Metrica': 'Tasa de Descuento',
                        'Valor': f'{tasa_descuento:.2f}%',
                        'Objetivo': '< 5%', 'Estado': 'ALERTA'})

df_ventas = pd.DataFrame(ventas_data)
output_ventas = os.path.join(REPORTES_DIR, 'ventas_febrero_2025_analisis.csv')
df_ventas.to_csv(output_ventas, index=False, encoding='utf-8')
print(f'\n[OK] Guardado: {output_ventas}')


print('ANALISIS COMPLETADO')
