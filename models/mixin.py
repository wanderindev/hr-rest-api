from db import db


class ModelsMixin(object):
    def __iter__(self):
        return ((k, v) for k, v in vars(self).items() if not k.startswith('_'))

    def __repr__(self):
        class_name = type(self).__name__
        attributes = ", ".join([f'{k!r}={v!r}' for k, v in self])

        return f'<{class_name}({attributes})>'

    def activate(self):
        if hasattr(self, 'is_active'):
            self.active = True
            self.save_to_db()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def inactivate(self):
        if hasattr(self, 'is_active'):
            self.active = False
            self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        output = {}
        for k, v in self:
            output[k] = v
        return output
