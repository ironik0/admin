from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Device
import subprocess

def ping_device(ip):
    try:
        output = subprocess.check_output(["ping", "-c", "1", "-W", "1", ip], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

@app.route("/")
def index():
    devices = Device.query.all()
    statuses = {device.id: ping_device(device.ip_address) for device in devices}
    return render_template("index.html", devices=devices, statuses=statuses)

@app.route("/device/<int:device_id>")
def device_detail(device_id):
    device = Device.query.get_or_404(device_id)
    status = ping_device(device.ip_address)
    return render_template("device.html", device=device, status=status)

@app.route("/add", methods=["GET", "POST"])
def add_device():
    if request.method == "POST":
        name = request.form["name"]
        ip_address = request.form["ip_address"]
        device_type = request.form["device_type"]
        description = request.form["description"]
        new_device = Device(name=name, ip_address=ip_address, device_type=device_type, description=description)
        db.session.add(new_device)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_device.html")