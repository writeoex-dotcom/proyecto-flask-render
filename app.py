from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# 🔥 CONFIGURACIÓN CORRECTA (TU NUEVA DB)
DB_HOST = 'dpg-d7b83l2a214c73cnufb0-a.oregon-postgres.render.com'
DB_NAME = 'personas_db_sd3v'
DB_USER = 'personas_user'
DB_PASSWORD = '6TICHW04xrur3WyDHr5UTd9k0bbDkkqg'  # 👈 cambia esto
DB_PORT = '5432'


# 🔌 CONEXIÓN
def conectar_db():
    try:
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            sslmode='require'
        )
    except Exception as e:
        print("Error:", e)
        return None


# 🔥 CREAR TABLA
def crear_tabla():
    conn = conectar_db()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personas (
        id SERIAL PRIMARY KEY,
        dni VARCHAR(20) NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        direccion TEXT,
        telefono VARCHAR(20)
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()


# ➕ INSERTAR
def crear_persona(dni, nombre, apellido, direccion, telefono):
    conn = conectar_db()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO personas (dni, nombre, apellido, direccion, telefono)
        VALUES (%s, %s, %s, %s, %s)
    """, (dni, nombre, apellido, direccion, telefono))

    conn.commit()
    cursor.close()
    conn.close()


# 📋 LISTAR
def obtener_registros():
    conn = conectar_db()
    if conn is None:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas ORDER BY id DESC")
    datos = cursor.fetchall()

    cursor.close()
    conn.close()
    return datos


# ❌ ELIMINAR
def eliminar_persona(id):
    conn = conectar_db()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()


# 🌐 RUTAS
@app.route('/')
def index():
    mensaje = request.args.get('mensaje')
    return render_template('index.html', mensaje=mensaje)


@app.route('/registrar', methods=['POST'])
def registrar():
    crear_persona(
        request.form['dni'],
        request.form['nombre'],
        request.form['apellido'],
        request.form['direccion'],
        request.form['telefono']
    )
    return redirect(url_for('index', mensaje="Registro exitoso"))


@app.route('/administrar')
def administrar():
    registros = obtener_registros()
    return render_template('administrar.html', registros=registros)


@app.route('/eliminar/<int:id>')
def eliminar(id):
    eliminar_persona(id)
    return redirect(url_for('administrar'))


# 🚀 INICIO
if __name__ == '__main__':
    crear_tabla()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)