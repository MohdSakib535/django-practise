# views.py
from django.shortcuts import render
from .models import Car, Truck, Motorcycle
from .services import BasicMaintenanceService, PremiumMaintenanceService
from django.http import JsonResponse
from django.http import HttpResponse

def vehicle_data_created(request):
    # Create some vehicles
    car = Car.objects.create(
        make="Honda",
        model="Accord",
        year=2022,
        vin="1HGCV1F14NA123456",
        mileage=15000,
        num_doors=4,
        car_type="sedan"
    )
    
    truck = Truck.objects.create(
        make="Chevrolet",
        model="Silverado",
        year=2021,
        vin="3GCUYDED0MG123456",
        mileage=32000,
        payload_capacity=3.0,  # in tons
        axles=2
    )
    
    motorcycle = Motorcycle.objects.create(
        make="Yamaha",
        model="MT-07",
        year=2023,
        vin="JYARM06E9PA123456",
        mileage=500,
        engine_cc=689
    )
    return HttpResponse("OK")
    
    # # Using abstract methods
    # vehicles = [car, truck, motorcycle]
    # vehicle_info = [{
    #     'description': f"{v.make} {v.model}",
    #     'type': v.get_vehicle_type(),
    #     'needs_service': v.needs_maintenance()
    # } for v in vehicles]
    
    # # Using abstract service
    # service = PremiumMaintenanceService()  # Could be BasicMaintenanceService()
    # maintenance_report = service.generate_report(truck)
    
    # return render(request, 'dashboard.html', {
    #     'vehicles': vehicle_info,
    #     'report': maintenance_report
    # })

def vehicle_dashboard(request):
    """
    Displays a dashboard of vehicles filtered by type with dropdown selection
    """
    # Get the selected vehicle type from request (default to 'car')
    selected_type = request.GET.get('vehicle_type', 'car')
    
    # Initialize variables
    vehicles = []
    vehicle_data = []
    
    # Get vehicles based on selected type
    if selected_type == 'car':
        vehicles = Car.objects.all()
    elif selected_type == 'truck':
        vehicles = Truck.objects.all()
    elif selected_type == 'motorcycle':
        vehicles = Motorcycle.objects.all()
    
    # Prepare vehicle data for template
    for vehicle in vehicles:
        print("---for----",vehicle.needs_maintenance())
        vehicle_data.append({
            'id': vehicle.id,
            'make': vehicle.make,
            'model': vehicle.model,
            'type': vehicle.get_vehicle_type(),
            'year': vehicle.year,
            'mileage': vehicle.mileage,
            'last_service': vehicle.last_service_date,
            'needs_service': vehicle.needs_maintenance(),
            'vin': vehicle.vin,
            'vehicle_type': vehicle.__class__.__name__.lower()
        })
    
    # Get service statistics for the first vehicle (if exists)
    basic_service = BasicMaintenanceService()
    premium_service = PremiumMaintenanceService()
    example_report = None
    
    if vehicles:
        example_report = {
            'basic': basic_service.generate_report(vehicles[0]),
            'premium': premium_service.generate_report(vehicles[0])
        }
    
    return render(request, 'dashboard.html', {
        'vehicles': vehicle_data,
        'total_vehicles': len(vehicles),
        'selected_type': selected_type,
        'service_examples': example_report,
        'vehicle_types': [
            {'value': 'car', 'label': 'Cars'},
            {'value': 'truck', 'label': 'Trucks'},
            {'value': 'motorcycle', 'label': 'Motorcycles'}
        ]
    })


# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Car, Truck, Motorcycle
from .services import BasicMaintenanceService, PremiumMaintenanceService

def service_vehicle(request, vehicle_type, vehicle_id):
    # Map type string to actual model
    model_map = {
        'car': Car,
        'truck': Truck,
        'motorcycle': Motorcycle,
    }
    model_class = model_map.get(vehicle_type.lower())
    
    if not model_class:
        return JsonResponse({'status': 'error', 'message': 'Invalid vehicle type'}, status=400)

    # Try to fetch the vehicle
    try:
        vehicle = model_class.objects.get(pk=vehicle_id)
    except model_class.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Vehicle not found'}, status=404)

    # Continue with service logic
    try:
        if request.user.is_authenticated and hasattr(request.user, 'is_premium_member') and request.user.is_premium_member:
            print('pre')
            service = PremiumMaintenanceService()
        else:
            print("basic----")
            service = BasicMaintenanceService()
        
        success = service.perform_maintenance(vehicle)
        report = service.generate_report(vehicle)

       
        
        return JsonResponse({
            'status': 'success',
            'vehicle': {
                'id': vehicle.id,
                'make': vehicle.make,
                'model': vehicle.model,
                'type': vehicle_type,
                'vin': vehicle.vin,
            },
            'service_performed': {
                'service_type': service.__class__.__name__,
                'success': success,
                'last_service_date': vehicle.last_service_date.strftime('%Y-%m-%d') if vehicle.last_service_date else None,
                'next_service_due': vehicle.needs_maintenance()
            },
            'report': report
        })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


