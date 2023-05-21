
from django.core.exceptions import ValidationError
import datetime
from django.conf import settings

MULTIPLY_A=settings.MULTIPLY_A
ALWAYS_CHECK_C=settings.ALWAYS_CHECK_C


class ProductionClass:
        @classmethod
        def method(cls, a, b, c):
            if not isinstance(a, int):
                raise ValidationError("This field accepts interger only")
            if not isinstance(b, str):
                raise ValidationError("This field accepts string only")
            if not isinstance(c, datetime):
                raise ValidationError("This field accepts datetime only")
            if(a==2 or b!='foo') or ALWAYS_CHECK_C==True:
             if c.year!=datetime.now.year+1:
                raise ValidationError("This field accepts datetime of next year only")
            if b=='bar':
                return a*3
            return a*MULTIPLY_A