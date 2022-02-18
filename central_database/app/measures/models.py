from __future__ import annotations
import logging
from copy import deepcopy

from django.db import models

from rest_framework.exceptions import NotFound

from app.base_models import CDPModel
from app.patients.models import Patient
from app.encounters.models import Encounter


logger = logging.getLogger('logger')


class MeasureType(CDPModel, models.Model):
    '''
    Type of data that is measured
    '''
    name = models.CharField(max_length=40, unique=True)
    unique_id = models.CharField(
        max_length=40, unique=True, blank=True, null=True,
        help_text='code of a code system that identifies the MeasureType inter-systems.'
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name', 'unique_id']),
            models.Index(fields=['unique_id', 'name']),
        ]

    def __str__(self):
        return f'MeasureType [{self.name}] with unique_id={self.unique_id}'


class MeasureUnit(CDPModel, models.Model):
    '''
    Unit of data that is measured
    '''
    name = models.CharField(max_length=40, unique=True)
    unique_id = models.CharField(
        max_length=40, unique=True,
        help_text='code of a code system that identifies the MeasureUnit inter-systems.'
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name', 'unique_id']),
            models.Index(fields=['unique_id', 'name']),
        ]

    def __str__(self):
        return f'Unit [{self.name}] with unique_id={self.unique_id}'


class Measure(CDPModel, models.Model):
    '''
    The measure that is stored
    '''
    UNIT_CONVERSIONS = {
        ('m', 'cm'): lambda x: 100 * x,
        ('cm', 'm'): lambda x: (1/100) * x
    }

    date = models.DateTimeField(blank=True, null=True)
    value = models.FloatField()
    measure_type = models.ForeignKey(MeasureType, related_name='measures', on_delete=models.PROTECT)
    measure_unit = models.ForeignKey(MeasureUnit, related_name='measures', on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='measures')

    class Meta:
        ordering = ['patient__id', 'measure_type__id', 'date']
        indexes = [
            models.Index(fields=['patient', 'measure_type', 'date', 'value']),
            models.Index(fields=['measure_type', 'date', 'patient', 'value']),
            models.Index(fields=['date', 'patient', 'measure_type', 'value']),
        ]

    def __str__(self):
        if self.date is not None:
            return f'{self.measure_type.name} : {self.value} {self.measure_unit.name} on {self.date}'
        else:
            return f'{self.measure_type.name} : {self.value} {self.measure_unit.name}'

    def get_new_measure_with_converted_unit(self, new_unit: str) -> Measure:
        obj_unit = MeasureUnit.objects.filter(name=new_unit).first()
        if obj_unit is None:
            str_error = f'Not found unit with name={new_unit}'
            logger.error(str_error)
            raise NotFound(str_error)
        elif obj_unit == self.measure_unit:
            obj_measure = deepcopy(self)
            return obj_measure
        elif (self.measure_unit.name, new_unit) in self.UNIT_CONVERSIONS:
            obj_measure = deepcopy(self)
            obj_measure.measure_unit = obj_unit
            obj_measure.value = self.UNIT_CONVERSIONS[(self.measure_unit.name, new_unit)](obj_measure.value)
            return obj_measure
        else:
            str_error = f'Not found ({self.measure_unit.name}, {new_unit}) in UNIT_CONVERSIONS'
            logger.error(str_error)
            raise NotFound(str_error)


class Question(CDPModel, models.Model):
    '''
    Question of a questionnaire
    '''
    text = models.CharField(max_length=250, unique=True)
    code = models.CharField(
        max_length=50, blank=True, help_text='code of a code system that identifies the Question inter-systems.'
    )
    locale = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering = ['code']
        indexes = [
            models.Index(fields=['text', 'code', 'locale']),
            models.Index(fields=['text', 'locale', 'code']),
            models.Index(fields=['code', 'text', 'locale']),
            models.Index(fields=['code', 'locale', 'text']),
            models.Index(fields=['locale', 'text', 'code']),
            models.Index(fields=['locale', 'code', 'text']),
        ]

    def __str__(self):
        return (
            f'Question [{self.text}] with code=[{self.code}]' if self.code is not None else f'Question [{self.text}]'
        )


class Answer(CDPModel, models.Model):
    '''
    Answer of a questionnaire
    '''
    text = models.CharField(max_length=250, unique=True)
    code = models.CharField(
        max_length=50, blank=True, help_text='code of a code system that identifies the Answer inter-systems.'
    )
    locale = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering = ['code']
        indexes = [
            models.Index(fields=['text', 'code', 'locale']),
            models.Index(fields=['text', 'locale', 'code']),
            models.Index(fields=['code', 'text', 'locale']),
            models.Index(fields=['code', 'locale', 'text']),
            models.Index(fields=['locale', 'text', 'code']),
            models.Index(fields=['locale', 'code', 'text']),
        ]

    def __str__(self):
        return f'Answer [{self.text}] with code=[{self.code}]' if self.code is not None else f'Answer [{self.text}]'


class QuestionAnswer(CDPModel, models.Model):
    '''
    Represents a Question and it's Answers associated
    '''
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='question_answers')
    encounter = models.ForeignKey(
        Encounter, on_delete=models.SET_NULL, related_name='question_answers', null=True, blank=True
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers')
    answers = models.ManyToManyField(Answer, related_name='question_answers')
    subquestions = models.ManyToManyField(
        'self', related_name='parent_question_answers', symmetrical=False, blank=True
    )

    class Meta:
        ordering = ['question']
        indexes = [
            models.Index(fields=['patient', 'question']),
            models.Index(fields=['encounter', 'question'])
        ]

    def __str__(self):
        return f'[{self.question}] with [{self.answers.all()}]'
