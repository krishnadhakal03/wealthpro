import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from main.models import InsuranceType, InsuranceBaseRate, InsuranceInvestmentReturn, StateRateAdjustment
from decimal import Decimal

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create sample insurance data for the calculator'

    def handle(self, *args, **kwargs):
        try:
            # Use transaction to ensure all or nothing
            with transaction.atomic():
                # Delete existing data
                self.stdout.write('Deleting existing insurance data...')
                InsuranceBaseRate.objects.all().delete()
                InsuranceInvestmentReturn.objects.all().delete()
                StateRateAdjustment.objects.all().delete()
                InsuranceType.objects.all().delete()
                
                # Create insurance types
                self.stdout.write('Creating insurance types...')
                life = InsuranceType.objects.create(
                    name='Life',
                    description='Life insurance provides financial protection for your family in case of your death.',
                    icon='fa-heart-pulse'
                )
                
                health = InsuranceType.objects.create(
                    name='Health',
                    description='Health insurance covers medical expenses for illnesses, injuries, and preventive care.',
                    icon='fa-hospital'
                )
                
                auto = InsuranceType.objects.create(
                    name='Auto',
                    description='Auto insurance protects against financial loss in the event of an accident or theft.',
                    icon='fa-car'
                )
                
                home = InsuranceType.objects.create(
                    name='Home',
                    description='Home insurance covers damage to your house and belongings from disasters, theft, and accidents.',
                    icon='fa-house'
                )
                
                # Create base rates for Life insurance
                self.stdout.write('Creating base rates for Life insurance...')
                InsuranceBaseRate.objects.create(
                    insurance_type=life,
                    min_age=18,
                    max_age=30,
                    gender='M',
                    base_monthly_rate=Decimal('20.00'),
                    rate_per_thousand=Decimal('0.10')
                )
                
                InsuranceBaseRate.objects.create(
                    insurance_type=life,
                    min_age=18,
                    max_age=30,
                    gender='F',
                    base_monthly_rate=Decimal('18.00'),
                    rate_per_thousand=Decimal('0.08')
                )
                
                InsuranceBaseRate.objects.create(
                    insurance_type=life,
                    min_age=31,
                    max_age=45,
                    gender='M',
                    base_monthly_rate=Decimal('25.00'),
                    rate_per_thousand=Decimal('0.15')
                )
                
                InsuranceBaseRate.objects.create(
                    insurance_type=life,
                    min_age=31,
                    max_age=45,
                    gender='F',
                    base_monthly_rate=Decimal('22.00'),
                    rate_per_thousand=Decimal('0.12')
                )
                
                InsuranceBaseRate.objects.create(
                    insurance_type=life,
                    min_age=46,
                    max_age=60,
                    gender='M',
                    base_monthly_rate=Decimal('40.00'),
                    rate_per_thousand=Decimal('0.30')
                )
                
                InsuranceBaseRate.objects.create(
                    insurance_type=life,
                    min_age=46,
                    max_age=60,
                    gender='F',
                    base_monthly_rate=Decimal('35.00'),
                    rate_per_thousand=Decimal('0.25')
                )
                
                # Create base rates for Health insurance
                self.stdout.write('Creating base rates for Health insurance...')
                InsuranceBaseRate.objects.create(
                    insurance_type=health,
                    min_age=18,
                    max_age=30,
                    gender='ANY',
                    base_monthly_rate=Decimal('150.00'),
                    rate_per_thousand=Decimal('0.05')
                )
                
                InsuranceBaseRate.objects.create(
                    insurance_type=health,
                    min_age=31,
                    max_age=45,
                    gender='ANY',
                    base_monthly_rate=Decimal('200.00'),
                    rate_per_thousand=Decimal('0.10')
                )
                
                InsuranceBaseRate.objects.create(
                    insurance_type=health,
                    min_age=46,
                    max_age=60,
                    gender='ANY',
                    base_monthly_rate=Decimal('300.00'),
                    rate_per_thousand=Decimal('0.20')
                )
                
                # Create base rates for Auto insurance
                self.stdout.write('Creating base rates for Auto insurance...')
                InsuranceBaseRate.objects.create(
                    insurance_type=auto,
                    min_age=18,
                    max_age=25,
                    gender='M',
                    base_monthly_rate=Decimal('120.00'),
                    rate_per_thousand=Decimal('0.40')
                )
                
                InsuranceBaseRate.objects.create(
                    insurance_type=auto,
                    min_age=18,
                    max_age=25,
                    gender='F',
                    base_monthly_rate=Decimal('100.00'),
                    rate_per_thousand=Decimal('0.30')
                )
                
                InsuranceBaseRate.objects.create(
                    insurance_type=auto,
                    min_age=26,
                    max_age=65,
                    gender='ANY',
                    base_monthly_rate=Decimal('80.00'),
                    rate_per_thousand=Decimal('0.20')
                )
                
                # Create base rates for Home insurance
                self.stdout.write('Creating base rates for Home insurance...')
                InsuranceBaseRate.objects.create(
                    insurance_type=home,
                    min_age=18,
                    max_age=100,
                    gender='ANY',
                    base_monthly_rate=Decimal('50.00'),
                    rate_per_thousand=Decimal('0.05')
                )
                
                # Create investment return data for Life insurance
                self.stdout.write('Creating investment return data for Life insurance...')
                InsuranceInvestmentReturn.objects.create(
                    insurance_type=life,
                    term_years=10,
                    annual_return_rate=Decimal('4.50'),
                    guaranteed_return=True,
                    tax_benefits=True,
                    maturity_bonus_percent=Decimal('2.00')
                )
                
                InsuranceInvestmentReturn.objects.create(
                    insurance_type=life,
                    term_years=15,
                    annual_return_rate=Decimal('5.25'),
                    guaranteed_return=True,
                    tax_benefits=True,
                    maturity_bonus_percent=Decimal('3.50')
                )
                
                InsuranceInvestmentReturn.objects.create(
                    insurance_type=life,
                    term_years=20,
                    annual_return_rate=Decimal('6.00'),
                    guaranteed_return=True,
                    tax_benefits=True,
                    maturity_bonus_percent=Decimal('5.00')
                )
                
                InsuranceInvestmentReturn.objects.create(
                    insurance_type=life,
                    term_years=30,
                    annual_return_rate=Decimal('6.75'),
                    guaranteed_return=False,
                    tax_benefits=True,
                    maturity_bonus_percent=Decimal('7.50')
                )
                
                # Create investment return data for Health insurance
                self.stdout.write('Creating investment return data for Health insurance...')
                InsuranceInvestmentReturn.objects.create(
                    insurance_type=health,
                    term_years=5,
                    annual_return_rate=Decimal('3.00'),
                    guaranteed_return=False,
                    tax_benefits=True,
                    maturity_bonus_percent=Decimal('0.00')
                )
                
                InsuranceInvestmentReturn.objects.create(
                    insurance_type=health,
                    term_years=10,
                    annual_return_rate=Decimal('3.50'),
                    guaranteed_return=False,
                    tax_benefits=True,
                    maturity_bonus_percent=Decimal('1.00')
                )
                
                # No significant investment returns for Auto insurance
                
                # Create investment return data for Home insurance
                self.stdout.write('Creating investment return data for Home insurance...')
                InsuranceInvestmentReturn.objects.create(
                    insurance_type=home,
                    term_years=15,
                    annual_return_rate=Decimal('2.50'),
                    guaranteed_return=False,
                    tax_benefits=False,
                    maturity_bonus_percent=Decimal('0.00')
                )
                
                InsuranceInvestmentReturn.objects.create(
                    insurance_type=home,
                    term_years=30,
                    annual_return_rate=Decimal('3.00'),
                    guaranteed_return=False,
                    tax_benefits=False,
                    maturity_bonus_percent=Decimal('0.00')
                )
                
                # Create state rate adjustments for Auto insurance
                self.stdout.write('Creating state rate adjustments for insurance types...')
                
                # High-cost auto insurance states
                high_cost_auto_states = [
                    ('NY', 'High population density and traffic congestion', Decimal('1.35')),
                    ('MI', 'No-fault insurance state with unlimited medical benefits', Decimal('1.40')),
                    ('FL', 'High number of uninsured drivers and weather risks', Decimal('1.25')),
                    ('CA', 'High cost of living and repair costs', Decimal('1.30')),
                    ('NJ', 'Dense population and high traffic areas', Decimal('1.25')),
                ]
                
                for state_code, desc, multiplier in high_cost_auto_states:
                    StateRateAdjustment.objects.create(
                        insurance_type=auto,
                        state=state_code,
                        rate_multiplier=multiplier,
                        description=desc
                    )
                
                # Low-cost auto insurance states
                low_cost_auto_states = [
                    ('ME', 'Low population density and fewer accidents', Decimal('0.85')),
                    ('OH', 'Competitive insurance market', Decimal('0.90')),
                    ('VT', 'Low population density and fewer claims', Decimal('0.85')),
                    ('NC', 'State regulation keeps rates lower', Decimal('0.90')),
                    ('ID', 'Fewer drivers and less traffic congestion', Decimal('0.80')),
                ]
                
                for state_code, desc, multiplier in low_cost_auto_states:
                    StateRateAdjustment.objects.create(
                        insurance_type=auto,
                        state=state_code,
                        rate_multiplier=multiplier,
                        description=desc
                    )
                
                # High-cost health insurance states
                high_cost_health_states = [
                    ('WY', 'Low population and fewer insurance providers', Decimal('1.30')),
                    ('AK', 'Remote location and high healthcare costs', Decimal('1.45')),
                    ('WV', 'High rates of chronic conditions', Decimal('1.25')),
                    ('CT', 'High cost of living and medical services', Decimal('1.20')),
                    ('NY', 'Expensive medical care and comprehensive coverage requirements', Decimal('1.25')),
                ]
                
                for state_code, desc, multiplier in high_cost_health_states:
                    StateRateAdjustment.objects.create(
                        insurance_type=health,
                        state=state_code,
                        rate_multiplier=multiplier,
                        description=desc
                    )
                
                # Low-cost health insurance states
                low_cost_health_states = [
                    ('UT', 'Healthier population and competitive market', Decimal('0.85')),
                    ('MN', 'Efficient healthcare system', Decimal('0.90')),
                    ('NM', 'Lower cost of living and healthcare services', Decimal('0.85')),
                    ('MI', 'Competitive insurance market', Decimal('0.90')),
                    ('PA', 'Multiple insurance providers', Decimal('0.95')),
                ]
                
                for state_code, desc, multiplier in low_cost_health_states:
                    StateRateAdjustment.objects.create(
                        insurance_type=health,
                        state=state_code,
                        rate_multiplier=multiplier,
                        description=desc
                    )
                
                # Home insurance - high cost states (natural disasters, etc.)
                high_cost_home_states = [
                    ('FL', 'Hurricane risk', Decimal('1.40')),
                    ('LA', 'Flood and hurricane risk', Decimal('1.35')),
                    ('TX', 'Multiple natural disaster risks', Decimal('1.25')),
                    ('OK', 'Tornado alley and storm damage', Decimal('1.30')),
                    ('CA', 'Wildfire and earthquake risks', Decimal('1.45')),
                ]
                
                for state_code, desc, multiplier in high_cost_home_states:
                    StateRateAdjustment.objects.create(
                        insurance_type=home,
                        state=state_code,
                        rate_multiplier=multiplier,
                        description=desc
                    )
                
                # Life insurance - generally less state variation, but some examples
                high_cost_life_states = [
                    ('MS', 'Lower life expectancy', Decimal('1.15')),
                    ('AL', 'Higher rates of health conditions', Decimal('1.10')),
                    ('WV', 'Higher mortality rates', Decimal('1.10')),
                ]
                
                for state_code, desc, multiplier in high_cost_life_states:
                    StateRateAdjustment.objects.create(
                        insurance_type=life,
                        state=state_code,
                        rate_multiplier=multiplier,
                        description=desc
                    )
                
                # Low-cost life insurance states
                low_cost_life_states = [
                    ('HI', 'Higher life expectancy', Decimal('0.90')),
                    ('MN', 'Better overall health metrics', Decimal('0.95')),
                    ('CA', 'Lower mortality rates', Decimal('0.95')),
                ]
                
                for state_code, desc, multiplier in low_cost_life_states:
                    StateRateAdjustment.objects.create(
                        insurance_type=life,
                        state=state_code,
                        rate_multiplier=multiplier,
                        description=desc
                    )
                
                self.stdout.write(self.style.SUCCESS('Successfully created sample insurance data and state adjustments'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating insurance data: {str(e)}')) 