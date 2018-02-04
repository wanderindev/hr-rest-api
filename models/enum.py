from db import db

PAYMENT_PERIOD = db.Enum('Diario', 'Semanal', 'Bisemanal',
                         'Quincenal', 'Mensual',
                         name='payment_period')

DAYS_OF_WEEK = db.Enum('Lunes', 'Martes', 'Miércoles', 'Jueves',
                       'Viernes', 'Sábado', 'Domingo',
                       name='days_of_week')