import pymysql

class DAOUsuario:
    def connect(self):
        return pymysql.connect("localhost","root","","electroquiz" )

    def login(self, data):
        con = DAOUsuario.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("SELECT * FROM usuarios where login = %s", (data['login'],))
            contra = cursor.fetchall()
            for row in contra:
                if  data['contraseña'] == row[3] :
                    return row[4]
                else:
                    return()
        except:
            return ()
        finally:
            con.close()
    
    def read(self, id):
        con = DAOUsuario.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM preguntas order by enunciado asc")
            else:
                cursor.execute("SELECT * FROM preguntas where id = %s order by enunciado asc", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
    
    def numero_filas_electricos(self):
        con = DAOUsuario.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("select count(*) from preguntas")
            numero = len(cursor.fetchall())
            return numero
        except:
            return ()
        finally:
            con.close()
    
    def update(self, id, data):
        con = DAOUsuario.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE preguntas set enunciado = %s, ans1 = %s, ans2 = %s, ans4 = %s, ans4 = %s, correct_ans = %s, tipo = %s where id = %s", (data['enunciado'],data['op1'],data['op2'],data['op3'],data['op4'],data['corr'],data['estate'],id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
    
    def delete(self, id):
        con = DAOUsuario.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM preguntas where id = %s", (id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    