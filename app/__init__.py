from .models import app

from .main import main
app.register_blueprint(main)

from .auth import auth
app.register_blueprint(auth)
