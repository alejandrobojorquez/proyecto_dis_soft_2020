from flask import Flask, flash, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL
from dao.DAOUsuario import DAOUsuario

import mysql.connector
import random


app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = DAOUsuario()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'electroquiz'
mysql = MySQL(app)
ruta='/admin'

@app.route('/')
def inicio():
    if session.get('user'):
        return render_template('usuario/main.html')
    elif session.get('admin'):
        return render_template('admin/main.html')
    else:
        return render_template('index.html')
    


#GESTIÓN DE CUENTAS DE USUARIOS (REGISTER Y LOGIN)
@app.route('/signup', methods=['GET','POST'])
def signup():
    error = None
    success = None
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        
        nombres = request.form.get('nombre')
        login = request.form.get('username')
        password = request.form.get('pass1')
        password2 = request.form.get('pass2')
        tipo = "alumno"

        
        if len(nombres) < 4:
            error = "Colocar nombre completo"
        elif len(login) < 6:
            error = "Tu nombre de usuario debe contener al menos 6 caracteres"
        elif len(password) < 6:
            error = "Tu contraseña debe tener al menos 6 caracteres"
        elif password != password2:
            error = "Las contraseñas no coinciden"
        else:

            query = "INSERT INTO usuarios(id, nombres, login, clave, tipo) VALUES(NULL, %s, %s, %s, %s)"
            cur.execute(query, ( nombres, login, password, tipo))
            mysql.connection.commit()
            success = "¡Tu cuenta ha sido creada con éxito! :D"



    return render_template('register.html', error=error, msg=success)

@app.route('/login', methods = ['POST', 'GET'])
# @app.route('/usuario/')
def login():
    if request.method == 'POST' and request.form['login']:
        tipo=db.login(request.form)
        if tipo=="admin":
            session['admin']=True
            session['user']=False
            return render_template('admin/main.html')
        elif tipo=="alumno":
            session['user']=True
            session['admin']=False
            return render_template('usuario/main.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session['user'] = False
    session['admin'] = False
    return render_template('login.html')

#********************************************************************************************

@app.route('/categorias')
def categorias():
    if session.get('user'):
        return render_template('usuario/categorias.html')
    elif session.get('admin'):
        return render_template('admin/categorias.html')
    else:
        return render_template('login.html')

@app.route('/enviar_pregunta', methods=['GET','POST'])
def enviar_pregunta():
    error = None
    success = None
    cur = mysql.connection.cursor()

    
    
    if request.method == 'POST':
        
        enun = request.form.get('enunciado')
        altern1 = request.form.get('alt1')
        altern2 = request.form.get('alt2')
        altern3 = request.form.get('alt3')
        altern4 = request.form.get('alt4')
        correcta_rpta = request.form.get('cor_alt')
        estado = "n"
        altern_correcta = None
        
        if correcta_rpta == '1':
            altern_correcta=altern1
        elif correcta_rpta == '2':
            altern_correcta = altern2
        elif correcta_rpta == '3':
            altern_correcta = altern3
        else:
            altern_correcta = altern4        
        
        if len(enun) < 2:
            error = "Colocar enunciado"
        elif len(altern1) < 1:
            error = "Colocar alternativas"
        elif len(altern2) < 1:
            error = "Colocar alternativas"
        elif len(altern3) < 1:
            error = "Colocar alternativas"
        elif len(altern4) < 1:
            error = "Colocar alternativas"
        elif correcta_rpta == '0':
            error = "Indique la alternativa correcta"        
        else:
            
                
            query = "INSERT INTO preguntas(id, enunciado,ans1,ans2,ans3, ans4, correct_ans,tipo) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, ( enun, altern1, altern2, altern3, altern4, altern_correcta, estado))
            mysql.connection.commit()
            success = "¡Tu pregunta se ha enviado con éxito! :D"

    if session.get('user'):
        return render_template('usuario/enviarpregunta.html',error=error, msg=success)
    elif session.get('admin'):
        return render_template('admin/enviarpregunta.html',error=error, msg=success)
    else:
        return render_template('login.html')


#******************
#   Menus de los Quizzes de los  cursos
total=db.numero_filas_electricos()
    
numeros = [0] * total
@app.route('/electricos')
def electricos():
    
    total=db.numero_filas_electricos()
    
    numeros = [0] * total
    cuenta=0
    while cuenta < total:
        numeros[cuenta]=cuenta
        cuenta=cuenta+1

    if session.get('user'):
        return render_template('usuario/electricos_menu.html')
    elif session.get('admin'):
        return render_template('admin/electricos_menu.html')
    else:
        return render_template('login.html')



@app.route('/pregunta/', methods = ['POST', 'GET'])
def testeo1():
    cur = mysql.connection.cursor()
    cur.execute('select * from preguntas')
    data = cur.fetchall()
    elementos = len(data)
    x=random.randint(0,elementos-1)
    
    
    msg=None
    q_select=None
    q_select=data[x]
    if request.method == 'POST':
        
        opcion = request.form.get('opcion')     
        

        if opcion == q_select[6]:
            msg = "¡Bien Hecho!"
            return render_template('post_q.html', msg=msg)
        else:
            msg="¡Uy! Respuesta incorrecta"
            return render_template('post_q.html', msg=msg)
    return render_template('pregunta.html', question=data[x])




#*****************************************************







#****************************************
@app.route(ruta+'/')
# @app.route('/usuario/')
def evaluar():
    data = db.read(None)
    if session.get('admin'):
        return render_template('admin/evaluarpregunta.html', data = data)
    else:
        return render_template('login.html')

@app.route(ruta+'/update/<int:id>/')
def update(id):
    data = db.read(id);
    if session.get('admin'):
        if len(data) == 0:
            return redirect(url_for('evaluar'))
        else:
            session['update'] = id
            return render_template('admin/update_q.html', data = data)
    else:
        return render_template('login.html')
    

@app.route(ruta+'/updateusuario', methods = ['POST'])
def updateusuario():
    if request.method == 'POST' and request.form['update']:

        if db.update(session['update'], request.form):
            flash('Se actualizo correctamente')
        else:
            flash('ERROR en actualizar')

        session.pop('update', None)

        return redirect(url_for('evaluar'))
    else:
        return redirect(url_for('evaluar'))

@app.route(ruta+'/delete/<int:id>/')
def delete(id):
    data = db.read(id);

    if len(data) == 0:
        return redirect(url_for('evaluar'))
    else:
        session['delete'] = id
        return render_template('admin/delete_q.html', data = data)

@app.route(ruta+'/deleteusuario', methods = ['POST'])
def deleteusuario():
    if request.method == 'POST' and request.form['delete']:

        if db.delete(session['delete']):
            flash('Pregunta Eliminada')
        else:
            flash('ERROR al eliminar')
        session.pop('delete', None)

        return redirect(url_for('evaluar'))
    else:
        return redirect(url_for('evaluar'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')



if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0",debug=True)

