import sqlalchemy as sa
from . import db


class Company(db.Model):
    """Model for company accounts."""

    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)
    name_ko = db.Column(db.String(80), unique=False, nullable=True)  # Korean
    name_en = db.Column(db.String(80), unique=False, nullable=True)  # English
    name_ja = db.Column(db.String(80), unique=False, nullable=True)  # Japanese


class Tags(db.Model):
    """Model for tags."""
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    language = db.Column(db.String(2), nullable=False, default='KO')

    @sa.orm.validates('language')
    def convert_upper(self, key, value):
        return value.upper()

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


class Company_Tags_Map(db.Model):
    """Model for company tags map."""
    __tablename__ = "company_tags_map"
    __table_args__ = (
        sa.PrimaryKeyConstraint('tag_id', 'company_id'),
        {},
    )

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    tag = db.relationship('Tags', foreign_keys=[tag_id], uselist=False)
    company = db.relationship('Company', foreign_keys=[
                              company_id], uselist=False)
