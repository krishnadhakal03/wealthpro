#!/usr/bin/env python
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wealthpro.settings')
django.setup()

from main.models import CSOMortalityTable, InsuranceRiskFactor, RiskFactorValue, DisclaimerText, StateRegulation, InsuranceType

def populate_cso_tables():
    """
    Populate CSO Mortality Tables with 2017 CSO Table values
    Data is simplified but representative of actual values
    """
    print("Populating 2017 CSO Mortality Tables...")
    
    # Clear existing data
    # CSOMortalityTable.objects.all().delete()
    
    # 2017 CSO Mortality Table - simplified version
    # Based on actual 2017 CSO table values
    # Format: age, male_nonsmoker, male_smoker, female_nonsmoker, female_smoker
    mortality_data = [
        # Age, M-NS, M-S, F-NS, F-S (rates per 1,000)
        (18, 0.608, 1.216, 0.373, 0.746),
        (19, 0.645, 1.290, 0.385, 0.770),
        (20, 0.682, 1.364, 0.397, 0.794),
        (21, 0.747, 1.494, 0.406, 0.812),
        (22, 0.815, 1.630, 0.416, 0.832),
        (23, 0.865, 1.730, 0.426, 0.852),
        (24, 0.915, 1.830, 0.437, 0.874),
        (25, 0.953, 1.906, 0.450, 0.900),
        (26, 0.978, 1.956, 0.465, 0.930),
        (27, 1.003, 2.006, 0.480, 0.960),
        (28, 1.028, 2.056, 0.498, 0.996),
        (29, 1.053, 2.106, 0.518, 1.036),
        (30, 1.082, 2.164, 0.538, 1.076),
        (31, 1.113, 2.226, 0.560, 1.120),
        (32, 1.147, 2.294, 0.584, 1.168),
        (33, 1.182, 2.364, 0.610, 1.220),
        (34, 1.222, 2.444, 0.638, 1.276),
        (35, 1.265, 2.530, 0.669, 1.338),
        (36, 1.315, 2.630, 0.703, 1.406),
        (37, 1.370, 2.740, 0.739, 1.478),
        (38, 1.432, 2.864, 0.780, 1.560),
        (39, 1.502, 3.004, 0.824, 1.648),
        (40, 1.580, 3.160, 0.873, 1.746),
        (41, 1.667, 3.334, 0.926, 1.852),
        (42, 1.765, 3.530, 0.984, 1.968),
        (43, 1.875, 3.750, 1.047, 2.094),
        (44, 1.997, 3.994, 1.116, 2.232),
        (45, 2.132, 4.264, 1.191, 2.382),
        (46, 2.283, 4.566, 1.272, 2.544),
        (47, 2.448, 4.896, 1.359, 2.718),
        (48, 2.630, 5.260, 1.454, 2.908),
        (49, 2.830, 5.660, 1.558, 3.116),
        (50, 3.048, 6.096, 1.671, 3.342),
        (51, 3.287, 6.574, 1.793, 3.586),
        (52, 3.548, 7.096, 1.925, 3.850),
        (53, 3.833, 7.666, 2.067, 4.134),
        (54, 4.145, 8.290, 2.219, 4.438),
        (55, 4.485, 8.970, 2.384, 4.768),
        (56, 4.857, 9.714, 2.561, 5.122),
        (57, 5.265, 10.53, 2.752, 5.504),
        (58, 5.712, 11.424, 2.959, 5.918),
        (59, 6.200, 12.40, 3.182, 6.364),
        (60, 6.733, 13.466, 3.426, 6.852),
        (61, 7.314, 14.628, 3.691, 7.382),
        (62, 7.952, 15.904, 3.981, 7.962),
        (63, 8.647, 17.294, 4.298, 8.596),
        (64, 9.410, 18.82, 4.647, 9.294),
        (65, 10.247, 20.494, 5.033, 10.066),
        (66, 11.167, 22.334, 5.462, 10.924),
        (67, 12.178, 24.356, 5.939, 11.878),
        (68, 13.290, 26.58, 6.472, 12.944),
        (69, 14.518, 29.036, 7.069, 14.138),
        (70, 15.871, 31.742, 7.737, 15.474),
        (71, 17.364, 34.728, 8.487, 16.974),
        (72, 19.012, 38.024, 9.328, 18.656),
        (73, 20.832, 41.664, 10.275, 20.55),
        (74, 22.843, 45.686, 11.340, 22.68),
        (75, 25.061, 50.122, 12.540, 25.08),
        (76, 27.505, 55.01, 13.895, 27.79),
        (77, 30.194, 60.388, 15.424, 30.848),
        (78, 33.151, 66.302, 17.147, 34.294),
        (79, 36.398, 72.796, 19.084, 38.168),
        (80, 39.962, 79.924, 21.259, 42.518),
        (81, 43.869, 87.738, 23.686, 47.372),
        (82, 48.142, 96.284, 26.389, 52.778),
        (83, 52.799, 105.598, 29.385, 58.77),
        (84, 57.855, 115.71, 32.695, 65.39),
        (85, 63.341, 126.682, 36.345, 72.69),
        (86, 69.279, 138.558, 40.357, 80.714),
        (87, 75.687, 151.374, 44.767, 89.534),
        (88, 82.592, 165.184, 49.598, 99.196),
        (89, 90.021, 180.042, 54.882, 109.764),
        (90, 98.002, 196.004, 60.642, 121.284),
        (91, 106.562, 213.124, 66.908, 133.816),
        (92, 115.731, 231.462, 73.711, 147.422),
        (93, 125.534, 251.068, 81.086, 162.172),
        (94, 136.002, 272.004, 89.061, 178.122),
        (95, 147.155, 294.31, 97.664, 195.328),
        (96, 159.014, 318.028, 106.927, 213.854),
        (97, 171.603, 343.206, 116.882, 233.764),
        (98, 184.932, 369.864, 127.56, 255.12),
        (99, 199.011, 398.022, 139.004, 278.008),
        (100, 213.869, 427.738, 151.244, 302.488),
    ]
    
    # Create entries for each age and category
    count = 0
    for age, m_ns, m_s, f_ns, f_s in mortality_data:
        # Male non-smoker
        CSOMortalityTable.objects.get_or_create(
            age=age,
            gender='M',
            smoker_status='NS',
            defaults={
                'mortality_rate': Decimal(str(m_ns)),
                'table_version': '2017 CSO'
            }
        )
        
        # Male smoker
        CSOMortalityTable.objects.get_or_create(
            age=age,
            gender='M',
            smoker_status='SM',
            defaults={
                'mortality_rate': Decimal(str(m_s)),
                'table_version': '2017 CSO'
            }
        )
        
        # Female non-smoker
        CSOMortalityTable.objects.get_or_create(
            age=age,
            gender='F',
            smoker_status='NS',
            defaults={
                'mortality_rate': Decimal(str(f_ns)),
                'table_version': '2017 CSO'
            }
        )
        
        # Female smoker
        CSOMortalityTable.objects.get_or_create(
            age=age,
            gender='F',
            smoker_status='SM',
            defaults={
                'mortality_rate': Decimal(str(f_s)),
                'table_version': '2017 CSO'
            }
        )
        
        count += 4
    
    print(f"Added {count} CSO Mortality Table entries.")
    
    # Create aggregate entries for "ANY" smoker status
    for age in range(18, 101):
        for gender in ['M', 'F']:
            # Get the specific entries
            smoker = CSOMortalityTable.objects.get(age=age, gender=gender, smoker_status='SM')
            non_smoker = CSOMortalityTable.objects.get(age=age, gender=gender, smoker_status='NS')
            
            # Calculate weighted average (assuming 75% non-smokers, 25% smokers)
            avg_rate = (non_smoker.mortality_rate * Decimal('0.75')) + (smoker.mortality_rate * Decimal('0.25'))
            
            # Create or update the ANY entry
            CSOMortalityTable.objects.get_or_create(
                age=age,
                gender=gender,
                smoker_status='ANY',
                defaults={
                    'mortality_rate': avg_rate,
                    'table_version': '2017 CSO'
                }
            )
    
    print(f"Added aggregate entries for smoker status 'ANY'")
    print("CSO Mortality Tables population complete!")

def populate_risk_factors():
    """Populate risk factors for different insurance types"""
    print("Populating insurance risk factors...")
    
    # Life Insurance Risk Factors
    life_factors = [
        {
            'name': 'Smoker Status',
            'description': 'Smoking status affects mortality risk substantially',
            'values': [
                ('Non-smoker', '1.0'),
                ('Occasional smoker', '1.5'),
                ('Regular smoker', '2.0'),
                ('Heavy smoker', '2.5'),
            ]
        },
        {
            'name': 'Family History',
            'description': 'Family history of serious medical conditions',
            'values': [
                ('No history', '1.0'),
                ('History of cancer', '1.3'),
                ('History of heart disease', '1.4'),
                ('History of diabetes', '1.2'),
                ('Multiple conditions', '1.6'),
            ]
        },
        {
            'name': 'Occupation Risk',
            'description': 'Risk level associated with occupation',
            'values': [
                ('Low risk', '1.0'),
                ('Moderate risk', '1.2'),
                ('High risk', '1.5'),
                ('Very high risk', '2.0'),
            ]
        },
        {
            'name': 'BMI Category',
            'description': 'Body Mass Index category affecting health risks',
            'values': [
                ('Normal weight', '1.0'),
                ('Overweight', '1.15'),
                ('Obese', '1.35'),
                ('Severely obese', '1.7'),
            ]
        },
    ]
    
    # Health Insurance Risk Factors
    health_factors = [
        {
            'name': 'Pre-existing Conditions',
            'description': 'Major pre-existing health conditions',
            'values': [
                ('None', '1.0'),
                ('Diabetes', '1.3'),
                ('Hypertension', '1.25'),
                ('Heart disease', '1.4'),
                ('Cancer history', '1.5'),
                ('Multiple conditions', '1.8'),
            ]
        },
        {
            'name': 'Lifestyle',
            'description': 'Overall lifestyle health assessment',
            'values': [
                ('Excellent', '0.9'),
                ('Good', '1.0'),
                ('Fair', '1.2'),
                ('Poor', '1.4'),
            ]
        },
        {
            'name': 'Prescription Medications',
            'description': 'Number of regular prescription medications',
            'values': [
                ('None', '1.0'),
                ('1-2 medications', '1.1'),
                ('3-5 medications', '1.3'),
                ('More than 5', '1.5'),
            ]
        },
    ]
    
    # Auto Insurance Risk Factors
    auto_factors = [
        {
            'name': 'Driving Record',
            'description': 'History of driving violations and accidents',
            'values': [
                ('Clean record', '0.9'),
                ('Minor violations', '1.1'),
                ('Major violations', '1.5'),
                ('DUI history', '2.0'),
                ('Multiple accidents', '1.7'),
            ]
        },
        {
            'name': 'Vehicle Type',
            'description': 'Type and category of vehicle',
            'values': [
                ('Economy sedan', '1.0'),
                ('Mid-size sedan', '1.1'),
                ('SUV', '1.2'),
                ('Luxury vehicle', '1.3'),
                ('Sports car', '1.5'),
                ('High-performance', '1.8'),
            ]
        },
        {
            'name': 'Annual Mileage',
            'description': 'Miles driven annually',
            'values': [
                ('Under 5,000', '0.9'),
                ('5,000-10,000', '1.0'),
                ('10,001-15,000', '1.1'),
                ('15,001-20,000', '1.2'),
                ('Over 20,000', '1.3'),
            ]
        },
        {
            'name': 'Vehicle Age',
            'description': 'Age of the insured vehicle',
            'values': [
                ('New (0-3 years)', '1.2'),
                ('Recent (4-7 years)', '1.0'),
                ('Older (8-12 years)', '0.9'),
                ('Vintage (12+ years)', '1.1'),
            ]
        },
    ]
    
    # Home Insurance Risk Factors
    home_factors = [
        {
            'name': 'Construction Type',
            'description': 'Primary construction material of the home',
            'values': [
                ('Brick/Masonry', '0.9'),
                ('Wood Frame', '1.1'),
                ('Steel Frame', '0.95'),
                ('Mixed Materials', '1.0'),
            ]
        },
        {
            'name': 'Roof Age',
            'description': 'Age of the roof in years',
            'values': [
                ('New (0-5 years)', '0.9'),
                ('Mid-age (6-15 years)', '1.0'),
                ('Older (16-25 years)', '1.2'),
                ('Very old (25+ years)', '1.4'),
            ]
        },
        {
            'name': 'Location Risk',
            'description': 'Risk based on geographic location',
            'values': [
                ('Low risk area', '0.9'),
                ('Moderate risk', '1.0'),
                ('High risk - flood zone', '1.4'),
                ('High risk - wildfire', '1.5'),
                ('High risk - hurricane', '1.6'),
                ('Multiple hazards', '1.8'),
            ]
        },
        {
            'name': 'Security Features',
            'description': 'Home security and safety systems',
            'values': [
                ('Comprehensive security', '0.8'),
                ('Basic security', '0.9'),
                ('Minimal security', '1.0'),
                ('No security features', '1.1'),
            ]
        },
    ]
    
    # Process and create all risk factors
    factor_groups = [
        ('LIFE', life_factors),
        ('HEALTH', health_factors),
        ('AUTO', auto_factors),
        ('HOME', home_factors),
    ]
    
    total_factors = 0
    total_values = 0
    
    for factor_type, factors in factor_groups:
        for factor_data in factors:
            # Create the risk factor
            risk_factor, created = InsuranceRiskFactor.objects.get_or_create(
                name=factor_data['name'],
                factor_type=factor_type,
                defaults={
                    'description': factor_data['description']
                }
            )
            
            if created:
                total_factors += 1
            
            # Create the risk factor values
            for value_name, multiplier in factor_data['values']:
                value, value_created = RiskFactorValue.objects.get_or_create(
                    risk_factor=risk_factor,
                    value_name=value_name,
                    defaults={
                        'multiplier': Decimal(multiplier)
                    }
                )
                
                if value_created:
                    total_values += 1
    
    print(f"Added {total_factors} risk factors with {total_values} values.")

def create_insurance_disclaimers():
    """Create legal disclaimers for the insurance calculator"""
    print("Creating insurance disclaimers...")
    
    # General disclaimer for all insurance types
    general_disclaimer = """
    <p>DISCLAIMER: This calculator provides ESTIMATES ONLY and is for informational purposes only. The actual premium you may pay for any insurance product will depend on a comprehensive evaluation of your application and underwriting by the insurance company.</p>
    
    <p>Factors not considered in this calculator that may affect your actual premium include but are not limited to: detailed medical history, credit score, specific location details, complete driving history, exact home characteristics, and other risk-related information collected during the formal application process.</p>
    
    <p>The results provided by this calculator are not a guarantee of insurability or premium amount. Final determination of insurance rates, coverage eligibility, and policy terms can only be made by the insurer after a complete application and underwriting process.</p>
    
    <p>Please consult with a licensed insurance professional before making any insurance decisions.</p>
    """
    
    # Type-specific disclaimers
    disclaimers = {
        'Life': """
        <p>Life insurance premium calculations use simplified mortality assumptions based on the 2017 Commissioners Standard Ordinary (CSO) Mortality Tables. Actual underwriting will involve a more detailed evaluation of health and risk factors.</p>
        
        <p>Investment returns shown for permanent life insurance policies represent non-guaranteed illustrations based on current company crediting rates and are subject to change. Only the guaranteed minimum interest rate, which is lower than illustrated, is guaranteed by the insurer.</p>
        
        <p>This calculator does not account for all available riders and policy options that may affect premiums and benefits.</p>
        """,
        
        'Health': """
        <p>Health insurance premium estimates do not account for specific plan deductibles, coinsurance, copays, or out-of-pocket maximums. Actual plan options and costs will vary by insurer.</p>
        
        <p>Subsidies or tax credits that may reduce your premium costs are not calculated here. You may qualify for financial assistance through federal or state programs.</p>
        
        <p>This calculator does not account for all medical conditions or treatments that may affect insurability or premium rates.</p>
        
        <p>Due to the Affordable Care Act, some factors shown may not affect actual premiums for ACA-compliant plans in your state.</p>
        """,
        
        'Auto': """
        <p>Auto insurance premium estimates are based on general risk factors and do not account for your specific driving record, credit history, or exact location details that insurers use for rating.</p>
        
        <p>No-fault states and states with specific insurance requirements may have different baseline premiums than shown here.</p>
        
        <p>Discounts for multi-policy, safe driver programs, telematics devices, or other special programs are not fully accounted for in this estimate.</p>
        """,
        
        'Home': """
        <p>Home insurance premium estimates do not account for specific property characteristics, exact construction details, proximity to fire stations, or specific natural hazard exposure that would be evaluated in a full underwriting process.</p>
        
        <p>Replacement cost calculations are estimates and may differ from actual rebuilding costs in your area.</p>
        
        <p>This calculator provides estimates for standard homeowners insurance (HO-3 policy) and does not include flood, earthquake, or other specialized coverage that may be required or recommended for your property.</p>
        """
    }
    
    # Create the disclaimers
    for insurance_type in InsuranceType.objects.all():
        # Create general disclaimer
        DisclaimerText.objects.get_or_create(
            insurance_type=insurance_type,
            title="General Calculator Disclaimer",
            defaults={
                'content': general_disclaimer,
                'is_active': True,
            }
        )
        
        # Create specific disclaimer if available
        if insurance_type.name in disclaimers:
            DisclaimerText.objects.get_or_create(
                insurance_type=insurance_type,
                title=f"{insurance_type.name} Insurance Specific Disclaimer",
                defaults={
                    'content': disclaimers[insurance_type.name],
                    'is_active': True,
                }
            )
    
    print("Disclaimers created successfully!")

def create_state_regulations():
    """Create sample state regulations for insurance types"""
    print("Creating state insurance regulations...")
    
    from main.models import InsuranceType, StateRegulation
    from decimal import Decimal
    
    regulations = [
        # Life insurance regulations
        {
            'type': 'Life',
            'state': 'NY',
            'min_coverage': None,
            'special_requirements': 'New York requires specific disclosure forms including Regulation 60 disclosures for replacements and special free-look provisions.',
            'filing_requirements': 'All life insurance policies must be filed with and approved by the NY Department of Financial Services.'
        },
        {
            'type': 'Life',
            'state': 'CA',
            'min_coverage': None,
            'special_requirements': 'California requires a specific illustration and disclosure format and has unique requirements for policy loans and nonforfeiture provisions.',
            'filing_requirements': 'File with the CA Department of Insurance. Policy forms must be compliant with California-specific regulations.'
        },
        
        # Auto insurance regulations
        {
            'type': 'Auto',
            'state': 'MI',
            'min_coverage': Decimal('50000.00'),
            'special_requirements': 'Michigan has a unique no-fault insurance system with unlimited personal injury protection (PIP) requirements with recent reforms allowing for coverage level selection.',
            'filing_requirements': 'Rate filings must be approved by the Michigan Department of Insurance and Financial Services.'
        },
        {
            'type': 'Auto',
            'state': 'FL',
            'min_coverage': Decimal('10000.00'),
            'special_requirements': 'Florida requires Personal Injury Protection (PIP) coverage of $10,000 and Property Damage Liability of $10,000.',
            'filing_requirements': 'File with the Florida Office of Insurance Regulation.'
        },
        {
            'type': 'Auto',
            'state': 'NJ',
            'min_coverage': Decimal('15000.00'),
            'special_requirements': 'New Jersey has a choice no-fault system with specific PIP requirements and coverage options.',
            'filing_requirements': 'File with the NJ Department of Banking and Insurance.'
        },
        
        # Health insurance regulations
        {
            'type': 'Health',
            'state': 'MA',
            'min_coverage': None,
            'special_requirements': 'Massachusetts has its own health care reform laws in addition to the ACA, with specific minimum creditable coverage standards.',
            'filing_requirements': 'All plans must be filed with and approved by the MA Division of Insurance.'
        },
        {
            'type': 'Health',
            'state': 'CA',
            'min_coverage': None,
            'special_requirements': 'California has expanded ACA provisions and specific requirements for essential health benefits.',
            'filing_requirements': 'Rate review through the Department of Managed Health Care or CA Department of Insurance.'
        },
        
        # Home insurance regulations
        {
            'type': 'Home',
            'state': 'FL',
            'min_coverage': None,
            'special_requirements': 'Florida requires specific hurricane deductible disclosures and mitigation options. Separate hurricane/windstorm deductibles apply.',
            'filing_requirements': 'File with Florida Office of Insurance Regulation. Rate increases over 15% require public hearings.'
        },
        {
            'type': 'Home',
            'state': 'TX',
            'min_coverage': None,
            'special_requirements': 'Texas allows for percentage deductibles for wind/hail damage and has specific disclosure requirements for replacement cost coverage.',
            'filing_requirements': 'File and use system with the Texas Department of Insurance.'
        },
        {
            'type': 'Home',
            'state': 'CA',
            'min_coverage': None,
            'special_requirements': 'California requires specific earthquake insurance offerings and disclosures. FAIR Plan for high fire risk areas.',
            'filing_requirements': 'Prior approval required from the CA Department of Insurance for rates and forms.'
        },
    ]
    
    # Create the regulations
    count = 0
    for reg in regulations:
        insurance_type = InsuranceType.objects.filter(name=reg['type']).first()
        if insurance_type:
            _, created = StateRegulation.objects.get_or_create(
                insurance_type=insurance_type,
                state=reg['state'],
                defaults={
                    'min_coverage_required': reg['min_coverage'],
                    'special_requirements': reg['special_requirements'],
                    'filing_requirements': reg['filing_requirements'],
                }
            )
            if created:
                count += 1
    
    print(f"Created {count} state insurance regulations.")

if __name__ == "__main__":
    print("Starting data population...")
    populate_cso_tables()
    populate_risk_factors()
    create_insurance_disclaimers()
    create_state_regulations()
    print("All data population complete!") 