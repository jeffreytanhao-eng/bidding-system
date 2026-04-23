import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from src.main import app


def handler(request, context):
    return app(request, context)
