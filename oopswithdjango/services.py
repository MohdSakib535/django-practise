# services.py
from abc import ABC, abstractmethod
from .models import *

class AbstractMaintenanceService(ABC):
    @abstractmethod
    def perform_maintenance(self, vehicle):
        pass
    
    @abstractmethod
    def generate_report(self, vehicle):
        pass

class BasicMaintenanceService(AbstractMaintenanceService):
    def perform_maintenance(self, vehicle):
        print(f"Performing basic maintenance on {vehicle.make} {vehicle.model}")
        # Update last service date
        from datetime import date
        vehicle.last_service_date = date.today()
        vehicle.save()
        return True
    
    def generate_report(self, vehicle):
        return {
            'vehicle': f"{vehicle.make} {vehicle.model}",
            'type': vehicle.get_vehicle_type(),
            'last_service': vehicle.last_service_date,
            'next_service': "Due soon" if vehicle.needs_maintenance() else "Good"
        }

class PremiumMaintenanceService(AbstractMaintenanceService):
    def perform_maintenance(self, vehicle):
        print(f"Performing premium maintenance on {vehicle.make} {vehicle.model}")
        # Update last service date and reset maintenance flags
        from datetime import date
        vehicle.last_service_date = date.today()
        if hasattr(vehicle, 'maintenance_flag'):
            vehicle.maintenance_flag = False
        vehicle.save()
        return True
    
    def generate_report(self, vehicle):
        detailed_status = "Urgent" if vehicle.mileage % 10000 == 0 else "Regular"
        return {
            'vehicle': f"{vehicle.make} {vehicle.model}",
            'type': vehicle.get_vehicle_type(),
            'last_service': vehicle.last_service_date,
            'next_service': detailed_status,
            'recommendations': self._get_recommendations(vehicle)
        }
    
    def _get_recommendations(self, vehicle):
        if isinstance(vehicle, Truck):
            return ["Check brakes", "Inspect suspension"]
        elif isinstance(vehicle, Motorcycle):
            return ["Check chain tension", "Inspect tires"]
        return ["Standard checkup"]