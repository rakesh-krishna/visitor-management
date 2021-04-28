from main import app
from init_db import db_setup
if __name__ == "__main__":
  db_setup()
  app.run()