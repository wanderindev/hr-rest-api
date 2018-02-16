from models.marital_status import MaritalStatusModel
from tests.base_test import BaseTest


class TestMaritalStatus(BaseTest):
    """Integration tests for the MaritalStatusModel."""
    def test_find_all(self):
        """Test the find_all method of MaritalStatusModel."""
        with self.app_context():
            m_s_list = MaritalStatusModel.find_all()

            self.assertIsNotNone(m_s_list)
            self.assertTrue(len(m_s_list) > 0)
