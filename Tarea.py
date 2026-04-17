# Equipo Participantes : # - Carlos Alberto Correa - 2240396 / # - Clara Acevedo Urbano - 2240713 / # - Jhon Brandon Arboleda - 2243499 

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

libros = []
leyendo = []

class Libro(BaseModel):
    id: int
    titulo: str = Field(..., min_length=1)
    autor: str = Field(..., min_length=1)
    categoria: str
    anio_publicacion: int
    total_ejemplares: int = Field(..., gt=0)
    ejemplares_disponibles: int

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}

@app.post("/libros")
def crear_libro(libro: Libro):
    libros.append(libro)
    return {"mensaje": "Libro creado"}

@app.get("/libros")
def listar_libros():
    return libros

@app.get("/libros/{id}")
def obtener_libro(id: int):
    for libro in libros:
        if libro.id == id:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.put("/libros/{id}")
def actualizar_libro(id: int, libro_actualizado: Libro):
    for i, libro in enumerate(libros):
        if libro.id == id:
            libros[i] = libro_actualizado
            return {"mensaje": "Libro actualizado"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.delete("/libros/{id}")
def eliminar_libro(id: int):
    for libro in libros:
        if libro.id == id:
            libros.remove(libro)
            return {"mensaje": "Libro eliminado"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.post("/libros/{id}/prestar")
def prestar_libro(id: int):
    for libro in libros:
        if libro.id == id:
            if libro.ejemplares_disponibles <= 0:
                raise HTTPException(status_code=400, detail="No hay ejemplares disponibles")
            libro.ejemplares_disponibles -= 1
            return {"mensaje": "Libro prestado"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.post("/leyendo")
def agregar_leyendo(libro: Libro):
    leyendo.append(libro)
    return {"mensaje": "Libro agregado a lectura actual"}

@app.get("/leyendo")
def ver_leyendo():
    return leyendo