import os
import validacion
from formulario import Contactenos, Menu, Nosotros, Registro, Plato,ListaDeseo,Pedido, Usuario
from flask import Flask, render_template, flash, request, redirect, url_for, session, send_file, current_app, g
from db import close_db, get_db
from werkzeug.security import generate_password_hash, check_password_hash
from metodos import pasarAForm,getComentarios,getMenu,getPedidos, updateUsuario, validarDatosDeUsuario
app = Flask(__name__)
app.secret_key = os.urandom(24)

PlatosTempo = [ [3,2],[4,1] ]

@app.route('/')
def index():
    return render_template('home.html')

    
@app.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    user_id = session.get( 'user_id' )
    if user_id is None:
        return render_template('home.html')
    else:
        if (session.get( 'rol' )!=1):
            return render_template('dashboard.html')
        else:
            form = Menu()
            return render_template( 'menu.html',  form=form )
@app.route('/detplato', methods=('GET', 'POST'))
def detplato():
    if request.method == 'POST':
        plato = request.form['busqueda'].upper()
        select="SELECT * FROM PLATO WHERE NOMBRE LIKE'%"+plato+"%'"
        db = get_db()
        detplato = db.execute(
            select
        ).fetchall()
        close_db()
        return render_template('detplato.html', detplato = detplato, titulo="Busqueda")


@app.route('/busqueda', methods=('GET', 'POST'))
def busqueda():
    try:
        if request.method == 'POST':
            print("busqueda")
            plato = request.form['busqueda'].upper()
            print(plato)
            error = None
            db = get_db()
            # select="SELECT * FROM PLATO WHERE NOMBRE LIKE'%"+plato+"%'"
            select="SELECT * FROM PLATO"
            print(select)
            resplatos = db.execute(select).fetchall()
            print(resplatos[0][2])
            close_db()
            print(resplatos)
            form = Plato()
            return render_template('busqueda.html', form=form ,palabra=plato,resplatos = resplatos)
        return render_template('menu.html')
    except:
        return render_template('menu.html')


@app.route('/usuario', methods=('GET', 'POST'))
def usuarios():
    user_id = session.get( 'user_id' )
    if user_id is None:
        return redirect( url_for( 'login' ) )
    else:
        if (session.get( 'rol' )==1):
            return redirect( url_for( 'menu' ) )
            
    db = get_db()
    usuarios = db.execute(
    'SELECT id,usuario,nombres,apellidos,correo,identificacion,fechanacimiento,celular,rolID FROM Usuario'
    ).fetchall()
    return render_template('usuarios.html', usuarios = usuarios)
    
@app.route('/usuario/<id>', methods=('GET', 'POST'))
def usuario(id):  
    user_id = session.get( 'user_id' )
    if user_id is None:
        return redirect( url_for( 'login' ) )
    else:
        if (session.get( 'rol' )==1):
            return redirect( url_for( 'menu' ) )
    form = pasarAForm(id)
    comentario = getComentarios(id)
    pedido = getPedidos(id)
    if request.method == 'POST':
        updateUsuario(id)
    print(comentario)
    print(pedido)
    return render_template('usuario.html', form=form, comentario=comentario, pedido=pedido, titulo='Usuario')

@app.route('/usuario/<id>/edit', methods=('GET', 'POST'))
def editarUsuario(id):
    user_id = session.get( 'user_id' )
    if user_id is None:
        return redirect( url_for( 'login' ) )
    else:
        if (session.get( 'rol' )==1):
            return redirect( url_for( 'menu' ) )
    form = pasarAForm(id)
    if request.method == 'POST':
        updateUsuario(id)
        return redirect( url_for( 'usuarios' ) )
    return render_template('edit_usuario.html', form=form,  titulo='Editar usuario')

@app.route('/usuario/<id>/delete', methods=('GET', 'POST'))
def deleteUsuario(id):
    user_id = session.get( 'user_id' )
    if user_id is None:
        return redirect( url_for( 'login' ) )
    else:
        if (session.get( 'rol' )==1):
            return redirect( url_for( 'menu' ) )    
    form = pasarAForm(id)
    if request.method == 'POST':
        db = get_db()
        orden = "DELETE FROM Usuario WHERE id= ?"
        db.execute(orden,(id,))
        db.commit()
        db.close()
        return redirect( url_for( 'usuarios' ) )
    return render_template('delete_usuario.html', form=form, titulo='Eliminar usuario')

@app.route('/usuario/create', methods=('GET', 'POST'))
def crearUsuario():
    user_id = session.get( 'user_id' )
    if user_id is None:
        return redirect( url_for( 'login' ) )
    else:
        if (session.get( 'rol' )==1):
            return redirect( url_for( 'menu' ) )
    form = Usuario()
    if request.method == 'POST':
        datos = [request.form['nombres'], request.form['apellidos'], request.form['correo'], request.form['identificacion'], request.form['fechaDeNacimiento'], request.form['celular'], request.form['contraseña'], request.form['usuario'], request.form['rol'] ]
        correo = datos[2]
        identificacion = datos[3]
        fechaDeNacimiento = datos[4]
        fechaDeNacimiento=fechaDeNacimiento.split("-")
        celular = datos[5]   
        fallo = validarDatosDeUsuario(datos[7],correo,fechaDeNacimiento,celular,identificacion)
        db= get_db()
        if  fallo == None:
            orden = "SELECT id FROM Usuario WHERE identificacion= ?"
            if db.execute(orden,(datos[3],)).fetchone()  == None:
                orden = "SELECT id FROM Usuario WHERE correo= ?"
                if db.execute(orden,(datos[2],)).fetchone() == None:
                    orden = "SELECT id FROM Usuario WHERE usuario= ?"
                    if db.execute(orden,(datos[7],)).fetchone() == None:
                        orden = "INSERT INTO Usuario (nombres,apellidos,correo,identificacion,fechanacimiento,celular,password,usuario,rolID) VALUES (?,?,?,?,?,?,?,?,?)"
                        db.execute(orden,(datos[0], datos[1], datos[2], datos[3], datos[4],  datos[5], generate_password_hash(datos[6]),datos[7], datos[8]))
                        db.commit()
                        db.close()
                        return redirect( url_for( 'usuarios' ) )
                    else:
                        fallo = "Usuario ya existe en base de datos"    
                else:
                    fallo = "Correo ya existe en base de datos"
            else:
               fallo = "Identificacion ya existe en base de datos"
        if fallo is not None:
            flash(fallo)
        db.close()
    return render_template('create_usuario.html', form=form,  titulo='Editar usuario')

@app.route('/login', methods=('GET', 'POST'))
def login():
    try:
        if request.method == 'POST':
            db = get_db()
            error = None
            username = request.form['username'].lower()
            password = request.form['password']
            error = None
            if not username:
                error = 'Debes ingresar el usuario'
                flash( error )

            if not validacion.isUsernameValid(username):
                error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                flash(error)

            if not password:
                error = 'Contraseña requerida'
                flash( error )
            
            print(password)
            print(generate_password_hash(password))
            user = db.execute(
                'SELECT * FROM usuario WHERE lower(usuario) = ?  ', (username, ) 
            ).fetchone()
            close_db()
            if user is None:
                error = 'Usuario o contraseña inválidos'
                flash(error)

            else:                           
                pwd_almacenada= user[8]
                resultado=check_password_hash(pwd_almacenada,password)

                if(not resultado):
                    error = 'Usuario o contraseña inválidos'
                    flash(error)
                else:
                    session.clear()
                    session['user_id'] = user[0]
                    session['user_name'] = user[1]
                    session['rol'] = user[9]
                    return redirect( url_for( 'dashboard' ) ) 
            if error is not None:
                print("Tiene Errores")  
                return render_template("login.html")
            else:
                print("No Tiene Errores")  
                return render_template('dashboard.html')
        return render_template('login.html')
    except:
        return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route( '/logout' )
def logout():
    session.clear()
    return redirect( url_for( 'home' ) )

@app.route('/contacto', methods=('GET', 'POST'))
def contacto():
    form = Contactenos()
    return render_template( 'contacto.html',  form=form )

@app.route('/nosotros')
def nosotros():
    form = Nosotros()
    return render_template( 'nosotros.html',  form=form )

@app.route('/menu')
def menu():
    form = Menu()
    menu = getMenu()
    print(menu)
    return render_template( 'menu.html',  form=form, menu=menu ) 

@app.route('/plato/<id>')
def detalle_plato(id):
    db = get_db()
    detplato = db.execute(
        'SELECT * FROM plato WHERE id = ?', [id]
    ).fetchone()
    #print(detplato[1])
    close_db()
    return render_template('detalle_plato.html', detplato = detplato)
    #return render_template('detalle_plato.html')

@app.route('/gestion_platos')
def gestion_platos():
    print("Entró a gestión de platos")
    select = "SELECT * FROM PLATO"
    db = get_db()
    lista_platos = db.execute(
        select
    ).fetchall()
    close_db()
    return render_template('gestion_platos.html', lista_platos=lista_platos)


@app.route('/registro', methods=('GET', 'POST'))
def registro():
    form = Registro()
    if request.method == 'POST':
        datos = [request.form['nombres'], request.form['apellidos'], request.form['correo'], request.form['identificacion'], request.form['fechaDeNacimiento'], request.form['celular'], request.form['password'], request.form['username'], 1 ]
        correo = datos[2]
        identificacion = datos[3]
        fechaDeNacimiento = datos[4]
        fechaDeNacimiento=fechaDeNacimiento.split("-")
        celular = datos[5]   
        fallo = validarDatosDeUsuario(datos[7], correo,fechaDeNacimiento,celular,identificacion)
        db= get_db()
        if  fallo == None:
            orden = "SELECT id FROM Usuario WHERE identificacion= ?"
            if db.execute(orden,(datos[3],)).fetchone()  == None:
                orden = "SELECT id FROM Usuario WHERE correo= ?"
                if db.execute(orden,(datos[2],)).fetchone() == None:
                    orden = "SELECT id FROM Usuario WHERE usuario= ?"
                    if db.execute(orden,(datos[7],)).fetchone() == None:
                        orden = "INSERT INTO Usuario (nombres,apellidos,correo,identificacion,fechanacimiento,celular,password,usuario,rolID) VALUES (?,?,?,?,?,?,?,?,?)"
                        db.execute(orden,(datos[0], datos[1], datos[2], datos[3], datos[4],  datos[5], generate_password_hash(datos[6]),datos[7], datos[8]))
                        db.commit()
                        db.close()
                        return redirect( url_for( 'login' ) )
                    else:
                        fallo = "Usuario ya existe en base de datos"    
                else:
                    fallo = "Correo ya existe en base de datos"
            else:
               fallo = "Identificacion ya existe en base de datos"
        if fallo is not None:
            flash(fallo)
        db.close()
    return render_template('registro.html',  form=form)

@app.route('/pedido', methods=('GET', 'POST'))
def pedido():
    form = Pedido()
    menu = getMenu()
    PlatosPedidos=[]
    for jplato in PlatosTempo:
        for i in range(len(menu)):
            if menu[i][0] == jplato[0]:
                plato=[menu[i][1],jplato [1], menu[i][3],jplato [1] * menu[i][3] , menu[i][0]]
                PlatosPedidos.append(plato)  
    if request.method == ('POST'):
        db=get_db()
        valorTotal=0
        for plato in PlatosPedidos:
            valorTotal += plato [3]
        orden = "INSERT INTO Pedido (usuarioID, valorTotal, estado) VALUES (?,?,?)"
        db.execute(orden,(session['user_id'], valorTotal, 1))
        db.commit()
        consulta = db.execute('SELECT ID FROM Pedido WHERE usuarioID=?',(session['user_id'],)).fetchall()
        consulta = list(consulta)
        consulta.reverse()
        for plato in PlatosPedidos:
            valorTotal += plato [3]
            orden = "INSERT INTO PlatoPedido (platoID, pedidoID, cantidad,valor) VALUES (?,?,?,?)"
            if len(consulta) > 0:
                db.execute(orden,(plato[4], consulta[0][0] , plato[1],plato[2]))
                db.commit()
        db.close()
        
        
    return render_template('pedido.html',  form=form,lista_platos=PlatosPedidos)

@app.route('/listadeseos', methods=('GET', 'POST'))
def listaDeseo():
    form = ListaDeseo()
    return render_template('listadeseos.html',  form=form)


@app.route('/add_plato', methods=('GET', 'POST'))
def add_plato():
    form = Plato()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        #imagen = request.form['imagen']
        print(nombre)
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO plato (nombre, descripcion, precio, imagen)'
                ' VALUES (?, ?, ?, ?)',
                (nombre, descripcion, precio, '')
            )
            db.commit()
            return redirect(url_for('gestion_platos'))

    return render_template( 'add_plato.html',  form=form )

@app.route('/edit_plato/<id>', methods=('GET', 'POST'))
def edit_plato(id):
    form = Plato()
    db = get_db()
    detplato = db.execute(
        'SELECT * FROM plato WHERE id = ?', [id]
    ).fetchone()
    form.nombre.data = detplato[1]
    form.descripcion.data = detplato[2]
    form.precio.data = detplato[3]
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        #imagen = request.form['imagen']
        print(nombre)
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE plato SET nombre = ?, descripcion = ?, precio = ?, imagen = ?'
                ' WHERE id = ?',
                (nombre, descripcion, precio, '', id)
            )
            db.commit()
            return redirect(url_for('gestion_platos'))

    return render_template( 'edit_plato.html',  form=form, id=id )
    #form.descripcion.data = 'AppetiteMaker para disfrutar en familia'
    #return render_template( 'edit_plato.html',  form=form )

@app.route('/delete/<id>')
def delete(id):
    db = get_db()
    detplato = db.execute(
        'SELECT * FROM plato WHERE id = ?', [id]
    ).fetchone()
    # print(detplato[1])
    close_db()
    return render_template('delete.html', detplato=detplato)

@app.route('/delete/<id>/confirm')
def delete_confirm(id):
    db = get_db()
    db.execute(
        'DELETE FROM plato WHERE id = ?', [id]
    )
    db.commit()
    db.close()
    return redirect(url_for('gestion_platos'))

if __name__ == '__main__':
    app.run() 