from unittest import TestCase

from models.family_relation import FamilyRelationModel


class TestFamilyRelation(TestCase):
    """Unit tests for the FamilyRelationModel."""

    def test_init(self):
        """Test the __init__ method of the FamilyRelationModel class."""
        self.f_r = FamilyRelationModel('family_relation_f', 'family_relation_m')

        self.assertEqual(self.f_r.relation_feminine, 'family_relation_f')
        self.assertEqual(self.f_r.relation_masculine, 'family_relation_m')
