#!/usr/bin/env python
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wealthpro.settings')
django.setup()

from main.models import InsuranceType, InsuranceBaseRate, InsuranceInvestmentReturn, StateRateAdjustment

def create_insurance_types():
    """Create insurance types if they don't exist"""
    insurance_types = [
        {'name': 'Life', 'icon': 'fa-heartbeat', 'description': 'Life insurance offers financial protection for your loved ones in case of your death.'},
        {'name': 'Health', 'icon': 'fa-medkit', 'description': 'Health insurance covers medical expenses for illness, injury, and preventive care.'},
        {'name': 'Auto', 'icon': 'fa-car', 'description': 'Auto insurance protects against financial loss in the event of an accident or theft.'},
        {'name': 'Home', 'icon': 'fa-home', 'description': 'Home insurance protects your property against damage or loss.'}
    ]
    
    created_types = []
    for ins_type in insurance_types:
        obj, created = InsuranceType.objects.get_or_create(
            name=ins_type['name'],
            defaults={
                'icon': ins_type['icon'],
                'description': ins_type['description']
            }
        )
        created_types.append(obj)
        print(f"Insurance Type {ins_type['name']}: {'Created' if created else 'Already exists'}")
    
    return created_types

def create_base_rates(insurance_types):
    """Create base rates for each insurance type"""
    # Map insurance types by name for easier access
    types_dict = {ins.name.lower(): ins for ins in insurance_types}
    
    # Life insurance rates
    if 'life' in types_dict:
        life = types_dict['life']
        print(f"Creating Life insurance rates for ID: {life.id}")
        
        rate_data = [
            # Age 18-30
            {'min_age': 18, 'max_age': 30, 'gender': 'M', 'base_rate': '25.00', 'rate_per_k': '0.10'},
            {'min_age': 18, 'max_age': 30, 'gender': 'F', 'base_rate': '22.50', 'rate_per_k': '0.09'},
            # Age 31-45
            {'min_age': 31, 'max_age': 45, 'gender': 'M', 'base_rate': '35.00', 'rate_per_k': '0.15'},
            {'min_age': 31, 'max_age': 45, 'gender': 'F', 'base_rate': '32.00', 'rate_per_k': '0.13'},
            # Age 46-60
            {'min_age': 46, 'max_age': 60, 'gender': 'M', 'base_rate': '50.00', 'rate_per_k': '0.25'},
            {'min_age': 46, 'max_age': 60, 'gender': 'F', 'base_rate': '45.00', 'rate_per_k': '0.22'},
            # Age 61-80
            {'min_age': 61, 'max_age': 80, 'gender': 'M', 'base_rate': '85.00', 'rate_per_k': '0.45'},
            {'min_age': 61, 'max_age': 80, 'gender': 'F', 'base_rate': '75.00', 'rate_per_k': '0.40'},
        ]
        
        for data in rate_data:
            obj, created = InsuranceBaseRate.objects.get_or_create(
                insurance_type=life,
                min_age=data['min_age'],
                max_age=data['max_age'],
                gender=data['gender'],
                defaults={
                    'base_monthly_rate': Decimal(data['base_rate']),
                    'rate_per_thousand': Decimal(data['rate_per_k'])
                }
            )
            print(f"Life insurance rate for {data['gender']} {data['min_age']}-{data['max_age']}: {'Created' if created else 'Already exists'}")
    
    # Health insurance rates
    if 'health' in types_dict:
        health = types_dict['health']
        print(f"Creating Health insurance rates for ID: {health.id}")
        
        rate_data = [
            # Age 18-30
            {'min_age': 18, 'max_age': 30, 'gender': 'ANY', 'base_rate': '150.00', 'rate_per_k': '0.05'},
            # Age 31-45
            {'min_age': 31, 'max_age': 45, 'gender': 'ANY', 'base_rate': '200.00', 'rate_per_k': '0.08'},
            # Age 46-60
            {'min_age': 46, 'max_age': 60, 'gender': 'ANY', 'base_rate': '350.00', 'rate_per_k': '0.12'},
            # Age 61-80
            {'min_age': 61, 'max_age': 80, 'gender': 'ANY', 'base_rate': '500.00', 'rate_per_k': '0.20'},
        ]
        
        for data in rate_data:
            obj, created = InsuranceBaseRate.objects.get_or_create(
                insurance_type=health,
                min_age=data['min_age'],
                max_age=data['max_age'],
                gender=data['gender'],
                defaults={
                    'base_monthly_rate': Decimal(data['base_rate']),
                    'rate_per_thousand': Decimal(data['rate_per_k'])
                }
            )
            print(f"Health insurance rate for {data['gender']} {data['min_age']}-{data['max_age']}: {'Created' if created else 'Already exists'}")
    
    # Auto insurance rates
    if 'auto' in types_dict:
        auto = types_dict['auto']
        print(f"Creating Auto insurance rates for ID: {auto.id}")
        
        rate_data = [
            # Age 18-25
            {'min_age': 18, 'max_age': 25, 'gender': 'M', 'base_rate': '120.00', 'rate_per_k': '0.15'},
            {'min_age': 18, 'max_age': 25, 'gender': 'F', 'base_rate': '100.00', 'rate_per_k': '0.12'},
            # Age 26-40
            {'min_age': 26, 'max_age': 40, 'gender': 'ANY', 'base_rate': '80.00', 'rate_per_k': '0.08'},
            # Age 41-65
            {'min_age': 41, 'max_age': 65, 'gender': 'ANY', 'base_rate': '70.00', 'rate_per_k': '0.06'},
            # Age 66+
            {'min_age': 66, 'max_age': 100, 'gender': 'ANY', 'base_rate': '90.00', 'rate_per_k': '0.09'},
        ]
        
        for data in rate_data:
            obj, created = InsuranceBaseRate.objects.get_or_create(
                insurance_type=auto,
                min_age=data['min_age'],
                max_age=data['max_age'],
                gender=data['gender'],
                defaults={
                    'base_monthly_rate': Decimal(data['base_rate']),
                    'rate_per_thousand': Decimal(data['rate_per_k'])
                }
            )
            print(f"Auto insurance rate for {data['gender']} {data['min_age']}-{data['max_age']}: {'Created' if created else 'Already exists'}")
    
    # Home insurance rates
    if 'home' in types_dict:
        home = types_dict['home']
        print(f"Creating Home insurance rates for ID: {home.id}")
        
        rate_data = [
            # Age based rates for home insurance (proxy for financial stability)
            {'min_age': 18, 'max_age': 25, 'gender': 'ANY', 'base_rate': '60.00', 'rate_per_k': '0.05'},
            {'min_age': 26, 'max_age': 40, 'gender': 'ANY', 'base_rate': '50.00', 'rate_per_k': '0.04'},
            {'min_age': 41, 'max_age': 65, 'gender': 'ANY', 'base_rate': '45.00', 'rate_per_k': '0.035'},
            {'min_age': 66, 'max_age': 100, 'gender': 'ANY', 'base_rate': '55.00', 'rate_per_k': '0.045'},
        ]
        
        for data in rate_data:
            obj, created = InsuranceBaseRate.objects.get_or_create(
                insurance_type=home,
                min_age=data['min_age'],
                max_age=data['max_age'],
                gender=data['gender'],
                defaults={
                    'base_monthly_rate': Decimal(data['base_rate']),
                    'rate_per_thousand': Decimal(data['rate_per_k'])
                }
            )
            print(f"Home insurance rate for {data['gender']} {data['min_age']}-{data['max_age']}: {'Created' if created else 'Already exists'}")

def create_investment_returns(insurance_types):
    """Create investment return data for insurance products"""
    # Map insurance types by name for easier access
    types_dict = {ins.name.lower(): ins for ins in insurance_types}
    
    # Life insurance investment returns (typically has investment component)
    if 'life' in types_dict:
        life = types_dict['life']
        print(f"Creating Life insurance investment returns")
        
        return_data = [
            {'term': 5, 'rate': '4.5', 'guaranteed': True, 'tax_benefits': True, 'bonus': '2.0'},
            {'term': 10, 'rate': '5.5', 'guaranteed': True, 'tax_benefits': True, 'bonus': '3.0'},
            {'term': 15, 'rate': '6.0', 'guaranteed': True, 'tax_benefits': True, 'bonus': '4.0'},
            {'term': 20, 'rate': '6.5', 'guaranteed': True, 'tax_benefits': True, 'bonus': '5.0'},
            {'term': 30, 'rate': '7.0', 'guaranteed': True, 'tax_benefits': True, 'bonus': '6.0'},
        ]
        
        for data in return_data:
            obj, created = InsuranceInvestmentReturn.objects.get_or_create(
                insurance_type=life,
                term_years=data['term'],
                defaults={
                    'annual_return_rate': Decimal(data['rate']),
                    'guaranteed_return': data['guaranteed'],
                    'tax_benefits': data['tax_benefits'],
                    'maturity_bonus_percent': Decimal(data['bonus']),
                }
            )
            print(f"Life insurance return for {data['term']} years: {'Created' if created else 'Already exists'}")
    
    # Other insurance types with potential investment components
    for insurance_name in ['health', 'auto', 'home']:
        if insurance_name in types_dict:
            ins_type = types_dict[insurance_name]
            print(f"Creating {insurance_name.capitalize()} insurance investment returns")
            
            # Basic return data for other insurance types (minimal investment component)
            return_data = [
                {'term': 5, 'rate': '2.0', 'guaranteed': False, 'tax_benefits': False, 'bonus': '0.0'},
                {'term': 10, 'rate': '2.5', 'guaranteed': False, 'tax_benefits': False, 'bonus': '0.5'},
                {'term': 15, 'rate': '3.0', 'guaranteed': False, 'tax_benefits': False, 'bonus': '1.0'},
                {'term': 20, 'rate': '3.5', 'guaranteed': False, 'tax_benefits': False, 'bonus': '1.5'},
            ]
            
            for data in return_data:
                obj, created = InsuranceInvestmentReturn.objects.get_or_create(
                    insurance_type=ins_type,
                    term_years=data['term'],
                    defaults={
                        'annual_return_rate': Decimal(data['rate']),
                        'guaranteed_return': data['guaranteed'],
                        'tax_benefits': data['tax_benefits'],
                        'maturity_bonus_percent': Decimal(data['bonus']),
                    }
                )
                print(f"{insurance_name.capitalize()} insurance return for {data['term']} years: {'Created' if created else 'Already exists'}")

def create_state_adjustments(insurance_types):
    """Create state adjustment factors for insurance rates"""
    # Get a sample of US states with varying adjustment factors
    states = [
        # Higher cost states
        ('CA', 'California', 1.25),
        ('NY', 'New York', 1.30),
        ('NJ', 'New Jersey', 1.20),
        ('MA', 'Massachusetts', 1.15),
        ('FL', 'Florida', 1.15),
        
        # Medium cost states
        ('IL', 'Illinois', 1.05),
        ('TX', 'Texas', 1.10),
        ('PA', 'Pennsylvania', 1.05),
        ('OH', 'Ohio', 1.00),
        ('MI', 'Michigan', 1.05),
        
        # Lower cost states
        ('IA', 'Iowa', 0.90),
        ('KS', 'Kansas', 0.85),
        ('MO', 'Missouri', 0.95),
        ('NE', 'Nebraska', 0.85),
        ('OK', 'Oklahoma', 0.90),
    ]
    
    # Create state adjustments for each insurance type
    for insurance_type in insurance_types:
        print(f"Creating state adjustments for {insurance_type.name}")
        
        for code, name, factor in states:
            # Different descriptions based on insurance type
            if insurance_type.name.lower() == 'life':
                description = f"Life insurance rates in {name} adjusted by {factor}x due to state regulations and mortality statistics."
            elif insurance_type.name.lower() == 'health':
                description = f"Health insurance rates in {name} adjusted by {factor}x due to healthcare costs and regulations."
            elif insurance_type.name.lower() == 'auto':
                description = f"Auto insurance rates in {name} adjusted by {factor}x due to driving conditions, accident rates, and regulations."
            elif insurance_type.name.lower() == 'home':
                description = f"Home insurance rates in {name} adjusted by {factor}x due to property values, weather risks, and regulations."
            else:
                description = f"Insurance rates in {name} adjusted by {factor}x due to state-specific factors."
            
            obj, created = StateRateAdjustment.objects.get_or_create(
                insurance_type=insurance_type,
                state=code,
                defaults={
                    'rate_multiplier': Decimal(str(factor)),
                    'description': description,
                }
            )
            print(f"State adjustment for {insurance_type.name} in {name}: {'Created' if created else 'Already exists'}")

def main():
    print("Creating insurance data...")
    
    # Create or get insurance types
    insurance_types = create_insurance_types()
    
    # Create base rates
    create_base_rates(insurance_types)
    
    # Create investment returns
    create_investment_returns(insurance_types)
    
    # Create state adjustments
    create_state_adjustments(insurance_types)
    
    print("Insurance data creation complete!")

if __name__ == "__main__":
    main() 