from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
import datetime

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost/noticias'

mongo = PyMongo(app)

CORS(app)

most = mongo.db.cuenta_mostrador_prueba3
merc = mongo.db.cuenta_mercurio_prueba3

    
@app.route('/mostrador/verbos/<fecha>', methods=['GET'])
def getVerbosMostradorDia(fecha):
    dia = datetime.datetime.strptime(fecha, '%Y%m%d')
    fechatime = dia.strftime("%Y-%m-%d 00:00:00")
    doc = most.find_one({"dia":fechatime})
       
    return jsonify({'_id': str(ObjectId(doc['_id'])),
                'dia': str(doc['dia']),
                'verbos': str(doc['cuentas']['verbos'])})

@app.route('/mostrador/sustantivos_propios/<fecha>', methods=['GET'])
def getNombresMostradorDia(fecha):
    dia = datetime.datetime.strptime(fecha, '%Y%m%d')
    fechatime = dia.strftime("%Y-%m-%d 00:00:00")
    doc = most.find_one({"dia":fechatime})
    if doc:   
        return jsonify({'_id': str(ObjectId(doc['_id'])),
                    'dia': str(doc['dia']),
                    'sustantivos_propios': str(doc['cuentas']['sustantivos_propios'])})
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
                    'sustantivos_comunes': str(doc['cuentas']['sustantivos_comunes'])})
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
                'verbos': str(doc['cuentas']['verbos'])
            
            })
    return jsonify(verbos)

@app.route('/mercurio/todos', methods=['GET'])
def getTodosMerc():
    todos = []
    for doc in merc.find():
        if doc['cuentas']['sustantivos_comunes']:
            todos.append({
                '_id': str(ObjectId(doc['_id'])),
                'dia': str(doc['dia']),
                'cuentas': str(doc['cuentas'])
            
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
                'verbos': str(doc['cuentas']['verbos'])
            
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
                'sustantivos_propios': str(doc['cuentas']['sustantivos_propios'])
            
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
                'sustantivos_comunes': str(doc['cuentas']['sustantivos_comunes'])
            
            })
    return jsonify(sustantivos)

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    print(id)
    user = db.find_one({'_id':ObjectId(id)})
    return jsonify({
           '_id': str(ObjectId(user['_id'])),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
    })

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    db.delete_one({'_id':ObjectId(id)})
    return jsonify({'msg':"user {} deleted".format(id)})

@app.route('/user/<id>', methods=['PUT'])
def updateUser(id):
    db.update_one({'_id':ObjectId(id)}, {'$set':
    {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }
    })
    return jsonify({'msg':"user {} updated".format(id)})

if __name__== "__main__":
    app.run(debug=True)

