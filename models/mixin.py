from datetime import date, datetime, time
from decimal import Decimal

from sqlalchemy import MetaData
from sqlalchemy.orm import collections
from sqlalchemy.sql import sqltypes
from sqlalchemy.sql.schema import UniqueConstraint

from db import db


# noinspection PyAttributeOutsideInit
class ModelMixin(object):
    metadata = MetaData()

    def __iter__(self):
        return ((k, v) for k, v in vars(self).items() if not k.startswith('_'))

    def __repr__(self):
        class_name = type(self).__name__
        attributes = ", ".join([f'{k!r}={v!r}' for k, v in self])

        return f'<{class_name}({attributes})>'

    def activate(self):
        self.is_active = True
        self.save_to_db()

    def delete_from_db(self):
        if hasattr(self, 'is_active'):
            if self.is_active:
                self.inactivate()
            else:
                raise ValueError('Registro ya estaba inactivo.')
        else:
            db.session.delete(self)
            db.session.commit()

    @classmethod
    def get_unique_constraints(cls):
        u_contraints = []
        if cls.__table_args__:
            for arg in cls.__table_args__:
                if isinstance(arg, UniqueConstraint):
                    contraint = []
                    for col in cls.__table__.columns:
                        if arg.__contains__(col.key):
                            contraint.append(col.key)
                    u_contraints.append(tuple(contraint))

        return u_contraints

    def inactivate(self):
        self.is_active = False
        self.save_to_db()

    @classmethod
    def parse_model(cls):
        parsed_model = {
            'keys': [],
            'unique': [],
            'nullable': [],
            'int': [],
            'float': [],
            'bool': [],
            'str': []
        }

        for col in cls.__table__.columns:
            if col.key != 'id':
                parsed_model['keys'].append(col.key)
                if col.unique:
                    parsed_model['unique'].append(col.key)
                if col.nullable:
                    parsed_model['nullable'].append(col.key)
                if isinstance(col.type, sqltypes.Integer):
                    parsed_model['int'].append(col.key)
                elif isinstance(col.type, sqltypes.Numeric):
                    parsed_model['float'].append(col.key)
                elif isinstance(col.type, sqltypes.Boolean):
                    parsed_model['bool'].append(col.key)
                else:
                    parsed_model['str'].append(col.key)

        parsed_model['unique'] = cls.get_unique_constraints()

        return parsed_model

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        output = {}

        for k, v in self:
            if type(v) == collections.InstrumentedList:
                output[k] = [item.to_dict() for item in v]
            elif isinstance(v, (date, datetime, time)):
                output[k] = v.isoformat()
            elif isinstance(v, (float, Decimal)):
                output[k] = str(v)
            else:
                output[k] = v

        return output

    def update(self, data, exclude=()):
        for key, value in data.items():
            if key is 'password':
                setattr(self, 'password_hash', self.get_password_hash(value))
            elif key not in exclude:
                setattr(self, key, value)
        self.save_to_db()

        return self.id, self
