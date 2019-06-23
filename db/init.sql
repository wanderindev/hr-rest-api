CREATE USER hr_user WITH PASSWORD 'pass';

CREATE DATABASE hr_dev;

GRANT ALL PRIVILEGES ON DATABASE hr_dev TO hr_user;

\connect hr_dev hr_user

CREATE TYPE PAYMENT_METHOD AS ENUM ('Efectivo', 'Cheque', 'ACH');

CREATE TYPE PAYMENT_PERIOD AS ENUM ('Diario', 'Semanal', 'Bisemanal', 'Quincenal', 'Mensual');

CREATE TYPE DAYS_OF_WEEK AS ENUM ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo');

CREATE TYPE GENDER AS ENUM ('Mujer', 'Hombre');

CREATE TYPE TYPE_OF_CONTRACT AS ENUM ('Definido', 'Indefinido');

CREATE TYPE TERMINATION_REASON AS ENUM ('Renuncia', 'Período de Prueba', 'Expiración de Contrato', 'Despido Causa Justificada', 'Abandono de Trabajo');

CREATE TYPE ACCOUNT_TYPE AS ENUM ('Ahorro', 'Corriente');

CREATE TYPE HEALTH_PERMIT_TYPE AS ENUM ('Blanco', 'Verde');

CREATE TYPE PAYMENT_TYPE AS ENUM ('Salario Regular', 'Sobre Tiempo', 'Vacación', 'XIII Mes', 'Bonificación', 'Prima de Antigüedad', 'Indemnización', 'Prima de Producción', 'Gasto de Representación');

CREATE TYPE ATT_TYPE AS ENUM ('in', 'out');

CREATE TABLE organization
(
  id                SERIAL               NOT NULL
    CONSTRAINT organization_pkey
    PRIMARY KEY,
  organization_name VARCHAR(80)          NOT NULL,
  is_active         BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE app_user
(
  id              SERIAL                NOT NULL
    CONSTRAINT app_user_pkey
    PRIMARY KEY,
  organization_id INTEGER               NOT NULL
    CONSTRAINT app_user_organization__fk
    REFERENCES organization,
  username        VARCHAR(80)                                      NOT NULL,
  password_hash   VARCHAR(128)                                     NOT NULL,
  email           VARCHAR(80)                                      NOT NULL,
  is_owner        BOOLEAN DEFAULT FALSE                            NOT NULL,
  is_active       BOOLEAN DEFAULT TRUE                             NOT NULL,
  is_super        BOOLEAN DEFAULT FALSE                            NOT NULL,
  created_on      TIMESTAMP DEFAULT timezone('utc' :: TEXT, now()) NOT NULL,
  current_login   TIMESTAMP,
  last_login      TIMESTAMP,
  login_count     INTEGER DEFAULT 0
);

CREATE TABLE department
(
  id              SERIAL               NOT NULL
    CONSTRAINT department_pkey
    PRIMARY KEY,
  organization_id INTEGER              NOT NULL
    CONSTRAINT department_organization__fk
    REFERENCES organization,
  department_name VARCHAR(80)          NOT NULL,
  is_active       BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE marital_status
(
  id               SERIAL      NOT NULL
    CONSTRAINT marital_status_id_pk
    PRIMARY KEY,
  status_feminine  VARCHAR(25) NOT NULL,
  status_masculine VARCHAR(25) NOT NULL
);

CREATE TABLE employment_position
(
  id                      SERIAL      NOT NULL
    CONSTRAINT position_pkey
    PRIMARY KEY,
  organization_id         INTEGER     NOT NULL
    CONSTRAINT position_organization__fk
    REFERENCES organization,
  position_name_feminine  VARCHAR(80) NOT NULL,
  position_name_masculine VARCHAR(80) NOT NULL,
  minimum_hourly_wage     NUMERIC(8, 4),
  is_active               BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE shift
(
  id                               SERIAL               NOT NULL
    CONSTRAINT shift_pkey
    PRIMARY KEY,
  organization_id                  INTEGER              NOT NULL
    CONSTRAINT shift_organization__fk
    REFERENCES organization,
  shift_name                       VARCHAR(80)          NOT NULL,
  weekly_hours                     NUMERIC(3, 1)        NOT NULL,
  is_rotating                      BOOLEAN DEFAULT TRUE NOT NULL,
  payment_period                   PAYMENT_PERIOD       NOT NULL,
  rotation_start_hour              TIME,
  rotation_end_hour                TIME,
  break_length                     TIME                 NOT NULL,
  is_break_included_in_shift       BOOLEAN DEFAULT TRUE NOT NULL,
  fixed_start_hour_monday          TIME,
  fixed_start_break_hour_monday    TIME,
  fixed_end_break_hour_monday      TIME,
  fixed_end_hour_monday            TIME,
  fixed_start_hour_tuesday         TIME,
  fixed_start_break_hour_tuesday   TIME,
  fixed_end_break_hour_tuesday     TIME,
  fixed_end_hour_tuesday           TIME,
  fixed_start_hour_wednesday       TIME,
  fixed_start_break_hour_wednesday TIME,
  fixed_end_break_hour_wednesday   TIME,
  fixed_end_hour_wednesday         TIME,
  fixed_start_hour_thursday        TIME,
  fixed_start_break_hour_thursday  TIME,
  fixed_end_break_hour_thursday    TIME,
  fixed_end_hour_thursday          TIME,
  fixed_start_hour_friday          TIME,
  fixed_start_break_hour_friday    TIME,
  fixed_end_break_hour_friday      TIME,
  fixed_end_hour_friday            TIME,
  fixed_start_hour_saturday        TIME,
  fixed_start_break_hour_saturday  TIME,
  fixed_end_break_hour_saturday    TIME,
  fixed_end_hour_saturday          TIME,
  fixed_start_hour_sunday          TIME,
  fixed_start_break_hour_sunday    TIME,
  fixed_end_break_hour_sunday      TIME,
  fixed_end_hour_sunday            TIME,
  rest_day                         DAYS_OF_WEEK,
  is_active                        BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE employee
(
  id                                         SERIAL                  NOT NULL
    CONSTRAINT employee_pkey
    PRIMARY KEY,
  marital_status_id                          INTEGER                 NOT NULL
    CONSTRAINT employee_marital_status__fk
    REFERENCES marital_status,
  department_id                              INTEGER                 NOT NULL
    CONSTRAINT employee_department__fk
    REFERENCES department,
  position_id                                INTEGER                 NOT NULL
    CONSTRAINT employee_position__fk
    REFERENCES employment_position,
  shift_id                                   INTEGER                 NOT NULL
    CONSTRAINT employee_shift__fk
    REFERENCES shift,
  first_name                                 VARCHAR(40)             NOT NULL,
  second_name                                VARCHAR(40),
  first_surname                              VARCHAR(40)             NOT NULL,
  second_surname                             VARCHAR(40),
  national_id_number                         VARCHAR(20),
  is_panamanian                              BOOLEAN DEFAULT TRUE    NOT NULL,
  date_of_birth                              DATE                    NOT NULL,
  gender                                     GENDER                  NOT NULL,
  address                                    VARCHAR(300)            NOT NULL,
  home_phone                                 VARCHAR(10),
  mobile_phone                               VARCHAR(10),
  email                                      VARCHAR(50),
  type_of_contract                           TYPE_OF_CONTRACT        NOT NULL,
  employment_date                            DATE                    NOT NULL,
  contract_expiration_date                   DATE,
  termination_date                           DATE,
  termination_reason                         TERMINATION_REASON,
  salary_per_payment_period                  NUMERIC(7, 2)           NOT NULL,
  representation_expenses_per_payment_period NUMERIC(7, 2) DEFAULT 0 NOT NULL,
  payment_method                             PAYMENT_METHOD          NOT NULL,
  is_active                                  BOOLEAN                 NOT NULL
);

CREATE TABLE emergency_contact
(
  id           SERIAL      NOT NULL
    CONSTRAINT emergency_contact_pkey
    PRIMARY KEY,
  employee_id  INTEGER     NOT NULL
    CONSTRAINT emergency_contact_employee__fk
    REFERENCES employee,
  first_name   VARCHAR(40) NOT NULL,
  last_name    VARCHAR(40) NOT NULL,
  home_phone   VARCHAR(10),
  work_phone   VARCHAR(10),
  mobile_phone VARCHAR(10)
);


CREATE TABLE health_permit
(
  id                 SERIAL                 NOT NULL
    CONSTRAINT health_permit_pkey
    PRIMARY KEY,
  employee_id        INTEGER                NOT NULL
    CONSTRAINT health_permit_employee__fk
    REFERENCES employee,
  health_permit_type HEALTH_PERMIT_TYPE     NOT NULL,
  issue_date         DATE                   NOT NULL,
  expiration_date    DATE                   NOT NULL
);

CREATE TABLE country
(
  id           SERIAL      NOT NULL
    CONSTRAINT country_pkey
    PRIMARY KEY,
  country_name VARCHAR(80) NOT NULL,
  nationality  VARCHAR(80) NOT NULL
);

CREATE TABLE passport
(
  id              SERIAL      NOT NULL
    CONSTRAINT passport_pkey
    PRIMARY KEY,
  employee_id     INTEGER     NOT NULL
    CONSTRAINT passport_employee__fk
    REFERENCES employee,
  country_id      INTEGER     NOT NULL
    CONSTRAINT passport_country__fk
    REFERENCES country,
  passport_number VARCHAR(40) NOT NULL,
  issue_date      DATE        NOT NULL,
  expiration_date DATE        NOT NULL
);

CREATE TABLE uniform_item
(
  id              SERIAL      NOT NULL
    CONSTRAINT uniform_item_pkey
    PRIMARY KEY,
  organization_id INTEGER     NOT NULL
    CONSTRAINT uniform_item_organization__fk
    REFERENCES organization,
  item_name       VARCHAR(80) NOT NULL
);

CREATE TABLE uniform_size
(
  id               SERIAL      NOT NULL
    CONSTRAINT uniform_size_id_pk
    PRIMARY KEY,
  uniform_item_id  INTEGER     NOT NULL
    CONSTRAINT uniform_size_uniform_item__fk
    REFERENCES uniform_item,
  size_description VARCHAR(20) NOT NULL
);

CREATE TABLE uniform_requirement
(
  id              SERIAL  NOT NULL
    CONSTRAINT uniform_requirement_pkey
    PRIMARY KEY,
  employee_id     INTEGER NOT NULL
    CONSTRAINT uniform_requirement_employee__fk
    REFERENCES employee,
  uniform_item_id INTEGER NOT NULL
    CONSTRAINT uniform_requirement_uniform_item__fk
    REFERENCES uniform_item,
  uniform_size_id INTEGER NOT NULL
    CONSTRAINT uniform_requirement_uniform_size__fk
    REFERENCES uniform_size
);

CREATE TABLE bank
(
  id        SERIAL      NOT NULL
    CONSTRAINT bank_pkey
    PRIMARY KEY,
  bank_name VARCHAR(80) NOT NULL
);

CREATE TABLE bank_account
(
  id             SERIAL               NOT NULL
    CONSTRAINT bank_account_pkey
    PRIMARY KEY,
  employee_id    INTEGER              NOT NULL
    CONSTRAINT bank_account_employee__fk
    REFERENCES employee,
  bank_id        INTEGER              NOT NULL
    CONSTRAINT bank_account_bank__fk
    REFERENCES bank,
  account_number VARCHAR(50)          NOT NULL,
  account_type   ACCOUNT_TYPE         NOT NULL,
  is_active      BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE family_relation
(
  id                 SERIAL      NOT NULL
    CONSTRAINT family_relation_pkey
    PRIMARY KEY,
  relation_feminine  VARCHAR(25) NOT NULL,
  relation_masculine VARCHAR(25) NOT NULL
);

CREATE TABLE dependent
(
  id                 SERIAL      NOT NULL
    CONSTRAINT dependent_pkey
    PRIMARY KEY,
  family_relation_id INTEGER     NOT NULL
    CONSTRAINT dependent_family_relation__fk
    REFERENCES family_relation,
  employee_id        INTEGER     NOT NULL
    CONSTRAINT dependent_employee__fk
    REFERENCES employee,
  first_name         VARCHAR(40) NOT NULL,
  second_name        VARCHAR(40),
  first_surname      VARCHAR(40) NOT NULL,
  second_surname     VARCHAR(40),
  gender             GENDER      NOT NULL,
  date_of_birth      DATE
);

CREATE TABLE schedule
(
  id            SERIAL  NOT NULL
    CONSTRAINT schedule_pkey
    PRIMARY KEY,
  department_id INTEGER NOT NULL
    CONSTRAINT schedule_department__fk
    REFERENCES department,
  start_date    DATE    NOT NULL
);

CREATE TABLE schedule_detail
(
  id               SERIAL  NOT NULL
    CONSTRAINT schedule_detail_pkey
    PRIMARY KEY,
  schedule_id      INTEGER NOT NULL
    CONSTRAINT schedule_detail_schedule__fk
    REFERENCES schedule,
  employee_id      INTEGER NOT NULL
    CONSTRAINT schedule_detail_employee__fk
    REFERENCES employee,
  day_1_start      TIMESTAMP,
  day_1_end        TIMESTAMP,
  day_1_comment    VARCHAR(40),
  day_2_start      TIMESTAMP,
  day_2_end        TIMESTAMP,
  day_2_comment    VARCHAR(40),
  day_3_start      TIMESTAMP,
  day_3_end        TIMESTAMP,
  day_3_comment    VARCHAR(40),
  day_4_start      TIMESTAMP,
  day_4_end        TIMESTAMP,
  day_4_comment    VARCHAR(40),
  day_5_start      TIMESTAMP,
  day_5_end        TIMESTAMP,
  day_5_comment    VARCHAR(40),
  day_6_start      TIMESTAMP,
  day_6_end        TIMESTAMP,
  day_6_comment    VARCHAR(40),
  day_7_start      TIMESTAMP,
  day_7_end        TIMESTAMP,
  day_7_comment    VARCHAR(40)
);

CREATE TABLE payment
(
  id              SERIAL      NOT NULL
    CONSTRAINT payment_pkey
    PRIMARY KEY,
  employee_id     INTEGER     NOT NULL
    CONSTRAINT payment_employee__fk
    REFERENCES employee,
  payment_date    DATE        NOT NULL,
  document_number VARCHAR(40)
);

CREATE TABLE payment_detail
(
  id            SERIAL        NOT NULL
    CONSTRAINT payment_detail_pkey
    PRIMARY KEY,
  payment_id    INTEGER       NOT NULL
    CONSTRAINT payment_detail_payment__fk
    REFERENCES payment,
  payment_type  PAYMENT_TYPE  NOT NULL,
  gross_payment NUMERIC(7, 2) NOT NULL,
  ss_deduction  NUMERIC(7, 2),
  se_deduction  NUMERIC(7, 2),
  isr_deduction NUMERIC(7, 2)
);

CREATE TABLE creditor
(
  id              SERIAL      NOT NULL
    CONSTRAINT creditor_pkey
    PRIMARY KEY,
  organization_id INTEGER     NOT NULL
    CONSTRAINT creditor_organization__fk
    REFERENCES organization,
  creditor_name   VARCHAR(80) NOT NULL,
  phone_number    VARCHAR(10),
  email           VARCHAR(50),
  is_active       BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE deduction
(
  id                           SERIAL               NOT NULL
    CONSTRAINT deduction_pkey
    PRIMARY KEY,
  employee_id                  INTEGER              NOT NULL
    CONSTRAINT deduction_employee__fk
    REFERENCES employee,
  creditor_id                  INTEGER              NOT NULL
    CONSTRAINT deduction_creditor__fk
    REFERENCES creditor,
  start_date                   DATE                 NOT NULL,
  end_date                     DATE,
  deduction_per_payment_period NUMERIC(7, 2)        NOT NULL,
  payment_method               PAYMENT_METHOD       NOT NULL,
  deduct_in_december           BOOLEAN              NOT NULL,
  is_active                    BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE deduction_detail
(
  id              SERIAL        NOT NULL
    CONSTRAINT deduction_detail_pkey
    PRIMARY KEY,
  deduction_id    INTEGER       NOT NULL
    CONSTRAINT deduction_detail_deduction__fk
    REFERENCES deduction,
  payment_id      INTEGER       NOT NULL
    CONSTRAINT deduction_detail_payment__fk
    REFERENCES payment,
  deducted_amount NUMERIC(7, 2) NOT NULL
);

CREATE TABLE attendance
(
  id                           SERIAL  NOT NULL
    CONSTRAINT attendance_pkey
    PRIMARY KEY,
  employee_id                  INTEGER NOT NULL
    CONSTRAINT attendance_employee__fk
    REFERENCES employee,
  work_day                     DATE    NOT NULL,
  day_start                    TIMESTAMP,
  break_start                  TIMESTAMP,
  break_end                    TIMESTAMP,
  day_end                      TIMESTAMP
);

CREATE TABLE raw_attendance
(
  id                           SERIAL  NOT NULL
    CONSTRAINT raw_attendance_pkey
    PRIMARY KEY,
  stgid                        VARCHAR(20)           NOT NULL,
  userid                       INTEGER               NOT NULL,
  att_time                     BIGINT                NOT NULL,
  att_type                     ATT_TYPE              NOT NULL,
  was_processed                BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE sick_note
(
  id                        SERIAL                                           NOT NULL
    CONSTRAINT sick_note_pkey
    PRIMARY KEY,
  employee_id               INTEGER                                          NOT NULL
    CONSTRAINT sick_note_employee__fk
    REFERENCES employee,
  sick_note_date            DATE                                             NOT NULL,
  number_of_hours_requested NUMERIC(5, 2)                                    NOT NULL,
  number_of_hours_approved  NUMERIC(5, 2)                                    NOT NULL,
  date_received             DATE                                             NOT NULL
);

CREATE TABLE absence_authorization
(
  id                         SERIAL                                           NOT NULL
    CONSTRAINT absence_authorization_pkey
    PRIMARY KEY,
  employee_id                INTEGER
    CONSTRAINT absence_authorization_employee__fk
    REFERENCES employee,
  absence_date               DATE                                             NOT NULL,
  absence_reason             VARCHAR(200)                                     NOT NULL,
  is_payment_authorized      BOOLEAN DEFAULT FALSE,
  authorization_request_date DATE                                             NOT NULL
);

CREATE INDEX absence_authorization_employee_id_index
  ON public.absence_authorization (employee_id);

CREATE UNIQUE INDEX absence_authorization_employee_id_absence_date_uindex
  ON absence_authorization (employee_id, absence_date);

CREATE INDEX app_user_organization_id_index
  ON public.app_user (organization_id);

CREATE UNIQUE INDEX app_user_username_uindex
  ON app_user (username);

CREATE UNIQUE INDEX app_user_email_uindex
  ON app_user (email);

CREATE INDEX attendance_employee_id_index
  ON public.attendance (employee_id);

CREATE UNIQUE INDEX attendance_employee_id_work_day_uindex
  ON attendance (employee_id, work_day);

CREATE INDEX bank_bank_name_index
  ON public.bank (bank_name);

CREATE INDEX bank_account_employee_id_index
  ON public.bank_account (employee_id);

CREATE UNIQUE INDEX bank_account_account_number_employee_id_bank_id_uindex
  ON bank_account (account_number, employee_id, bank_id);

CREATE INDEX country_country_name_index
  ON public.country (country_name);

CREATE INDEX creditor_organization_id_index
  ON public.creditor (organization_id);

CREATE UNIQUE INDEX creditor_creditor_name_organization_id_uindex
  ON creditor (creditor_name, organization_id);

CREATE INDEX deduction_employee_id_index
  ON public.deduction (employee_id);

CREATE INDEX deduction_creditor_id_index
  ON public.deduction (creditor_id);

CREATE INDEX deduction_detail_deduction_id_index
  ON public.deduction_detail (deduction_id);

CREATE INDEX deduction_detail_payment_id_index
  ON public.deduction_detail (payment_id);

CREATE INDEX department_organization_id_index
  ON public.department (organization_id);

CREATE UNIQUE INDEX department_department_name_organization_id_uindex
  ON department (department_name, organization_id);

CREATE INDEX dependent_employee_id_index
  ON public.dependent (employee_id);

CREATE INDEX emergency_contact_employee_id_index
  ON public.emergency_contact (employee_id);

CREATE INDEX employee_department_id_index
  ON public.employee (department_id);

CREATE INDEX employee_position_id_index
  ON public.employee (position_id);

CREATE INDEX employee_first_name_first_surname_index
  ON public.employee (first_name, first_surname);

CREATE INDEX employee_is_active_index
  ON public.employee (is_active);

CREATE INDEX employment_position_organization_id_index
  ON public.employment_position (organization_id);

CREATE UNIQUE INDEX employment_position_p_name_feminine_organization_id_uindex
  ON employment_position (position_name_feminine, organization_id);

CREATE UNIQUE INDEX employment_position_p_name_masculine_organization_id_uindex
  ON employment_position (position_name_masculine, organization_id);

CREATE INDEX health_permit_employee_id_index
  ON public.health_permit (employee_id);

CREATE UNIQUE INDEX organization_organization_name_uindex
  ON organization (organization_name);

CREATE INDEX passport_employee_id_index
  ON public.passport (employee_id);

CREATE INDEX payment_employee_id_index
  ON public.payment (employee_id);

CREATE INDEX payment_detail_payment_id_index
  ON public.payment_detail (payment_id);

CREATE INDEX raw_attendance_userid_was_processed_index
  ON public.raw_attendance (userid, was_processed);

CREATE UNIQUE INDEX schedule_department_id_start_date_uindex
  ON public.schedule (department_id, start_date);

CREATE INDEX schedule_detail_schedule_id_index
  ON public.schedule_detail (schedule_id);

CREATE INDEX schedule_detail_employee_id_index
  ON public.schedule_detail (employee_id);

CREATE UNIQUE INDEX schedule_detail_employee_id_schedule_id_uindex
  ON public.schedule_detail (employee_id, employee_id);

CREATE INDEX shift_organization_id_index
  ON public.shift (organization_id);

CREATE UNIQUE INDEX shift_shift_name_organization_id_uindex
  ON shift (shift_name, organization_id);

CREATE INDEX sick_note_employee_id_index
  ON public.sick_note (employee_id);

CREATE INDEX uniform_item_organization_id_index
  ON public.uniform_item (organization_id);

CREATE UNIQUE INDEX uniform_item_item_name_organization_id_uindex
  ON uniform_item (item_name, organization_id);

CREATE INDEX uniform_requirement_employee_id_index
  ON public.uniform_requirement (employee_id);

CREATE INDEX uniform_size_uniform_item_id_index
  ON public.uniform_size (uniform_item_id);

CREATE UNIQUE INDEX uniform_requirement_employee_id_uniform_item_id_uindex
  ON uniform_requirement (employee_id, uniform_item_id);

CREATE UNIQUE INDEX uniform_size_size_description_uniform_item_id_uindex
  ON uniform_size (size_description, uniform_item_id);

INSERT INTO organization (organization_name, is_active) VALUES
  ('Nuvanz', TRUE);

INSERT INTO app_user (organization_id, username, password_hash, email, is_owner, is_active, is_super) VALUES
  (1,
   'nuvanz',
   'pbkdf2:sha256:50000$m2iazcdk$19e47588ec28c7d519a4f4aff58804573dbf70b9764059beb0915a9ca6a1bfd6',
   'support@nuvanz.com',
   TRUE,
   TRUE,
   TRUE);

INSERT INTO marital_status (status_feminine, status_masculine) VALUES
  ('Soltera', 'Soltero'),
  ('Unida', 'Unido'),
  ('Casada', 'Casado'),
  ('Divorciada', 'Divorciado'),
  ('Viuda', 'Viudo');

INSERT INTO country (country_name, nationality) VALUES
  ('Argentina', 'argentina'),
  ('Brasil', 'brasileña'),
  ('Canadá', 'canadiense'),
  ('Chile', 'chilena'),
  ('Colombia', 'colombiana'),
  ('Costa Rica', 'costarricence'),
  ('Ecuador', 'ecuatoriana'),
  ('El Salvador', 'salvadoreña'),
  ('Guatemala', 'guatemalteca'),
  ('Honduras', 'hodureña'),
  ('México', 'mexicana'),
  ('Nicaragua', 'nicaragüense'),
  ('Paraguay', 'paraguaya'),
  ('Perú', 'peruana'),
  ('República Dominicana', 'dominicana'),
  ('Uruguay', 'uruguaya'),
  ('Venezuela', 'venezolana');

INSERT INTO bank (bank_name) VALUES
  ('AllBank'),
  ('BAC – Credomatic'),
  ('Banco Aliado'),
  ('Banco Azteca'),
  ('Banco BAC de Panama'),
  ('Banco Canal Bank'),
  ('Banco Delta'),
  ('Banco Ficohsa'),
  ('Banco General'),
  ('Banco Internacional de Costa Rica'),
  ('Banco Lafise'),
  ('Banco Nacional de Panamá'),
  ('Banco Panama'),
  ('Banco Panameño de la Vivienda'),
  ('Banco Pichincha'),
  ('Bancolombia'),
  ('Banesco'),
  ('Banisi'),
  ('Banistmo'),
  ('BBP Bank'),
  ('BCT Bank'),
  ('BI Bank'),
  ('Cacechi'),
  ('Caja de Ahorros'),
  ('Capital Bank'),
  ('Citibank N.A.'),
  ('COEDUCO'),
  ('COOESAN'),
  ('COOPEDUC'),
  ('Cooperativa Cristobal'),
  ('Cooperativa Profesionales R.L.'),
  ('COOPEVE'),
  ('Credicorp Bank'),
  ('Davivienda'),
  ('FPB Bank'),
  ('Global Bank'),
  ('Mercantil Bank'),
  ('Metro Bank'),
  ('MMG Bank'),
  ('Multibank'),
  ('Prival Bank'),
  ('Scotia Bank'),
  ('Scotiabank Transformandose'),
  ('St. Georges Bank'),
  ('Towerbank Int.'),
  ('Uni Bank & Trust Inc.');

INSERT INTO family_relation (relation_feminine, relation_masculine) VALUES
  ('Hija', 'Hijo'),
  ('Madre', 'Padre'),
  ('Esposa', 'Esposo'),
  ('Nieta', 'Nieto'),
  ('Abuela', 'Abuelo'),
  ('Hermana', 'Hermano');

\connect postgres postgres

CREATE DATABASE hr_test TEMPLATE hr_dev;

GRANT ALL PRIVILEGES ON DATABASE hr_test TO hr_user;