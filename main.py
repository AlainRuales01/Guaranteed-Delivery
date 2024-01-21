from flask import Flask, request, jsonify
from store_mediator import StoreMediator
import json
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
scheduler = BackgroundScheduler()
store_mediator_instance = StoreMediator()

def background_task():
    mensaje_respuesta = store_mediator_instance.enviar_mensajes_pendientes()
    print(mensaje_respuesta)

scheduler.add_job(background_task, 'interval', seconds=5)
scheduler.start()


# @app.route('/api/Test', methods=['POST'])
# def test():
#     mensaje_respuesta = store_mediator_instance.enviar_mensajes_pendientes()
#     return jsonify({'mensaje': mensaje_respuesta}), 200

@app.route('/api/SendMessage', methods=['POST'])
def send_message():
    mensaje_respuesta = ''
    data = request.get_json()  # obtener el json de la solicitud
    nombre = data.get('nombre')  # obtener el campo 'nombre' del json
    if nombre is None:
        return jsonify({'error': 'No se proporcionó el campo nombre'}), 400
    json_data = json.dumps(data)
    mensaje_respuesta = store_mediator_instance.enviar_mensaje(json_data)
    
    return jsonify({'mensaje': mensaje_respuesta}), 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)