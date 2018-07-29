from copy import deepcopy
from functools import lru_cache

from werkzeug.security import generate_password_hash

from models.attendance import AttendanceModel
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
    'resources': ['User', 'ActivateUser', 'Users'],
    'model': AppUserModel,
    'post_objects': [
        {
            'username': 'test_u_0',
            'password': 'test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'test_u_0@test_o_0.com',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
            'is_super': True,
            'is_owner': True,
            'is_active': True
        },
        {
            'username': 'test_u_1',
            'password': 'test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'test_u_1@test_o_0.com',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
            'is_super': True,
            'is_owner': True,
            'is_active': True
        },
        {
            'username': 'test_u_2',
            'password': 'test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'test_u_2@test_o_0.com',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
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
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][1]),
            'is_super': False,
            'is_owner': False,
            'is_active': False
        },
        {
            'username': 'test_u_0',
            'password': 'new_test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'new_test_u_1@test_o_0.com',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
            'is_super': False,
            'is_owner': False,
            'is_active': True
        },
        {
            'username': 'new_test_u_2',
            'password': 'new_test_p',
            'password_hash': generate_password_hash('test_p'),
            'email': 'test_u_0@test_o_0.com',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
            'is_super': False,
            'is_owner': False,
            'is_active': True
        }
    ],
    'endpoints': ['user', 'activate_user', 'users'],
    'user_type': 'root'
}

DEPARTMENT = {
    'resources': ['Department', 'ActivateDepartment', 'Departments'],
    'model': DepartmentModel,
    'post_objects': [
        {
            'department_name': 'test_d_0',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
            'is_active': True
        },
        {
            'department_name': 'test_d_1',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
            'is_active': True
        },
        {
            'department_name': 'test_d_0',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][1]),
            'is_active': True
        }
    ],
    'put_objects': [
        {
            'department_name': 'new_test_d_0',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][1]),
            'is_active': False
        },
        {
            'department_name': 'test_d_0',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
            'is_active': True
        }
    ],
    'endpoints': ['department', 'activate_department', 'departments'],
    'user_type': 'test_0'
}

MARITAL_STATUS = {
    'resources': [None, None, 'MaritalStatuses'],
    'model': MaritalStatusModel,
    'post_objects': [
        {
            'status_feminine': 'marital_status_f',
            'status_masculine': 'marital_status_m'
        }
    ],
    'put_objects': [],
    'endpoints': [None, None, 'marital_statuses'],
    'user_type': 'test_0'
}

EMPLOYMENT_POSITION = {
    'resources': ['EmploymentPosition', 'ActivateEmploymentPosition',
                  'EmploymentPositions'],
    'model': EmploymentPositionModel,
    'post_objects': [
        {
            'position_name_feminine': 'test_e_p_f_0',
            'position_name_masculine': 'test_e_p_m_0',
            'minimum_hourly_wage': 1.00,
            'is_active': True,
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
        },
        {
            'position_name_feminine': 'test_e_p_f_1',
            'position_name_masculine': 'test_e_p_m_1',
            'minimum_hourly_wage': 1.00,
            'is_active': True,
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
        },
        {
            'position_name_feminine': 'test_e_p_f_0',
            'position_name_masculine': 'test_e_p_m_0',
            'minimum_hourly_wage': 1.00,
            'is_active': True,
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][1]),
        }
    ],
    'put_objects': [
        {
            'position_name_feminine': 'new_test_e_p_f',
            'position_name_masculine': 'new_test_e_p_m',
            'minimum_hourly_wage': 2.00,
            'is_active': False,
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][1]),
        },
        {
            'position_name_feminine': 'test_e_p_f_0',
            'position_name_masculine': 'new_test_e_p_m_0',
            'minimum_hourly_wage': 2.00,
            'is_active': True,
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
        },
        {
            'position_name_feminine': 'new_test_e_p_f_0',
            'position_name_masculine': 'test_e_p_m_0',
            'minimum_hourly_wage': 2.00,
            'is_active': True,
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
        }
    ],
    'endpoints': ['employment_position', 'activate_employment_position',
                  'employment_positions'],
    'user_type': 'test_0'
}

SHIFT_R = {
    'resources': ['Shift', 'ActivateShift', 'Shifts'],
    'model': ShiftModel,
    'post_objects': [
        {
            'shift_name': 'test_s_r_0',
            'weekly_hours': 48,
            'is_rotating': True,
            'payment_period': 'Quincenal',
            'break_length': '00:30:00',
            'is_break_included_in_shift': False,
            'is_active': True,
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
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
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
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
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][1]),
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
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][1]),
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
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
            'rotation_start_hour': '00:00:00',
            'rotation_end_hour': '15:00:00'
        }
    ],
    'endpoints': ['shift', 'activate_shift', 'shifts'],
    'user_type': 'test_0'
}

SHIFT_F = {
    'resources': ['Shift', 'ActivateShift', 'Shifts'],
    'model': ShiftModel,
    'post_objects': [
        {
            'shift_name': 'test_s_f_0',
            'weekly_hours': 44,
            'is_rotating': False,
            'payment_period': 'Quincenal',
            'break_length': '00:30:00',
            'is_break_included_in_shift': False,
            'is_active': True,
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
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
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
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
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][1]),
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
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][1]),
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
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
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
    'user_type': 'test_0'
}

EMPLOYEE = {
    'resources': ['Employee', 'ActivateEmployee', 'Employees'],
    'model': EmployeeModel,
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
            'department_id': (DEPARTMENT['model'],
                              DEPARTMENT['post_objects'][0]),
            'position_id': (EMPLOYMENT_POSITION['model'],
                            EMPLOYMENT_POSITION['post_objects'][0]),
            'shift_id': (SHIFT_R['model'], SHIFT_R['post_objects'][0])
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
            'department_id': (DEPARTMENT['model'],
                              DEPARTMENT['post_objects'][0]),
            'position_id': (EMPLOYMENT_POSITION['model'],
                            EMPLOYMENT_POSITION['post_objects'][0]),
            'shift_id': (SHIFT_R['model'], SHIFT_R['post_objects'][0])
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
            'department_id': (DEPARTMENT['model'],
                              DEPARTMENT['post_objects'][1]),
            'position_id': (EMPLOYMENT_POSITION['model'],
                            EMPLOYMENT_POSITION['post_objects'][1]),
            'shift_id': (SHIFT_R['model'], SHIFT_R['post_objects'][1])
        }
    ],
    'endpoints': ['employee', 'activate_employee', 'employees'],
    'user_type': 'test_0'
}

HEALTH_PERMIT = {
    'resources': ['HealthPermit', None, 'HealthPermits'],
    'model': HealthPermitModel,
    'post_objects': [
        {
            'health_permit_type': 'Verde',
            'issue_date': '2018-01-01',
            'expiration_date': '2019-01-01',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0])
        },
        {
            'health_permit_type': 'Blanco',
            'issue_date': '2018-01-31',
            'expiration_date': '2019-01-31',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0])
        }
    ],
    'put_objects': [
        {
            'health_permit_type': 'Blanco',
            'issue_date': '2018-01-31',
            'expiration_date': '2019-01-31',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1])
        }
    ],
    'endpoints': ['health_permit', None, 'health_permits'],
    'user_type': 'test_0'
}

EMERGENCY_CONTACT = {
    'resources': ['EmergencyContact', None, 'EmergencyContacts'],
    'model': EmergencyContactModel,
    'post_objects': [
        {
            'first_name': 'f_n_0',
            'last_name': 'l_n_0',
            'home_phone': '111-1111',
            'work_phone': '222-2222',
            'mobile_phone': '6666-6666',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0])
        },
        {
            'first_name': 'f_n_1',
            'last_name': 'l_n_1',
            'home_phone': '111-1111',
            'work_phone': '222-2222',
            'mobile_phone': '6666-6666',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0])
        }
    ],
    'put_objects': [
        {
            'first_name': 'new_f_n_0',
            'last_name': 'new_l_n_0',
            'home_phone': '333-3333',
            'work_phone': '444-4444',
            'mobile_phone': '6666-7777',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1])
        }
    ],
    'endpoints': ['emergency_contact', None, 'emergency_contacts'],
    'user_type': 'test_0'
}

COUNTRY = {
    'resources': [None, None, 'Countries'],
    'model': CountryModel,
    'post_objects': [
        {
            'country_name': 'Panamá',
            'nationality': 'panameña'
        }
    ],
    'put_objects': [],
    'endpoints': [None, None, 'countries'],
    'user_type': 'test_0'
}

PASSPORT = {
    'resources': ['Passport', None, 'Passports'],
    'model': PassportModel,
    'post_objects': [
        {
            'passport_number': '123456',
            'issue_date': '2018-01-01',
            'expiration_date': '2019-01-01',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
            'country_id': 1
        },
        {
            'passport_number': '654321',
            'issue_date': '2018-01-01',
            'expiration_date': '2019-01-01',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1]),
            'country_id': 2
        }
    ],
    'put_objects': [
        {
            'passport_number': '654321',
            'issue_date': '2018-01-31',
            'expiration_date': '2019-01-31',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1]),
            'country_id': 2
        }
    ],
    'endpoints': ['passport', None, 'passports'],
    'user_type': 'test_0'
}

UNIFORM_ITEM = {
    'resources': ['UniformItem', None, 'UniformItems'],
    'model': UniformItemModel,
    'post_objects': [
        {
            'item_name': 'test_u_i_0',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0])
        },
        {
            'item_name': 'test_u_i_1',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0])
        },
        {
            'item_name': 'test_u_i_0',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][1])
        }
    ],
    'put_objects': [
        {
            'item_name': 'new_test_u_i_0',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][1])
        },
        {
            'item_name': 'test_u_i_0',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0])
        }
    ],
    'endpoints': ['uniform_item', None, 'uniform_items'],
    'user_type': 'test_0'
}

UNIFORM_SIZE = {
    'resources': ['UniformSize', None, 'UniformSizes'],
    'model': UniformSizeModel,
    'post_objects': [
        {
            'size_description': 'test_u_s_0',
            'uniform_item_id': (UNIFORM_ITEM['model'],
                                UNIFORM_ITEM['post_objects'][0])
        },
        {
            'size_description': 'test_u_s_1',
            'uniform_item_id': (UNIFORM_ITEM['model'],
                                UNIFORM_ITEM['post_objects'][1])
        },
        {
            'size_description': 'test_u_s_0',
            'uniform_item_id': (UNIFORM_ITEM['model'],
                                UNIFORM_ITEM['post_objects'][1])
        }
    ],
    'put_objects': [
        {
            'size_description': 'new_test_u_s',
            'uniform_item_id': (UNIFORM_ITEM['model'],
                                UNIFORM_ITEM['post_objects'][1])
        },
        {
            'size_description': 'test_u_s_0',
            'uniform_item_id': (UNIFORM_ITEM['model'],
                                UNIFORM_ITEM['post_objects'][0])
        }
    ],
    'endpoints': ['uniform_size', None, 'uniform_sizes'],
    'user_type': 'test_0'
}

UNIFORM_REQUIREMENT = {
    'resources': ['UniformRequirement', None, 'UniformRequirements'],
    'model': UniformRequirementModel,
    'post_objects': [
        {
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
            'uniform_item_id': (UNIFORM_ITEM['model'],
                                UNIFORM_ITEM['post_objects'][0]),
            'uniform_size_id': (UNIFORM_SIZE['model'],
                                UNIFORM_SIZE['post_objects'][0])
        },
        {
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
            'uniform_item_id': (UNIFORM_ITEM['model'],
                                UNIFORM_ITEM['post_objects'][1]),
            'uniform_size_id': (UNIFORM_SIZE['model'],
                                UNIFORM_SIZE['post_objects'][1])
        },
        {
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1]),
            'uniform_item_id': (UNIFORM_ITEM['model'],
                                UNIFORM_ITEM['post_objects'][1]),
            'uniform_size_id': (UNIFORM_SIZE['model'],
                                UNIFORM_SIZE['post_objects'][1])
        }
    ],
    'put_objects': [
        {
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1]),
            'uniform_item_id': (UNIFORM_ITEM['model'],
                                UNIFORM_ITEM['post_objects'][0]),
            'uniform_size_id': (UNIFORM_SIZE['model'],
                                UNIFORM_SIZE['post_objects'][0])
        },
        {
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
            'uniform_item_id': (UNIFORM_ITEM['model'],
                                UNIFORM_ITEM['post_objects'][0]),
            'uniform_size_id': (UNIFORM_SIZE['model'],
                                UNIFORM_SIZE['post_objects'][0])
        }
    ],
    'endpoints': ['uniform_requirement', None, 'uniform_requirements'],
    'user_type': 'test_0'
}

BANK = {
    'resources': [None, None, 'Banks'],
    'model': BankModel,
    'post_objects': [
        {
            'bank_name': 'test_b'
        }
    ],
    'put_objects': [],
    'endpoints': [None, None, 'banks'],
    'user_type': 'test_0'
}

BANK_ACCOUNT = {
    'resources': ['BankAccount', 'ActivateBankAccount', 'BankAccounts'],
    'model': BankAccountModel,
    'post_objects': [
        {
            'account_number': '1234',
            'account_type': 'Corriente',
            'is_active': True,
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
            'bank_id': 1
        },
        {
            'account_number': '1234',
            'account_type': 'Corriente',
            'is_active': True,
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
            'bank_id': 2
        }
    ],
    'put_objects': [
        {
            'account_number': '4321',
            'account_type': 'Ahorro',
            'is_active': False,
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1]),
            'bank_id': 2,
        },
        {
            'account_number': '1234',
            'account_type': 'Corriente',
            'is_active': True,
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
            'bank_id': 1,
        }
    ],
    'endpoints': ['bank_account', 'activate_bank_account', 'bank_accounts'],
    'user_type': 'test_0'
}

FAMILY_RELATION = {
    'resources': [None, None, 'FamilyRelations'],
    'model': FamilyRelationModel,
    'post_objects': [
        {
            'relation_feminine': 'family_relation_f',
            'relation_masculine': 'family_relation_m'
        }
    ],
    'put_objects': [],
    'endpoints': [None, None, 'family_relations'],
    'user_type': 'test_0'
}

DEPENDENT = {
    'resources': ['Dependent', None, 'Dependents'],
    'model': DependentModel,
    'post_objects': [
        {
            'first_name': 'f_n_0',
            'second_name': 's_n_0',
            'first_surname': 'f_sn_0',
            'second_surname': 's_sn_0',
            'gender': 'Mujer',
            'date_of_birth': '2018-01-01',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
            'family_relation_id': 1
        },
        {
            'first_name': 'f_n_1',
            'second_name': 's_n_1',
            'first_surname': 'f_sn_1',
            'second_surname': 's_sn_1',
            'gender': 'Mujer',
            'date_of_birth': '2018-01-01',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
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
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1]),
            'family_relation_id': 2
        }
    ],
    'endpoints': ['dependent', None, 'dependents'],
    'user_type': 'test_0'
}

SCHEDULE = {
    'resources': ['Schedule', None, 'Schedules'],
    'model': ScheduleModel,
    'post_objects': [
        {
            'start_date': '2018-01-01',
            'department_id': (DEPARTMENT['model'],
                              DEPARTMENT['post_objects'][0])
        },
        {
            'start_date': '2018-01-08',
            'department_id': (DEPARTMENT['model'],
                              DEPARTMENT['post_objects'][0])
        },
        {
            'start_date': '2018-01-01',
            'department_id': (DEPARTMENT['model'],
                              DEPARTMENT['post_objects'][1])
        }
    ],
    'put_objects': [
        {
            'start_date': '2018-01-31',
            'department_id': (DEPARTMENT['model'],
                              DEPARTMENT['post_objects'][0])
        },
        {
            'start_date': '2018-01-01',
            'department_id': (DEPARTMENT['model'],
                              DEPARTMENT['post_objects'][0])
        }
    ],
    'endpoints': ['schedule', None, 'schedules'],
    'user_type': 'test_0'
}

SCHEDULE_DETAIL = {
    'resources': ['ScheduleDetail', None, 'ScheduleDetails'],
    'model': ScheduleDetailModel,
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
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
            'schedule_id': (SCHEDULE['model'], SCHEDULE['post_objects'][0])
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
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1]),
            'schedule_id': (SCHEDULE['model'], SCHEDULE['post_objects'][0])
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
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1]),
            'schedule_id': (SCHEDULE['model'], SCHEDULE['post_objects'][0])
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
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
            'schedule_id': (SCHEDULE['model'], SCHEDULE['post_objects'][0])
        }
    ],
    'endpoints': ['schedule_detail', None, 'schedule_details'],
    'user_type': 'test_0'
}

PAYMENT = {
    'resources': ['Payment', None, 'Payments'],
    'model': PaymentModel,
    'post_objects': [
        {
            'payment_date': '2018-01-01',
            'document_number': '1234-abc',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0])
        },
        {
            'payment_date': '2018-01-15',
            'document_number': '4321-abc',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0])
        }
    ],
    'put_objects': [
        {
            'payment_date': '2018-02-01',
            'document_number': '1234-def',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1])
        }
    ],
    'endpoints': ['payment', None, 'payments'],
    'user_type': 'test_0'
}

PAYMENT_DETAIL = {
    'resources': ['PaymentDetail', None, 'PaymentDetails'],
    'model': PaymentDetailModel,
    'post_objects': [
        {
            'payment_type': 'Salario Regular',
            'gross_payment': 1234.56,
            'ss_deduction': 123.45,
            'se_deduction': 12.34,
            'isr_deduction': 1.23,
            'payment_id': (PAYMENT['model'], PAYMENT['post_objects'][0])
        },
        {
            'payment_type': 'Vacación',
            'gross_payment': 234.56,
            'ss_deduction': 23.45,
            'se_deduction': 2.34,
            'isr_deduction': 0.23,
            'payment_id': (PAYMENT['model'], PAYMENT['post_objects'][0])
        }
    ],
    'put_objects': [
        {
            'payment_type': 'Vacación',
            'gross_payment': 2345.67,
            'ss_deduction': 234.56,
            'se_deduction': 23.45,
            'isr_deduction': 2.34,
            'payment_id': (PAYMENT['model'], PAYMENT['post_objects'][1])
        }
    ],
    'endpoints': ['payment_detail', None, 'payment_details'],
    'user_type': 'test_0'
}

CREDITOR = {
    'resources': ['Creditor', 'ActivateCreditor', 'Creditors'],
    'model': CreditorModel,
    'post_objects': [
        {
            'creditor_name': 'test_cr_0',
            'phone_number': '123-4567',
            'email': 'test@test_cr_0.com',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
            'is_active': True
        },
        {
            'creditor_name': 'test_cr_1',
            'phone_number': '123-4567',
            'email': 'test@test_cr_1.com',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
            'is_active': True
        }
    ],
    'put_objects': [
        {
            'creditor_name': 'new_test_cr_0',
            'phone_number': '456-7890',
            'email': 'test@new_test_cr_0.com',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][1]),
            'is_active': False
        },
        {
            'creditor_name': 'test_cr_0',
            'phone_number': '456-7890',
            'email': 'test@new_test_cr_0.com',
            'organization_id': (ORGANIZATION['model'],
                                ORGANIZATION['post_objects'][0]),
            'is_active': True
        }
    ],
    'endpoints': ['creditor', 'activate_creditor', 'creditors'],
    'user_type': 'test_0'
}

DEDUCTION = {
    'resources': ['Deduction', 'ActivateDeduction', 'Deductions'],
    'model': DeductionModel,
    'post_objects': [
        {
            'start_date': '2018-01-01',
            'end_date': '2018-01-31',
            'deduction_per_payment_period': 123.45,
            'payment_method': 'Cheque',
            'deduct_in_december': True,
            'is_active': True,
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
            'creditor_id': (CREDITOR['model'], CREDITOR['post_objects'][0])
        },
        {
            'start_date': '2018-02-01',
            'end_date': '2018-02-28',
            'deduction_per_payment_period': 321.45,
            'payment_method': 'ACH',
            'deduct_in_december': False,
            'is_active': True,
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0]),
            'creditor_id': (CREDITOR['model'], CREDITOR['post_objects'][1])
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
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1]),
            'creditor_id': (CREDITOR['model'], CREDITOR['post_objects'][1])
        }
    ],
    'endpoints': ['deduction', 'activate_deduction', 'deductions'],
    'user_type': 'test_0'
}

DEDUCTION_DETAIL = {
    'resources': ['DeductionDetail', None, 'DeductionDetails'],
    'model': DeductionDetailModel,
    'post_objects': [
        {
            'deducted_amount': 123.45,
            'payment_id': (PAYMENT['model'], PAYMENT['post_objects'][0]),
            'deduction_id': (DEDUCTION['model'], DEDUCTION['post_objects'][0])
        },
        {
            'deducted_amount': 321.45,
            'payment_id': (PAYMENT['model'], PAYMENT['post_objects'][0]),
            'deduction_id': (DEDUCTION['model'], DEDUCTION['post_objects'][1])
        }
    ],
    'put_objects': [
        {
            'deducted_amount': 89.01,
            'payment_id': (PAYMENT['model'], PAYMENT['post_objects'][1]),
            'deduction_id': (DEDUCTION['model'], DEDUCTION['post_objects'][1])
        }
    ],
    'endpoints': ['deduction_detail', None, 'deduction_details'],
    'user_type': 'test_0'
}

ATTENDANCE = {
    'resources': ['Attendance', None, 'Attendances'],
    'model': AttendanceModel,
    'post_objects': [
        {
            'work_day': '2018-01-01',
            'day_start': '2018-01-01T06:00:00',
            'break_start': '2018-01-01T10:00:00',
            'break_end': '2018-01-01T10:30:00',
            'day_end': '2018-01-01T14:00:00',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0])
        },
        {
            'work_day': '2018-01-02',
            'day_start': '2018-01-02T06:00:00',
            'break_start': '2018-01-02T10:00:00',
            'break_end': '2018-01-02T10:30:00',
            'day_end': '2018-01-02T14:00:00',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0])
        }
    ],
    'put_objects': [
        {
            'work_day': '2018-01-03',
            'day_start': '2018-01-03T06:15:00',
            'break_start': '2018-01-03T10:30:00',
            'break_end': '2018-01-03T11:00:00',
            'day_end': '2018-01-03T13:59:00',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][1])
        },
        {
            'work_day': '2018-01-01',
            'day_start': '2018-01-01T06:00:00',
            'break_start': '2018-01-01T10:00:00',
            'break_end': '2018-01-01T10:30:00',
            'day_end': '2018-01-01T14:00:00',
            'employee_id': (EMPLOYEE['model'], EMPLOYEE['post_objects'][0])
        }
    ],
    'endpoints': ['attendance', None, 'attendances'],
    'user_type': 'test_0'
}

CREDENTIALS = {
    'root': {
        'username': 'jfeliu',
        'password': '1234'
    },
    'test_0': {
        'username': 'test_0',
        'password': 'test_p'
    },
    'test_1': {
        'username': 'test_1',
        'password': 'test_p'
    },
    'fake': {
        'username': 'fake_u',
        'password': 'fake_p'
    }
}

OBJECTS_TO_TEST = [ORGANIZATION, USER, DEPARTMENT, MARITAL_STATUS,
                   EMPLOYMENT_POSITION, SHIFT_R, SHIFT_F, EMPLOYEE,
                   HEALTH_PERMIT, EMERGENCY_CONTACT, COUNTRY, PASSPORT,
                   UNIFORM_ITEM, UNIFORM_SIZE, UNIFORM_REQUIREMENT, BANK,
                   BANK_ACCOUNT, FAMILY_RELATION, DEPENDENT, SCHEDULE,
                   SCHEDULE_DETAIL, PAYMENT, PAYMENT_DETAIL, CREDITOR,
                   DEDUCTION, DEDUCTION_DETAIL, ATTENDANCE]


def create_test_user(user_type):
    """
    Create a user in the db and return its credentials.

    :param user_type: String representing the type of user
    :type user_type: str
    :return: Dictionary with the username and password of the
        user that was created
    :rtype: dict
    """
    credentials = CREDENTIALS[user_type]
    org: dict = ORGANIZATION['post_objects'][0]

    if user_type != 'root' and user_type != 'fake':
        # Only add test users to the db since root user is already
        # seeded and fake user should not be able to authenticate.
        if user_type == 'test_1':
            org = ORGANIZATION['post_objects'][1]

        organization_id = get_item_from_db(ORGANIZATION['model'], **org).id

        _ = get_item_from_db(USER['model'], **{
            'username': credentials['username'],
            'password': credentials['password'],
            'password_hash': generate_password_hash(credentials['password']),
            'email': f'{credentials["username"]}@test_o.com',
            'organization_id': organization_id,
            'is_super': user_type == 'super',
            'is_owner': True,
            'is_active': True
        })

    return credentials


@lru_cache(maxsize=256)
def get_item_from_db(model, **kwargs):
    """
    Return an instance of a SQLAlchemy model.

    Returns the instance from the db if it is there.  If not, instantiates a
    new object, saves it to the db, and returns it.

    The results of the function are cache to avoid unnecessary db queries.  The
    cache is cleared at the end of each subtest.

    :param model: The SQLAlchemy model which will be instantiated and returned
    :param kwargs: A dictionary with the information needed to
        instantiate the model
    :type model: db.Model
    :type kwargs: dict
    :returns: An instance of a SQLAlchemy model
    :rtype: db.Model
    """
    # Instances of AppUserModel need to be treated differently because password
    # is needed for instantiation but it is not a column in the model.
    if model is AppUserModel:
        inst = model.query.filter_by(username=kwargs['username']).first()
    else:
        inst = model.query.filter_by(**kwargs).first()

    if inst:
        # Return the instance if item is already in the db.
        return inst

    # Instantiate and save to the db.
    inst = model(**kwargs)
    inst.save_to_db()

    return model.query.filter_by(id=inst.id).first()


def get_object_list(obj_list, num_p):
    if num_p == 'first':
        return [solve_obj_dependencies(obj_list[0])]
    elif num_p == 'all':
        return [solve_obj_dependencies(obj) for obj in obj_list]

    return None


def get_sys_test_params(b_obj, res_type=0, num_post='none', num_put='none',
                        user_type=None):
    """
    Return the parameters needed to run a system test.

    :param b_obj: Object containing the test parameters
    :param res_type: Type of resource being tested (0 for record, 1 for
        activate, 2 for list)
    :param num_post: Number of items from the post_objects list that will
        be returned ('none' will return 0 items, 'first' will return the
        first item, 'all' will return all items)
    :param num_put: Number of items from the put_objects list that will be
        returned ('none' will return 0 items, 'first' will return the
        first item, 'all' will return all items)
    :param user_type: Override the user_type from the b_obj
    :type b_obj: dict
    :type res_type: int
    :type num_post: str
    :type num_put: str
    :type user_type: str
    :return:
        resource (str): Name of the resource being tested.
        model (db.Model): SQLAlchemy model related to the resource.
        required_objects (list): List of business objects that must exist
            in the db prior to running the test.
        post_objects (list): List of objects for testing the post
            method of the resource.
        put_objects (list): List of objects for testing the put
            method of the resource.
        endpoint (str): Endpoint that will receive the request.
        user_type (str): The type of user that will be sending the request.
    """
    resource = b_obj['resources'][res_type]
    model = b_obj['model']
    endpoints = b_obj['endpoints']
    post_objects = get_object_list(b_obj['post_objects'], num_post) \
        if endpoints[0] else None
    put_objects = get_object_list(b_obj['put_objects'], num_put) \
        if endpoints[0] else None
    user = create_test_user(user_type if user_type else b_obj['user_type'])

    return resource, model, post_objects, put_objects, endpoints, user


def get_unit_test_params(b_obj):
    obj_copy = deepcopy(b_obj['post_objects'][0])
    for k, v in obj_copy.items():
        if type(v) == tuple:
            obj_copy[k] = 1

    return b_obj['model'], obj_copy


def solve_obj_dependencies(child_obj):
    """
    Check if an object depends on another object.  If it does, create
    the parent object in the db (if it is not already there) and add the
    parent object's id to a corresponding property in the child object.

    Note:  Parent objects might depend on other object so they are
    recursively sent to this function so their dependencies can
    be resolved.

    :param child_obj: Dictionary representing the child object
    :type child_obj: dict
    :return: A dictionary representing the child object with the references
        to all of its parent's id resolved
    :rtype: dict
    """
    # Make deep copy of the object to avoid modifying the original object
    # since it need to be used in subsequent subtests.
    child_copy = deepcopy(child_obj)

    # Check all properties of the object.
    for k, v in child_copy.items():
        # Parent object are represented by a Tuple, the first element is its
        # SQLAlchemy model and the second element is a dict with the kwargs
        # needed to instantiate the model.
        if type(v) is tuple:
            model, _dict = v
            # Recursively solve any dependencies in the kwargs.
            kwargs = solve_obj_dependencies(_dict)

            # Create and get the parent object.
            parent_obj = get_item_from_db(model, **kwargs)

            # Add the parent's id to the child object.
            child_copy[k] = parent_obj.id

    return child_copy
