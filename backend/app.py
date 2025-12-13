# This file is deprecated - use app/__init__.py instead
# Kept for backwards compatibility during migration
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
