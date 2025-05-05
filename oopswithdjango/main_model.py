# models.py
from django.db import models
from django.core.exceptions import ValidationError

class AbstractVehicle(models.Model):
    
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    vin = models.CharField(max_length=17, unique=True)
    mileage = models.PositiveIntegerField(default=0)
    last_service_date = models.DateField(null=True, blank=True)
    
    # Abstract method - must be implemented by subclasses
    def get_vehicle_type(self):
        raise NotImplementedError("Subclasses must implement get_vehicle_type()")
    
    # Abstract method for type-specific maintenance check
    def needs_maintenance(self):
        raise NotImplementedError("Subclasses must implement needs_maintenance()")
    
    # Common validation
    def clean(self):
        super().clean()
        if self.year < 1900 or self.year > 2025:
            raise ValidationError("Invalid year")
        if len(self.vin) != 17:
            raise ValidationError("VIN must be 17 characters")
    
    class Meta:
        abstract = True
        ordering = ['make', 'model']

