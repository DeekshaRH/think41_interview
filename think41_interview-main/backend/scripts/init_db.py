# scripts/init_db.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import engine
from db import models

models.Base.metadata.create_all(bind=engine)
print("✅ All tables created successfully.")
