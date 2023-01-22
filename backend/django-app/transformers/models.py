from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.postgres.indexes import GinIndex


class Toyline(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Subline(models.Model):
    toyline = models.ForeignKey(Toyline, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Transformer(models.Model):
    MANUFACTURERS = (
        ('H', 'Hasbro'),
        ('T', 'Takara Tomy'),
    )

    # TODO: Probably need to remove slug as it would probably not be unique for same named tfs

    picture = models.ImageField(unique=True, null=True)
    name = models.CharField(max_length=50)
    release_date = models.DateField()
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    toyline = models.ForeignKey(Toyline, to_field='name', default='None', on_delete=models.SET_DEFAULT)
    subline = models.ForeignKey(Subline, to_field='name', default='None', on_delete=models.SET_DEFAULT)
    size_class = models.CharField(max_length=255, null=True)
    description = models.TextField()
    manufacturer = models.CharField(max_length=1, choices=MANUFACTURERS)
    is_visible = models.BooleanField(default=True)


    class Meta:
        ordering = ('name', )
        indexes = [
            GinIndex(name='NewGinIndex', fields=['name', 'toyline', 'subline', 'size_class'], opclasses=['gin_trgm_ops', 'gin_trgm_ops', 'gin_trgm_ops', 'gin_trgm_ops'])
        ]

    def __str__(self):
        return self.name



