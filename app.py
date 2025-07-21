from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# -------------------------------
# CONEXIÓN A SQL SERVER
# -------------------------------
def get_db_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=ADMINISTRADOR\\SQLEXPRESS;"
            "DATABASE=PROYECTOP;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        print("❌ Error de conexión:", e)
        return None

# -------------------------------
# REGISTRAR VISITANTE
# -------------------------------
@app.route("/registrar_visitante", methods=["POST"])
def registrar_visitante():
    cedula = request.form["documento"]
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    edad = request.form["edad"]

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO VISITANTE (CEDULA, NOMBRE, APELLIDO, EDAD)
                OUTPUT INSERTED.ID
                VALUES (?, ?, ?, ?)
            """, (cedula, nombre, apellido, edad))
            visitante_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            # ✅ Muestra boleta después de registrar visitante
            return render_template("registro.html", visitante_registrado=True, visitante_id=visitante_id)
        except Exception as e:
            return f"❌ Error al guardar visitante: {e}"
    else:
        return "❌ Error de conexión a la base de datos"

# -------------------------------
# REGISTRAR BOLETA
# -------------------------------
@app.route("/registrar_boleta", methods=["POST"])
def registrar_boleta():
    n_boleta = request.form["numero_boleta"]
    tipo = request.form["tipo"]
    id_visitante = request.form["visitante"]

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO BOLETA (N_BOLETA, TIPO_DE_BOLETA, ID_VISITANTE)
                VALUES (?, ?, ?)
            """, (n_boleta, tipo, id_visitante))
            conn.commit()
            conn.close()
            return render_template("registro.html", boleta_registrada=True)
        except Exception as e:
            return f"❌ Error al guardar boleta: {e}"
    else:
        return "❌ Error de conexión a la base de datos"

# -------------------------------
# PÁGINA INICIAL
# -------------------------------
@app.route("/")
def home():
    return render_template("registro.html")

# -------------------------------
# INICIO DE LA APP
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
