from models.creditor import CreditorModel
from models.organization import OrganizationModel
from tests.base_test import BaseTest


class TestCreditor(BaseTest):
    """Integration tests for the CreditorModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an
        organization and a creditor.
        """
        super(TestCreditor, self).setUp()

        with self.app_context():
            self.o = self.get_organization()
            self.cr = self.get_creditor()

    def test_find_creditor(self):
        """Test the find_by_id method of CreditorModel."""
        with self.app_context():
            cr = CreditorModel.find_by_id(self.cr.id,
                                          self.u)

            self.assertIsNotNone(cr)

    def test_creditor_list_in_organization(self):
        """Test that the organization object contains a creditor list."""
        with self.app_context():
            cred_list = CreditorModel.query.filter_by(
                organization_id=self.o.id).all()
            cred_list_in_org = OrganizationModel.find_by_id(self.o.id,
                                                            self.u).creditors

            self.assertListEqual(cred_list, cred_list_in_org)
