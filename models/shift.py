from datetime import time

from db import db
from models.enum import DAYS_OF_WEEK, PAYMENT_PERIOD
from models.mixin import ModelsMixin


class ShiftModel(ModelsMixin, db.Model):
    __tablename__ = 'shift'

    id = db.Column(db.Integer, primary_key=True)
    shift_name = db.Column(db.String(80), nullable=False)
    weekly_hours = db.Column(db.Numeric(3, 1), nullable=False)
    is_rotating = db.Column(db.Boolean, nullable=False)
    payment_period = db.Column(PAYMENT_PERIOD, nullable=False)
    rotation_start_hour = db.Column(db.Time)
    rotation_end_hour = db.Column(db.Time)
    break_length = db.Column(db.Integer, nullable=False)
    is_break_included_in_shift = db.Column(db.Boolean, nullable=False)
    fixed_start_hour_monday = db.Column(db.Time)
    fixed_start_break_hour_monday = db.Column(db.Time)
    fixed_end_break_hour_monday = db.Column(db.Time)
    fixed_end_hour_monday = db.Column(db.Time)
    fixed_start_hour_tuesday = db.Column(db.Time)
    fixed_start_break_hour_tuesday = db.Column(db.Time)
    fixed_end_break_hour_tuesday = db.Column(db.Time)
    fixed_end_hour_tuesday = db.Column(db.Time)
    fixed_start_hour_wednesday = db.Column(db.Time)
    fixed_start_break_hour_wednesday = db.Column(db.Time)
    fixed_end_break_hour_wednesday = db.Column(db.Time)
    fixed_end_hour_wednesday = db.Column(db.Time)
    fixed_start_hour_thursday = db.Column(db.Time)
    fixed_start_break_hour_thursday = db.Column(db.Time)
    fixed_end_break_hour_thursday = db.Column(db.Time)
    fixed_end_hour_thursday = db.Column(db.Time)
    fixed_start_hour_friday = db.Column(db.Time)
    fixed_start_break_hour_friday = db.Column(db.Time)
    fixed_end_break_hour_friday = db.Column(db.Time)
    fixed_end_hour_friday = db.Column(db.Time)
    fixed_start_hour_saturday = db.Column(db.Time)
    fixed_start_break_hour_saturday = db.Column(db.Time)
    fixed_end_break_hour_saturday = db.Column(db.Time)
    fixed_end_hour_saturday = db.Column(db.Time)
    fixed_start_hour_sunday = db.Column(db.Time)
    fixed_start_break_hour_sunday = db.Column(db.Time)
    fixed_end_break_hour_sunday = db.Column(db.Time)
    fixed_end_hour_sunday = db.Column(db.Time)
    rest_day = db.Column(DAYS_OF_WEEK)
    is_active = db.Column(db.Boolean, nullable=False)
    organization_id = db.Column(db.Integer,
                                db.ForeignKey('organization.id'),
                                nullable=False, index=True)

    def __init__(self, shift_name, weekly_hours, is_rotating,
                 payment_period, break_length, is_break_included_in_shift,
                 is_active, organization_id, **kwargs):
        self.shift_name = shift_name
        self.weekly_hours = weekly_hours
        self.is_rotating = is_rotating
        self.payment_period = payment_period
        self.break_length = break_length
        self.is_break_included_in_shift = is_break_included_in_shift
        self.is_active = is_active
        self.organization_id = organization_id

        if self.is_rotating:
            self.rotation_start_hour = kwargs.get('rotation_start_hour',
                                                  time(0))
            self.rotation_end_hour = kwargs.get('rotation_end_hour',
                                                time(12, 59, 59))
        else:
            self.fixed_start_hour_monday = kwargs.get(
                'fixed_start_hour_monday')
            self.fixed_start_break_hour_monday = kwargs.get(
                'fixed_start_break_hour_monday')
            self.fixed_end_break_hour_monday = kwargs.get(
                'fixed_end_break_hour_monday')
            self.fixed_end_hour_monday = kwargs.get(
                'fixed_end_hour_monday')

            self.fixed_start_hour_tuesday = kwargs.get(
                'fixed_start_hour_tuesday')
            self.fixed_start_break_hour_tuesday = kwargs.get(
                'fixed_start_break_hour_tuesday')
            self.fixed_end_break_hour_tuesday = kwargs.get(
                'fixed_end_break_hour_tuesday')
            self.fixed_end_hour_tuesday = kwargs.get(
                'fixed_end_hour_tuesday')

            self.fixed_start_hour_wednesday = kwargs.get(
                'fixed_start_hour_wednesday')
            self.fixed_start_break_hour_wednesday = kwargs.get(
                'fixed_start_break_hour_wednesday')
            self.fixed_end_break_hour_wednesday = kwargs.get(
                'fixed_end_break_hour_wednesday')
            self.fixed_end_hour_wednesday = kwargs.get(
                'fixed_end_hour_wednesday')

            self.fixed_start_hour_thursday = kwargs.get(
                'fixed_start_hour_thursday')
            self.fixed_start_break_hour_thursday = kwargs.get(
                'fixed_start_break_hour_thursday')
            self.fixed_end_break_hour_thursday = kwargs.get(
                'fixed_end_break_hour_thursday')
            self.fixed_end_hour_thursday = kwargs.get(
                'fixed_end_hour_thursday')

            self.fixed_start_hour_friday = kwargs.get(
                'fixed_start_hour_friday')
            self.fixed_start_break_hour_friday = kwargs.get(
                'fixed_start_break_hour_friday')
            self.fixed_end_break_hour_friday = kwargs.get(
                'fixed_end_break_hour_friday')
            self.fixed_end_hour_friday = kwargs.get(
                'fixed_end_hour_friday')

            self.fixed_start_hour_saturday = kwargs.get(
                'fixed_start_hour_saturday')
            self.fixed_start_break_hour_saturday = kwargs.get(
                'fixed_start_break_hour_saturday')
            self.fixed_end_break_hour_saturday = kwargs.get(
                'fixed_end_break_hour_saturday')
            self.fixed_end_hour_saturday = kwargs.get(
                'fixed_end_hour_saturday')

            self.fixed_start_hour_sunday = kwargs.get(
                'fixed_start_hour_sunday')
            self.fixed_start_break_hour_sunday = kwargs.get(
                'fixed_start_break_hour_sunday')
            self.fixed_end_break_hour_sunday = kwargs.get(
                'fixed_end_break_hour_sunday')
            self.fixed_end_hour_sunday = kwargs.get(
                'fixed_end_hour_sunday')

            self.rest_day = kwargs.get('rest_day')

    @classmethod
    def find_by_name(cls, shift_name, organization_id):
        return cls.query.filter_by(shift_name=shift_name,
                                   organization_id=organization_id).first()
