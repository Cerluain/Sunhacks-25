import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
import hmac

db = sa.create_engine("sqlite:///./data.db", echo=False)
Session = sessionmaker(bind=db)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(sa.String(255), nullable=False)

def main() -> None:
    # create the SQLite file and tables only if the users table doesn't exist yet
    inspector = sa.inspect(db)
    if not inspector.has_table(User.__tablename__):
        Base.metadata.create_all(db)
        print("Created tables")
    else:
        print("Tables already exist, skipping create_all")


def authenticate(email: str, password_hash: str) -> None|any:
    if not email or not password_hash:
        return None

    with Session() as session:
        user = session.query(User).filter_by(email=email).one_or_none()
        if user is None:
            return None
        try:
            return ((id, email, password_hash) 
                    if hmac.compare_digest(user.password_hash, password_hash) else None)
        except Exception:
            return None


def create_user(email: str, password_hash: str) -> User | None:
    if not email or not password_hash:
        return None

    with Session() as session:
        # Check for existing email
        exists = session.query(User).filter_by(email=email).first()
        if exists:
            return None

        new_user = User(email=email, password_hash=password_hash)
        session.add(new_user)
        session.commit()
        # refresh to get generated id
        session.refresh(new_user)
        return new_user


def get_user_by_email(email: str) -> User | None:
    if not email:
        return None
    with Session() as session:
        return session.query(User).filter_by(email=email).one_or_none()


def update_user_password(email: str, new_password_hash: str) -> bool:
    if not email or not new_password_hash:
        return False
    with Session() as session:
        user = session.query(User).filter_by(email=email).one_or_none()
        if user is None:
            return False
        user.password_hash = new_password_hash
        session.add(user)
        session.commit()
        return True


def delete_user(email: str) -> bool:
    if not email:
        return False
    with Session() as session:
        user = session.query(User).filter_by(email=email).one_or_none()
        if user is None:
            return False
        session.delete(user)
        session.commit()
        return True


if __name__ == "__main__":
    main()
    # Example auth checks (use emails as unique identifiers)
    print("Auth check (correct) for ricky@gmail.com:", authenticate("Ricky@gmail.com", "aonhtuea12903487aonth"))
    print("Auth check (incorrect) for ricky@gmail.com:", authenticate("Ricky@gmail.com", "wrong_password"))
