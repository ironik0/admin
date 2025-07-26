from app import db

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<Device {self.name}>'