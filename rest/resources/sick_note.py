from models.sick_note import SickNoteModel
from resources.mixin import ListMixin, ResourceMixin


class SickNote(ResourceMixin):
    model = SickNoteModel
    parsed_model = model.parse_model()


class SickNotes(ListMixin):
    model = SickNoteModel
