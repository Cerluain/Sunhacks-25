import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base

print("DB Script Running")
db = sa.create_engine("sqlite:///./data.db", echo=False)
Session = sessionmaker(bind=db)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(sa.String(255), nullable=False)

    def __repr__(self) -> str:  # helpful for debugging
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


def main() -> None:
    print("Main function triggered")
    # create the SQLite file and tables
    Base.metadata.create_all(db)

    # Insert example users if they don't already exist
    user1 = User(username="Ricky", email="Ricky@gmail.com", password_hash="aonhtuea12903487aonth")
    user2 = User(username="Robert", email="ROBERT23@gmail.com", password_hash="4321aonhtuea12903487aonth")

    with Session() as session:
        # avoid duplicate inserts for repeated runs: check if users exist
        existing = session.query(User).filter(User.username.in_([user1.username, user2.username])).all()
        if not existing:
            session.add_all([user1, user2])
            session.commit()
            print("Added example users")
        else:
            print("Example users already exist (skipping insert):", existing)

        # list users
        users = session.query(User).all()
        print("Users in DB:", users)
        print("Session ending")



if __name__ == "__main__":
    main()
