from db import db


class ModelMixin(object):
    def __repr__(self):
        prop_str = ", ".join(
            [
                f'{k!s}={v!r}'
                for k, v in vars(self).items()
                if k != '_sa_instance_state'
            ]
        )

        return f'<{self.__class__.__name__}({prop_str})>'

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
