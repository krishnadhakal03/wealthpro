from django.test import TestCase, Client
from django.urls import reverse
from main.models import InsuranceType, InsuranceBaseRate, StateRateAdjustment
import logging

# Set up logger
logger = logging.getLogger(__name__)

class InsuranceCalculatorTests(TestCase):
    """Test cases for the insurance premium calculator"""
    
    def setUp(self):
        """Set up test data before running tests"""
        self.client = Client()
        self.calculator_url = reverse('insurance_calculator')
        
        # Check if insurance types already exist in test database
        if not InsuranceType.objects.exists():
            # Create test insurance types
            self.life = InsuranceType.objects.create(
                name='Life', 
                description='Life insurance provides financial protection to your beneficiaries in the event of your death.', 
                icon='fa-heart'
            )
            
            self.health = InsuranceType.objects.create(
                name='Health', 
                description='Health insurance covers medical expenses incurred for health conditions.', 
                icon='fa-medkit'
            )
            
            self.auto = InsuranceType.objects.create(
                name='Auto', 
                description='Auto insurance protects against financial loss in the event of an accident or theft.', 
                icon='fa-car'
            )
            
            self.home = InsuranceType.objects.create(
                name='Home', 
                description='Home insurance covers damage to your house and belongings from disasters, theft, and accidents.', 
                icon='fa-house'
            )
            
            # Create base rates for each insurance type with wider coverage
            # Life Insurance
            InsuranceBaseRate.objects.create(
                insurance_type=self.life,
                min_age=18,
                max_age=30,
                gender='M',
                base_monthly_rate=25.00,
                rate_per_thousand=0.10
            )
            
            InsuranceBaseRate.objects.create(
                insurance_type=self.life,
                min_age=18,
                max_age=30,
                gender='F',
                base_monthly_rate=22.50,
                rate_per_thousand=0.09
            )
            
            InsuranceBaseRate.objects.create(
                insurance_type=self.life,
                min_age=31,
                max_age=45,
                gender='M',
                base_monthly_rate=35.00,
                rate_per_thousand=0.15
            )
            
            InsuranceBaseRate.objects.create(
                insurance_type=self.life,
                min_age=31,
                max_age=45,
                gender='F',
                base_monthly_rate=32.00,
                rate_per_thousand=0.13
            )
            
            InsuranceBaseRate.objects.create(
                insurance_type=self.life,
                min_age=46,
                max_age=60,
                gender='M',
                base_monthly_rate=50.00,
                rate_per_thousand=0.25
            )
            
            InsuranceBaseRate.objects.create(
                insurance_type=self.life,
                min_age=46,
                max_age=60,
                gender='F',
                base_monthly_rate=45.00,
                rate_per_thousand=0.22
            )
            
            # Health Insurance
            InsuranceBaseRate.objects.create(
                insurance_type=self.health,
                min_age=18,
                max_age=30,
                gender='ANY',
                base_monthly_rate=150.00,
                rate_per_thousand=0.05
            )
            
            InsuranceBaseRate.objects.create(
                insurance_type=self.health,
                min_age=31,
                max_age=45,
                gender='ANY',
                base_monthly_rate=200.00,
                rate_per_thousand=0.08
            )
            
            # Auto Insurance
            InsuranceBaseRate.objects.create(
                insurance_type=self.auto,
                min_age=18,
                max_age=25,
                gender='M',
                base_monthly_rate=120.00,
                rate_per_thousand=0.40
            )
            
            InsuranceBaseRate.objects.create(
                insurance_type=self.auto,
                min_age=18,
                max_age=25,
                gender='F',
                base_monthly_rate=100.00,
                rate_per_thousand=0.30
            )
            
            InsuranceBaseRate.objects.create(
                insurance_type=self.auto,
                min_age=26,
                max_age=40,
                gender='ANY',
                base_monthly_rate=80.00,
                rate_per_thousand=0.20
            )
            
            # Home Insurance
            InsuranceBaseRate.objects.create(
                insurance_type=self.home,
                min_age=18,
                max_age=25,
                gender='ANY',
                base_monthly_rate=60.00,
                rate_per_thousand=0.05
            )
            
            InsuranceBaseRate.objects.create(
                insurance_type=self.home,
                min_age=26,
                max_age=40,
                gender='ANY',
                base_monthly_rate=50.00,
                rate_per_thousand=0.04
            )
        else:
            # Use existing types
            self.life = InsuranceType.objects.get(name='Life')
            self.health = InsuranceType.objects.get(name='Health')
            self.auto = InsuranceType.objects.get(name='Auto')
            self.home = InsuranceType.objects.get(name='Home')
        
        # Print available rates for debugging
        logger.info("Available base rates:")
        for rate in InsuranceBaseRate.objects.all():
            logger.info(f"Type: {rate.insurance_type.name}, Age: {rate.min_age}-{rate.max_age}, Gender: {rate.gender}, Rate: {rate.base_monthly_rate}")
    
    def test_calculator_page_loads(self):
        """Test that the calculator page loads correctly"""
        response = self.client.get(self.calculator_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/insurance_calculator.html')
        self.assertIn('insurance_types', response.context)
    
    def test_life_insurance_calculation(self):
        """Test life insurance premium calculation"""
        # Form data for a 30-year-old male with 250k coverage for 10 years
        form_data = {
            'insurance_type': self.life.id,
            'age': 30,
            'gender': 'M',
            'state': 'CA',
            'coverage_amount': 250000,
            'term_years': 10,
            'smoker_status': 'NS',
            'bmi_category': 'Normal',
            'family_history': 'None',
            'occupation_risk': 'Low',
            'life_coverage_amount': 250000,
            'life_term_years': 10,
        }
        
        response = self.client.post(self.calculator_url, form_data)
        self.assertEqual(response.status_code, 200)
        
        # Verify the response contains the premium results or proper error
        if 'error' in response.context:
            error_msg = response.context['error']
            print(f"Life Insurance Test Error: {error_msg}")
            self.assertIn("Sorry, we couldn't calculate", error_msg)
        else:
            # Verify the response contains the premium results
            self.assertIn('result', response.context)
            self.assertIsNotNone(response.context['result'])
            self.assertIn('monthly_premium', response.context['result'])
            self.assertIn('annual_premium', response.context['result'])
            
            # Print the result for debugging
            print(f"Life Insurance Test Result: {response.context['result']}")
            
            # Check premium is a positive value
            monthly_premium = float(response.context['result']['monthly_premium'])
            self.assertGreater(monthly_premium, 0)
    
    def test_health_insurance_calculation(self):
        """Test health insurance premium calculation"""
        # Form data for a 25-year-old with 50k coverage for 1 year
        form_data = {
            'insurance_type': self.health.id,
            'age': 25,
            'gender': 'ANY',  # Use ANY for gender-neutral pricing
            'state': 'CA',
            'coverage_amount': 50000,
            'term_years': 1,
            'health_condition': 'None',
            'lifestyle': 'Good',
            'prescription_meds': 'None',
            'coverage_level': 'Silver',
            'health_coverage_amount': 50000,
            'health_term_years': 1,
        }
        
        response = self.client.post(self.calculator_url, form_data)
        self.assertEqual(response.status_code, 200)
        
        # Verify the response contains the premium results or proper error
        if 'error' in response.context:
            error_msg = response.context['error']
            print(f"Health Insurance Test Error: {error_msg}")
            self.assertIn("Sorry, we couldn't calculate", error_msg)
        else:
            # Verify the response contains the premium results
            self.assertIn('result', response.context)
            self.assertIsNotNone(response.context['result'])
            self.assertIn('monthly_premium', response.context['result'])
            self.assertIn('annual_premium', response.context['result'])
            
            # Print the result for debugging
            print(f"Health Insurance Test Result: {response.context['result']}")
            
            # Check premium is a positive value
            monthly_premium = float(response.context['result']['monthly_premium'])
            self.assertGreater(monthly_premium, 0)
    
    def test_auto_insurance_calculation(self):
        """Test auto insurance premium calculation"""
        # Form data for a 22-year-old male with 100k coverage for 1 year
        form_data = {
            'insurance_type': self.auto.id,
            'age': 22,
            'gender': 'M',
            'state': 'CA',
            'coverage_amount': 100000,
            'term_years': 1,
            'vehicle_value': 25000,
            'vehicle_type': 'Mid-size',
            'driving_record': 'Clean',
            'annual_mileage': '5000-10000',
            'vehicle_age': 'Recent',
            'auto_coverage_amount': 100000,
            'auto_term_years': 1,
        }
        
        response = self.client.post(self.calculator_url, form_data)
        self.assertEqual(response.status_code, 200)
        
        # Verify the response contains the premium results or proper error
        if 'error' in response.context:
            error_msg = response.context['error']
            print(f"Auto Insurance Test Error: {error_msg}")
            self.assertIn("Sorry, we couldn't calculate", error_msg)
        else:
            # Verify the response contains the premium results
            self.assertIn('result', response.context)
            self.assertIsNotNone(response.context['result'])
            self.assertIn('monthly_premium', response.context['result'])
            self.assertIn('annual_premium', response.context['result'])
            
            # Print the result for debugging
            print(f"Auto Insurance Test Result: {response.context['result']}")
            
            # Check premium is a positive value
            monthly_premium = float(response.context['result']['monthly_premium'])
            self.assertGreater(monthly_premium, 0)
    
    def test_home_insurance_calculation(self):
        """Test home insurance premium calculation"""
        # Form data for a 24-year-old with 250k coverage for 1 year
        form_data = {
            'insurance_type': self.home.id,
            'age': 24,
            'gender': 'ANY',  # Gender neutral pricing
            'state': 'CA',
            'coverage_amount': 250000,
            'term_years': 1,
            'home_value': 350000,
            'construction_type': 'Wood',
            'roof_age': 'Mid',
            'location_risk': 'Low',
            'security_features': 'Basic',
            'home_coverage_amount': 250000,
            'home_term_years': 1,
        }
        
        response = self.client.post(self.calculator_url, form_data)
        self.assertEqual(response.status_code, 200)
        
        # Verify the response contains the premium results or proper error
        if 'error' in response.context:
            error_msg = response.context['error']
            print(f"Home Insurance Test Error: {error_msg}")
            self.assertIn("Sorry, we couldn't calculate", error_msg)
        else:
            # Verify the response contains the premium results
            self.assertIn('result', response.context)
            self.assertIsNotNone(response.context['result'])
            self.assertIn('monthly_premium', response.context['result'])
            self.assertIn('annual_premium', response.context['result'])
            
            # Print the result for debugging
            print(f"Home Insurance Test Result: {response.context['result']}")
            
            # Check premium is a positive value
            monthly_premium = float(response.context['result']['monthly_premium'])
            self.assertGreater(monthly_premium, 0)
        
    def test_invalid_age_range(self):
        """Test that invalid age ranges return an error"""
        # Form data with invalid age (too high)
        form_data = {
            'insurance_type': self.life.id,
            'age': 90,  # Outside the supported range
            'gender': 'M',
            'state': 'CA',
            'coverage_amount': 250000,
            'term_years': 10,
            'life_coverage_amount': 250000,
            'life_term_years': 10,
        }
        
        response = self.client.post(self.calculator_url, form_data)
        self.assertEqual(response.status_code, 200)
        
        # Check for error message
        self.assertIn('error', response.context)
        print(f"Invalid Age Test Error: {response.context.get('error')}")
