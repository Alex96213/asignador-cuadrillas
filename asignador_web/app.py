from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import csv
import os
from datetime import datetime
from asignador.logic.assign import procesar_excel

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

# Rutas y carpetas
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'ordenes')
HISTORIAL_CSV = os.path.join(UPLOAD_FOLDER, 'historial.csv')
USUARIOS_CSV = os.path.join(UPLOAD_FOLDER, 'usuarios.csv')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta de inicio
@app.route("/")
def index():
    return render_template("index.html")

# Ruta de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]

        try:
            with open(USUARIOS_CSV, newline='') as f:
                lector = csv.reader(f)
                for fila in lector:
                    if fila[0] == usuario and fila[1] == contraseña:
                        return redirect(url_for("upload"))
        except FileNotFoundError:
            flash("Archivo de usuarios no encontrado.")
            return redirect(url_for("login"))

        flash("Usuario o contraseña incorrectos.")
    return render_template("login.html")

# Ruta de registro de usuario
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]

        with open(USUARIOS_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([usuario, contraseña])

        flash("Usuario registrado con éxito.")
        return redirect(url_for("login"))

    return render_template("register.html")

# Subida de archivo Excel
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        archivo = request.files["archivo"]
        if archivo.filename.endswith(".xlsx") or archivo.filename.endswith(".xls"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"agenda_{timestamp}.xlsx"
            ruta_guardado = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
            archivo.save(ruta_guardado)

            ruta_resultado = procesar_excel(ruta_guardado)

            with open(HISTORIAL_CSV, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([nombre_archivo, ruta_resultado])

            return redirect(url_for("success", archivo=os.path.basename(ruta_resultado)))
        else:
            flash("El archivo debe tener extensión .xls o .xlsx")

    return render_template("upload.html")

# Página de éxito tras asignación
@app.route("/success")
def success():
    archivo = request.args.get("archivo")
    return render_template("success.html", archivo=archivo)

# Descargar archivo procesado
@app.route("/descargar/<archivo>")
def descargar(archivo):
    ruta = os.path.join(app.config['UPLOAD_FOLDER'], archivo)
    return send_file(ruta, as_attachment=True)

# Historial de archivos procesados
@app.route("/historial")
def historial():
    archivos = []
    if os.path.exists(HISTORIAL_CSV):
        with open(HISTORIAL_CSV, newline='') as f:
            lector = csv.reader(f)
            archivos = list(lector)
    return render_template("historial.html", archivos=archivos)

# Iniciar la app localmente
if __name__ == "__main__":
    app.run(debug=True)
