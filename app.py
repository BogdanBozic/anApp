from flask import Flask, render_template
from flask_bootstrap import Bootstrap
# from db import db
# from model import vendorModel, itemModel, customerModel
from resources.vendorResource import vendor_blueprint
from resources.itemResource import item_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = '123'

bootstrap = Bootstrap(app)
app.register_blueprint(item_blueprint)
app.register_blueprint(vendor_blueprint)


# @app.before_first_request
# def create_tables():
#     db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # db.init_app(app)
    app.run(debug=True)
