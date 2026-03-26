import sqlite3

def crear_base_de_datos():
    conexion = sqlite3.connect('cobranzas.db')
    cursor = conexion.cursor()
    
    # Creamos la tabla facturas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            cedula TEXT PRIMARY KEY,
            nombre TEXT,
            fecha_exp_cedula TEXT,
            num_factura TEXT,
            valor REAL,
            fecha_emision TEXT,
            fecha_vencimiento TEXT
        )
    ''')
    
    # Insertamos un dato de prueba para que podás testear
    try:
        cursor.execute('''
            INSERT INTO facturas VALUES 
            ('12345', 'Juan Perez', '2010-05-15', 'FAC-001', 500000, '2026-01-01', '2026-02-01')
        ''', )
        conexion.commit()
        print("✅ Base de datos creada y dato de prueba insertado.")
    except sqlite3.IntegrityError:
        print("⚠️ La base de datos ya existe con datos.")
    
    conexion.close()

if __name__ == '__main__':
    crear_base_de_datos()