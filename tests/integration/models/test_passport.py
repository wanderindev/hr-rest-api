from models.country import CountryModel
from models.employee import EmployeeModel
from models.passport import PassportModel
from tests.base_test import BaseTest


class TestPassport(BaseTest):
    """Integration tests for the PassportModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an employee
        and a passport.
        """
        super(TestPassport, self).setUp()

        self.e = self.get_employee()
        self.p = self.get_passport()

    def test_find_id(self):
        """Test the find_by_id method of PassportModel."""
        with self.app_context():
            p = PassportModel.find_by_id(self.p.id, self.u)

            self.assertIsNotNone(p)

    def test_passport_list_in_employee(self):
        """Test that the employee object contains an passport list."""
        with self.app_context():
            p_list = PassportModel.query.filter_by(employee_id=self.e.id).all()
            p_list_in_employee = EmployeeModel.find_by_id(
                self.e.id, self.u).passports

            self.assertListEqual(p_list, p_list_in_employee)

    def test_passport_list_in_country(self):
        """ Test that the country object contains an passport list."""
        with self.app_context():
            p_list = PassportModel.query.filter_by(employee_id=self.e.id).all()
            p_list_in_country = CountryModel.query.filter_by(
                id=1).first().passports

            self.assertListEqual(p_list, p_list_in_country)
