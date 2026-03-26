import sqlite3

def cargar_datos():
    conexion = sqlite3.connect('cobranzas.db')
    cursor = conexion.cursor()

    # Lista de 10 usuarios con datos variados (formato: cedula, nombre, exp_cedula, factura, valor, fecha_emision, fecha_venc)
    usuarios = [
        ('1001', 'Mao Zapata', '2015-05-20', 'FAC-101', 1500000, '2026-03-01', '2026-04-01'),
        ('1002', 'Samuel Rojo', '2012-10-10', 'FAC-102', 450000, '2026-02-15', '2026-03-15'),
        ('1003', 'Carlos Restrepo', '2018-01-15', 'FAC-103', 890000, '2026-03-05', '2026-04-05'),
        ('1004', 'Mariana Lopera', '2020-07-22', 'FAC-104', 120000, '2026-01-10', '2026-02-10'),
        ('1005', 'Andres Calle', '2014-03-30', 'FAC-105', 2300000, '2026-03-10', '2026-04-10'),
        ('1006', 'Sofia Henao', '2016-11-05', 'FAC-106', 75000, '2026-02-28', '2026-03-28'),
        ('1007', 'Mateo Arango', '2011-09-12', 'FAC-107', 600000, '2026-03-12', '2026-04-12'),
        ('1008', 'Isabel Uribe', '2019-04-18', 'FAC-108', 320000, '2025-12-01', '2026-01-01'),
        ('1009', 'Jorge Velez', '2013-06-25', 'FAC-109', 1100000, '2026-03-15', '2026-04-15'),
        ('1010', 'Valentina Ruiz', '2021-02-14', 'FAC-110', 950000, '2026-03-18', '2026-04-18')
    ]

    try:
        # Usamos executemany para insertar toda la lista de golpe
        cursor.executemany('INSERT OR REPLACE INTO facturas VALUES (?, ?, ?, ?, ?, ?, ?)', usuarios)
        conexion.commit()
        print(f"✅ ¡Éxito! Se han cargado {len(usuarios)} usuarios a la base de datos.")
    except Exception as e:
        print(f"❌ Error al cargar: {e}")
    finally:
        conexion.close()

if __name__ == '__main__':
    cargar_datos()