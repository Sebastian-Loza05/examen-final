from flask import Flask, request, jsonify, abort
import datetime

app = Flask(__name__)

BD = []

class Operacion:
    def __init__(self, fecha, monto, numero_destino: str, numero_emision):
        self.fecha = fecha
        self.monto = monto
        self.numero_destino = numero_destino,
        self.numero_emision = numero_emision

    def format(self):
        return {
            'fecha': self.fecha,
            'monto': self.monto,
            'numero_destino': self.numero_destino,
            'numero_emision': self.numero_emision
        }


class Cuenta:
    def __init__(self, numero, saldo, dueño, contactos: list, operaciones):
        self.numero = numero
        self.dueño = dueño
        self.saldo = saldo
        self.contactos = contactos
        self.operaciones = operaciones

    def historial(self):
        historial = {
            "message": f"Saldo de {self.dueño}: {self.saldo}",
            "message2": f"Operaciones de {self.dueño}",
            "operaciones": []
        }
        for i in self.operaciones:
            print(i.format())
            print("mi nunmero: ", self.numero, "destino: ", i.numero_destino[0])
            if i.numero_destino[0] == self.numero:
                historial["operaciones"] += [f"Recibido: {i.monto} de {i.numero_emision}"]
            else:
                historial["operaciones"] += [f"Enviado: {i.monto} a {i.numero_destino[0]}"]
        return historial

    def pagar(self, destino, valor):
        if self.saldo < int(valor):
            return -1
        if destino not in self.contactos:
            return -2

        self.saldo -= int(valor)

        operacion = Operacion(fecha=datetime.datetime.now(), monto=int(valor), numero_destino=str(destino), numero_emision=self.numero)

        for i in BD:
            if i.numero == destino:
                i.saldo += int(valor)
                i.operaciones += [operacion]
                break

        self.operaciones += [operacion]
        return 1


cuenta1 = Cuenta(numero="21345", dueño="Arnaldo", saldo=200, contactos=["123", "456"], operaciones=[])
BD += [cuenta1]

cuenta = Cuenta(numero="123", dueño="Luisa", saldo=400, contactos=["456"], operaciones=[])
BD += [cuenta]

cuenta = Cuenta(numero="456", dueño="Andrea", saldo=300, contactos=["21345"], operaciones=[])
BD += [cuenta]


@app.route('/billetera/contactos/', methods=['GET'])
def contactos():
    try:
        minumero = request.args.get('minumero')

        cuenta = None
        for i in BD:
            if i.numero == minumero:
                cuenta = i
                break
        if cuenta is None:
            error404 = True
            abort(404)

        res = {}
        for contacto in cuenta.contactos:
            for i in BD:
                if i.numero == contacto:
                    res[i.dueño] = contacto
        if len(res.items()) == 0:
            abort(404)
        return jsonify(res)
    except Exception as e:
        print(e)
        if error404:
            abort(404)
        else:
            abort(500)

@app.route('/billetera/pagar/', methods=['GET'])
def pagar():
    error404 = False
    error406 = False
    try:
        minumero = request.args.get('minumero')
        numerodestino = request.args.get('numerodestino')
        valor = request.args.get('valor')
        cuenta = None
        for i in BD:
            if i.numero == minumero:
                cuenta = i
                break

        if cuenta is None:
            error404 = True
            abort(404)

        correct = cuenta.pagar(numerodestino, valor)
        if correct == -1:
            error406 = True
            abort(406)

        if correct == -2:
            error404 = True
            abort(404)

        return jsonify({
            'success': True,
            'code': 200,
            'message': f'Realizado en {datetime.datetime.now()}'
        })

    except Exception as e:
        print(e)
        if error404:
            abort(404)
        elif error406:
            abort(406)
        else:
            abort(500)

@app.route('/billetera/historial/', methods=['GET'])
def historial():
    error404 = False
    try:
        minumero = request.args.get('minumero')
        cuenta = None
        for i in BD:
            if i.numero == minumero:
                cuenta = i
                break

        if cuenta is None:
            error404 = True
            abort(404)

        res = cuenta.historial()

        return jsonify(res)

    except Exception as e:
        print(e)
        if error404:
            abort(404)
        else:
            abort(500)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'code': 404,
        'message': 'resource not found'
    }), 404

@app.errorhandler(406)
def not_accepted(error):
    return jsonify({
        'success': False,
        'code': 406,
        'message': 'Not accepted'
    }), 406

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'code': 500,
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    app.run(debug=True)
