from rest_framework.serializers import ValidationError


class LinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)
        code = 'youtube.com'
        if code not in url:
            raise ValidationError('Недопустимая ссылка на ресурс')
