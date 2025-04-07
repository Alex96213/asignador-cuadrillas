import os
import sys
import csv
from flask import Flask, render_template, request, redirect, send_file, flash, session, url_for
from datetime import datetime

# Agrega la ruta para importar la función procesar_excel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from asignador.logic.assign import procesar_excel

app = Flask(__name__)
app.secret_key = 'clave_segura'  # Requerido para sesiones y flash

USUARIOS_CSV = os.path.join('ordenes', 'usuarios.csv')

# Ruta principal (redirige a login si no ha iniciado sesión)
@app.route('/')
def index():
    if 'usuario' in session:
        return redirect('/upload')
    return redirect('/login')

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        clave = request.form.get('clave')

        if not usuario or not clave:
            flash("Por favor completa todos los campos.")
            return redirect('/login')

        # Verificar si el usuario existe en el archivo CSV
        try:
            with open(USUARIOS_CSV, newline='') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    if fila['usuario'] == usuario and fila['clave'] == clave:
                        session['usuario'] = usuario
                        return redirect('/upload')
            flash("Usuario o clave incorrecta.")
        except FileNotFoundError:
            flash("No hay usuarios registrados aún.")
    return render_template('login.html')

# Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        clave = request.form.get('clave')

        if not usuario or not clave:
            flash("Por favor completa todos los campos.")
            return redirect('/register')

        # Crear archivo si no existe
        if not os.path.exists(USUARIOS_CSV):
            with open(USUARIOS_CSV, 'w', newline='') as f:
                escritor = csv.writer(f)
                escritor.writerow(['usuario', 'clave'])

        # Verificar si el usuario ya existe
        with open(USUARIOS_CSV, newline='') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                if fila['usuario'] == usuario:
                    flash("El usuario ya existe.")
                    return redirect('/register')

        # Guardar nuevo usuario
        with open(USUARIOS_CSV, 'a', newline='') as f:
            escritor = csv.writer(f)
            escritor.writerow([usuario, clave])

        flash("Usuario registrado con éxito. Inicia sesión.")
        return redirect('/login')

    return render_template('register.html')

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Sesión cerrada correctamente.")
    return redirect('/login')

# Página de subida de archivo (solo si ha iniciado sesión)
@app.route('/upload')
def upload_file():
    if 'usuario' not in session:
        flash("Debes iniciar sesión.")
        return redirect('/login')
    return render_template('upload.html')

# Procesar archivo subido
@app.route('/procesar', methods=['POST'])
def procesar():
    if 'usuario' not in session:
        flash("Debes iniciar sesión.")
        return redirect('/login')

    archivo = request.files.get('archivo')
    if archivo:
        nombre_archivo = archivo.filename
        ruta_guardado = os.path.join('ordenes', nombre_archivo)
        archivo.save(ruta_guardado)

        # Procesar con la función personalizada
        archivo_salida = procesar_excel(ruta_guardado)

        return send_file(archivo_salida, as_attachment=True, download_name="archivo_asignado.xlsx")

    flash("No se subió ningún archivo.")
    return redirect('/upload')


if __name__ == '__main__':
    app.run(debug=True)
