from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    chats: so.WriteOnlyMapped['Chat'] = so.relationship(
        back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Chat(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    msg: so.Mapped[str] = so.mapped_column(sa.String(1024))
    content: so.Mapped[str] = so.mapped_column(sa.String(4096))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    user: so.Mapped[User] = so.relationship(back_populates='chats')

    def __repr__(self):
        return '<Chat {}>'.format(self.msg)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'msg': self.msg,
            'content': self.content,
            'user_id': self.user_id,
        }


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
