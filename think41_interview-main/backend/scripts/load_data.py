import csv
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import models, database
from sqlalchemy.orm import Session

# Initialize DB
models.Base.metadata.create_all(bind=database.engine)

def load_products_from_csv(csv_file: str, db: Session):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            product = models.Product(
                name=row["name"],
                category=row["category"],
                price=float(row["price"]),
                stock=int(row["stock"])
            )
            db.add(product)
        db.commit()
        print("✅ CSV data successfully loaded.")

if __name__ == "__main__":
    db = database.SessionLocal()
    load_products_from_csv("data/products.csv", db)
    db.close()
