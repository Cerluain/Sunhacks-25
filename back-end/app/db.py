import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
import hmac

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
    # create the SQLite file and tables only if the users table doesn't exist yet
    inspector = sa.inspect(db)
    if not inspector.has_table(User.__tablename__):
        Base.metadata.create_all(db)
        print("Created tables")
    else:
        print("Tables already exist, skipping create_all")

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



def authenticate(username: str, password_hash: str) -> bool:
    if not username or not password_hash:
        return False

    with Session() as session:
        user = session.query(User).filter_by(username=username).one_or_none()
        if user is None:
            return False
        try:
            return hmac.compare_digest(user.password_hash, password_hash)
        except Exception:
            return False


if __name__ == "__main__":
    main()
    # Example auth checks
    print("Auth check (correct) for Ricky:", authenticate("Ricky", "aonhtuea12903487aonth"))
    print("Auth check (incorrect) for Ricky:", authenticate("Ricky", "wrong_password"))
