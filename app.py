from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
import datetime

'''
la siguiente es la estructura para las llamadas a la api
(cada nivel posee todas las opciones de niveles inferiores)

APIURI/
        mostrador/
        mercurio/
                    verbos/
                    sustantivos_propios/
                    sustantivos_comunes/
                    todos/
                                        <fecha AAAAMMDD> (opcional)
   


'''

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost/noticias'

mongo = PyMongo(app)

CORS(app)

most = mongo.db.cuenta_mostrador_prueba4
merc = mongo.db.cuenta_mercurio_prueba4

    
@app.route('/mostrador/verbos/<fecha>', methods=['GET'])
def getVerbosMostradorDia(fecha):
    dia = datetime.datetime.strptime(fecha, '%Y%m%d')
    fechatime = dia.strftime("%Y-%m-%d 00:00:00")
    doc = most.find_one({"dia":fechatime})
       
    return jsonify({'_id': str(ObjectId(doc['_id'])),
                'dia': str(doc['dia']),
                'verbos': doc['cuentas']['verbos']})

@app.route('/mostrador/sustantivos_propios/<fecha>', methods=['GET'])
def getNombresMostradorDia(fecha):
    dia = datetime.datetime.strptime(fecha, '%Y%m%d')
    fechatime = dia.strftime("%Y-%m-%d 00:00:00")
    doc = most.find_one({"dia":fechatime})
    if doc:   
        return jsonify({'_id': str(ObjectId(doc['_id'])),
                    'dia': str(doc['dia']),
                    'sustantivos_propios': doc['cuentas']['sustantivos_propios']})
    else:
        return jsonify("no hay doc para tal fecha")

@app.route('/mostrador/sustantivos_comunes/<fecha>', methods=['GET'])
def getSustantivosMostradorDia(fecha):
    dia = datetime.datetime.strptime(fecha, '%Y%m%d')
    fechatime = dia.strftime("%Y-%m-%d 00:00:00")
    doc = most.find_one({"dia":fechatime})
    if doc:   
        return jsonify({'_id': str(ObjectId(doc['_id'])),
                    'dia': str(doc['dia']),
                    'sustantivos_comunes': doc['cuentas']['sustantivos_comunes']})
    else:
        return jsonify("no hay doc para tal fecha")

@app.route('/mostrador/todos/<fecha>', methods=['GET'])
def getTodosMostradorDia(fecha):
    dia = datetime.datetime.strptime(fecha, '%Y%m%d')
    fechatime = dia.strftime("%Y-%m-%d 00:00:00")
    doc = most.find_one({"dia":fechatime})
    if doc:   
        return jsonify({'_id': str(ObjectId(doc['_id'])),
                    'dia': str(doc['dia']),
                    'cuentas': doc['cuentas']})
    else:
        return jsonify("no hay doc para tal fecha")


@app.route('/mostrador/verbos', methods=['GET'])
def getVerbosMost():
    verbos = []
    for doc in most.find():
        if doc['cuentas']['verbos']:
            verbos.append({
                '_id': str(ObjectId(doc['_id'])),
                'dia': str(doc['dia']),
                'verbos': doc['cuentas']['verbos']
            
            })
    return jsonify(verbos)

@app.route('/mostrador/sustantivos_propios', methods=['GET'])
def getNombresMost():
    nombres = []
    for doc in most.find():
        if doc['cuentas']['sustantivos_propios']:
            nombres.append({
                '_id': str(ObjectId(doc['_id'])),
                'dia': str(doc['dia']),
                'sustantivos_propios': doc['cuentas']['sustantivos_propios']
            
            })
    return jsonify(nombres)

@app.route('/mostrador/sustantivos_comunes', methods=['GET'])
def getSustantivosMost():
    sustantivos = []
    for doc in most.find():
        if doc['cuentas']['sustantivos_comunes']:
            sustantivos.append({
                '_id': str(ObjectId(doc['_id'])),
                'dia': str(doc['dia']),
                'sustantivos_comunes': doc['cuentas']['sustantivos_comunes']
            
            })
    return jsonify(sustantivos)

@app.route('/mostrador/todos', methods=['GET'])
def getTodosMost():
    todos = []
    for doc in most.find():
        if doc['cuentas']['sustantivos_comunes']:
            todos.append({
                '_id': str(ObjectId(doc['_id'])),
                'dia': str(doc['dia']),
                'cuentas': doc['cuentas']
            
            })
    return jsonify(todos)


@app.route('/mercurio/todos', methods=['GET'])
def getTodosMerc():
    todos = []
    for doc in merc.find():
        if doc['cuentas']['sustantivos_comunes']:
            todos.append({
                '_id': str(ObjectId(doc['_id'])),
                'dia': str(doc['dia']),
                'cuentas': doc['cuentas']
            
            })
    return jsonify(todos)

@app.route('/mercurio/verbos', methods=['GET'])
def getVerbosMerc():
    verbos = []
    for doc in merc.find():
        if doc['cuentas']['verbos']:
            verbos.append({
                '_id': str(ObjectId(doc['_id'])),
                'dia': str(doc['dia']),
                'verbos': doc['cuentas']['verbos']
            
            })
    return jsonify(verbos)

@app.route('/mercurio/sustantivos_propios', methods=['GET'])
def getNombresMerc():
    nombres = []
    for doc in merc.find():
        if doc['cuentas']['sustantivos_propios']:
            nombres.append({
                '_id': str(ObjectId(doc['_id'])),
                'dia': str(doc['dia']),
                'sustantivos_propios': doc['cuentas']['sustantivos_propios']
            
            })
    return jsonify(nombres)

@app.route('/mercurio/sustantivos_comunes', methods=['GET'])
def getSustantivosMerc():
    sustantivos = []
    for doc in merc.find():
        if doc['cuentas']['sustantivos_comunes']:
            sustantivos.append({
                '_id': str(ObjectId(doc['_id'])),
                'dia': str(doc['dia']),
                'sustantivos_comunes': doc['cuentas']['sustantivos_comunes']
            
            })
    return jsonify(sustantivos)

    
@app.route('/mercurio/verbos/<fecha>', methods=['GET'])
def getVerbosMercurioDia(fecha):
    dia = datetime.datetime.strptime(fecha, '%Y%m%d')
    fechatime = dia.strftime("%Y-%m-%d 00:00:00")
    doc = merc.find_one({"dia":fechatime})
       
    return jsonify({'_id': str(ObjectId(doc['_id'])),
                'dia': str(doc['dia']),
                'verbos': doc['cuentas']['verbos']})

@app.route('/mercurio/sustantivos_propios/<fecha>', methods=['GET'])
def getNombresMercurioDia(fecha):
    dia = datetime.datetime.strptime(fecha, '%Y%m%d')
    fechatime = dia.strftime("%Y-%m-%d 00:00:00")
    doc = merc.find_one({"dia":fechatime})
    if doc:   
        return jsonify({'_id': str(ObjectId(doc['_id'])),
                    'dia': str(doc['dia']),
                    'sustantivos_propios': doc['cuentas']['sustantivos_propios']})
    else:
        return jsonify("no hay doc para tal fecha")

@app.route('/mercurio/sustantivos_comunes/<fecha>', methods=['GET'])
def getSustantivosMercurioDia(fecha):
    dia = datetime.datetime.strptime(fecha, '%Y%m%d')
    fechatime = dia.strftime("%Y-%m-%d 00:00:00")
    doc = merc.find_one({"dia":fechatime})
    if doc:   
        return jsonify({'_id': str(ObjectId(doc['_id'])),
                    'dia': str(doc['dia']),
                    'sustantivos_comunes': doc['cuentas']['sustantivos_comunes']})
    else:
        return jsonify("no hay doc para tal fecha")

@app.route('/mercurio/todos/<fecha>', methods=['GET'])
def getTodosMercuriorDia(fecha):
    dia = datetime.datetime.strptime(fecha, '%Y%m%d')
    fechatime = dia.strftime("%Y-%m-%d 00:00:00")
    doc = merc.find_one({"dia":fechatime})
    if doc:   
        return jsonify({'_id': str(ObjectId(doc['_id'])),
                    'dia': str(doc['dia']),
                    'cuentas': doc['cuentas']})
    else:
        return jsonify("no hay doc para tal fecha")


if __name__== "__main__":
    app.run(debug=True)

