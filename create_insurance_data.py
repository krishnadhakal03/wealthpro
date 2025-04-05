from main.models import InsuranceType, InsuranceBaseRate, StateRateAdjustment
from decimal import Decimal

def create_insurance_data():
    # Get all insurance types
    insurance_types = InsuranceType.objects.all()
    insurance_types_dict = {ins.name.lower(): ins for ins in insurance_types}
    
    print(f"Found insurance types: {list(insurance_types_dict.keys())}")

    # Create base rates for each insurance type
    # Life Insurance
    if 'life' in insurance_types_dict:
        life = insurance_types_dict['life']
        print(f"Creating Life insurance rates for ID: {life.id}")
        
        # Create age brackets for life insurance
        obj, created = InsuranceBaseRate.objects.get_or_create(
            insurance_type=life,
            min_age=18,
            max_age=30,
            gender='M',
            defaults={
                'base_monthly_rate': Decimal('25.00'),
                'rate_per_thousand': Decimal('0.10')
            }
        )
        print(f"Created life insurance rate for M 18-30: {created}")
        
        obj, created = InsuranceBaseRate.objects.get_or_create(
            insurance_type=life,
            min_age=18,
            max_age=30,
            gender='F',
            defaults={
                'base_monthly_rate': Decimal('22.50'),
                'rate_per_thousand': Decimal('0.09')
            }
        )
        print(f"Created life insurance rate for F 18-30: {created}")
        
        # more life insurance rates...
        InsuranceBaseRate.objects.get_or_create(
            insurance_type=life,
            min_age=31,
            max_age=45,
            gender='M',
            defaults={
                'base_monthly_rate': Decimal('35.00'),
                'rate_per_thousand': Decimal('0.15')
            }
        )
        
        InsuranceBaseRate.objects.get_or_create(
            insurance_type=life,
            min_age=31,
            max_age=45,
            gender='F',
            defaults={
                'base_monthly_rate': Decimal('32.00'),
                'rate_per_thousand': Decimal('0.13')
            }
        )
        
        InsuranceBaseRate.objects.get_or_create(
            insurance_type=life,
            min_age=46,
            max_age=60,
            gender='M',
            defaults={
                'base_monthly_rate': Decimal('50.00'),
                'rate_per_thousand': Decimal('0.25')
            }
        )
        
        InsuranceBaseRate.objects.get_or_create(
            insurance_type=life,
            min_age=46,
            max_age=60,
            gender='F',
            defaults={
                'base_monthly_rate': Decimal('45.00'),
                'rate_per_thousand': Decimal('0.22')
            }
        )
        
        InsuranceBaseRate.objects.get_or_create(
            insurance_type=life,
            min_age=61,
            max_age=80,
            gender='M',
            defaults={
                'base_monthly_rate': Decimal('85.00'),
                'rate_per_thousand': Decimal('0.45')
            }
        )
        
        InsuranceBaseRate.objects.get_or_create(
            insurance_type=life,
            min_age=61,
            max_age=80,
            gender='F',
            defaults={
                'base_monthly_rate': Decimal('75.00'),
                'rate_per_thousand': Decimal('0.40')
            }
        )
    else:
        print("Life insurance type not found")

    # Health Insurance
    if 'health' in insurance_types_dict:
        health = insurance_types_dict['health']
        print(f"Creating Health insurance rates for ID: {health.id}")
        
        obj, created = InsuranceBaseRate.objects.get_or_create(
            insurance_type=health,
            min_age=18,
            max_age=30,
            gender='ANY',
            defaults={
                'base_monthly_rate': Decimal('200.00'),
                'rate_per_thousand': Decimal('0.05')
            }
        )
        print(f"Created health insurance rate for 18-30: {created}")
        
        # more health insurance rates...
        InsuranceBaseRate.objects.get_or_create(
            insurance_type=health,
            min_age=31,
            max_age=45,
            gender='ANY',
            defaults={
                'base_monthly_rate': Decimal('250.00'),
                'rate_per_thousand': Decimal('0.07')
            }
        )
        
        InsuranceBaseRate.objects.get_or_create(
            insurance_type=health,
            min_age=46,
            max_age=60,
            gender='ANY',
            defaults={
                'base_monthly_rate': Decimal('350.00'),
                'rate_per_thousand': Decimal('0.10')
            }
        )
        
        InsuranceBaseRate.objects.get_or_create(
            insurance_type=health,
            min_age=61,
            max_age=80,
            gender='ANY',
            defaults={
                'base_monthly_rate': Decimal('450.00'),
                'rate_per_thousand': Decimal('0.15')
            }
        )
    else:
        print("Health insurance type not found")

    # Auto Insurance
    if 'auto' in insurance_types_dict:
        auto = insurance_types_dict['auto']
        print(f"Creating Auto insurance rates for ID: {auto.id}")
        
        obj, created = InsuranceBaseRate.objects.get_or_create(
            insurance_type=auto,
            min_age=18,
            max_age=25,
            gender='ANY',
            defaults={
                'base_monthly_rate': Decimal('150.00'),
                'rate_per_thousand': Decimal('0.30')
            }
        )
        print(f"Created auto insurance rate for 18-25: {created}")
        
        # more auto insurance rates...
        InsuranceBaseRate.objects.get_or_create(
            insurance_type=auto,
            min_age=26,
            max_age=50,
            gender='ANY',
            defaults={
                'base_monthly_rate': Decimal('100.00'),
                'rate_per_thousand': Decimal('0.15')
            }
        )
        
        InsuranceBaseRate.objects.get_or_create(
            insurance_type=auto,
            min_age=51,
            max_age=80,
            gender='ANY',
            defaults={
                'base_monthly_rate': Decimal('120.00'),
                'rate_per_thousand': Decimal('0.20')
            }
        )
    else:
        print("Auto insurance type not found")

    # Home Insurance
    if 'home' in insurance_types_dict:
        home = insurance_types_dict['home']
        print(f"Creating Home insurance rates for ID: {home.id}")
        
        obj, created = InsuranceBaseRate.objects.get_or_create(
            insurance_type=home,
            min_age=18,
            max_age=100,
            gender='ANY',
            defaults={
                'base_monthly_rate': Decimal('80.00'),
                'rate_per_thousand': Decimal('0.07')
            }
        )
        print(f"Created home insurance rate for 18-100: {created}")
    else:
        print("Home insurance type not found")

    # Create state rate adjustments
    # High cost states
    high_cost_states = ['CA', 'NY', 'NJ', 'FL', 'MA']
    medium_cost_states = ['TX', 'IL', 'PA', 'WA', 'CO', 'MD', 'VA', 'CT']

    print(f"Creating state rate adjustments for {len(insurance_types)} insurance types")
    
    # Apply state adjustments to all insurance types
    for insurance_type in insurance_types:
        print(f"Creating adjustments for {insurance_type.name}")
        
        # High cost states
        for state in high_cost_states:
            obj, created = StateRateAdjustment.objects.get_or_create(
                insurance_type=insurance_type,
                state=state,
                defaults={
                    'rate_multiplier': Decimal('1.25'),
                    'description': f'Higher premiums due to increased risk factors, claim frequency, and regulatory requirements in {dict(StateRateAdjustment.STATE_CHOICES).get(state)}'
                }
            )
            if created:
                print(f"Created high cost adjustment for {insurance_type.name} in {state}")
            
        # Medium cost states  
        for state in medium_cost_states:
            StateRateAdjustment.objects.get_or_create(
                insurance_type=insurance_type,
                state=state,
                defaults={
                    'rate_multiplier': Decimal('1.10'),
                    'description': f'Slightly elevated premiums due to moderate risk factors in {dict(StateRateAdjustment.STATE_CHOICES).get(state)}'
                }
            )
        
        # Low cost state example
        StateRateAdjustment.objects.get_or_create(
            insurance_type=insurance_type,
            state='WY',
            defaults={
                'rate_multiplier': Decimal('0.85'),
                'description': 'Lower premiums due to reduced risk factors and claim frequency in Wyoming'
            }
        )

    print(f'Created {InsuranceBaseRate.objects.count()} insurance base rates')
    print(f'Created {StateRateAdjustment.objects.count()} state rate adjustments')

if __name__ == '__main__':
    import os
    import django
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wealthpro.settings")
    django.setup()
    
    create_insurance_data() 