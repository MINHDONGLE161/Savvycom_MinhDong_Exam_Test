from django.db import models


class Student(models.Model):
    name        = models.CharField(max_length=25, unique=True)
    age         = models.IntegerField(null=False)
    birthdate   = models.DateTimeField(null=False)

    class Meta:
        db_table = 'student'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'birthdate': self.birthdate,
        }