from flask import Flask, redirect, render_template, request, url_for
from modelo.Dao import Categoria, Juego, db
app = Flask(__name__)

# datos
games= ['GTA', 'Among us', 'Fortnite',
          'Counter Strike', 'Warzone', 'Mario Kart 4']
cate = ['Accion', 'Battle Royale', 'Aventura', 'Arcade', 'Simulacion']
bib = ['GTA', 'Fortnite', 'Warzone']
usuarios = ['Cinti', 'Hector', 'Edgar']

#base de datos
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/gamestore' #cadena de conexion
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/')
def index():
    return render_template('principal.html')


@app.route('/validar', methods=['post'])
def validar():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    cont = 0
    contrasenas = ['123', '456', '789']
    for u in usuarios:
        # si el usuario es igual a lo que esta en usuarios y lo de contrasena igual a lo que esta en contrasenas
        if u == usuario and contrasena == contrasenas[cont]:
            return render_template('menu.html', usuario=usuario)
        cont = cont+1
    return render_template('login.html', aviso='datos incorrectos')

# juegos
@app.route('/juegos', methods=['GET'])
def juegos():
    game=Juego()
    games=game.consultaGeneral()
    return render_template('juegos/juegos.html', games=games)

@app.route('/juegos/consultarImagen/<int:id>')
def consultarImagenJuego(id):
    game=Juego()
    return game.consultarImagen(id)    

@app.route('/registrarJuego', methods=['GET', 'POST'])
def registrarJuego():
    if request.method == 'POST':
        gameA=Juego()
        gameA.nombre=request.form['nombreJuego']
        gameA.descripcion=request.form['descJuego']
        gameA.precio=request.form['precioJuego']
        gameA.existencia=request.form['existJuego']
        gameA.id_categoria=request.form['categoria']
        gameA.imagen=request.files['imagenJuego'].stream.read()
        gameA.estatus='Activo'
        gameA.agregar()
        return redirect(url_for('juegos'))
    cate=Categoria()
    cates=cate.consultaGeneral()    
    return render_template('juegos/registrarJuego.html', cates=cates)

@app.route('/actualizarJuego/<int:numJuego>', methods=['GET', 'POST'])
def actualizarJuego(numJuego):
    if request.method == 'POST':
        gameA=Juego()
        gameA.id_juego=numJuego
        gameA.nombre=request.form['nombreJuego']
        gameA.descripcion=request.form['descJuego']
        gameA.precio=request.form['precioJuego']
        gameA.existencia=request.form['existJuego']
        gameA.id_categoria=request.form['categoria']
        gameA.imagen=request.files['imagenJuego'].stream.read()
        gameA.estatus='Activo'
        gameA.editar()
        return redirect(url_for('juegos'))  
    cate=Categoria()
    cates=cate.consultaGeneral()
    j=Juego() 
    j=j.consultaIndividual(numJuego)
    return render_template('actualizarJuego.html', game=j, cates=cates)

@app.route('/eliminarJuego/<int:numJuego>', methods=['GET', 'POST'])
def eliminarJuego(numJuego):
    j=Juego()
    if request.method == 'POST':
        j.eliminar(numJuego)
        return redirect(url_for('juegos'))
    j=j.consultaIndividual(numJuego)
    return render_template('eliminarJuegos.html', game=j)

@app.route('/videojuego/<int:numJuego>', methods=['get', 'POST'])
def verVideojuego(numJuego):

    precios = ['', '200', '67', '160', '300', '400', '600']
    return 'el videojuego que elegiste es: ' + juegos[numJuego]+' y su precio es ' + precios[numJuego]
# fin juegos

# categorias
@app.route('/categorias', methods=['GET'])
def categorias():
    cate=Categoria()
    cates=cate.consultaGeneral()
    return render_template('categorias/categorias.html', cates=cates)

@app.route('/registrarCategoria', methods=['GET', 'POST'])
def registrarCategoria():
    if request.method == 'POST':
        nomCate = request.form['nombreCategoria']
        #codigo para guardar en la BD
        catN=Categoria()
        catN.nombre=nomCate
        catN.imagen=request.files['imgCategoria'].stream.read()
        catN.estatus='Activa'
        catN.agregar()
        return redirect(url_for('categorias'))
        #return'categoria guardada'
    return render_template('categorias/registrarCategoria.html') 

@app.route('/actualizarCategoria/<int:numCategoria>', methods=['GET', 'POST'])
def actualizarCategoria(numCategoria):
    if request.method == 'POST':
        nomCate = request.form['nombreCategoria']
        cate[numCategoria-1] = nomCate
        return redirect(url_for('categorias'))
    return render_template('actualizarCategoria.html', numCategoria=numCategoria, cate=cate[numCategoria-1])


@app.route('/eliminarCategoria/<int:numCategoria>', methods=['GET', 'POST'])
def eliminarCategoria(numCategoria):
    if request.method == 'POST':
        nomCate = request.form['nombreCategoria']
        cate.remove(nomCate)
        return redirect(url_for('categorias'))
    return render_template('eliminarCategoria.html', numCategoria=numCategoria, cate=cate[numCategoria-1])

# Biblioteca


@app.route('/biblioteca', methods=['GET'])
def biblioteca():
    return render_template('biblioteca.html', bib=bib)

@app.route('/registrarBiblioteca', methods=['GET', 'POST'])
def registrarBiblioteca():
    if request.method == 'POST':
        np = request.form['nombreJuegoBib']
        bib.append(np)
        # print(np)
        return redirect(url_for('biblioteca'))
    return render_template('registrarBiblioteca.html')



@app.route('/actualizarBiblioteca/<int:numBiblioteca>', methods=['GET', 'POST'])
def actualizarBiblioteca(numBiblioteca):
    if request.method == 'POST':
        np = request.form['nombreJuegoBib']
        bib [numBiblioteca-1]=np
        return redirect(url_for('biblioteca'))
    return render_template('actualizarBiblioteca.html', numBiblioteca=numBiblioteca, bib=bib[numBiblioteca-1])

@app.route('/eliminarBiblioteca/<int:numBiblioteca>', methods=['GET', 'POST'])
def eliminarBiblioteca(numBiblioteca):
    if request.method == 'POST':
        np = request.form['nombreBiblioteca']
        bib.remove(np)
        return redirect(url_for('biblioteca'))
    return render_template('eliminarBiblioteca.html', numBiblioteca=numBiblioteca, bib=bib[numBiblioteca-1])

# Ajustes

@app.route('/perfiles', methods=['GET'])
def perfiles():
    return render_template('perfiles.html', usuarios=usuarios)

@app.route('/registrarUsuario', methods=['GET', 'POST'])
def registrarUsuario():
    if request.method == 'POST':
        np = request.form['nombreUsuario']
        usuarios.append(np)
        # print(np)
        return redirect(url_for('perfiles'))
    return render_template('registrarUsuario.html')



@app.route('/actualizarUsuario/<int:numUsuario>', methods=['GET', 'POST'])
def actualizarUsuario(numUsuario):
    if request.method == 'POST':
        np = request.form['nombreUsuario']
        usuarios [numUsuario-1]=np
        return redirect(url_for('perfiles'))
    return render_template('actualizarUsuario.html', numUsuario=numUsuario, usuarios=usuarios[numUsuario-1])

@app.route('/eliminarUsuario/<int:numUsuario>', methods=['GET', 'POST'])
def eliminarUsuario(numUsuario):
    if request.method == 'POST':
        np = request.form['nombreUsuario']
        usuarios.remove(np)
        return redirect(url_for('perfiles'))
    return render_template('eliminarUsuario.html', numUsuario=numUsuario, usuarios=usuarios[numUsuario-1])

# Login
@app.route('/loguearse', methods=['GET'])
def loguearse():
    return render_template('login.html')


@app.route('/cerrarsesion', methods=['GET'])
def cerrarsesion():
    return render_template('principal.html')


@app.route('/regresar', methods=['GET'])
def regresar():
    return render_template('menu.html')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
#  python -m venv venv  crear el entorno virtula 
# venv\scripts\activate.bat actva el entorno virtual
# pip install flask para instalar flask solo una ves
# python -m main levantar el servidor