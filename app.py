"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, jsonify
from models import  db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


with app.app_context():
    connect_db(app)
    db.create_all()

app.app_context().push() ##

def serialize(SQLcupcake):
    """ function to erialize a SQLAlchemy Cupcake obj to python dictionary to make it JSON compatible"""
    return {
        "id": SQLcupcake.id,
        "flavor": SQLcupcake.flavor,
        "size" : SQLcupcake.size,
        "rating": SQLcupcake.rating,
        "image": SQLcupcake.image,
    }

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/cupcakes")
def all_cupcakes_info():
    """Get data about all cupcakes.
        Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
        The values should come from each cupcake instance."""
    all_cupcakes = Cupcake.query.all()
    serialized_cupcake = [serialize(c) for c in all_cupcakes]
    return jsonify(cupcakes=serialized_cupcake)

@app.route("/api/cupcakes/<int:cupcake_id>")
def single_cupcake_info(cupcake_id):
    """Get data about a single cupcake.
        Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
        This should raise a 404 if the cupcake cannot be found."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized_cupcake = serialize(cupcake)
    return jsonify(cupcake=serialized_cupcake)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request.
        Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}."""
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]
    new_cupcake = Cupcake(flavor=flavor,
                        size = size,
                        rating = rating,
                        image = image,
    )
    db.session.add(new_cupcake)
    db.session.commit()
    serialized_cupcake = serialize(new_cupcake)
    return (jsonify(cupcake=serialized_cupcake), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. 
        You can always assume that the entire cupcake object will be passed to the backend.
        This should raise a 404 if the cupcake cannot be found.
        Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.add(cupcake)
    db.session.commit()
    serialized_cupcake = serialize(cupcake)
    return jsonify(cupcake=serialized_cupcake)
    

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """This should raise a 404 if the cupcake cannot be found. 
    Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted cupcake")