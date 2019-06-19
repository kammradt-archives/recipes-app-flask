import uuid
from flask import Flask, request, jsonify, make_response
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'Qw3yU1a8Rn_qxBENFoCZzEDq-qWf1lRzBCcUQ3ZnJzk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    ingredients = db.Column(db.String(400))
    picture = db.Column(db.String(600))
    difficulty = db.Column(db.String(20))
    preparation_time = db.Column(db.Integer, default=5)
    preparation_guide = db.Column(db.String(600))
    is_public = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


class RecipeView(MethodView):

    decorators = [token_required]

    def get(self, current_user, recipe_id):
        if recipe_id is None:
            recipes = Recipe.query.filter_by(user_id=current_user.id).all()

            response = [{
                'id': recipe.id,
                'name': recipe.name,
                'ingredients': recipe.ingredients,
                'picture': recipe.picture,
                'difficulty': recipe.difficulty,
                'preparation_time': recipe.preparation_time,
                'preparation_guide': recipe.preparation_guide,
                'is_public': recipe.is_public
            } for recipe in recipes]

            return jsonify({'recipes': response})
        else:
            recipe = Recipe.query.filter_by(id=recipe_id).first()

            if not recipe:
                return jsonify({'message': 'No recipe found!'})

            recipe_data = {
                'id': recipe.id,
                'name': recipe.name,
                'ingredients': recipe.ingredients,
                'picture': recipe.picture,
                'difficulty': recipe.difficulty,
                'preparation_time': recipe.preparation_time,
                'preparation_guide': recipe.preparation_guide,
                'is_public': recipe.is_public
            }

            if recipe.is_public:
                return jsonify({'recipe': recipe_data})
            elif recipe.user_id == current_user.id:
                return jsonify({'recipe': recipe_data})
            else:
                return jsonify({'message': 'No recipe found!'})

    def post(self, current_user):
        data = request.get_json()

        new_recipe = Recipe(
            name=data['name'],
            ingredients=data['ingredients'],
            picture=data['picture'],
            difficulty=data['difficulty'],
            preparation_time=data['preparation_time'],
            preparation_guide=data['preparation_guide'],
            is_public=data['is_public'],
            user_id=current_user.id
        )
        db.session.add(new_recipe)
        db.session.commit()

        return jsonify({'message': 'New recipe added!'})

    def put(self, current_user, recipe_id):
        recipe = Recipe.query.filter_by(id=recipe_id, user_id=current_user.id).first()

        if not recipe:
            return jsonify({'message': 'No recipe found!'})

        put_data = request.get_json()
        recipe.name = put_data['name']
        recipe.ingredients = put_data['ingredients']
        recipe.picture = put_data['picture']
        recipe.difficulty = put_data['difficulty']
        recipe.preparation_time = put_data['preparation_time']
        recipe.preparation_guide = put_data['preparation_guide']
        recipe.is_public = put_data['is_public']
        db.session.commit()

        return jsonify({'message': 'Recipe updated!'})

    def delete(self, current_user, recipe_id):
        recipe = Recipe.query.filter_by(id=recipe_id, user_id=current_user.id).first()

        if not recipe:
            return jsonify({'message': 'No recipe found!'})

        db.session.delete(recipe)
        db.session.commit()

        return jsonify({'message': 'Recipe deleted!'})


recipe_view = RecipeView.as_view('recipe_api')
app.add_url_rule('/api/recipe', defaults={'recipe_id': None}, view_func=recipe_view, methods=['GET', ])
app.add_url_rule('/api/recipe', view_func=recipe_view, methods=['POST', ])
app.add_url_rule('/api/recipe/<int:recipe_id>', view_func=recipe_view, methods=['GET', 'PUT', 'DELETE'])


class UserView(MethodView):

    decorators = [token_required]

    def get(self, current_user, public_id):
        if public_id is None:
            if not current_user.is_admin:
                return jsonify({'message': 'Cannot perform this call!'})

            users = User.query.all()
            response = [{
                'public_id': user.public_id,
                'username': user.username,
                'is_admin': user.is_admin
            } for user in users]

            return jsonify({'users': response})
        else:
            user = User.query.filter_by(public_id=public_id).first()

            if not user:
                return jsonify({'message': 'No user found!'})

            user_data = {'public_id': user.public_id, 'username': user.username, 'is_admin': user.is_admin}

            return jsonify({'user': user_data})

    def put(self, current_user, public_id):
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            return jsonify({'message': 'No user found!'})

        put_data = request.get_json()
        user.username = put_data['username']
        user.is_admin = put_data['is_admin']
        db.session.commit()

        return jsonify({'message': 'User updated!'})

    def delete(self, current_user, public_id):
        if not current_user.is_admin:
            return jsonify({'message': 'Cannot perform this call!'})

        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            return jsonify({'message': 'No user found!'})

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted!'})


user_view = UserView.as_view('user_api')
app.add_url_rule('/api/user', defaults={'public_id': None}, view_func=user_view, methods=['GET',])
app.add_url_rule('/api/user/<string:public_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])


@app.route('/api/user', methods=['POST'])
def create_user():
    post_data = request.get_json()

    hashed_password = generate_password_hash(post_data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username=post_data['username'], password=hashed_password,
                    is_admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route('/api/recipes', methods=['GET'])
def get_all_public_recipes():
    recipes = Recipe.query.filter_by(is_public=True).all()

    response = [{
        'id': recipe.id,
        'name': recipe.name,
        'ingredients': recipe.ingredients,
        'picture': recipe.picture,
        'difficulty': recipe.difficulty,
        'preparation_time': recipe.preparation_time,
        'preparation_guide': recipe.preparation_guide,
        'is_public': recipe.is_public
    } for recipe in recipes]

    return jsonify({'recipes': response})


@app.route('/api/login')
def login():
    auth_data = request.authorization

    if not auth_data.username or not auth_data.password:
        return make_response('Please insert data!', 401, {'WWW-Authenticate': 'Basic realm="Please insert data!"'})

    user = User.query.filter_by(username=auth_data.username).first()

    if not user:
        return make_response('No user found!', 401, {'WWW-Authenticate': 'Basic realm="No user found!"'})

    if check_password_hash(user.password, auth_data.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
            app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Verify your credentials!', 401,
                         {'WWW-Authenticate': 'Basic realm="Verify your credentials!"'})


if __name__ == '__main__':
    app.run(debug=True)
