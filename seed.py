from .database import SessionLocal


def seed_database():
    db = SessionLocal()

    print("Seeding database...")

    db.close()


if __name__ == "__main__":
    seed_database()