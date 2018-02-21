from models.family_relation import FamilyRelationModel
from tests.base_test import BaseTest


class TestFamilyRelation(BaseTest):
    """Integration tests for the FamilyRelationModel."""
    def test_find_all(self):
        """Test the find_all method of FamilyRelationModel."""
        with self.app_context():
            f_r_list = FamilyRelationModel.find_all()

            self.assertIsNotNone(f_r_list)
            self.assertTrue(len(f_r_list) > 0)
