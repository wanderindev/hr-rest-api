from db import db

ACCOUNT_TYPE = db.Enum('Ahorro', 'Corriente', name='account_type')

DAYS_OF_WEEK = db.Enum('Lunes', 'Martes', 'Miércoles', 'Jueves',
                       'Viernes', 'Sábado', 'Domingo',
                       name='days_of_week')

GENDER = db.Enum('Mujer', 'Hombre', name='gender')

HEALTH_PERMIT_TYPE = db.Enum('Blanco', 'Verde', name='health_permit_type')

PAYMENT_METHOD = db.Enum('Efectivo', 'Cheque', 'ACH', name='payment_method')

PAYMENT_PERIOD = db.Enum('Diario', 'Semanal', 'Bisemanal',
                         'Quincenal', 'Mensual',
                         name='payment_period')

PAYMENT_TYPE = db.Enum('Salario Regular', 'Sobre Tiempo', 'Vacación',
                       'XIII Mes', 'Bonificación', 'Prima de Antigüedad',
                       'Indemnización', 'Prima de Producción',
                       'Gasto de Representación', name='payment_type')

TERMINATION_REASON = db.Enum('Renuncia', 'Período de Prueba',
                             'Expiración de Contrato',
                             'Despido Causa Justificada', 'Abandono de Trabajo',
                             name='termination_reason')

TYPE_OF_CONTRACT = db.Enum('Definido', 'Indefinido', name='type_of_contract')
