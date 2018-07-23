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
    'users': ['root']
}

USER = {
    'model': AppUserModel,
    'required_objects': [ORGANIZATION],
    'post_objects': [
        {
            'username': 'test_u_0',
            'password': 'test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'test_u_0@test_o_0.com',
            'organization_id': 0,
            'is_super': True,
            'is_owner': True,
            'is_active': True
        },
        {
            'username': 'test_u_1',
            'password': 'test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'test_u_1@test_o_0.com',
            'organization_id': 0,
            'is_super': True,
            'is_owner': True,
            'is_active': True
        },
        {
            'username': 'test_u_2',
            'password': 'test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'test_u_2@test_o_0.com',
            'organization_id': 0,
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
            'organization_id': 1,
            'is_super': False,
            'is_owner': False,
            'is_active': False
        },
        {
            'username': 'test_u_0',
            'password': 'new_test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'new_test_u_1@test_o_0.com',
            'organization_id': 0,
            'is_super': False,
            'is_owner': False,
            'is_active': True
        },
        {
            'username': 'new_test_u_2',
            'password': 'new_test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'test_u_0@test_o_0.com',
            'organization_id': 0,
            'is_super': False,
            'is_owner': False,
            'is_active': True
        }
    ],
    'endpoints': ['user', 'activate_user', 'users'],
    'users': ['root']
}

DEPARTMENT = {
    'model': DepartmentModel,
    'required_objects': [ORGANIZATION],
    'post_objects': [
        {
            'department_name': 'test_d_0',
            'organization_id': 0,
            'is_active': True
        },
        {
            'department_name': 'test_d_1',
            'organization_id': 0,
            'is_active': True
        },
        {
            'department_name': 'test_d_0',
            'organization_id': 1,
            'is_active': True
        }
    ],
    'put_objects': [
        {
            'department_name': 'new_test_d_0',
            'organization_id': 1,
            'is_active': False
        },
        {
            'department_name': 'test_d_0',
            'organization_id': 0,
            'is_active': True
        }
    ],
    'endpoints': ['department', 'activate_department', 'departments'],
    'users': ['test']
}

MARITAL_STATUS = {
    'model': MaritalStatusModel,
    'required_objects': [],
    'post_objects': [],
    'put_objects': [],
    'endpoints': [None, None, 'marital_statuses'],
    'users': ['test']
}

EMPLOYMENT_POSITION = {
    'model': EmploymentPositionModel,
    'required_objects': [ORGANIZATION],
    'post_objects': [
        {
            'position_name_feminine': 'test_e_p_f_0',
            'position_name_masculine': 'test_e_p_m_0',
            'minimum_hourly_wage': 1.00,
            'is_active': True,
            'organization_id': 0,
        },
        {
            'position_name_feminine': 'test_e_p_f_1',
            'position_name_masculine': 'test_e_p_m_1',
            'minimum_hourly_wage': 1.00,
            'is_active': True,
            'organization_id': 0,
        },
        {
            'position_name_feminine': 'test_e_p_f_0',
            'position_name_masculine': 'test_e_p_m_0',
            'minimum_hourly_wage': 1.00,
            'is_active': True,
            'organization_id': 1,
        }
    ],
    'put_objects': [
        {
            'position_name_feminine': 'new_test_e_p_f',
            'position_name_masculine': 'new_test_e_p_m',
            'minimum_hourly_wage': 2.00,
            'is_active': False,
            'organization_id': 1,
        },
        {
            'position_name_feminine': 'test_e_p_f_0',
            'position_name_masculine': 'new_test_e_p_m_0',
            'minimum_hourly_wage': 2.00,
            'is_active': True,
            'organization_id': 0,
        },
        {
            'position_name_feminine': 'new_test_e_p_f_0',
            'position_name_masculine': 'test_e_p_m_0',
            'minimum_hourly_wage': 2.00,
            'is_active': True,
            'organization_id': 0,
        }
    ],
    'endpoints': ['employment_position', 'activate_employment_position', 'employment_positions'],
    'users': ['test']
}

SHIFT_R = {
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
            'organization_id': 0,
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
            'organization_id': 0,
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
            'organization_id': 1,
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
            'organization_id': 1,
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
            'organization_id': 0,
            'rotation_start_hour': '00:00:00',
            'rotation_end_hour': '15:00:00'
        }
    ],
    'endpoints': ['shift', 'activate_shift', 'shifts'],
    'users': ['test']
}

SHIFT_F = {
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
            'organization_id': 0,
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
            'organization_id': 0,
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
            'organization_id': 1,
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
            'organization_id': 1,
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
            'organization_id': 0,
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
    'users': ['test']
}

EMPLOYEE = {
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
            'department_id': 0,
            'position_id': 0,
            'shift_id': 0
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
            'department_id': 0,
            'position_id': 0,
            'shift_id': 0
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
            'department_id': 1,
            'position_id': 1,
            'shift_id': 1
        }
    ],
    'endpoints': ['employee', 'activate_employee', 'employees'],
    'users': ['test']
}

HEALTH_PERMIT = {
    'model': HealthPermitModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'health_permit_type': 'Verde',
            'issue_date': '2018-01-01',
            'expiration_date': '2019-01-01',
            'employee_id': 0
        },
        {
            'health_permit_type': 'Blanco',
            'issue_date': '2018-01-31',
            'expiration_date': '2019-01-31',
            'employee_id': 0
        }
    ],
    'put_objects': [
        {
            'health_permit_type': 'Blanco',
            'issue_date': '2018-01-31',
            'expiration_date': '2019-01-31',
            'employee_id': 1
        }
    ],
    'endpoints': ['health_permit', None, 'health_permits'],
    'users': ['test']
}

EMERGENCY_CONTACT = {
    'model': EmergencyContactModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'first_name': 'f_n_0',
            'last_name': 'l_n_0',
            'home_phone': '111-1111',
            'work_phone': '222-2222',
            'mobile_phone': '6666-6666',
            'employee_id': 0
        },
        {
            'first_name': 'f_n_1',
            'last_name': 'l_n_1',
            'home_phone': '111-1111',
            'work_phone': '222-2222',
            'mobile_phone': '6666-6666',
            'employee_id': 0
        }
    ],
    'put_objects': [
        {
            'first_name': 'new_f_n_0',
            'last_name': 'new_l_n_0',
            'home_phone': '333-3333',
            'work_phone': '444-4444',
            'mobile_phone': '6666-7777',
            'employee_id': 1
        }
    ],
    'endpoints': ['emergency_contact', None, 'emergency_contacts'],
    'users': ['test']
}

COUNTRY = {
    'model': CountryModel,
    'required_objects': [],
    'post_objects': [],
    'put_objects': [],
    'endpoints': [None, None, 'countries'],
    'users': ['test']
}

PASSPORT = {
    'model': PassportModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'passport_number': '123456',
            'issue_date': '2018-01-01',
            'expiration_date': '2019-01-01',
            'employee_id': 0,
            'country_id': 1
        },
        {
            'passport_number': '654321',
            'issue_date': '2018-01-01',
            'expiration_date': '2019-01-01',
            'employee_id': 1,
            'country_id': 2
        }
    ],
    'put_objects': [
        {
            'passport_number': '654321',
            'issue_date': '2018-01-31',
            'expiration_date': '2019-01-31',
            'employee_id': 1,
            'country_id': 2
        }
    ],
    'endpoints': ['passport', None, 'passports'],
    'users': ['test']
}

UNIFORM_ITEM = {
    'model': UniformItemModel,
    'required_objects': [ORGANIZATION],
    'post_objects': [
        {
            'item_name': 'test_u_i_0',
            'organization_id': 0
        },
        {
            'item_name': 'test_u_i_1',
            'organization_id': 0
        },
{
            'item_name': 'test_u_i_0',
            'organization_id': 1
        }
    ],
    'put_objects': [
        {
            'item_name': 'new_test_u_i_0',
            'organization_id': 1
        },
        {
            'item_name': 'test_u_i_0',
            'organization_id': 0
        }
    ],
    'endpoints': ['uniform_item', None, 'uniform_item'],
    'users': ['test']
}

UNIFORM_SIZE = {
    'model': UniformSizeModel,
    'required_objects': [ORGANIZATION, UNIFORM_ITEM],
    'post_objects': [
        {
            'size_description': 'test_u_s_0',
            'uniform_item_id': 0
        },
        {
            'size_description': 'test_u_s_1',
            'uniform_item_id': 1
        },
        {
            'size_description': 'test_u_s_0',
            'uniform_item_id': 1
        }
    ],
    'put_objects': [
        {
            'size_description': 'new_test_u_s',
            'uniform_item_id': 1
        },
        {
            'size_description': 'test_u_s_0',
            'uniform_item_id': 0
        }
    ],
    'endpoints': ['uniform_size', None, 'uniform_sizes'],
    'users': ['test']
}

UNIFORM_REQUIREMENT = {
    'model': UniformRequirementModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE, UNIFORM_ITEM, UNIFORM_SIZE],
    'post_objects': [
        {
            'employee_id': 0,
            'uniform_item_id': 0,
            'uniform_size_id': 0
        },
        {
            'employee_id': 0,
            'uniform_item_id': 1,
            'uniform_size_id': 1
        },
        {
            'employee_id': 1,
            'uniform_item_id': 1,
            'uniform_size_id': 1
        }
    ],
    'put_objects': [
        {
            'employee_id': 1,
            'uniform_item_id': 0,
            'uniform_size_id': 0
        },
        {
            'employee_id': 0,
            'uniform_item_id': 0,
            'uniform_size_id': 0
        }
    ],
    'endpoints': ['uniform_requirement', None, 'uniform_requirements'],
    'users': ['test']
}

BANK = {
    'model': BankModel,
    'required_objects': [],
    'post_objects': [],
    'put_objects': [],
    'endpoints': [None, None, 'banks'],
    'users': ['test']
}

BANK_ACCOUNT = {
    'model': BankAccountModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'account_number': '1234',
            'account_type': 'Corriente',
            'is_active': True,
            'employee_id': 0,
            'bank_id': 1
        },
        {
            'account_number': '4321',
            'account_type': 'Ahorros',
            'is_active': True,
            'employee_id': 0,
            'bank_id': 1
        },
        {
            'account_number': '1234',
            'account_type': 'Corriente',
            'is_active': True,
            'employee_id': 1,
            'bank_id': 1
        },
        {
            'account_number': '1234',
            'account_type': 'Corriente',
            'is_active': True,
            'employee_id': 0,
            'bank_id': 2
        }
    ],
    'put_objects': [
        {
            'account_number': '4321',
            'account_type': 'Ahorro',
            'is_active': False,
            'employee_id': 1,
            'bank_id': 2,
        },
        {
            'account_number': '1234',
            'account_type': 'Corriente',
            'is_active': True,
            'employee_id': 0,
            'bank_id': 1,
        }
    ],
    'endpoints': ['bank_account', 'activate_bank_account', 'bank_accounts'],
    'users': ['test']
}

FAMILY_RELATION = {
    'model': FamilyRelationModel,
    'required_objects': [],
    'post_objects': [],
    'put_objects': [],
    'endpoints': [None, None, 'family_relations'],
    'users': ['test']
}

DEPENDENT = {
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
            'employee_id': 0,
            'family_relation_id': 1
        },
        {
            'first_name': 'f_n_1',
            'second_name': 's_n_1',
            'first_surname': 'f_sn_1',
            'second_surname': 's_sn_1',
            'gender': 'Mujer',
            'date_of_birth': '2018-01-01',
            'employee_id': 0,
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
            'employee_id': 1,
            'family_relation_id': 2
        }
    ],
    'endpoints': ['dependent', None, 'dependents'],
    'users': ['test']
}

SCHEDULE = {
    'model': ScheduleModel,
    'required_objects': [ORGANIZATION, DEPARTMENT],
    'post_objects': [
        {
            'start_date': '2018-01-01',
            'department_id': 0
        },
        {
            'start_date': '2018-01-08',
            'department_id': 0
        },
        {
            'start_date': '2018-01-01',
            'department_id': 1
        }
    ],
    'put_objects': [
        {
            'start_date': '2018-01-31',
            'department_id': 0
        },
        {
            'start_date': '2018-01-01',
            'department_id': 0
        }
    ],
    'endpoints': ['schedule', None, 'schedules'],
    'users': ['test']
}

SCHEDULE_DETAIL = {
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
            'employee_id': 0,
            'schedule_id': 0
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
            'employee_id': 1,
            'schedule_id': 1
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
            'employee_id': 1,
            'schedule_id': 0
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
            'employee_id': 0,
            'schedule_id': 1
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
            'employee_id': 1,
            'schedule_id': 0
        }
    ],
    'endpoints': ['schedule_detail', None, 'schedule_details'],
    'users': ['test']
}

PAYMENT = {
    'model': PaymentModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE],
    'post_objects': [
        {
            'payment_date': '2018-01-01',
            'document_number': '1234-abc',
            'employee_id': 0
        },
        {
            'payment_date': '2018-01-15',
            'document_number': '4321-abc',
            'employee_id': 0
        }
    ],
    'put_objects': [
        {
            'payment_date': '2018-02-01',
            'document_number': '1234-def',
            'employee_id': 1
        }
    ],
    'endpoints': ['payment', None, 'payments'],
    'users': ['test']
}

PAYMENT_DETAIL = {
    'model': PaymentDetailModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE, PAYMENT],
    'post_objects': [
        {
            'payment_type': 'Salario Regular',
            'gross_payment': 1234.56,
            'ss_deduction': 123.45,
            'se_deduction': 12.34,
            'isr_deduction': 1.23,
            'payment_id': 0
        },
        {
            'payment_type': 'Vacación',
            'gross_payment': 234.56,
            'ss_deduction': 23.45,
            'se_deduction': 2.34,
            'isr_deduction': 0.23,
            'payment_id': 0
        }
    ],
    'put_objects': [
        {
            'payment_type': 'Vacación',
            'gross_payment': 2345.67,
            'ss_deduction': 234.56,
            'se_deduction': 23.45,
            'isr_deduction': 2.34,
            'payment_id': 1
        }
    ],
    'endpoints': ['payment_detail', None, 'payment_details'],
    'users': ['test']
}

CREDITOR = {
    'model': CreditorModel,
    'required_objects': [ORGANIZATION],
    'post_objects': [
        {
            'creditor_name': 'test_cr_0',
            'phone_number': '123-4567',
            'email': 'test@test_cr_0.com',
            'organization_id': 0,
            'is_active': True
        },
        {
            'creditor_name': 'test_cr_1',
            'phone_number': '123-4567',
            'email': 'test@test_cr_1.com',
            'organization_id': 0,
            'is_active': True
        },
{
            'creditor_name': 'test_cr_0',
            'phone_number': '123-4567',
            'email': 'test@test_cr_0.com',
            'organization_id': 1,
            'is_active': True
        }
    ],
    'put_objects': [
        {
            'creditor_name': 'new_test_cr_0',
            'phone_number': '456-7890',
            'email': 'test@new_test_cr_0.com',
            'organization_id': 1,
            'is_active': False
        },
        {
            'creditor_name': 'new_test_cr_0',
            'phone_number': '456-7890',
            'email': 'test@new_test_cr_0.com',
            'organization_id': 0,
            'is_active': True
        }
    ],
    'endpoints': ['creditor', 'activate_creditor', 'creditors'],
    'users': ['test']
}

DEDUCTION = {
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
            'employee_id': 0,
            'creditor_id': 0
        },
        {
            'start_date': '2018-02-01',
            'end_date': '2018-02-31',
            'deduction_per_payment_period': 321.45,
            'payment_method': 'Transferencia',
            'deduct_in_december': False,
            'is_active': True,
            'employee_id': 0,
            'creditor_id': 1
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
            'employee_id': 1,
            'creditor_id': 1
        }
    ],
    'endpoints': ['deduction', 'activate_deduction', 'deductions'],
    'users': ['test']
}

DEDUCTION_DETAIL = {
    'model': DeductionDetailModel,
    'required_objects': [ORGANIZATION, DEPARTMENT, EMPLOYMENT_POSITION, SHIFT_R, EMPLOYEE, PAYMENT, DEDUCTION],
    'post_objects': [
        {
            'deducted_amount': 123.45,
            'payment_id': 0,
            'deduction_id': 0
        },
        {
            'deducted_amount': 321.45,
            'payment_id': 0,
            'deduction_id': 1
        }
    ],
    'put_objects': [
        {
            'deducted_amount': 89.01,
            'payment_id': 1,
            'deduction_id': 1
        }
    ],
    'endpoints': ['deduction_detail', None, 'deduction_detail'],
    'users': ['test']
}