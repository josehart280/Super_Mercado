'''Como el negocio no tiene clasificación de productos, se clasifican los productos por categoría para poder hacer una presentacion en PowerBi mas practica'''


import pandas as pd

enero = pd.read_excel('datos/Ventas_Enero.xlsx')
febrero = pd.read_excel('datos/Ventas_Febrero.xlsx')

def classify_product(desc):
    if pd.isna(desc):
        return 'Otros'
    desc_upper = str(desc).upper()

    # Lacteos - INCLUYE VAINICA SEGUN GOOGLE 
    lacteos = ['LECHE', 'QUESO', 'YOGUR', 'CREMA', 'MANTEQUILLA', 'LACTEOS', 'LACTOCREMA',
               'LACTUARIO', 'QUESILLO', 'REQUESON', 'CUAJADA', 'YOGURT', 'FLAN', 'CAJETA',
               'DULCE DE LECHE', 'FRESCOLECHE', 'QUEBRANTO', 'POSTRE', 'LACTEA', 'CHOCOLATE',
               'QUESITO', 'NATILLA', 'QUEBRANTO', 'DULCE ', 'CARAJILLO', 'VAINICA']
    if any(kw in desc_upper for kw in lacteos):
        return 'Lacteos'

    # Panaderia - INCLUYE CANDELA, TORTIRRICA, POPUSA
    panaderia = ['PAN ', 'GALLETA', 'CUETE', 'CHURRO', 'DONUT', 'BAGUETTE', 'BOLLO',
                 'EMPANADA', 'TARTA', 'PASTEL', 'BISCOCHO', 'CHOCOBAO', 'MILHOJA',
                 'BIMBO', 'OSMAY', 'TORTILLA', 'AREPA', 'TOSTY', 'WAFFER', 'BARQUILLO', 'QUEQUE',
                 'MASA ', 'HARINA', 'POLVO HORNEAR', 'GELATINA', 'FRIAND', 'PANQUEQUE',
                 'CROISSANT', 'MERMELADA', 'CUPcake', 'PUDING', 'BROWNIE', 'CANDELA',
                 'TORTIRRICA', 'POPUSA', 'DULCES', 'CHOCOLATE', 'CONFITE', 'CARAMELO']
    if any(kw in desc_upper for kw in panaderia):
        return 'Panaderia'

    # Limpieza - INCLUYE DOVE, GEX, DORIVAL
    limpieza_y_cuidado_personal = ['DETERGENTE', 'JABON', 'LIMPIEZA', 'LIMPIADOR', 'DESINFECTANTE', 'CLORO',
                'WIPE', 'ESPONJA', 'LAVAPLATOS', 'SUAVIZANTE', 'SHAMPU', 'SHAMPOO',
                'PASTA DENTAL', 'DESODORANTE', 'ANTITRANSPIRANTE', 'ALCOHOL', 'ANTIBACTERIAL',
                'HEAD', 'COLGATE', 'FORT', 'MONTEAZUL', 'BABOL', 'PALMOLIVE', 'AXION',
                'BOLSA', 'SERVILLETAS', 'PAPEL HIGIENICO', 'POPELE', 'POPULAR', 'SABA', 'INCONTINENCIA',
                'TRIDENT', 'MENTA', 'CHICLE', 'GOMA MASCAR', 'CEPILLO', 'MAQUINILLA', 'AFEITAR',
                'GELITAN', 'SEDA DENTAL', 'CERA DEPILAR', 'ALGODON', 'CUIDADO PERSONAL',
                'DOVE', 'GEX', 'DORIVAL', 'TABSIN', 'BAYER', 'PANADOL', 'SALUTA', 'ALKA SELTZER']
    if any(kw in desc_upper for kw in limpieza_y_cuidado_personal):
        return 'Limpieza y Cuidado Personal'

    # Carnes
    carnes = ['CARNE', 'POLLO', 'CHORIZO', 'SALCHICHA', 'JAMON', 'TOCINO', 'PORK', 'BEEF',
              'HAM', 'SAUSAGE', 'MORTADELA', 'FILETE', 'BISTEC', 'CHURRASCO', 'ALAS',
              'PIERNA', 'PECHUGA', 'HUESO', 'COSTILLA', 'LENGUA', 'TRIPAS', 'HUEVO',
              'ATUN', 'SALMON', 'CAMARON', 'PESCADO', 'MARISCOS', 'SALCHICHON', 'PATI', 'HOT DOG',
              'TILAPIA', 'CORVINA', 'PARGO', 'MOJARRA', 'LANGOSTA', 'JAIVA', 'SARGAZO',
              'GAMBA', 'MUSLO', 'ALA POLLO', 'FILETE PESCADO', 'TRUCHA', 'CABRILLA', 'MEJILLA']
    if any(kw in desc_upper for kw in carnes):
        return 'Carnes'

    # Bebidas - INCLUYE IMPERIAL, BOHEMIA, RAPTOR, BIG ROJA
    bebidas = ['AGUA', 'REFRESCO', 'COLA', 'JUGO', 'FANTA', 'SPRITE', 'PEPSI', '7UP',
                'GASEOSA', 'SODA', 'TONIC', 'ENERGIZANTE', 'MONSTER', 'CAFE', 'TE ',
                'MALTEADA', 'CERVEZA', 'PILSEN', 'BRAMA', 'HEINEKEN', 'CORONA', 'VINO',
                'WHISKY', 'RON', 'VODKA', 'BEBIDA', 'GAMMA', 'COCACOLA', 'BIG COLA',
                'GUARO', 'CUBA LIBRE', 'BRANDY', 'LICOR', 'SKOL', 'RED LABEL', 'QUILIMES',
                'PAP', 'H2O', 'DELAWARE', 'TROPICO', 'FRUTEX', 'VIP ', 'MIRINDA', 'LICUADO',
                'IMPERIAL', 'BOHEMIA', 'RAPTOR', 'BIG ROJA', 'RED LABEL', 'POKER',
                'BARRIL', 'TOSTA', 'CLARA']
    if any(kw in desc_upper for kw in bebidas):
        return 'Bebidas'

    # Vegetales/Snacks - INCLUYE CHOCO MAX, BARRITA, GOMITA, MENEITOS, AJO, TOMILLO
    vegetal = ['PAPA', 'CEBOLLA', 'TOMATE', 'ZANAHORIA', 'LECHUGA', 'APIO', 'PIMENTO',
              'CHILE', 'JALAPENO', 'AGUACATE', 'PLATANO', 'BANANO', 'PAPAYA', 'MANGO',
              'PIÑA', 'NARANJA', 'MANZANA', 'UVA', 'MELON', 'SANDIA', 'FRUTA', 'VERDURA',
              'FRIJOL', 'LENTEJA', 'GARBANZO', 'SOYA', 'CHICHARRON', 'CHIPS', 'PAPAS',
              'TOSTADA', 'NACHOS', 'PALOMITAS', 'SEMILLA', 'NUECES', 'ALMENDRAS',
              'OREGANO', 'CULANTRO', 'PEREJIL', 'AJI', 'CULANTRO', 'LIMON', 'YUCA',
              'AYOTE', 'CHAYOTE', 'REMOLACHA', 'COLIFLOR', 'BROCOLI', 'ESPINACA',
              'BERENJENA', 'PEPINO', 'RABANO', 'LAUREL', 'COMINO', 'ALBAHACA',
              'ENSALADA', 'HELADO', 'ACETAMINOFEN', 'PASTILLA', 'MEDICAMENTO',
              'JARABE', 'CURITA', 'VENDAS', 'GASA', 'TINTURA', 'YODOPOVIDONA', 'OXITOL',
              'CHOCO MAX', 'BARRITA', 'GOMITA', 'MENEITOS', 'AJO', 'TOMILLO', 'WANCHIZ',
              'KITTY', 'PALITO', 'BOMBON', 'CHURRUL', 'NATA', 'PALETAS']
    if any(kw in desc_upper for kw in vegetal):
        return 'Bebidas/Snacks Vegetales'

    # Canasta basica - INCLUYE CONSOME, TAQUERITOS
    canasta = ['AZUCAR', 'SAL ', 'ACEITE', 'PANELA', 'PASTA', 'FIDEO', 'SOPA', 'CEREAL',
               'AVENA', 'ALUBIA', 'VINAGRE', 'MOSTAZA', 'KETCHUP', 'MAYONESA', 'MANTECA',
               'FIDEOS', 'SARDINA', 'SALSA', 'ESPECIA', 'AJINOMOTO', 'KNORR', 'SABRITAS',
               'DORITOS', 'RUFFLES', 'LAYS', 'CHURRUMELLI', 'KELLOGGS', 'NESCAFE', 'QUAKER',
               'FIDEO', 'ARROZ', 'FRIJOL NEGRO', 'LENTEJA ROJA', 'CHOCLO LATA',
               'CONSOME', 'TAQUERITOS', 'FRIJOLES', 'ARROZ GRADO']
    if any(kw in desc_upper for kw in canasta):
        return 'Canasta Basica'

    return 'Otros'

enero['Categoria'] = enero['Descripcion'].apply(classify_product)
febrero['Categoria'] = febrero['Descripcion'].apply(classify_product)

# Get counts
enero_counts = enero['Categoria'].value_counts().reset_index()
enero_counts.columns = ['Categoria', 'Cantidad_Enero']

febrero_counts = febrero['Categoria'].value_counts().reset_index()
febrero_counts.columns = ['Categoria', 'Cantidad_Febrero']

# Merge and calculate totals
summary = pd.merge(enero_counts, febrero_counts, on='Categoria', how='outer').fillna(0)
summary['Cantidad_Enero'] = summary['Cantidad_Enero'].astype(int)
summary['Cantidad_Febrero'] = summary['Cantidad_Febrero'].astype(int)
summary['Total'] = summary['Cantidad_Enero'] + summary['Cantidad_Febrero']

# Add row totals
total_row = pd.DataFrame({'Categoria': ['TOTAL'],
                          'Cantidad_Enero': [summary['Cantidad_Enero'].sum()],
                          'Cantidad_Febrero': [summary['Cantidad_Febrero'].sum()],
                          'Total': [summary['Total'].sum()]})
summary = pd.concat([summary, total_row], ignore_index=True)

print('=== RESUMEN CLASIFICACION FINAL ===')
print(summary.to_string(index=False))

# Save to Excel
with pd.ExcelWriter('datos/Clasificacion_Categorias_Radar.xlsx', engine='openpyxl') as writer:
    summary.to_excel(writer, sheet_name='Resumen', index=False)

    # Also save detailed data
    enero_detailed = enero[['Descripcion', 'Categoria']].copy()
    enero_detailed['Mes'] = 'Enero'
    febrero_detailed = febrero[['Descripcion', 'Categoria']].copy()
    febrero_detailed['Mes'] = 'Febrero'

    detailed = pd.concat([enero_detailed, febrero_detailed], ignore_index=True)
    detailed.to_excel(writer, sheet_name='Detalle_Clasificacion', index=False)

print('\nExcel creado: datos/Clasificacion_Categorias_Radar.xlsx')