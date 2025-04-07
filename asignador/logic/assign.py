import pandas as pd
from io import BytesIO

CUADRILLAS = {
    'Melgar': ['ATENCION 15', 'ATENCION 16', 'ATENCION 19'],
    'Espinal': ['ATENCION 2', 'ATENCION 8', 'ATENCION 10'],
    'Chaparral': ['Chaparral_1', 'Chaparral_2', 'Chaparral_3'],
    'Ibagué': ['Ibague_1', 'Ibague_2', 'Ibague_3', 'Ibague_4', 'Ibague_5', 'Ibague_6',
               'Ibague_7', 'Ibague_8', 'Ibague_9', 'Ibague_10', 'Ibague_11', 'Ibague_12',
               'Ibague_13', 'Ibague_14', 'Ibague_15'],
}

CUADRILLAS_TR_TORRE = ['ATENCION 25', 'ATENCION 26']

def procesar_excel(file_path):
    """Procesa el archivo Excel y asigna cuadrillas según la zona."""
    try:
        df = pd.read_excel(file_path)

        if 'ZONA' not in df.columns or 'DIRECCIÓN' not in df.columns:
            raise Exception("El archivo debe tener las columnas 'ZONA' y 'DIRECCIÓN'")

        df['ASIGNADA'] = ''
        contadores = {zona: 0 for zona in CUADRILLAS}

        for i, row in df.iterrows():
            zona = row['ZONA']
            direccion = str(row['DIRECCIÓN']).upper()

            if 'TR' in direccion or 'TORRE' in direccion:
                df.at[i, 'ASIGNADA'] = CUADRILLAS_TR_TORRE[i % len(CUADRILLAS_TR_TORRE)]
            elif zona in CUADRILLAS:
                cuadrilla_idx = contadores[zona] % len(CUADRILLAS[zona])
                df.at[i, 'ASIGNADA'] = CUADRILLAS[zona][cuadrilla_idx]
                contadores[zona] += 1
            else:
                df.at[i, 'ASIGNADA'] = 'SIN CUADRILLA'

        # Guardar en memoria
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        return output

    except Exception as e:
        print(f"❌ Error en la asignación: {e}")
        return None
