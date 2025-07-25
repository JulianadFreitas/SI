# from flask import Flask, render_template, redirect, url_for
# from datetime import datetime
# from models import db, Call

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calls.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)

# # Criação do banco na primeira execução
# with app.app_context():
#     db.create_all()

# @app.route("/call/<table_id>")
# def call(table_id):
#     new_call = Call(table_id=table_id, created_at=datetime.utcnow(), status="Pendente")

#     db.session.add(new_call)
#     db.session.commit()
#     return render_template("call.html", table=table_id)

# def parse_time_str(time_str):
#     return datetime.strptime(time_str, "%H:%M:%S")

# @app.route('/kitchen')
# def kitchen():
#     calls = Call.query.order_by(Call.id.desc()).all()
#     if calls:
#         calls[0].is_new = True 
#     now = datetime.utcnow()  # <-- alterado de datetime.now()
#     for call in calls:
#         elapsed_seconds = (now - call.created_at).total_seconds()
#         minutes = int(elapsed_seconds // 60)
#         if minutes >= 60:
#             hours = minutes // 60
#             mins = minutes % 60
#             call.elapsed_str = f"{hours}h {mins}min"
#         else:
#             call.elapsed_str = f"{minutes} min"
#     return render_template('kitchen.html', calls=calls)

# @app.route("/attend/<int:call_id>")
# def attend(call_id):
#     call = Call.query.get(call_id)
#     if call:
#         call.status = "Atendido"
#         db.session.commit()
#     return redirect(url_for('kitchen'))

# @app.route("/kitchen/length")
# def kitchen_length():
#     total = Call.query.count()
#     return {"total": total}

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
from datetime import datetime
from models import db, Call
import os
app = Flask(__name__)
socketio = SocketIO(app)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "calls.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/call/<table_id>")
def call(table_id):
    new_call = Call(table_id=table_id, created_at=datetime.utcnow(), status="Pendente")
    db.session.add(new_call)
    db.session.commit()

    # Notifica todos os clientes conectados sobre novo chamado
    socketio.emit("new_call", {"table_id": table_id})
    return render_template("call.html", table=table_id)

@app.route('/kitchen')
def kitchen():
    calls = Call.query.order_by(Call.id.desc()).all()
    if calls:
        calls[0].is_new = True
    now = datetime.utcnow()
    for call in calls:
        elapsed_seconds = (now - call.created_at).total_seconds()
        minutes = int(elapsed_seconds // 60)
        if minutes >= 60:
            h, m = divmod(minutes, 60)
            call.elapsed_str = f"{h}h {m}min"
        else:
            call.elapsed_str = f"{minutes} min"
    return render_template('kitchen.html', calls=calls)

@app.route("/attend/<int:call_id>")
def attend(call_id):
    call = Call.query.get(call_id)
    if call:
        call.status = "Atendido"
        db.session.commit()
        # Notifica todos os clientes conectados sobre atualização
        socketio.emit("call_updated", {"call_id": call.id})
    return redirect(url_for('kitchen'))

@app.route("/kitchen/length")
def kitchen_length():
    total = Call.query.count()
    return {"total": total}

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     socketio.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)