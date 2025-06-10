from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS
from database.database import MY_DATABASE
from config import DevelopmentConfig
from app.users.routes import user_v1
from app.posts.routes import post_v1
from app.comments.routes import comment_v1
from app.follow.route import follow_v1



app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(DevelopmentConfig)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=1)
JWTManager(app)

app.register_blueprint(user_v1)
app.register_blueprint(post_v1)
app.register_blueprint(comment_v1)
app.register_blueprint(follow_v1)

MY_DATABASE.connect_to_db()
MY_DATABASE.create_user_table()
MY_DATABASE.create_follows_table()
MY_DATABASE.create_post_table()
MY_DATABASE.create_comments_table()
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)



# postgres://username:HGzNwJa5MCmYLakLgiw7IlslNPb6m3EL@dpg-ciujmt5iuiedpv0esq4g-a.oregon-postgres.render.com/online_chat_mlo2