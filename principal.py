#!/usr/bin/env python

"""En Python, cada uno de nuestros archivos .py se denominan módulos. Estos módulos, a la vez,
 pueden formar parte de paquetes. Un paquete, es una carpeta que contiene archivos .py. Pero, 
 para que una carpeta pueda ser considerada un paquete, debe contener un archivo de inicio 
 llamado __init__.py. Este archivo, no necesita contener ninguna instrucción. De hecho, puede
  estar completamente vacío."""

from flask_bootstrap import Bootstrap
""" del framework Bootstrap utilizamos la extansión Flask-Bootstrap para  trabajar con plantillas que utilicen hojas de 
 estilo y javascript. Se generan una plantilla base de la que podemos extender las nuestras."""


from flask import Flask, render_template,session, redirect, url_for, request, flash, send_file
"""Flask es un microframework (libreria)para Python para realizar aplicaciones web"""

from formulario import MyLogin, MyRegistro, MyConsultaCliente, MyConsultaProducto, MyConsulta, MyContrasenia
"""importan la clases que hemos creado"""

import archivo   # importa el modulo archivo

from flask_wtf import CSRFProtect
"""Por defecto Flask-WTF protege los formularios contra el ataque CSRF (Cross-Site Request Forgery o falsificación
 de petición en sitios cruzados). Este ataque se produce cuando un sitio web malicioso envía solicitudes a un sitio
  web en el que está conectada la víctima.

Para implementar la protección CSRF, Flask-WTF necesita que configuremos una clave de cifrado, para generar tokens
 encriptados que se utilizarán para verificar la autenticidad de la petición. Para ello, en nuestro programa
 principal:

app.secret_key = 'clave de cifrado lo más robusta posible'

Cada vez que generemos un formulario se incluirá un campo oculto que contendrá el token cifrado que permitirá 
verificar que el envió del formulario ha sido lícita. Para generar este campo oculto utilizamos el método 
form.csrf_token() que mostrará un código HTML parecido a este:

<input id="csrf_token" name="csrf_token" type="hidden" value="IjE5OWRiYmY0MGE2MT...">
"""

from datetime import datetime #importamos el modulo datetime


app = Flask(__name__)
"""El objeto app de la clase Flask es nuestra aplicación WSGI, que nos permitirá posteriormente 
desplegar nuestra aplicación en un servidor Web. Se le pasa como parámetro el módulo actual (__name__)."""
app.config["SECRET_KEY"] = "String dificil de adivinar"
bootstrap = Bootstrap(app)
Csrf = CSRFProtect(app)


@app.route("/logout")
def logout():
    """funcion para salir de la sesion generada al ingresar a traves de la pagina login"""
    session.pop('nombre', None) #borra variable y termina la sesion
    return redirect(url_for('index')) # se  redirecciona a pagina index


@app.route("/users", methods = ('GET', 'POST'))
def user():
    """listado de usuarios creados, solo se puede ver si el usuario que ingreso a la sesion es admin"""
    if session.get("nombre"): ## Si existe algún 'nombre' en sesión, si no es asi se muestra mensaje flash,
    # y se redirecciona a la pagina login, quiere decir que no se ha logueado

        users = archivo.leer("archivos_csv/passws.csv") # se guarda en users el contenido del archivo passws.csv
        return render_template('users.html', users = users) # se renderiza la pagina users.html
    flash('Debe estar logueado para acceder') # mensaje del tipo flash
    # mensajes rápidos es que una vez son requeridos a través de la función get_flashed_messages(en html) son 
     # eliminados de la lista de mensajes, por lo que estos mensajes aparecen en la página luego de que
     # la función  flash sea llamada y posteriormente desaparecen.   

    return redirect(url_for('login')) # se redirecciona la la pagina login, 

## la ruta(route) se utiliza para enlazar la url a una funcion (login()), si un usario visita la pagina login
## el retorno de la funcion se muestra en el explorador

"""El decorador router gestiona la petición HTTP recibida y crea un objeto reponse con la respuesta HTTP: 
el código de estado, las cabaceras y los datos devueltos. Esta respuesta la prepara a partir de lo que 
devuelve la función vista ejecutada con cada route. Esta funcion devuelve:
    -Una cadena, o la generación de una plantilla (que veremos posteriormente). Por defecto se indica un 
    código 200 y las cabeceras por defecto.
"""
@app.route("/login", methods = ('GET', 'POST'))## se accede a la url login a traves de los metodo get o post
"""Enviando y gestionando la información del formulario

Vamos a usar un patrón de diseño basado en la creación de una vista que se comporte de la siguiente manera:

   1-La primera vez que accedemos a la ruta accedemos utilizando el método GET. En nuestro caso se creará un 
    formulario sin datos (ya que request.form no tiene ningún dato) , el formulario no se ha enviado y por
    lo tanto se devuelve la plantilla con el formulario vacío.
   2- Se rellena el formulario y se manda la información a la misma ruta pero utilizando el método POST.
    En este caso se crea un formulario que se rellena con la información que se ha recibido del formulario.
   3- Si el formulario es válido se gestiona la información y se realiza la acción que se tenga que hacer 
    (guardar en una base de datos, mostrar una plantilla resultado,...)
   4-Si el formulario no es válido se vuelve a generar la plantilla con el formulario con datos, mostrando 
    si lo hemos codificado los errores de validación oportunos.
"""

def login():
    """Aqui se realiza el logueo del usuario, se valida si el usuario se encuentra registrado comparando los datos
     ingresados en la pagina con con los datos de usuarios registrados que contiene el archivo passws.csv, esta info es
     asignada  a la variable user2. Si el usuario ingresado es admin, se redigira a la pagina ventas, sino a la pagina
     usuario"""
    user2 = archivo.leer("archivos_csv/passws.csv") # se asigna a user2 el contenido del archivo passws.csv
    form2 = MyLogin()
    #podemos crea un objeto a partir de la clase MyLogin() que se importo y creo previamente
    # en  el archivo formulario.py
    if form2.validate_on_submit(): # Nos permite comprobar si el formulario ha sido enviado y es válido.
        for l in user2: #se recorre el contenido de la varialbe users2 (diccionario con lista de usuarios)
            if l['usuario'] == form2.usu.data.strip(): # Para cada campo form2.usu.data nos devuelve su valor.
            ## se comprueba que el contenido en usuario sea igual al usuario ingresado
                if l['login'] == form2.passw.data.strip(): 
                ## se comprueba que el contenido en login sea igual al login ingresado
                    session["nombre"] = form2.usu.data.strip()
                    """Cuando un usuario se haya logueado de manera adecuada, se crea variable de sesiones 
                     el nombre de usuario. si el usuario sale del sistema ira a logout para borrar dicha variable
                      y terminar la sesión.
                    """
                    return redirect(url_for('ventas')) ## si el usuario y login conciden con la info de users2, se 
                    # redirecciona a la pagina ventas.html
                    #con la funcion redirec realizamos una redicirección HTTP a otra URL 
                else:
                    form2.passw.data = "" # si el login no coincide, se limpia el campo
                    # a traves de la variable msj, en html se informa que se verifique la contraseña
                    return render_template('login.html', form = form2, msj = "ok")
                    #se renderiza la pagina login con el mensajer de verificar contraseña
        form2.passw.data = "" # se limpia campo
        form2.usu.data = "" #se limpia campo
         ##a traves de la variable msj, en html se informa usuario no encontrado
        return render_template("login.html", form=form2, msj="mal")
        # se rendieriza pagina con mensaje usario no encontrado
    return render_template("login.html", form = form2) #aca se ingresa por primera vez
"""Flask utiliza por defecto jinja2 para generar documentos HTML, para generar una plantilla 
utilizamos la función render_template que recibe como parámetro el fichero donde guardamos la 
plantilla y las variables que se pasan a esta."""
## Las plantillas las vamos a guardar en ficheros en el directorio templates


@app.route("/")
@app.route("/index", methods = ('GET', 'POST'))
def index():
    """pagina de bienvenida al iniciar la aplicacion"""
    if not session.get("nombre"):## Si no existe algún 'nombre' en sesión
    ## //esta mal!!!, va if session.gent("nombre")
       return render_template('index.html')
    return redirect(url_for('login'))


@app.route("/registro", methods = ('GET', 'POST'))
def registro():
    """Aqui se realiza la registracion de nuevos usuarios, se valida si el usuario se encuentra registrado comparando
    los datos ingresados en la pagina con con los datos de usuarios registrados que contiene el archivo passws.csv, esta
     info es asignada  a la variable user, luego de esta validacion se comparan que coincidan los campos que hacen
     refencia al nombre y contraseñaa del nuevo usuario, si esto es afirmativo, se procedera a grabar los datos en el
     arhivo passws.csv"""
    def limpiar():
        #limpieza de los campos de la pagina
        form.passw1.data = " "
        form.usu1.data = " "
        form.passw.data = " "
        form.usu.data = " "
    user = archivo.leer("archivos_csv/passws.csv")
    form = MyRegistro()
    registrado = True
    if form.validate_on_submit():
        for l in user: ## se recorre lista para buscar si el usuario se encuentra registrado
            if l['usuario'] == form.usu.data.strip():
                limpiar()
                # a traves de la vairable msj, en html se informa que usuario se encuentra registrado
                return render_template('registro.html', form = form, msj="reg")
            else:
                 registrado = False # si no esta registrado se asigna a la varible false
        if form.passw1.data.strip() == form.passw.data.strip(): # verifica que lo ingresado coincida
            if form.usu1.data.strip() == form.usu.data.strip(): # verifica que lo ingresado coincida
                if registrado == False: # si registrado es false
                ## graba lo ingresado al archivo
                    archivo.grabar("archivos_csv/passws.csv", form.passw.data.strip(), form.usu.data.strip())
                    limpiar() #  funcion que limpia los campos
                    # a traves de la variable msj, en html se informa la registracion exitosa
                    return render_template('registro.html', form = form, msj = "ok")
            else:
                # a traves de la variable usu, en html se muestra mensaje indicando que no coinciden los usuarios ingresados
                return render_template('registro.html', form=form, msj="usu")
        else:
            # a traves de la variable msjn en html se muestra mensaje indicando que no coinciden las contraseñas ingresadas
            return render_template('registro.html', form=form, msj="pass")
    return render_template('registro.html', form  = form)


@app.route("/ventas")
def ventas():
    """Pagina de bienvenida para el usuario logueado admnin"""
    if session.get("nombre"):## Si existe algún 'nombre' en sesión
        clientes = archivo.leer("archivos_csv/archivo.csv")
        ## se valida el archivo, si fue exitosa, a traves de la variable clientes se envia los datos
        ##  a traves de usuario el nombre de la persona que se logueo y con ff se genera la tabla
        ##(modificado, error en el final)
        return render_template('ventas.html', clientes = clientes, usuario = session.get('nombre'), ff = True)
    flash('Debe estar logueado para acceder')
    return redirect(url_for('login'))


# para el final se modifico, no se usa mas
# @app.route("/usuario")
# def usuario():
#     """Pagina de bienvenida para el usuario logueado que NO es admin"""
#     usuario = session['nombre'] #se asigna a la variable usuario el valor de la session
#     return render_template('usuario.html', usuario = usuario)#se renderiza la pagina usuario


@app.route("/cliente", methods = ('GET', 'POST'))
def cliente():
    """Funciona junto con la pagina mostrar para listar todos los productos que compro un cliente, en esta pagina el
    usuario debe ingresar 3 caracteres que componen el nombre del cliente a buscar, como resultado se obtendra una lista
    de posibles clientes, en la cual el usuario debe elegir uno de ellos, y al clickear el boton seleccionar se
    redireccionara a la pagina mostrar, en donde se visualizara el listado"""
    if session.get("nombre"):## Si existe algún 'nombre' en sesión
        form = MyConsultaCliente()
        lista_busqueda = archivo.lista_clientes("archivos_csv/archivo.csv") # archivo que contiene lista de
        ## clientes solamente
        ff = False # se inicializa la variabla  false
        msg = "" # se inicializa la variable vacio
        if form.validate_on_submit():
            lista = [] #crea lista vacia
            if form.cliente.data != None:  # si el contenido del campo es distinto de none
                for palabra in lista_busqueda: # se recorre la lista
                    if form.cliente.data.upper() in palabra: # si las letras ingresadas estan en la lista 
                    #se guarda en lista las coincidencias
                        lista.append(palabra)
                if len(lista) != 0: #si la lista no esta vacia
                    ff = True # se asignat true
                else:
                    ff = False # se asigna false
                    msg = "No se encontro nombre del cliente"
                    # ff habilita la visualizacion del contenido de la variable lista, y se muestra las
                    # coincidencias al renderizar la pagina cliente
                return render_template("cliente.html", form = form, lista = lista, msg = msg , ff = ff)
        return render_template("cliente.html", form = form, ff = False) #aca se ingresa por primera vez
    flash('Debe estar logueado para acceder')
    return redirect(url_for('login'))
    # la función redirect le dice al navegador del cliente que navegue a una página difrente en vez de la requerida.


@app.route("/producto", methods = ('GET', 'POST'))
def producto():
    """ Funciona junto con la pagina mostrar para listar todos los clientes que compraron un  determinado producto, en
    esta pagina el usuario debe ingresar 3 caracteres que componen el nombre del producto a buscar, como resultado se
    obtendra una lista de posibles productos, en la cual el usuario debe elegir uno de ellos, y al clickear el boton
    seleccionar se redireccionara a la pagina mostrar, en donde se visualizara el listado"""
    if session.get("nombre"):
        form = MyConsultaProducto()
        lista_busqueda = archivo.lista_producto("archivos_csv/archivo.csv")
        ff = False
        msg = ""
        if form.validate_on_submit():
            lista = []
            if form.producto.data != None:
                for palabra in lista_busqueda:
                    if form.producto.data.upper() in palabra:
                        lista.append(palabra)
                if len(lista) != 0:
                    ff = True
                else:
                    ff = False
                    msg = "No se encontro nombre del producto"
                    # ff habilita la visualizacion del contenido de la variable lista
                return render_template('producto.html', form = form, lista = lista, msg = msg , ff = ff)
        return render_template('producto.html', form = form, ff = False)#aca se ingresa por primera vez
    flash('Debe estar logueado para acceder')
    return redirect(url_for('login'))


@app.route("/mostrar", methods=('GET', 'POST'))
def mostrar():
    """En base al nombre seleccionado en las paginas cliente o producto, se genera el listado correspondiente, el mismo
    se visualizara en esta misma pagina"""
    if session.get("nombre"):
        if request.method == 'POST': ##El método HTTP con el qué hemos accedido.
            lista = [] # se declara lista vacia
            msg = "" # variable msg se asigna vacia
            msg2 = ""
            msg3 = ""
            listado = archivo.leer("archivos_csv/archivo.csv")
            """ objeto request.form : Información recibida en el cuerpo de la petición cuando se utiliza el método POST, 
            enviada a traves del formulario en la pagina clientes.html o productos.html."""
            seleccion = request.form['selecc'] # se asigna a la variable seleccion el option button seleccionado de la
            ##pagina clientes o productos
            for l in listado: # recorre los datos del archivo
                if seleccion == l['CLIENTE']: # si la seleccion coincide con la info del campo cliente
                    msg = "Listado de todos los productos que compro un Cliente"
                    msg2 = seleccion
                    msg3 = "cliente"
                    lista.append(l)
                elif seleccion == l['PRODUCTO']:
                    lista.append(l)
                    msg = "Listado de clientes que comparon un producto"
                    msg2 = seleccion
                    msg3 = "producto"
                    # ff no va !!
                    # la variable msg es titulo de la consulta, msg2 item seleccionado, msg para volver
                    # a la pagina donde se origino la consulta, se usa en boton volver
            archivo.grabar_consulta(lista,msg, msg2)
            return render_template('mostrar.html', lista=lista, ff=True, msg=msg, msg2=msg2, msg3=msg3)
        return render_template('mostrar.html') ## se ingresa desde el navegador
    flash('Debe estar logueado para acceder')
    return redirect(url_for('login'))


@app.route("/mejores_clientes", methods = ('GET', 'POST'))
def mejores_clientes():
    """En esta pagina se generara y visualizara el listado de los clientes que realizaron la mayor cantidad de compras,
     para realizar esto se necesita:
      l- la cantidad de clientes que se quiere mostrar, el usuario ingresara este dato.
      2- la informacion de las ventas se obtiene del archivo archivo.csv, el cual sera leido y asignados los datos en la
         variable listado.
      3- la  variable lista_busqueda en la cual se asigna el listado de clientes sin duplicados que contiene el archivo
         archivo.csv.
      Primero se genera una lista que contiene el nombre del cliente y cuanto gasto, y luego con ella se genera otra
      lista con la cantidad de items que pide el usuario, se la ordena para que los valores sean visualizados en forma
      descendente."""
    if session.get("nombre"):
        form = MyConsulta()
        if form.validate_on_submit():
            listado = archivo.leer("archivos_csv/archivo.csv")
            masgasto = []
            consulta = []
            lista_busqueda = archivo.lista_clientes("archivos_csv/archivo.csv")
            for listcli in lista_busqueda: ##recorre  lista de clientes
                gastoTotal = 0
                for clientes in listado: ## recorre archivo ventas
                # en estos dos recorridos se busca agrupar los datos por cliente
                    if listcli == clientes['CLIENTE']:
                        gasto = float(clientes['CANTIDAD']) * float(clientes['PRECIO'])
                        gastoTotal = gastoTotal + gasto
                        #se calcula cuanto gasto cada cliete
                masgasto.append([listcli, gastoTotal]) #se guarda lista cuanto gasto cada cliente
            cont = 1
            masgasto.sort(key=lambda c: c[1], reverse=True) # se ordena la lista masgasto de mayor a menor
            # print(masgasto) ## no va
            for datos in masgasto: #recorre lista mas gasto 
                if cont <= form.cantidad.data: # si contador es menor/igual al dato que ingreso el usuario
                    consulta.append(datos) #agrega lista consulta registro
                    cont = cont + 1 # 
            archivo.grabar_consulta_mjor_cliente(consulta)# se graba la consulta en archivo consulta.csv
            return render_template('mejores_clientes.html', form = form, fc = True, consulta = consulta, msg2 = "IMPORTE")
            # la variable fc se usa como condicion para mostrar la info en la variable consulta
            # msg2 se usa para agregar nombre celda en la tabla
        return render_template('mejores_clientes.html', form = form)#aca se ingresa por primera vez
    flash('Debe estar logueado para acceder')
    return redirect(url_for('login'))

@app.route("/mas_vendidos", methods = ('GET', 'POST'))
def mas_vendidos():
    """En esta pagina se generara y visualizara el listado de los productos de mayor venta para realizar esto se
    necesita:
          l- a cantidad de productos que se quiere mostrar, el usuario ingresara este dato.
          2- la informacion de las ventas se obtiene del archivo archivo.csv, el cual sera leido y asignados los datos
           en la variable listado.
          3- la  variable lista_busqueda en la cual se asigna el listado de productos sin duplicados que contiene el
          archivo archivo.csv.
          Primero se genera una lista que contiene el nombre del producto, cantidad vendida y codigo, y luego con ella
          se genera otra lista con la cantidad de items que pide el usuario, se la ordena para que los valores sean
          visualizados en forma descendente."""
    if session.get("nombre"):
        form = MyConsulta()
        if form.validate_on_submit():
            listado = archivo.leer("archivos_csv/archivo.csv")
            masvendio = []
            consulta = []
            lista_busqueda = archivo.lista_producto("archivos_csv/archivo.csv")
            for listcli in lista_busqueda: # recorre lista de productos
                cant = 0
                codigo = 0
                for clientes in listado: # reocorre lista de ventas
                    if listcli == clientes['PRODUCTO']:
                         cant = cant + float(clientes['CANTIDAD']) #va acumulando cantidad vendidad
                         codigo = clientes['CODIGO']
                masvendio.append([codigo, listcli,int(cant) ]) #agrega en lista datos de codigo,cliente y cant
            cont = 1
            masvendio.sort(key=lambda c: c[2], reverse=True) #ordena de mayor a menor
            for datos in masvendio:
                if cont <= form.cantidad.data: #si contador es menor cantidad ingressada por el usuario
                    consulta.append(datos)
                    cont = cont + 1
            archivo.grabar_consulta_mas_vendidos(consulta) #guarda consulta en archivo consulta.csv
            return render_template('mas_vendidos.html', form = form, fc = True, consulta = consulta, msg2 = "CANTIDAD")
        return render_template('mas_vendidos.html', form = form)#aca se ingresa por primera vez
    flash('Debe estar logueado para acceder')
    return redirect(url_for('login'))


@app.errorhandler(404)
def no_encontrado(e):
    """en caso de error se muestra la pagina 404.html"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_interno(e):
    """en caso de error se muestra la pagina 500.html"""
    return render_template('500.html'), 500


@app.route("/cambio-contrasenia", methods = ('GET', 'POST'))
def cambio_contrasenia():
    """cambio de contraseña del usuario, se guarda en variable el diccionario, para
    poder asignarle el cambio de contraseña, y luego se guarda en archivo la modificacion realizada"""
    if session.get("nombre"):
        form = MyContrasenia()
        if form.validate_on_submit():
            usuarios = archivo.leer("archivos_csv/passws.csv")
            if form.passw1.data.strip() == form.passw.data.strip(): # si los datos ingresado coinciden
                for l in usuarios : # recorre la lista con los datos de los usuarios
                    if l['usuario'] ==  session["nombre"] : # si nombre de session es igual dato usuario en lista
                        l['login'] = form.passw1.data.strip() # se cambia login con el ingresado
                archivo.grabar_lista("archivos_csv/passws.csv", usuarios) # guarda los datos igresados en el archivo
                return render_template('cambio-contrasenia.html', form=form, msj="ok") # envia mesaje cambio exitoso
            else:
                return render_template('cambio-contrasenia.html', form=form, msj="mal") # los datos ingresados no coinciden
        return render_template('cambio-contrasenia.html', form=form)#aca se ingresa por primera vez
    flash('Debe estar logueado para acceder')
    return redirect(url_for('login'))


@app.route('/bajar-archivo/')
## rutas terminando en / son consideradas como un directorio de un sistema de fichero
def baja_archivo():
    """funcion que permite desde la web bajar el archivo consulta, asignandole un nombre
    con determinado formato"""
    if session.get("nombre"):
      nombre_arch = "resultados_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv" # se establece el formato del 
      ## nombre del archivo
      return send_file('archivos_csv/consulta.csv', as_attachment=True, attachment_filename=nombre_arch, cache_timeout=6)
      # se baja el archivo csv: nombre de archvivo, envio con contenido header, nombre de archivo que se va a bajar, tiempo de la info en el cache
    flash('Debe estar logueado para acceder')
    return redirect(url_for('login'))

if __name__ == "__main__":
    """si ejecutamos este módulo se ejecuta el método run que ejecuta un servidor web para
     que podamos probar la aplicación."""
    app.run()
