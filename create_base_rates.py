#!/usr/bin/env python
import os
import django
import sys
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wealthpro.settings')
django.setup()

from main.models import (
    InsuranceType, 
    InsuranceBaseRate, 
    InsuranceInvestmentReturn,
    StateRateAdjustment,
    CSOMortalityTable,
    InsuranceRiskFactor,
    RiskFactorValue,
    DisclaimerText,
    StateRegulation
)

def create_base_rates():
    """Create base insurance rates for all insurance types"""
    print("Creating insurance base rates...")
    
    types = InsuranceType.objects.all()
    types_dict = {ins.name.lower(): ins for ins in types}
    
    print(f"Found insurance types: {list(types_dict.keys())}")
    
    if not types:
        print("No insurance types found. Please run migrations and create insurance types first.")
        return False
    
    # Life Insurance Rates
    if 'life' in types_dict:
        life = types_dict['life']
        print(f"Creating Life insurance rates for ID: {life.id}")
        
        for gender in ['M', 'F']:
            for age_range in [(18, 30), (31, 45), (46, 60), (61, 80)]:
                base_rate = '25.00' if gender == 'M' else '22.50'
                rate_per_k = '0.10' if gender == 'M' else '0.09'
                
                # Adjust rates for older age brackets
                if age_range[0] > 30:
                    base_rate = str(float(base_rate) * 1.4)
                    rate_per_k = str(float(rate_per_k) * 1.5)
                if age_range[0] > 45:
                    base_rate = str(float(base_rate) * 1.5)
                    rate_per_k = str(float(rate_per_k) * 1.7)
                if age_range[0] > 60:
                    base_rate = str(float(base_rate) * 1.7)
                    rate_per_k = str(float(rate_per_k) * 1.8)
                
                obj, created = InsuranceBaseRate.objects.get_or_create(
                    insurance_type=life,
                    min_age=age_range[0],
                    max_age=age_range[1],
                    gender=gender,
                    defaults={
                        'base_monthly_rate': Decimal(base_rate),
                        'rate_per_thousand': Decimal(rate_per_k)
                    }
                )
                print(f"Life insurance rate for {gender} {age_range[0]}-{age_range[1]}: {'Created' if created else 'Already exists'}")
    
    # Health Insurance Rates
    if 'health' in types_dict:
        health = types_dict['health']
        print(f"Creating Health insurance rates for ID: {health.id}")
        
        for age_range in [(18, 30), (31, 45), (46, 60), (61, 80)]:
            base_rate = '150.00'
            rate_per_k = '0.05'
            
            if age_range[0] > 30:
                base_rate = '200.00'
                rate_per_k = '0.08'
            if age_range[0] > 45:
                base_rate = '350.00'
                rate_per_k = '0.12'
            if age_range[0] > 60:
                base_rate = '500.00'
                rate_per_k = '0.20'
                
            obj, created = InsuranceBaseRate.objects.get_or_create(
                insurance_type=health,
                min_age=age_range[0],
                max_age=age_range[1],
                gender='ANY',
                defaults={
                    'base_monthly_rate': Decimal(base_rate),
                    'rate_per_thousand': Decimal(rate_per_k)
                }
            )
            print(f"Health insurance rate for ages {age_range[0]}-{age_range[1]}: {'Created' if created else 'Already exists'}")
    
    # Auto Insurance Rates
    if 'auto' in types_dict:
        auto = types_dict['auto']
        print(f"Creating Auto insurance rates for ID: {auto.id}")
        
        # Young drivers (separate rates for M/F)
        for gender in ['M', 'F']:
            base_rate = '120.00' if gender == 'M' else '100.00'
            rate_per_k = '0.40' if gender == 'M' else '0.30'
            
            obj, created = InsuranceBaseRate.objects.get_or_create(
                insurance_type=auto,
                min_age=18,
                max_age=25,
                gender=gender,
                defaults={
                    'base_monthly_rate': Decimal(base_rate),
                    'rate_per_thousand': Decimal(rate_per_k)
                }
            )
            print(f"Auto insurance rate for {gender} 18-25: {'Created' if created else 'Already exists'}")
        
        # Older drivers (gender neutral)
        for age_range in [(26, 40), (41, 65), (66, 100)]:
            base_rate = '80.00'
            rate_per_k = '0.20'
            
            obj, created = InsuranceBaseRate.objects.get_or_create(
                insurance_type=auto,
                min_age=age_range[0],
                max_age=age_range[1],
                gender='ANY',
                defaults={
                    'base_monthly_rate': Decimal(base_rate),
                    'rate_per_thousand': Decimal(rate_per_k)
                }
            )
            print(f"Auto insurance rate for ANY {age_range[0]}-{age_range[1]}: {'Created' if created else 'Already exists'}")
    
    # Home Insurance Rates
    if 'home' in types_dict:
        home = types_dict['home']
        print(f"Creating Home insurance rates for ID: {home.id}")
        
        for age_range in [(18, 25), (26, 40), (41, 65), (66, 100)]:
            if age_range[0] <= 25:
                base_rate = '60.00'
                rate_per_k = '0.05'
            elif age_range[0] <= 40:
                base_rate = '50.00'
                rate_per_k = '0.04'
            elif age_range[0] <= 65:
                base_rate = '45.00'
                rate_per_k = '0.035'
            else:
                base_rate = '55.00'
                rate_per_k = '0.045'
                
            obj, created = InsuranceBaseRate.objects.get_or_create(
                insurance_type=home,
                min_age=age_range[0],
                max_age=age_range[1],
                gender='ANY',
                defaults={
                    'base_monthly_rate': Decimal(base_rate),
                    'rate_per_thousand': Decimal(rate_per_k)
                }
            )
            print(f"Home insurance rate for ANY {age_range[0]}-{age_range[1]}: {'Created' if created else 'Already exists'}")
    
    return True

def create_placeholder_data():
    """Create minimal required data for insurance calculator to work"""
    print("Creating placeholder data for required models...")
    
    # Create placeholder CSO mortality table entry if needed
    if CSOMortalityTable.objects.count() == 0:
        print("Creating placeholder CSO mortality table entries...")
        for age in range(18, 81):
            for gender in ['M', 'F']:
                for smoker in ['NS', 'SM', 'ANY']:
                    # Create very basic rate based on age
                    base_rate = age / 100.0  # Simple age-based rate
                    
                    # Adjust for gender and smoking
                    if gender == 'F':
                        base_rate *= 0.8  # Lower for females
                    
                    if smoker == 'SM':
                        base_rate *= 2.0  # Higher for smokers
                    elif smoker == 'ANY':
                        base_rate *= 1.25  # Average
                    
                    CSOMortalityTable.objects.get_or_create(
                        age=age,
                        gender=gender,
                        smoker_status=smoker,
                        defaults={
                            'mortality_rate': Decimal(str(base_rate)),
                            'table_version': '2017 CSO'
                        }
                    )
        print(f"Added {CSOMortalityTable.objects.count()} CSO Mortality Table entries.")
    
    # Create placeholder risk factors
    if InsuranceRiskFactor.objects.count() == 0:
        print("Creating placeholder risk factors...")
        # Life insurance risk factors
        life_factor = InsuranceRiskFactor.objects.create(
            name='Smoker Status',
            factor_type='LIFE',
            description='Adjustment based on smoking habits'
        )
        
        RiskFactorValue.objects.create(
            risk_factor=life_factor,
            value_name='Non-smoker',
            multiplier=Decimal('1.0')
        )
        
        RiskFactorValue.objects.create(
            risk_factor=life_factor,
            value_name='Smoker',
            multiplier=Decimal('1.5')
        )
        
        # Health insurance risk factor
        health_factor = InsuranceRiskFactor.objects.create(
            name='Pre-existing Conditions',
            factor_type='HEALTH',
            description='Adjustment based on pre-existing health conditions'
        )
        
        RiskFactorValue.objects.create(
            risk_factor=health_factor,
            value_name='None',
            multiplier=Decimal('1.0')
        )
        
        RiskFactorValue.objects.create(
            risk_factor=health_factor,
            value_name='Minor',
            multiplier=Decimal('1.2')
        )
        
        RiskFactorValue.objects.create(
            risk_factor=health_factor,
            value_name='Major',
            multiplier=Decimal('1.5')
        )
        
        print(f"Created {InsuranceRiskFactor.objects.count()} risk factors with {RiskFactorValue.objects.count()} values")
    
    # Create investment returns if needed
    if InsuranceInvestmentReturn.objects.count() == 0:
        print("Creating placeholder investment returns...")
        
        for insurance_type in InsuranceType.objects.all():
            for term in [5, 10, 15, 20, 30]:
                # Skip longer terms for some insurance types
                if term > 20 and insurance_type.name.lower() != 'life':
                    continue
                
                # Base annual return rate - higher for life insurance
                if insurance_type.name.lower() == 'life':
                    annual_rate = Decimal('4.5')
                elif insurance_type.name.lower() == 'health':
                    annual_rate = Decimal('3.5')
                else:
                    annual_rate = Decimal('3.0')
                
                # Conservative and aggressive variations
                conservative_rate = annual_rate - Decimal('1.5')
                aggressive_rate = annual_rate + Decimal('2.0')
                
                InsuranceInvestmentReturn.objects.get_or_create(
                    insurance_type=insurance_type,
                    term_years=term,
                    defaults={
                        'annual_return_rate': annual_rate,
                        'conservative_return_rate': conservative_rate,
                        'aggressive_return_rate': aggressive_rate,
                        'guaranteed_return': insurance_type.name.lower() == 'life',
                        'tax_benefits': insurance_type.name.lower() in ['life', 'health'],
                        'maturity_bonus_percent': Decimal('5.0') if insurance_type.name.lower() == 'life' and term >= 15 else Decimal('0'),
                        'historical_performance': f"Historical {term}-year returns for {insurance_type.name} insurance have averaged {annual_rate}% with variations between {conservative_rate}% and {aggressive_rate}% depending on market conditions."
                    }
                )
        
        print(f"Created {InsuranceInvestmentReturn.objects.count()} investment return records.")
    
    # Create disclaimers
    if DisclaimerText.objects.count() == 0:
        print("Creating insurance disclaimers...")
        
        # General disclaimer for all insurance types
        DisclaimerText.objects.create(
            insurance_type=None,
            title="General Insurance Disclaimer",
            content="The premium estimates provided by this calculator are for illustration purposes only and do not constitute an offer of insurance. Actual premiums may vary based on underwriting, policy features, and other factors. Please consult with a licensed insurance agent for an accurate quote.",
            is_active=True
        )
        
        # Specific disclaimers for each insurance type
        for insurance_type in InsuranceType.objects.all():
            DisclaimerText.objects.create(
                insurance_type=insurance_type,
                title=f"{insurance_type.name} Insurance Disclaimer",
                content=f"This {insurance_type.name.lower()} insurance premium calculation is based on industry standard rates and may not reflect all risk factors. Final premiums are subject to underwriting approval and may differ from this estimate.",
                is_active=True
            )
        
        print(f"Created {DisclaimerText.objects.count()} disclaimers.")
    
    # Create state regulations if needed
    if StateRegulation.objects.count() == 0 and StateRateAdjustment.objects.count() == 0:
        print("Creating state regulations and rate adjustments...")
        
        states = dict(StateRateAdjustment.STATE_CHOICES)
        top_states = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'MI', 'NJ', 'MA']
        
        for state_code in top_states:
            state_name = states.get(state_code, "Unknown State")
            
            for insurance_type in InsuranceType.objects.all():
                # Create state regulation
                min_coverage = 25000
                if insurance_type.name.lower() == 'auto':
                    min_coverage = 50000 if state_code in ['CA', 'NY', 'NJ'] else 25000
                elif insurance_type.name.lower() == 'home':
                    min_coverage = 100000
                
                StateRegulation.objects.create(
                    insurance_type=insurance_type,
                    state=state_code,
                    special_requirements=f"Special regulatory requirements for {insurance_type.name} insurance in {state_name}.",
                    min_coverage_required=Decimal(str(min_coverage))
                )
                
                # Create state rate adjustment
                # Different states have different rate multipliers
                if state_code in ['CA', 'NY', 'NJ']:
                    multiplier = Decimal('1.15')  # Higher rates in these states
                elif state_code in ['TX', 'FL']:
                    multiplier = Decimal('1.10')  # Slightly higher
                elif state_code in ['OH', 'MI', 'PA']:
                    multiplier = Decimal('0.95')  # Slightly lower
                else:
                    multiplier = Decimal('1.0')  # Base rate
                
                # Adjust for insurance type
                if insurance_type.name.lower() == 'auto' and state_code in ['MI', 'NJ']:
                    multiplier *= Decimal('1.2')  # Higher auto rates in these states
                elif insurance_type.name.lower() == 'home' and state_code in ['FL', 'CA']:
                    multiplier *= Decimal('1.25')  # Higher home rates due to natural disasters
                
                StateRateAdjustment.objects.create(
                    insurance_type=insurance_type,
                    state=state_code,
                    rate_multiplier=multiplier,
                    description=f"Rate adjustment for {insurance_type.name} insurance in {state_name} based on state regulations and risk factors."
                )
        
        print(f"Created {StateRegulation.objects.count()} state regulations and {StateRateAdjustment.objects.count()} rate adjustments.")
    
    return True

def fix_database():
    """Complete database fix for insurance calculator"""
    try:
        print("\n==== FIXING INSURANCE CALCULATOR DATABASE ====\n")
        
        # Check for required models
        print("Checking database status...")
        insurance_types = InsuranceType.objects.count()
        base_rates = InsuranceBaseRate.objects.count()
        cso_tables = CSOMortalityTable.objects.count()
        risk_factors = InsuranceRiskFactor.objects.count()
        inv_returns = InsuranceInvestmentReturn.objects.count()
        state_adjustments = StateRateAdjustment.objects.count()
        
        print(f"Insurance Types: {insurance_types}")
        print(f"Base Rates: {base_rates}")
        print(f"CSO Mortality Tables: {cso_tables}")
        print(f"Risk Factors: {risk_factors}")
        print(f"Investment Returns: {inv_returns}")
        print(f"State Rate Adjustments: {state_adjustments}")
        
        # Create base rates
        if base_rates == 0:
            print("\nCreating insurance base rates...")
            success = create_base_rates()
            if not success:
                print("Failed to create base rates. Exiting.")
                return False
            base_rates = InsuranceBaseRate.objects.count()
            print(f"Now have {base_rates} base rates.")
        
        # Create other required data
        if cso_tables == 0 or risk_factors == 0 or inv_returns == 0 or state_adjustments == 0:
            print("\nCreating additional required data...")
            success = create_placeholder_data()
            if not success:
                print("Failed to create placeholder data. Exiting.")
                return False
        
        print("\n==== DATABASE FIX COMPLETED SUCCESSFULLY ====")
        print(f"Insurance Types: {InsuranceType.objects.count()}")
        print(f"Base Rates: {InsuranceBaseRate.objects.count()}")
        print(f"CSO Mortality Tables: {CSOMortalityTable.objects.count()}")
        print(f"Risk Factors: {InsuranceRiskFactor.objects.count()}")
        print(f"Risk Factor Values: {RiskFactorValue.objects.count()}")
        print(f"Investment Returns: {InsuranceInvestmentReturn.objects.count()}")
        print(f"State Rate Adjustments: {StateRateAdjustment.objects.count()}")
        print(f"State Regulations: {StateRegulation.objects.count()}")
        print(f"Disclaimers: {DisclaimerText.objects.count()}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fix_database()
    if success:
        print("\nDatabase fix completed successfully. Insurance calculator should now work properly.")
        sys.exit(0)
    else:
        print("\nDatabase fix failed. Please check the error messages above.")
        sys.exit(1) 