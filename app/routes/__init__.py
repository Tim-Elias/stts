from flask import Flask
from .login_routes import login_bp
from .google_auth_route import google_auth_bp
from .account_route import account_bp
from .transcription_route import transcription_bp
from .prompt_route import prompt_bp
from .audio_route import audio_bp
from .logs_route import logs_bp




def register_routes(app: Flask):
    app.register_blueprint(login_bp)  
    #app.register_blueprint(google_auth_bp)  
    app.register_blueprint(account_bp)
    app.register_blueprint(transcription_bp)
    app.register_blueprint(prompt_bp)
    app.register_blueprint(audio_bp)
    app.register_blueprint(logs_bp)
