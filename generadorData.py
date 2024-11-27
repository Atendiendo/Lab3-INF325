import random
import json
from py2neo import Graph, Node, Relationship

# Conexión a la base de datos Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", ""))  # Cambia la contraseña si configuraste otra

# Generar datos de prueba y almacenar en un diccionario para JSON
def generar_datos():
    data = {
        "sectores": [],
        "encargados": [],
        "arboles": [],
        "formularios": [],
        "plagas": [],
        "enfermedades": [],
        "conteos": [],
        "aspersores": []
    }
    
    # Crear sectores
    sectores = []
    for i in range(1, 21):
        sector = Node("Sector", id_sector=str(i), nombre=f"Sector {i}", area_m2=random.randint(100, 1000))
        sectores.append(sector)
        graph.merge(sector, "Sector", "id_sector")
        data["sectores"].append({"id_sector": str(i), "nombre": f"Sector {i}", "area_m2": sector["area_m2"]})
    
    # Crear encargados
    encargados = []
    for i in range(1, 21):
        encargado = Node(
            "Encargado",
            id_encargado=str(i),
            nombre=f"Encargado {i}",
            porcentaje_cumplimiento=random.randint(60, 100),
        )
        encargados.append(encargado)
        graph.merge(encargado, "Encargado", "id_encargado")
        graph.merge(Relationship(encargado, "SUPERVISA", sectores[i-1]))
        data["encargados"].append({
            "id_encargado": str(i),
            "nombre": f"Encargado {i}",
            "porcentaje_cumplimiento": encargado["porcentaje_cumplimiento"]
        })
    
    # Lista de tipos de frutos y sus nombres científicos
    tipos_arboles = [
        {"tipo": "palto", "nombre_cientifico": "Persea americana"},
        {"tipo": "nogal", "nombre_cientifico": "Juglans regia"},
        {"tipo": "manzano", "nombre_cientifico": "Malus domestica"},
        {"tipo": "naranjo", "nombre_cientifico": "Citrus sinensis"},
    ]
    
    # Crear árboles y relacionarlos con sectores
    arboles = []
    for i in range(1, 31):
        arbol_tipo = random.choice(tipos_arboles)
        arbol = Node(
            "Arbol",
            id_arbol=str(i),
            tipo=arbol_tipo["tipo"],
            nombre_cientifico=arbol_tipo["nombre_cientifico"],
            latitud=round(random.uniform(-33.0, -35.0), 6),
            longitud=round(random.uniform(-70.0, -72.0), 6),
        )
        sector = random.choice(sectores)
        arboles.append(arbol)
        graph.create(arbol)
        graph.create(Relationship(arbol, "PERTENECE_A", sector))
        data["arboles"].append({
            "id_arbol": str(i),
            "tipo": arbol_tipo["tipo"],
            "nombre_cientifico": arbol_tipo["nombre_cientifico"],
            "latitud": arbol["latitud"],
            "longitud": arbol["longitud"]
        })
    
    # Crear formularios y asociarlos a encargados
    for i in range(1, 21):
        formulario = Node("Formulario", id_formulario=str(i))
        encargado = random.choice(encargados)
        arbol = random.choice(arboles)
        graph.merge(formulario, "Formulario", "id_formulario")
        graph.merge(Relationship(encargado, "RELLENA", formulario))
        graph.merge(Relationship(arbol, "REGISTRADO_EN", formulario))
        data["formularios"].append({"id_formulario": str(i), "encargado": encargado["nombre"], "arbol": arbol["id_arbol"]})
        
        # Agregar plagas
        plaga = Node(
            "Plagas",
            plaga_detectada=random.choice(["ARAÑITA ROJA", "TRIPS", "CONCHUELA NEGRA DEL OLIVO", "ESCAMA BLANCA", "CHANCHITO BLANCO", "BURRITO DE LA VID"]),
            grado_dano=random.choice(["LEVE", "MEDIO", "ALTO"]),
            poblacion=random.choice(["LEVE", "MEDIO", "ALTO"]),
            observacion=random.choice(["Plaga en proceso de crecimiento", "", "Plaga potencialmente peligrosa"]),
        )
        graph.create(plaga)
        graph.create(Relationship(formulario, "CONTIENE", plaga))
        data["plagas"].append({
            "plaga_detectada": plaga["plaga_detectada"],
            "grado_dano": plaga["grado_dano"],
            "poblacion": plaga["poblacion"],
            "observacion": plaga["observacion"]
        })
        
        # Agregar enfermedades
        enfermedad = Node(
            "Enfermedades",
            enfermedad_detectada=random.choice(["VERTICILOSIS", "FUSARIUM", "HONGO DE LA MADERA", "PHYTOPHTHORA"]),
            grado_enfermedad=random.choice(["LEVE", "MEDIO", "ALTO"]),
            observacion=random.choice(["Enfermedad poco avanzada", ""]),
        )
        graph.create(enfermedad)
        graph.create(Relationship(formulario, "CONTIENE", enfermedad))
        data["enfermedades"].append({
            "enfermedad_detectada": enfermedad["enfermedad_detectada"],
            "grado_enfermedad": enfermedad["grado_enfermedad"],
            "observacion": enfermedad["observacion"]
        })
        
        # Agregar conteo de frutas
        conteo = Node(
            "ConteoFrutas",
            num_frutas=random.randint(30, 100),
            kilos_frutas=random.randint(10, 50),
        )
        graph.create(conteo)
        graph.create(Relationship(formulario, "CONTIENE", conteo))
        data["conteos"].append({
            "num_frutas": conteo["num_frutas"],
            "kilos_frutas": conteo["kilos_frutas"]
        })
        
        # Agregar aspersores
        aspersor = Node(
            "Aspersor",
            estado=random.choice(["OPERATIVO", "TAPADO", "CAÍDO", "FALTANTE", "ROTO"]),
            observacion=random.choice(["", "Aspersor con poca presion"]),
        )
        graph.create(aspersor)
        graph.create(Relationship(formulario, "CONTIENE", aspersor))
        data["aspersores"].append({
            "estado": aspersor["estado"],
            "observacion": aspersor["observacion"]
        })
    
    return data

# Generar y cargar los datos
data = generar_datos()

# Guardar los datos en un archivo JSON
with open("datos_cargados.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Datos generados, cargados y guardados en 'datos_cargados.json' exitosamente.")
