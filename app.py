from flask  import Flask,render_template,request,flash,url_for,redirect
from  database import conectar
#crear la app del proyecto

app = Flask(__name__)

#crear la ruta principal
app.secret_key = "3158519351WS"
@app.route('/')
def inicio():
    return render_template("index.html")
#crear la ruta para registrar  usuarios

@app.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():

    usuario = request.form['txtusuario']
    password = request.form['txtcontrasena']
    rolusu = request.form['txtrol']
    documento =  request.form['txtdocumento']

     #llamar a la conexion
    con = conectar()
    cursor = con.cursor()

    #crear el sql
    # verificar que el empleado exista
    sqldep = "SELECT docuemple FROM empleados WHERE docuemple=%s"
    cursor.execute(sqldep, (documento,))
    resultado = cursor.fetchone()

    if resultado:

    # validar si usuario ya existe
        sql_validar = "SELECT * FROM usuarios WHERE usuario=%s"
        cursor.execute(sql_validar, (usuario,))
        existe = cursor.fetchone()

        if existe:
            print("El usuario ya existe")

        else:
            sql = "INSERT INTO usuarios (usuario, password, rol, docuemple) VALUES (%s, %s, %s, %s)"
            valores = (usuario, password, rolusu, documento)

            cursor.execute(sql, valores)
            con.commit()

            print("Usuario empleado registrado")

    else:
        print("Empleado no existe")
    

    return redirect(url_for('inicio'))

if __name__== '__main__':
    app.run(debug=True)