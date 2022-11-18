from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float,BLOB
from sqlalchemy.orm import relationship

db=SQLAlchemy()

class Categoria(db.Model):
    __tablename__='categorias'
    id_categoria=Column(Integer,primary_key=True)
    nombre=Column(String)
    imagen=Column(BLOB)
    estatus=Column(String)

    def consultarImagen(self,id):
        return self.consultaIndividual(id).imagen

    def consultaIndividual(self,id):
        return self.query.get(id)

    def consultaGeneral(self):
        return self.query.all()

    def editar(self):
        db.session.merge(self)
        db.session.commit()    

    def agregar(self):
        db.session.add(self)
        db.session.commit()  

    def eliminarCate(self,id):
        c=self.consultaIndividual(id)
        db.session.delete(c)
        db.session.commit()        

    def eliminacionLogica(self,id):
        c=self.consultaIndividual(id)
        c.estatus='Inactivo'
        c.editar()              

class Juego(db.Model):
    __tablename__='juegos'
    id_categoria=Column(Integer, ForeignKey('categorias.id_categoria'))
    nombre=Column(String)
    descripcion=Column(String)
    imagen=Column(BLOB)
    estatus=Column(String) 
    id_juego=Column(Integer, primary_key=True)
    precio=Column(Float)
    existencia=Column(Integer)
    categoria=relationship('Categoria',backref='juegos', lazy='select')

    def consultarImagen(self,id):
        return self.consultaIndividual(id).imagen

    def consultaIndividual(self,id):
        return self.query.get(id)    

    def consultaGeneral(self):
        return self.query.all()

    def editar(self):
        db.session.merge(self)
        db.session.commit()        

    def agregar(self):
        db.session.add(self)
        db.session.commit()         

    def eliminar(self,id):
        j=self.consultaIndividual(id)
        db.session.delete(j)
        db.session.commit()        

    def eliminacionLogica(self,id):
        j=self.consultaIndividual(id)
        j.estatus='Inactivo'
        j.editar() 