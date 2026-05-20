
from flask_moment import Moment
from app import create_app
import os
app = create_app()
moment=Moment(app)


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    with app.app_context():
         from app.extension import db
         db.create_all()
         
         app.run(debug=True)