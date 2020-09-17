from flask import current_app as app
from sqlalchemy.sql import null

from app import db, setup_logging

log = setup_logging("models", app.config)


class User(db.Model):
    """User DB model."""

    # __tablename__ = "user"  # Optional while using Flask-SQLAlchemy

    id = db.Column(
        db.Integer,
        primary_key=True,
        index=True,
        unique=True,
        autoincrement=True,
        nullable=False,
    )
    cpf = db.Column(db.String(128), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    full_name = db.Column(db.String(128), index=False, unique=False, nullable=False)
    punches = db.relationship("PunchClock", back_populates="user")
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)

    def get_id(self) -> int:
        """Get user unique ID (DB PK)."""
        return self.id

    def __repr__(self):
        return f"{self.full_name} ({self.cpf}) {self.email}"

    def __str__(self) -> str:
        return (
            f"User("
            f"id={self.get_id()};"
            f"full_name={self.full_name};"
            f"cpf={self.cpf};"
            f"email={self.email};"
            f"punches=[{self.punches}]"
            f"created={self.created};"
            f")"
        )


class PunchClock(db.Model):
    """PunchClock DB model."""

    __tablename__ = "punchclock"  # Optional while using Flask-SQLAlchemy

    id = db.Column(
        db.Integer,
        primary_key=True,
        index=True,
        unique=True,
        autoincrement=True,
        nullable=False,
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=True, default=null()
    )
    user = db.relationship("User", back_populates="punches")
    punch_type = db.Column(db.String(64), index=False, unique=False, nullable=False)
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)

    def get_id(self) -> int:
        """Get group unique ID (DB PK)."""
        return self.id

    def __repr__(self):
        return f"punch_id={self.get_id()}"

    def __str__(self) -> str:
        return (
            f"PunchClock("
            f"id={self.get_id()};"
            f"user={self.user.get_id()};"
            f"punch_type={self.punch_type};"
            f"created={self.created};"
            f")"
        )
