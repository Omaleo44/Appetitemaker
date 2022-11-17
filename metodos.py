from db import close_db, get_db
from formulario import Contactenos, Menu, Nosotros, Registro, Plato,ListaDeseo,Pedido, Usuario
import validacion
from flask import Flask, render_template, flash, request, redirect, url_for, session, send_file, current_app, g

def pasarAForm(id):
    form = Usuario()
    data = selectUsuario(id)
    form.nombres.default= data[0]
    form.apellidos.default= data[1]
    form.correo.default= data[2]
    form.identificacion.default =data[3]
    form.fechaDeNacimiento.default=data[4]
    form.celular.default =data[5]
    form.rol.default=data[6]
    form.process()
    return form

def validarDatosDeUsuario(usuario,correo,fechaDeNacimiento,celular,identificacion):
    error = None
    if len(usuario)<8:
        error = "El nombre de usuario es muy corto"
    if not validacion.isEmailValid(correo):
        error = "El correo ingresado no cumple con las características mínimas"
    if not celular.isdigit():
        error = 'No fue escrito un número de celular'
    if not len(celular)>=10 and len(celular)<=12:
        error = 'Número de celular no cumple con la longitud establecida'
    if not identificacion.isdigit():
        error = 'No fue escrito un número de identificaión'
    return error

def selectUsuario(idUsuario):
    db = get_db()
    orden = "SELECT nombres, apellidos, correo, identificacion, fechanacimiento, celular, rolID FROM Usuario WHERE id= ?"
    usuario = db.execute(orden, (idUsuario,)).fetchone()
    return usuario

def updateUsuario(id):
    datos = [request.form['nombres'], request.form['apellidos'], request.form['correo'], request.form['identificacion'], request.form['fechaDeNacimiento'], request.form['celular'], request.form['rol'], id ]
    nombres = datos[0]
    nombres = nombres.split(" ")
    apellidos = datos[1]
    apellidos = apellidos.split(" ")
    correo = datos[2]
    identificacion = datos[3]
    fechaDeNacimiento = datos[4]
    fechaDeNacimiento=fechaDeNacimiento.split("-")
    celular = datos[5]
    if validarDatosDeUsuario("NombreValido",correo,fechaDeNacimiento,celular,identificacion) ==  None:
        orden = "UPDATE Usuario SET nombres=?, apellidos = ?, correo=?, identificacion=?, fechanacimiento=?, celular=?, rolID=? WHERE id=?"
        db = get_db()
        db.execute(orden,(datos[0], datos[1], datos[2], datos[3], datos[4],  datos[5], datos[6], datos[7]))
        db.commit()
        db.close()

def getComentarios(id):
    db = get_db()
    comentariosTodos = db.execute('SELECT platoID, detalle, valoracion FROM Comentarios WHERE usuarioID = ?',(id,)).fetchall()
    comentariosTodos = list(comentariosTodos)
    comentariosTodos.reverse()
    comentarios=[]
    for i in range(len(comentariosTodos)):
        if(i>2):
            break
        else:
            comentarios.append(list(comentariosTodos[i]))
    for comentario in comentarios:
        consulta = db.execute('SELECT nombre FROM Plato WHERE id=?',(comentario[0],)).fetchall()
        if len(consulta) > 0:
            comentario[0] = consulta[0][0]
    return comentarios

def getPedidos(id):
    db = get_db()
    tiposDePedido = ["Solicitado", "Enviado", "Entregado"]
    pedidosTodos = db.execute('SELECT ID, estado FROM Pedido WHERE usuarioID = ?',(id)).fetchall()
    pedidosTodos = list(pedidosTodos)
    pedidosTodos.reverse()
    pedidos=[]
    for i in range(len(pedidosTodos)):
        if(i>2):
            break
        else:
            pedidos.append(list(pedidosTodos[i]))
    for pedido in pedidos:
        platosParaID = db.execute('SELECT platoID FROM PlatoPedido WHERE pedidoID=?',(pedido[0],)).fetchall()
        platosParaID = list(platosParaID)
        listaPlatos = ""
        for plato in platosParaID:
            consulta = db.execute('SELECT nombre FROM Plato WHERE id=?',(plato[0],)).fetchall()
            if len(consulta) > 0:
                listaPlatos[0] = consulta[0][0]
        pedido.append(listaPlatos)
        pedido[1] = tiposDePedido[pedido[1]]
    return pedidos

def getMenu():
    db = get_db()
    platosDatos = db.execute('SELECT *  FROM Plato').fetchall()
    platosDatos = list(platosDatos)
    platos=[]
    for i in range(len(platosDatos)):
        platos.append(list(platosDatos[i]))
    for plato in platos:
        valoraciones = db.execute('SELECT valoracion FROM Comentarios WHERE platoID=?',(plato[0],)).fetchall()
        valoracionPromedio = 0
        for val in valoraciones:
            valoracionPromedio += val[0]
        if len(valoraciones)==0:
            valoracionPromedio = 0
        else:
            valoracionPromedio /= len(valoraciones)    
        plato.append(int(valoracionPromedio)) 
    return platos   

