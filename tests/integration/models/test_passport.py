from models.country import CountryModel
from models.employee import EmployeeModel
from models.passport import PassportModel
from tests.base_test import BaseTest


class TestPassport(BaseTest):
    """Integration tests for the PassportModel."""
    def setUp(self):
        """
        Extend the BaseTest setUp method by setting up an organization,
        a department, an employment position, a shift, an employee,
        and an health_permit.
        """
        super(TestPassport, self).setUp()

        self.o = self.get_organization()
        self.d = self.get_department(self.o.id)
        self.e_p = self.get_employment_position(self.o.id)
        self.s = self.get_shift(self.o.id)
        self.e = self.get_employee(self.d.id, self.e_p.id, self.s.id, self.o.id)
        self.p = self.get_passport(self.e.id,  self.o.id)

    def test_find_id(self):
        """Test the find_by_id methods of PassportModel."""
        with self.app_context():
            p = PassportModel.find_by_id(self.p.id,
                                         self.o.id)

            self.assertIsNotNone(p)

    def test_passport_list_in_employee(self):
        """Test that the employee object contains an passport list."""
        with self.app_context():
            p_list = PassportModel.query.filter_by(employee_id=self.e.id).all()
            e_p_list = EmployeeModel.find_by_id(self.e.id, self.o.id).passports

            self.assertListEqual(p_list, e_p_list)

    def test_passport_list_in_country(self):
        """ Test that the country object contains an passport list."""
        with self.app_context():
            p_list = PassportModel.query.filter_by(employee_id=self.e.id).all()
            c_p_list = CountryModel.query.filter_by(id=1).first().passports

            self.assertListEqual(p_list, c_p_list)
