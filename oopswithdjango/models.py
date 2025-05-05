
from django.db import models
from .main_model import AbstractVehicle

# models.py (continued)
class Car(AbstractVehicle):
    num_doors = models.PositiveIntegerField(default=4)
    car_type = models.CharField(max_length=20, choices=[
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('coupe', 'Coupe'),
        ('hatchback', 'Hatchback')
    ])
    
    def get_vehicle_type(self):
        return f"Car ({self.car_type})"
    
    def needs_maintenance(self):
        # Cars need maintenance every 5,000 miles
        return self.mileage % 5000 < 100  # Within 100 miles of 5k interval

class Truck(AbstractVehicle):
    payload_capacity = models.DecimalField(max_digits=10, decimal_places=2)  # in tons
    axles = models.PositiveIntegerField(default=2)
    
    def get_vehicle_type(self):
        return f"Truck ({self.axles} axles)"
    
    def needs_maintenance(self):
        # Trucks need maintenance every 10,000 miles or yearly
        from datetime import date
        yearly_check = (date.today() - self.last_service_date).days > 365 if self.last_service_date else True
        return yearly_check or (self.mileage % 10000 < 200)

class Motorcycle(AbstractVehicle):
    engine_cc = models.PositiveIntegerField()
    has_sidecar = models.BooleanField(default=False)
    
    def get_vehicle_type(self):
        return f"Motorcycle ({self.engine_cc}cc)"
    
    def needs_maintenance(self):
        # Motorcycles need maintenance every 3,000 miles
        return self.mileage % 3000 < 100