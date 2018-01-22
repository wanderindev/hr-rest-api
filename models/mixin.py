from datetime import date, datetime

from sqlalchemy.orm import collections

from db import db


# noinspection PyAttributeOutsideInit
class ModelsMixin(object):
    def __iter__(self):
        return ((k, v) for k, v in vars(self).items() if not k.startswith('_'))

    def __repr__(self):
        class_name = type(self).__name__
        attributes = ", ".join([f'{k!r}={v!r}' for k, v in self])

        return f'<{class_name}({attributes})>'

    def activate(self):
        if hasattr(self, 'is_active'):
            self.is_active = True
            self.save_to_db()

    def delete_from_db(self):
        if hasattr(self, 'is_active'):
            raise ValueError('Deleting this record is not allowed.  '
                             'Try making it inactive')
        else:
            db.session.delete(self)
            db.session.commit()

    def inactivate(self):
        if hasattr(self, 'is_active'):
            self.is_active = False
            self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        output = {}

        for k, v in self:
            if type(v) == collections.InstrumentedList:
                output[k] = [item.to_dict() for item in v]
            elif isinstance(v, (date, datetime)):
                output[k] = v.isoformat()
            else:
                output[k] = v

        return output
