from django import forms
from .models import Student
from .models import StudentWellbeing


class StudentForm(forms.ModelForm):

    class Meta:

        model = Student

        fields = [

            'name',

            'register_number',

            'attendance',

            'marks',

            'discipline_score'
        ]


class WellbeingForm(forms.ModelForm):

    class Meta:

        model = StudentWellbeing

        fields = [

            'mood',

            'stress_level',

            'sleep_quality',

            'social_activity',

            'motivation_level'
        ]