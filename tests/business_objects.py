from werkzeug.security import generate_password_hash

from models.bank import BankModel
from models.bank_account import BankAccountModel
from models.country import CountryModel
from models.creditor import CreditorModel
from models.deduction import DeductionModel
from models.deduction_detail import DeductionDetailModel
from models.department import DepartmentModel
from models.dependent import DependentModel
from models.emergency_contact import EmergencyContactModel
from models.employee import EmployeeModel
from models.employment_position import EmploymentPositionModel
from models.family_relation import FamilyRelationModel
from models.health_permit import HealthPermitModel
from models.marital_status import MaritalStatusModel
from models.organization import OrganizationModel
from models.passport import PassportModel
from models.payment import PaymentModel
from models.payment_detail import PaymentDetailModel
from models.schedule import ScheduleModel
from models.schedule_detail import ScheduleDetailModel
from models.shift import ShiftModel
from models.uniform_item import UniformItemModel
from models.uniform_requirement import UniformRequirementModel
from models.uniform_size import UniformSizeModel
from models.user import AppUserModel

ORGANIZATION = {
    'resources': ['Organization', 'ActivateOrganization', 'Organizations'],
    'model': OrganizationModel,
    'required_objects': [],
    'post_objects': [
        {
            'organization_name': 'test_o_0',
            'is_active': True
        },
        {
            'organization_name': 'test_o_1',
            'is_active': True
        }
    ],
    'put_objects': [
        {
            'organization_name': 'new_test_o_0',
            'is_active': False
        },
        {
            'organization_name': 'test_o_0',
            'is_active': False
        }
    ],
    'endpoints': ['organization', 'activate_organization', 'organizations'],
    'user_type': 'root'
}

USER = {
    'resources': ['user_type', 'ActivateUser', 'Users'],
    'model': AppUserModel,
    'required_objects': [ORGANIZATION],
    'post_objects': [
        {
            'username': 'test_u_0',
            'password': 'test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'test_u_0@test_o_0.com',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'is_super': True,
            'is_owner': True,
            'is_active': True
        },
        {
            'username': 'test_u_1',
            'password': 'test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'test_u_1@test_o_0.com',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'is_super': True,
            'is_owner': True,
            'is_active': True
        },
        {
            'username': 'test_u_2',
            'password': 'test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'test_u_2@test_o_0.com',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'is_super': True,
            'is_owner': True,
            'is_active': True
        }
    ],
    'put_objects': [
        {
            'username': 'new_test_u_0',
            'password': 'new_test_p',
            'password_hash': generate_password_hash('new_test_p'),
            'email': 'new_test_u_0@test_o_0.com',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1]),
            'is_super': False,
            'is_owner': False,
            'is_active': False
        },
        {
            'username': 'test_u_0',
            'password': 'new_test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'new_test_u_1@test_o_0.com',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'is_super': False,
            'is_owner': False,
            'is_active': True
        },
        {
            'username': 'new_test_u_2',
            'password': 'new_test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'test_u_0@test_o_0.com',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'is_super': False,
            'is_owner': False,
            'is_active': True
        }
    ],
    'endpoints': ['user_type', 'activate_user', 'users'],
    'user_type': 'root'
}

DEPARTMENT = {
    'resources': ['Department', 'ActivateDepartment', 'Departments'],
    'model': DepartmentModel,
    'required_objects': [ORGANIZATION],
    'post_objects': [
        {
            'department_name': 'test_d_0',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'is_active': True
        },
        {
            'department_name': 'test_d_1',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'is_active': True
        },
        {
            'department_name': 'test_d_0',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1]),
            'is_active': True
        }
    ],
    'put_objects': [
        {
            'department_name': 'new_test_d_0',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1]),
            'is_active': False
        },
        {
            'department_name': 'test_d_0',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'is_active': True
        }
    ],
    'endpoints': ['department', 'activate_department', 'departments'],
    'user_type': 'test'
}

MARITAL_STATUS = {
    'resources': [None, None, 'MaritalStatuses'],
    'model': MaritalStatusModel,
    'required_objects': [],
    'post_objects': [],
    'put_objects': [],
    'endpoints': [None, None, 'marital_statuses'],
    'user_type': 'test'
}

EMPLOYMENT_POSITION = {
    'resources': ['EmploymentPosition', 'ActivateEmploymentPosition', 'EmploymentPositions'],
    'model': EmploymentPositionModel,
    'required_objects': [ORGANIZATION],
    'post_objects': [
        {
            'position_name_feminine': 'test_e_p_f_0',
            'position_name_masculine': 'test_e_p_m_0',
            'minimum_hourly_wage': 1.00,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
        },
        {
            'position_name_feminine': 'test_e_p_f_1',
            'position_name_masculine': 'test_e_p_m_1',
            'minimum_hourly_wage': 1.00,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
        },
        {
            'position_name_feminine': 'test_e_p_f_0',
            'position_name_masculine': 'test_e_p_m_0',
            'minimum_hourly_wage': 1.00,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1]),
        }
    ],
    'put_objects': [
        {
            'position_name_feminine': 'new_test_e_p_f',
            'position_name_masculine': 'new_test_e_p_m',
            'minimum_hourly_wage': 2.00,
            'is_active': False,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1]),
        },
        {
            'position_name_feminine': 'test_e_p_f_0',
            'position_name_masculine': 'new_test_e_p_m_0',
            'minimum_hourly_wage': 2.00,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
        },
        {
            'position_name_feminine': 'new_test_e_p_f_0',
            'position_name_masculine': 'test_e_p_m_0',
            'minimum_hourly_wage': 2.00,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
        }
    ],
    'endpoints': ['employment_position', 'activate_employment_position', 'employment_positions'],
    'user_type': 'test'
}

SHIFT_R = {
    'resources': ['Shift', 'ActivateShift', 'Shifts'],
    'model': ShiftModel,
    'required_objects': [ORGANIZATION],
    'post_objects': [
        {
            'shift_name': 'test_s_r_0',
            'weekly_hours': 48,
            'is_rotating': True,
            'payment_period': 'Quincenal',
            'break_length': '00:30:00',
            'is_break_included_in_shift': False,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'rotation_start_hour': '06:00:00',
            'rotation_end_hour': '21:00:00'
        },
        {
            'shift_name': 'test_s_r_1',
            'weekly_hours': 48,
            'is_rotating': True,
            'payment_period': 'Quincenal',
            'break_length': '00:30:00',
            'is_break_included_in_shift': False,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'rotation_start_hour': '06:00:00',
            'rotation_end_hour': '21:00:00'
        },
        {
            'shift_name': 'test_s_r_0',
            'weekly_hours': 48,
            'is_rotating': True,
            'payment_period': 'Quincenal',
            'break_length': '00:30:00',
            'is_break_included_in_shift': False,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1]),
            'rotation_start_hour': '06:00:00',
            'rotation_end_hour': '21:00:00'
        }
    ],
    'put_objects': [
        {
            'shift_name': 'new_test_s_r_0',
            'weekly_hours': 44,
            'is_rotating': True,
            'payment_period': 'Semanal',
            'break_length': '01:00:00',
            'is_break_included_in_shift': True,
            'is_active': False,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1]),
            'rotation_start_hour': '00:00:00',
            'rotation_end_hour': '15:00:00'
        },
        {
            'shift_name': 'test_s_r_0',
            'weekly_hours': 44,
            'is_rotating': True,
            'payment_period': 'Semanal',
            'break_length': '01:00:00',
            'is_break_included_in_shift': True,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'rotation_start_hour': '00:00:00',
            'rotation_end_hour': '15:00:00'
        }
    ],
    'endpoints': ['shift', 'activate_shift', 'shifts'],
    'user_type': 'test'
}

SHIFT_F = {
    'resources': ['Shift', 'ActivateShift', 'Shifts'],
    'model': ShiftModel,
    'required_objects': [ORGANIZATION],
    'post_objects': [
        {
            'shift_name': 'test_s_f_0',
            'weekly_hours': 44,
            'is_rotating': False,
            'payment_period': 'Quincenal',
            'break_length': '00:30:00',
            'is_break_included_in_shift': False,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'fixed_start_hour_monday': '08:00:00',
            'fixed_start_break_hour_monday': '12:00:00',
            'fixed_end_break_hour_monday': '12:30:00',
            'fixed_end_hour_monday': '16:30:00',
            'fixed_start_hour_tuesday': '08:00:00',
            'fixed_start_break_hour_tuesday': '12:00:00',
            'fixed_end_break_hour_tuesday': '12:30:00',
            'fixed_end_hour_tuesday': '16:30:00',
            'fixed_start_hour_wednesday': '08:00:00',
            'fixed_start_break_hour_wednesday': '12:00:00',
            'fixed_end_break_hour_wednesday': '12:30:00',
            'fixed_end_hour_wednesday': '16:30:00',
            'fixed_start_hour_thursday': '08:00:00',
            'fixed_start_break_hour_thursday': '12:00:00',
            'fixed_end_break_hour_thursday': '12:30:00',
            'fixed_end_hour_thursday': '16:30:00',
            'fixed_start_hour_friday': '08:00:00',
            'fixed_start_break_hour_friday': '12:00:00',
            'fixed_end_break_hour_friday': '12:30:00',
            'fixed_end_hour_friday': '16:30:00',
            'fixed_start_hour_saturday': '08:00:00',
            'fixed_end_hour_saturday': '12:00:00',
            'rest_day': 'Domingo'
        },
        {
            'shift_name': 'test_s_f_1',
            'weekly_hours': 44,
            'is_rotating': False,
            'payment_period': 'Quincenal',
            'break_length': '00:30:00',
            'is_break_included_in_shift': False,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'fixed_start_hour_monday': '08:00:00',
            'fixed_start_break_hour_monday': '12:00:00',
            'fixed_end_break_hour_monday': '12:30:00',
            'fixed_end_hour_monday': '16:30:00',
            'fixed_start_hour_tuesday': '08:00:00',
            'fixed_start_break_hour_tuesday': '12:00:00',
            'fixed_end_break_hour_tuesday': '12:30:00',
            'fixed_end_hour_tuesday': '16:30:00',
            'fixed_start_hour_wednesday': '08:00:00',
            'fixed_start_break_hour_wednesday': '12:00:00',
            'fixed_end_break_hour_wednesday': '12:30:00',
            'fixed_end_hour_wednesday': '16:30:00',
            'fixed_start_hour_thursday': '08:00:00',
            'fixed_start_break_hour_thursday': '12:00:00',
            'fixed_end_break_hour_thursday': '12:30:00',
            'fixed_end_hour_thursday': '16:30:00',
            'fixed_start_hour_friday': '08:00:00',
            'fixed_start_break_hour_friday': '12:00:00',
            'fixed_end_break_hour_friday': '12:30:00',
            'fixed_end_hour_friday': '16:30:00',
            'fixed_start_hour_saturday': '08:00:00',
            'fixed_end_hour_saturday': '12:00:00',
            'rest_day': 'Domingo'
        },
        {
            'shift_name': 'test_s_f_0',
            'weekly_hours': 44,
            'is_rotating': False,
            'payment_period': 'Quincenal',
            'break_length': '00:30:00',
            'is_break_included_in_shift': False,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1]),
            'fixed_start_hour_monday': '08:00:00',
            'fixed_start_break_hour_monday': '12:00:00',
            'fixed_end_break_hour_monday': '12:30:00',
            'fixed_end_hour_monday': '16:30:00',
            'fixed_start_hour_tuesday': '08:00:00',
            'fixed_start_break_hour_tuesday': '12:00:00',
            'fixed_end_break_hour_tuesday': '12:30:00',
            'fixed_end_hour_tuesday': '16:30:00',
            'fixed_start_hour_wednesday': '08:00:00',
            'fixed_start_break_hour_wednesday': '12:00:00',
            'fixed_end_break_hour_wednesday': '12:30:00',
            'fixed_end_hour_wednesday': '16:30:00',
            'fixed_start_hour_thursday': '08:00:00',
            'fixed_start_break_hour_thursday': '12:00:00',
            'fixed_end_break_hour_thursday': '12:30:00',
            'fixed_end_hour_thursday': '16:30:00',
            'fixed_start_hour_friday': '08:00:00',
            'fixed_start_break_hour_friday': '12:00:00',
            'fixed_end_break_hour_friday': '12:30:00',
            'fixed_end_hour_friday': '16:30:00',
            'fixed_start_hour_saturday': '08:00:00',
            'fixed_end_hour_saturday': '12:00:00',
            'rest_day': 'Domingo'
        }
    ],
    'put_objects': [
        {
            'shift_name': 'new_test_s_f_0',
            'weekly_hours': 48,
            'is_rotating': False,
            'payment_period': 'Diario',
            'break_length': '00:30:00',
            'is_break_included_in_shift': False,
            'is_active': False,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1]),
            'fixed_start_hour_sunday': '09:00:00',
            'fixed_start_break_hour_sunday': '13:00:00',
            'fixed_end_break_hour_sunday': '13:30:00',
            'fixed_end_hour_sunday': '17:30:00',
            'fixed_start_hour_monday': '09:00:00',
            'fixed_start_break_hour_monday': '13:00:00',
            'fixed_end_break_hour_monday': '13:30:00',
            'fixed_end_hour_monday': '17:30:00',
            'fixed_start_hour_tuesday': '09:00:00',
            'fixed_start_break_hour_tuesday': '13:00:00',
            'fixed_end_break_hour_tuesday': '13:30:00',
            'fixed_end_hour_tuesday': '17:30:00',
            'fixed_start_hour_wednesday': '09:00:00',
            'fixed_start_break_hour_wednesday': '13:00:00',
            'fixed_end_break_hour_wednesday': '13:30:00',
            'fixed_end_hour_wednesday': '17:30:00',
            'fixed_start_hour_thursday': '09:00:00',
            'fixed_start_break_hour_thursday': '13:00:00',
            'fixed_end_break_hour_thursday': '13:30:00',
            'fixed_end_hour_thursday': '17:30:00',
            'fixed_start_hour_friday': '09:00:00',
            'fixed_start_break_hour_friday': '13:00:00',
            'fixed_end_break_hour_friday': '13:30:00',
            'fixed_end_hour_friday': '17:30:00',
            'fixed_start_hour_saturday': None,
            'fixed_end_hour_saturday': None,
            'rest_day': 'Sábado'
        },
        {
            'shift_name': 'test_s_f_0',
            'weekly_hours': 48,
            'is_rotating': False,
            'payment_period': 'Diario',
            'break_length': '00:30:00',
            'is_break_included_in_shift': False,
            'is_active': True,
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'fixed_start_hour_sunday': '09:00:00',
            'fixed_start_break_hour_sunday': '13:00:00',
            'fixed_end_break_hour_sunday': '13:30:00',
            'fixed_end_hour_sunday': '17:30:00',
            'fixed_start_hour_monday': '09:00:00',
            'fixed_start_break_hour_monday': '13:00:00',
            'fixed_end_break_hour_monday': '13:30:00',
            'fixed_end_hour_monday': '17:30:00',
            'fixed_start_hour_tuesday': '09:00:00',
            'fixed_start_break_hour_tuesday': '13:00:00',
            'fixed_end_break_hour_tuesday': '13:30:00',
            'fixed_end_hour_tuesday': '17:30:00',
            'fixed_start_hour_wednesday': '09:00:00',
            'fixed_start_break_hour_wednesday': '13:00:00',
            'fixed_end_break_hour_wednesday': '13:30:00',
            'fixed_end_hour_wednesday': '17:30:00',
            'fixed_start_hour_thursday': '09:00:00',
            'fixed_start_break_hour_thursday': '13:00:00',
            'fixed_end_break_hour_thursday': '13:30:00',
            'fixed_end_hour_thursday': '17:30:00',
            'fixed_start_hour_friday': '09:00:00',
            'fixed_start_break_hour_friday': '13:00:00',
            'fixed_end_break_hour_friday': '13:30:00',
            'fixed_end_hour_friday': '17:30:00',
            'fixed_start_hour_saturday': None,
            'fixed_end_hour_saturday': None,
            'rest_day': 'Sábado'
        }
    ],
    'endpoints': ['shift', 'activate_shift', 'shifts'],
    'user_type': 'test'
}

EMPLOYEE = {
    'resources': ['Employee', 'ActivateEmployee', 'Employees'],
    'model': EmployeeModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R],
    'post_objects': [
        {
            'first_name': 'f_n_0',
            'second_name': 's_n_0',
            'first_surname': 'f_sn_0',
            'second_surname': 's_sn_0',
            'national_id_number': '1-11-111',
            'is_panamanian': True,
            'date_of_birth': '2000-01-31',
            'gender': 'Hombre',
            'address': 'Panamá',
            'home_phone': '222-2222',
            'mobile_phone': '6666-6666',
            'email': 'f_n_0@f_sn_0.com',
            'type_of_contract': 'Definido',
            'employment_date': '2018-01-01',
            'contract_expiration_date': '2018-01-31',
            'termination_date': '2018-01-15',
            'termination_reason': 'Período de Prueba',
            'salary_per_payment_period': 104,
            'representation_expenses_per_payment_period': 0,
            'payment_method': 'ACH',
            'is_active': True,
            'marital_status_id': 1,
            'department_id': ('get_department', DEPARTMENT['post_objects'][0]),
            'position_id': ('get_employment_position', EMPLOYMENT_POSITION['post_objects'][0]),
            'shift_id': ('get_shift', SHIFT_R['post_objects'][0])
        },
        {
            'first_name': 'f_n_1',
            'second_name': 's_n_1',
            'first_surname': 'f_sn_1',
            'second_surname': 's_sn_1',
            'national_id_number': '1-11-111',
            'is_panamanian': True,
            'date_of_birth': '2000-01-31',
            'gender': 'Mujer',
            'address': 'Panamá',
            'home_phone': '222-2222',
            'mobile_phone': '6666-6666',
            'email': 'f_n_1@f_sn_1.com',
            'type_of_contract': 'Indefinido',
            'employment_date': '2018-01-01',
            'contract_expiration_date': '2018-01-31',
            'termination_date': '2018-01-15',
            'termination_reason': 'Renuncia',
            'salary_per_payment_period': 104,
            'representation_expenses_per_payment_period': 0,
            'payment_method': 'Efectivo',
            'is_active': True,
            'marital_status_id': 1,
            'department_id': ('get_department', DEPARTMENT['post_objects'][0]),
            'position_id': ('get_employment_position', EMPLOYMENT_POSITION['post_objects'][0]),
            'shift_id': ('get_shift', SHIFT_R['post_objects'][0])
        }
    ],
    'put_objects': [
        {
            'first_name': 'new_f_n_0',
            'second_name': 'new_s_n_0',
            'first_surname': 'new_f_sn_0',
            'second_surname': 'new_s_sn_0',
            'national_id_number': 'N-1-11-111',
            'is_panamanian': False,
            'date_of_birth': '2001-01-31',
            'gender': 'Mujer',
            'address': 'Chiriquí',
            'home_phone': '333-3333',
            'mobile_phone': '6666-7777',
            'email': 'new_f_n_0@new_f_sn_0.com',
            'type_of_contract': 'Indefinido',
            'employment_date': '2019-01-01',
            'contract_expiration_date': '2019-01-31',
            'termination_date': '2019-01-15',
            'termination_reason': 'Renuncia',
            'salary_per_payment_period': 208,
            'representation_expenses_per_payment_period': 100,
            'payment_method': 'Cheque',
            'is_active': True,
            'marital_status_id': 2,
            'department_id': ('get_department', DEPARTMENT['post_objects'][1]),
            'position_id': ('get_employment_position', EMPLOYMENT_POSITION['post_objects'][1]),
            'shift_id': ('get_shift', SHIFT_R['post_objects'][1])
        }
    ],
    'endpoints': ['employee', 'activate_employee', 'employees'],
    'user_type': 'test'
}

HEALTH_PERMIT = {
    'resources': ['HealthPermit', None, 'HealthPermits'],
    'model': HealthPermitModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'health_permit_type': 'Verde',
            'issue_date': '2018-01-01',
            'expiration_date': '2019-01-01',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0])
        },
        {
            'health_permit_type': 'Blanco',
            'issue_date': '2018-01-31',
            'expiration_date': '2019-01-31',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0])
        }
    ],
    'put_objects': [
        {
            'health_permit_type': 'Blanco',
            'issue_date': '2018-01-31',
            'expiration_date': '2019-01-31',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1])
        }
    ],
    'endpoints': ['health_permit', None, 'health_permits'],
    'user_type': 'test'
}

EMERGENCY_CONTACT = {
    'resources': ['EmergencyContact', None, 'EmergencyContacts'],
    'model': EmergencyContactModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'first_name': 'f_n_0',
            'last_name': 'l_n_0',
            'home_phone': '111-1111',
            'work_phone': '222-2222',
            'mobile_phone': '6666-6666',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0])
        },
        {
            'first_name': 'f_n_1',
            'last_name': 'l_n_1',
            'home_phone': '111-1111',
            'work_phone': '222-2222',
            'mobile_phone': '6666-6666',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0])
        }
    ],
    'put_objects': [
        {
            'first_name': 'new_f_n_0',
            'last_name': 'new_l_n_0',
            'home_phone': '333-3333',
            'work_phone': '444-4444',
            'mobile_phone': '6666-7777',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1])
        }
    ],
    'endpoints': ['emergency_contact', None, 'emergency_contacts'],
    'user_type': 'test'
}

COUNTRY = {
    'resources': [None, None, 'Countries'],
    'model': CountryModel,
    'required_objects': [],
    'post_objects': [],
    'put_objects': [],
    'endpoints': [None, None, 'countries'],
    'user_type': 'test'
}

PASSPORT = {
    'resources': ['Passport', None, 'Passports'],
    'model': PassportModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'passport_number': '123456',
            'issue_date': '2018-01-01',
            'expiration_date': '2019-01-01',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'country_id': 1
        },
        {
            'passport_number': '654321',
            'issue_date': '2018-01-01',
            'expiration_date': '2019-01-01',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1]),
            'country_id': 2
        }
    ],
    'put_objects': [
        {
            'passport_number': '654321',
            'issue_date': '2018-01-31',
            'expiration_date': '2019-01-31',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1]),
            'country_id': 2
        }
    ],
    'endpoints': ['passport', None, 'passports'],
    'user_type': 'test'
}

UNIFORM_ITEM = {
    'resources': ['UniformItem', None, 'UniformItems'],
    'model': UniformItemModel,
    'required_objects': [ORGANIZATION],
    'post_objects': [
        {
            'item_name': 'test_u_i_0',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0])
        },
        {
            'item_name': 'test_u_i_1',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0])
        },
        {
            'item_name': 'test_u_i_0',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1])
        }
    ],
    'put_objects': [
        {
            'item_name': 'new_test_u_i_0',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1])
        },
        {
            'item_name': 'test_u_i_0',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0])
        }
    ],
    'endpoints': ['uniform_item', None, 'uniform_item'],
    'user_type': 'test'
}

UNIFORM_SIZE = {
    'resources': ['UniformSize', None, 'UniformSizes'],
    'model': UniformSizeModel,
    'required_objects': [ORGANIZATION, UNIFORM_ITEM],
    'post_objects': [
        {
            'size_description': 'test_u_s_0',
            'uniform_item_id': ('get_uniform_item', 0)
        },
        {
            'size_description': 'test_u_s_1',
            'uniform_item_id': ('get_uniform_item', 1)
        },
        {
            'size_description': 'test_u_s_0',
            'uniform_item_id': ('get_uniform_item', 1)
        }
    ],
    'put_objects': [
        {
            'size_description': 'new_test_u_s',
            'uniform_item_id': ('get_uniform_item', 1)
        },
        {
            'size_description': 'test_u_s_0',
            'uniform_item_id': ('get_uniform_item', 0)
        }
    ],
    'endpoints': ['uniform_size', None, 'uniform_sizes'],
    'user_type': 'test'
}

UNIFORM_REQUIREMENT = {
    'resources': ['UniformRequirement', None, 'UniformRequirements'],
    'model': UniformRequirementModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE, UNIFORM_ITEM, UNIFORM_SIZE],
    'post_objects': [
        {
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'uniform_item_id': ('get_uniform_item', 0),
            'uniform_size_id': ('get_uniform_size', 0)
        },
        {
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'uniform_item_id': ('get_uniform_item', 1),
            'uniform_size_id': ('get_uniform_size', 1)
        },
        {
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1]),
            'uniform_item_id': ('get_uniform_item', 1),
            'uniform_size_id': ('get_uniform_size', 1)
        }
    ],
    'put_objects': [
        {
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1]),
            'uniform_item_id': ('get_uniform_item', 0),
            'uniform_size_id': ('get_uniform_size', 0)
        },
        {
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'uniform_item_id': ('get_uniform_item', 0),
            'uniform_size_id': ('get_uniform_size', 0)
        }
    ],
    'endpoints': ['uniform_requirement', None, 'uniform_requirements'],
    'user_type': 'test'
}

BANK = {
    'resources': [None, None, 'Banks'],
    'model': BankModel,
    'required_objects': [],
    'post_objects': [],
    'put_objects': [],
    'endpoints': [None, None, 'banks'],
    'user_type': 'test'
}

BANK_ACCOUNT = {
    'resources': ['BankAccount', 'ActivateBankAccount', 'BankAccounts'],
    'model': BankAccountModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'account_number': '1234',
            'account_type': 'Corriente',
            'is_active': True,
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'bank_id': 1
        },
        {
            'account_number': '4321',
            'account_type': 'Ahorros',
            'is_active': True,
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'bank_id': 1
        },
        {
            'account_number': '1234',
            'account_type': 'Corriente',
            'is_active': True,
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1]),
            'bank_id': 1
        },
        {
            'account_number': '1234',
            'account_type': 'Corriente',
            'is_active': True,
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'bank_id': 2
        }
    ],
    'put_objects': [
        {
            'account_number': '4321',
            'account_type': 'Ahorro',
            'is_active': False,
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1]),
            'bank_id': 2,
        },
        {
            'account_number': '1234',
            'account_type': 'Corriente',
            'is_active': True,
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'bank_id': 1,
        }
    ],
    'endpoints': ['bank_account', 'activate_bank_account', 'bank_accounts'],
    'user_type': 'test'
}

FAMILY_RELATION = {
    'resources': [None, None, 'FamilyRelations'],
    'model': FamilyRelationModel,
    'required_objects': [],
    'post_objects': [],
    'put_objects': [],
    'endpoints': [None, None, 'family_relations'],
    'user_type': 'test'
}

DEPENDENT = {
    'resources': ['Dependent', None, 'Dependents'],
    'model': DependentModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'first_name': 'f_n_0',
            'second_name': 's_n_0',
            'first_surname': 'f_sn_0',
            'second_surname': 's_sn_0',
            'gender': 'Mujer',
            'date_of_birth': '2018-01-01',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'family_relation_id': 1
        },
        {
            'first_name': 'f_n_1',
            'second_name': 's_n_1',
            'first_surname': 'f_sn_1',
            'second_surname': 's_sn_1',
            'gender': 'Mujer',
            'date_of_birth': '2018-01-01',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'family_relation_id': 2
        }
    ],
    'put_objects': [
        {
            'first_name': 'new_f_n_0',
            'second_name': 'new_s_n_0',
            'first_surname': 'new_f_sn_0',
            'second_surname': 'new_s_sn_0',
            'gender': 'Hombre',
            'date_of_birth': '2018-01-31',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1]),
            'family_relation_id': 2
        }
    ],
    'endpoints': ['dependent', None, 'dependents'],
    'user_type': 'test'
}

SCHEDULE = {
    'resources': ['Schedule', None, 'Schedules'],
    'model': ScheduleModel,
    'required_objects': [ORGANIZATION, DEPARTMENT],
    'post_objects': [
        {
            'start_date': '2018-01-01',
            'department_id': ('get_department', DEPARTMENT['post_objects'][0])
        },
        {
            'start_date': '2018-01-08',
            'department_id': ('get_department', DEPARTMENT['post_objects'][0])
        },
        {
            'start_date': '2018-01-01',
            'department_id': ('get_department', DEPARTMENT['post_objects'][1])
        }
    ],
    'put_objects': [
        {
            'start_date': '2018-01-31',
            'department_id': ('get_department', DEPARTMENT['post_objects'][0])
        },
        {
            'start_date': '2018-01-01',
            'department_id': ('get_department', DEPARTMENT['post_objects'][0])
        }
    ],
    'endpoints': ['schedule', None, 'schedules'],
    'user_type': 'test'
}

SCHEDULE_DETAIL = {
    'resources': ['ScheduleDetail', None, 'ScheduleDetails'],
    'model': ScheduleDetailModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, SCHEDULE, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'day_1_start': '2018-01-01T06:00:00',
            'day_1_end': '2018-01-01T14:00:00',
            'day_1_comment': 'comment 1',
            'day_2_start': '2018-01-02T06:00:00',
            'day_2_end': '2018-01-02T14:00:00',
            'day_2_comment': 'comment 2',
            'day_3_start': '2018-01-03T06:00:00',
            'day_3_end': '2018-01-03T14:00:00',
            'day_3_comment': 'comment 3',
            'day_4_start': '2018-01-04T06:00:00',
            'day_4_end': '2018-01-04T14:00:00',
            'day_4_comment': 'comment 4',
            'day_5_start': None,
            'day_5_end': None,
            'day_5_comment': None,
            'day_6_start': '2018-01-06T22:00:00',
            'day_6_end': '2018-01-07T06:00:00',
            'day_6_comment': 'comment 6',
            'day_7_start': '2018-01-07T22:00:00',
            'day_7_end': '2018-01-08T06:00:00',
            'day_7_comment': 'comment 7',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'schedule_id': ('get_schedule', 0)
        },
        {
            'day_1_start': '2018-01-08T06:00:00',
            'day_1_end': '2018-01-08T14:00:00',
            'day_1_comment': 'comment 1',
            'day_2_start': '2018-01-09T06:00:00',
            'day_2_end': '2018-01-09T14:00:00',
            'day_2_comment': 'comment 2',
            'day_3_start': '2018-01-10T06:00:00',
            'day_3_end': '2018-01-10T14:00:00',
            'day_3_comment': 'comment 3',
            'day_4_start': '2018-01-11T06:00:00',
            'day_4_end': '2018-01-11T14:00:00',
            'day_4_comment': 'comment 4',
            'day_5_start': None,
            'day_5_end': None,
            'day_5_comment': None,
            'day_6_start': '2018-01-13T22:00:00',
            'day_6_end': '2018-01-13T06:00:00',
            'day_6_comment': 'comment 6',
            'day_7_start': '2018-01-17T22:00:00',
            'day_7_end': '2018-01-17T06:00:00',
            'day_7_comment': 'comment 7',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1]),
            'schedule_id': ('get_schedule', 1)
        },
        {
            'day_1_start': '2018-01-01T06:00:00',
            'day_1_end': '2018-01-01T14:00:00',
            'day_1_comment': 'comment 1',
            'day_2_start': '2018-01-02T06:00:00',
            'day_2_end': '2018-01-02T14:00:00',
            'day_2_comment': 'comment 2',
            'day_3_start': '2018-01-03T06:00:00',
            'day_3_end': '2018-01-03T14:00:00',
            'day_3_comment': 'comment 3',
            'day_4_start': '2018-01-04T06:00:00',
            'day_4_end': '2018-01-04T14:00:00',
            'day_4_comment': 'comment 4',
            'day_5_start': None,
            'day_5_end': None,
            'day_5_comment': None,
            'day_6_start': '2018-01-06T22:00:00',
            'day_6_end': '2018-01-07T06:00:00',
            'day_6_comment': 'comment 6',
            'day_7_start': '2018-01-07T22:00:00',
            'day_7_end': '2018-01-08T06:00:00',
            'day_7_comment': 'comment 7',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1]),
            'schedule_id': ('get_schedule', 0)
        }
    ],
    'put_objects': [
        {
            'day_1_start': '2018-01-08T06:00:00',
            'day_1_end': '2018-01-08T14:00:00',
            'day_1_comment': 'comment 1',
            'day_2_start': '2018-01-09T06:00:00',
            'day_2_end': '2018-01-09T14:00:00',
            'day_2_comment': 'comment 2',
            'day_3_start': '2018-01-10T06:00:00',
            'day_3_end': '2018-01-10T14:00:00',
            'day_3_comment': 'comment 3',
            'day_4_start': '2018-01-11T06:00:00',
            'day_4_end': '2018-01-11T14:00:00',
            'day_4_comment': 'comment 4',
            'day_5_start': None,
            'day_5_end': None,
            'day_5_comment': None,
            'day_6_start': '2018-01-13T22:00:00',
            'day_6_end': '2018-01-13T06:00:00',
            'day_6_comment': 'comment 6',
            'day_7_start': '2018-01-17T22:00:00',
            'day_7_end': '2018-01-17T06:00:00',
            'day_7_comment': 'comment 7',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'schedule_id': ('get_schedule', 1)
        },
        {
            'day_1_start': '2018-01-01T06:00:00',
            'day_1_end': '2018-01-01T14:00:00',
            'day_1_comment': 'comment 1',
            'day_2_start': '2018-01-02T06:00:00',
            'day_2_end': '2018-01-02T14:00:00',
            'day_2_comment': 'comment 2',
            'day_3_start': '2018-01-03T06:00:00',
            'day_3_end': '2018-01-03T14:00:00',
            'day_3_comment': 'comment 3',
            'day_4_start': '2018-01-04T06:00:00',
            'day_4_end': '2018-01-04T14:00:00',
            'day_4_comment': 'comment 4',
            'day_5_start': None,
            'day_5_end': None,
            'day_5_comment': None,
            'day_6_start': '2018-01-06T22:00:00',
            'day_6_end': '2018-01-07T06:00:00',
            'day_6_comment': 'comment 6',
            'day_7_start': '2018-01-07T22:00:00',
            'day_7_end': '2018-01-08T06:00:00',
            'day_7_comment': 'comment 7',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1]),
            'schedule_id': ('get_schedule', 0)
        }
    ],
    'endpoints': ['schedule_detail', None, 'schedule_details'],
    'user_type': 'test'
}

PAYMENT = {
    'resources': ['Payment', None, 'Payments'],
    'model': PaymentModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'payment_date': '2018-01-01',
            'document_number': '1234-abc',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0])
        },
        {
            'payment_date': '2018-01-15',
            'document_number': '4321-abc',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0])
        }
    ],
    'put_objects': [
        {
            'payment_date': '2018-02-01',
            'document_number': '1234-def',
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1])
        }
    ],
    'endpoints': ['payment', None, 'payments'],
    'user_type': 'test'
}

PAYMENT_DETAIL = {
    'resources': ['PaymentDetail', None, 'PaymentDetails'],
    'model': PaymentDetailModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE, PAYMENT],
    'post_objects': [
        {
            'payment_type': 'Salario Regular',
            'gross_payment': 1234.56,
            'ss_deduction': 123.45,
            'se_deduction': 12.34,
            'isr_deduction': 1.23,
            'payment_id': ('get_payment', PAYMENT['post_objects'][0])
        },
        {
            'payment_type': 'Vacación',
            'gross_payment': 234.56,
            'ss_deduction': 23.45,
            'se_deduction': 2.34,
            'isr_deduction': 0.23,
            'payment_id': ('get_payment', PAYMENT['post_objects'][0])
        }
    ],
    'put_objects': [
        {
            'payment_type': 'Vacación',
            'gross_payment': 2345.67,
            'ss_deduction': 234.56,
            'se_deduction': 23.45,
            'isr_deduction': 2.34,
            'payment_id': ('get_payment', PAYMENT['post_objects'][1])
        }
    ],
    'endpoints': ['payment_detail', None, 'payment_details'],
    'user_type': 'test'
}

CREDITOR = {
    'resources': ['Creditor', 'ActivateCreditor', 'Creditors'],
    'model': CreditorModel,
    'required_objects': [ORGANIZATION],
    'post_objects': [
        {
            'creditor_name': 'test_cr_0',
            'phone_number': '123-4567',
            'email': 'test@test_cr_0.com',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'is_active': True
        },
        {
            'creditor_name': 'test_cr_1',
            'phone_number': '123-4567',
            'email': 'test@test_cr_1.com',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'is_active': True
        },
        {
            'creditor_name': 'test_cr_0',
            'phone_number': '123-4567',
            'email': 'test@test_cr_0.com',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1]),
            'is_active': True
        }
    ],
    'put_objects': [
        {
            'creditor_name': 'new_test_cr_0',
            'phone_number': '456-7890',
            'email': 'test@new_test_cr_0.com',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][1]),
            'is_active': False
        },
        {
            'creditor_name': 'new_test_cr_0',
            'phone_number': '456-7890',
            'email': 'test@new_test_cr_0.com',
            'organization_id': ('get_organization', ORGANIZATION['post_objects'][0]),
            'is_active': True
        }
    ],
    'endpoints': ['creditor', 'activate_creditor', 'creditors'],
    'user_type': 'test'
}

DEDUCTION = {
    'resources': ['Deduction', 'ActivateDeduction', 'Deductions'],
    'model': DeductionModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'start_date': '2018-01-01',
            'end_date': '2018-01-31',
            'deduction_per_payment_period': 123.45,
            'payment_method': 'Cheque',
            'deduct_in_december': True,
            'is_active': True,
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'creditor_id': ('get_creditor', CREDITOR['post_objects'][0])
        },
        {
            'start_date': '2018-02-01',
            'end_date': '2018-02-31',
            'deduction_per_payment_period': 321.45,
            'payment_method': 'Transferencia',
            'deduct_in_december': False,
            'is_active': True,
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][0]),
            'creditor_id': ('get_creditor', CREDITOR['post_objects'][1])
        }
    ],
    'put_objects': [
        {
            'start_date': '2018-02-01',
            'end_date': '2018-02-28',
            'deduction_per_payment_period': 45.67,
            'payment_method': 'Efectivo',
            'deduct_in_december': False,
            'is_active': False,
            'employee_id': ('get_employee', EMPLOYEE['post_objects'][1]),
            'creditor_id': ('get_creditor', CREDITOR['post_objects'][1])
        }
    ],
    'endpoints': ['deduction', 'activate_deduction', 'deductions'],
    'user_type': 'test'
}

DEDUCTION_DETAIL = {
    'resources': ['DeductionDetail', None, 'DeductionDetails'],
    'model': DeductionDetailModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE, PAYMENT, DEDUCTION],
    'post_objects': [
        {
            'deducted_amount': 123.45,
            'payment_id': ('get_payment', PAYMENT['post_objects'][0]),
            'deduction_id': ('get_deduction', DEDUCTION['post_objects'][0])
        },
        {
            'deducted_amount': 321.45,
            'payment_id': ('get_payment', PAYMENT['post_objects'][0]),
            'deduction_id': ('get_deduction', DEDUCTION['post_objects'][1])
        }
    ],
    'put_objects': [
        {
            'deducted_amount': 89.01,
            'payment_id': ('get_payment', PAYMENT['post_objects'][1]),
            'deduction_id': ('get_deduction', DEDUCTION['post_objects'][1])
        }
    ],
    'endpoints': ['deduction_detail', None, 'deduction_detail'],
    'user_type': 'test'
}


def get_sys_test_params(b_obj, res_type=0):
    """
    Returns the parameters needed to run a system test.

    :param 
        b_obj (dict): Object containing the test parameters.
        res_type (int): Type of resource being tested (0 for record, 1 for activate, 2 for list).
    :return:
        resource (str): Name of the resource being tested.
        model (db.Model): SQLAlchemy model related to the resource.
        required_objects (list): List of business objects that must exist in the db prior to running the test.
        post_objects (list): List of objects for testing the post method of the resource.
        put_objects (list): List of objects for testing the put method of the resource.
        endpoint (str): Endpoint that will receive the request.
        user_type (str): The type of user that will be sending the request.
    """
    resource = b_obj['resources'][res_type]
    model = b_obj['model']
    required_objects = b_obj['required_objects']
    post_objects = b_obj['post_objects']
    put_objects = b_obj['put_objects']
    endpoint = b_obj['endpoints'][res_type]
    user_type = b_obj['user_type']
    
    return resource, model, required_objects, post_objects, put_objects, endpoint, user_type
