from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from datetime import datetime

class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pendente')
