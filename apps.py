from flask import Flask ,render_template,url_for,request,flash,redirect,session
from database import conectar



#crear la app del proyecto

apps = Flask(__name__)
apps.secret_key = "789456123"

#crear ruta de ingresar y mostrar el formulario
@apps.route('/')
def login():

     return render_template("login.html")


#procesar el formulario

@apps.route('/login',methods=["POST"])
def login_form():
         #crea variables de python user, contraseña para recibir del formulario
        user = request.form['txtusuario']
        password = request.form['txtcontrasena']

        #llamar a la bd

        con = conectar()
        cursor = con.cursor()

        sql = "SELECT  * FROM usuarios WHERE usuario=%s AND password=%s"
        cursor.execute(sql,(user,password))

        #resultado de la consulta
        user = cursor.fetchone()

        if user:

            #guarda las variables de sesion
            session['usuario'] = user[1]
            session['rol'] = user[3]  #olumna del rol


            #if rol == rol:

            if user[3] == "administrador":
                      return redirect(url_for('inicio'))
            else:
                return "Bienvenido empleado"

        else:
             flash("Usuario y contraseña incorrecto", "danger")
             return  redirect(url_for('login'))
#validar sesion en la pagina inicial
@apps.route('/inicio')
def inicio():

      if 'usuario'  not in session:
            return redirect(url_for('login'))

      con = conectar()
      cursor = con.cursor()

      sql = "SELECT  * FROM usuarios"
      cursor.execute(sql)

      lista = cursor.fetchall()


      return render_template('index.html', user=lista)
#cerrar la sesion
@apps.route('/salir')
def  salir():
      session.clear()
      return redirect(url_for('login'))

#crearuna rato para eliminar los usuarios tipo empleado
@apps.route('/eliminar/<int:id>')
def eliminarusu(id):
     if 'usuario'  not in session:
            return redirect(url_for('login'))

     con = conectar()
     cursor = con.cursor()

     #buscar el usuario

     sql = "SELECT rol FROM usuarios WHERE id_usuario=%s"
     cursor.execute(sql, (id,))

     usuario = cursor.fetchone()

     #validar el rol del usuario
     if usuario:
           rol = usuario[0]

           if rol == "administrador":
                 flash("No se puede eliminar el administrador")

           else:
                 cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id,))
                 con.commit()
                 flash("Empleado eliminado")

     cursor.close()
     con.close()

     return redirect(url_for("inicio"))


if __name__ == '__main__':
    apps.run(debug=True)
