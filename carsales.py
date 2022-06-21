from flask import Flask, redirect, render_template, request, jsonify, abort
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

carsales = Flask(__name__)
CORS(carsales)

carsales.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/vehicles'
carsales.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(carsales)


# Models

class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key = True)
    car_name = db.Column(db.String(100), nullable = False)
    car_type = db.Column(db.String(100), nullable = False)
    car_price = db.Column(db.Float(), nullable = False)
    car_year = db.Column(db.Integer(), nullable = False)
    car_plate = db.Column(db.String(10), nullable =False, unique=True)
    car_description = db.Column(db.String(500), nullable = False)

    def __repr__(self):
        return "<Car %r>" % self.car_name

db.create_all()

# API Endpoints

@carsales.route('/')
def index():
    return jsonify({"message": "Welcome to my hood"})

# Create method

@cross_origin()
@carsales.route('/addcar', methods=['POST'])
def addcar():
    car_data = request.json

    car_name = car_data['car_name']
    car_type = car_data['car_type']
    car_year = car_data['car_year']
    car_price = car_data['car_price']
    car_plate = car_data['car_plate']
    car_description = car_data['car_description']

    car = Car(car_name=car_name, car_type=car_type, car_year=car_year, car_price=car_price, car_description=car_description, car_plate=car_plate)
    db.session.add(car)
    db.session.commit()

    #TODO: add a new column called number_plate that's always unique, make sure the form doesn't
    #  get submitted if the same number plate is supplied and it's existing in the database

    return jsonify({
        "success": True,
        "message": "Car successfully added"
    })

#Get all cars

@carsales.route('/getcars', methods=['GET'])
def getcars():
    all_cars = []
    cars = Car.query.all()
    for car in cars:
        results = {
            "car_id": car.id,
            "car_name": car.car_name,
            "car_type": car.car_type,
            "car_price": car.car_price,
            "car_year": car.car_year,
            "car_plate": car.car_plate,
            "car_description": car.car_description
        }
        all_cars.append(results)
    

    return jsonify({
        "success": True,
        "cars": all_cars,
        "total_cars": len(cars)
    })

#Implementing the update method

@carsales.route('/getcar/<int:car_id>', methods=['GET'])
def get_car_by_id(car_id):
    car = Car.query.filter(Car.id == car_id).one_or_none()
    car_data = []
    for data in car:
            results = {
            "car_id": data.id,
            "car_name": data.car_name,
            "car_type": data.car_type,
            "car_price": data.car_price,
            "car_year": data.car_year,
            "car_plate": data.car_plate,
            "car_description": data.car_description
        }
    car_data.append(results)
    
    if car is None:
        abort(404)
    
    else:
         return jsonify({
        "success": True,
        "car": car_data,
        })



@carsales.route('/updatecar/<int:car_id>', methods=['PATCH'])
def updatecar(car_id):
    car = Car.query.get(car_id)

    car_name = request.json['car_name']
    car_type = request.json['car_type']
    car_price = request.json['car_price']

    if car is None:
        abort(404)
    else:
        car.car_name = car_name
        car.car_type = car_type
        car.car_price = car_price
        db.session.add(car)
        db.session.commit()
        return jsonify({
        "success": True,
        "message": "Car successfully updated"
    })

    #TODO: Implement the delete method

@carsales.route('/deletecar/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.get(car_id)

    if car is None:
        abort(404)
    else:
        db.session.delete(car)
        db.session.commit()
        return jsonify({
        "success": True,
        "message": "Car successfully deleted"
    })



# def connection():
#     server = 'localhost' #my server name
#     database = 'vehicles' 
#     username = 'postgres'
#     password = 'password'
#     conn = psycopg2.connect(host=server, database=database, user=username, password=password)
#     return conn

# @carsales.route('/')
# def main():
#     cars = []
#     conn = connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM MadridCars")
#     for row in cursor.fetchall():
#         cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
#     conn.close()

#     return render_template("carlist.html", cars = cars)

# @carsales.route('/addcar', methods=['GET', 'POST'])
# def addcar():
#     if request.method == 'GET':
#         return render_template("addcar.html", car = {})
#     if request.method == 'POST':
#         id = int(request.form["id"])
#         name = request.form["name"]
#         year = int(request.form["year"])
#         price = float(request.form["price"])
#         conn = connection()
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO MadridCars (id, name, year, price) VALUES (%s, %s, %s, %s)", (id, name, year, price))
#         conn.commit()
#         conn.close()
#         return redirect('/')

# @carsales.route('/updatecar/<int:id>', methods=['GET', 'POST'])
# def updatecar(id):
#     cr = []
#     conn = connection()
#     cursor = conn.cursor()
#     if request.method == 'GET':
#         cursor.execute("SELECT * FROM MadridCars WHERE id = %s", (str(id)))
#         for row in cursor.fetchall():
#             cr.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
#         conn.close()
#         return render_template("addcar.html", car = cr[0])
#     if request.method == 'POST':
#         name = request.form["name"]
#         year = int(request.form["year"])
#         price = float(request.form["price"])
#         cursor.execute("UPDATE MadridCars SET name = %s, year = %s, price = %s WHERE id = %s", (name, year, price, id))
#         conn.commit()
#         conn.close()
#         return redirect('/')

# @carsales.route('/deletecar/<int:id>')
# def deletecar(id):
#     conn = connection()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM MadridCars WHERE id = %s", (str(id)))
#     conn.commit()
#     conn.close()
#     return redirect('/')
    

if __name__ == '__main__':
    carsales.run(debug=True)