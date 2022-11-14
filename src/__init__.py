from flask import Flask

app = Flask(__name__, instance_relative_config=True)

import src.routes.routes
from src.models import User, Pings
