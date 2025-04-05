from django.db import models

# Create your models here.
class ToDoList(models.Model):
    name = models.CharField(max_length=100)

def __str__(self):
        return self.name

class Item(models.Model):
    todoList = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Videos(models.Model):
    url = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return self.title

class HomeInfoSection(models.Model):
    title = models.CharField(max_length=500)
    desc = models.CharField(max_length=1000)
    imgUrl = models.ImageField(upload_to='images/', default='images/default.jpg')
    imgAltText = models.CharField(max_length=500)
    imgClass = models.CharField(max_length=500)

    def __str__(self):
        return self.title

class HomeSliderImage(models.Model):
      sliderImageUrl = models.ImageField(upload_to='images/', default='images/default.jpg')
      sliderImageAltText = models.CharField(max_length=500)


class Team(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    websiteUrl = models.CharField(max_length=500)
    agentNo = models.CharField(max_length=100)
    profileUrl = models.ImageField(upload_to='images/', default='images/default.jpg')
    def __str__(self):
        return self.name


class ServicesSection(models.Model):
    title = models.CharField(max_length=500)
    desc = models.CharField(max_length=1000)
    imgUrl = models.ImageField(upload_to='images/', default='images/default.jpg')
    imgAltText = models.CharField(max_length=500)
    imgClass = models.CharField(max_length=500)
    serviceUrl = models.CharField(max_length=500)

    def __str__(self):
        return self.title

class FooterSection(models.Model):
    facebookUrl = models.CharField(max_length=500)
    youtubeUrl = models.CharField(max_length=500)
    linkedinUrl = models.CharField(max_length=500)
    instagramUrl = models.CharField(max_length=500)
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return self.desc

class Contactus(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('potential', 'Potential'),
    ]

    STATE_CHOICES = [
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
        # Territories
        ('DC', 'District of Columbia'),
        ('AS', 'American Samoa'),
        ('GU', 'Guam'),
        ('MP', 'Northern Mariana Islands'),
        ('PR', 'Puerto Rico'),
        ('VI', 'U.S. Virgin Islands'),
        ('UM', 'U.S. Minor Outlying Islands'),
    ]

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    addressline2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICES, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True, default='US')
    reason = models.CharField(max_length=1000)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )
    def __str__(self):
        return self.name

class BusinessContact(models.Model):
    STATE_CHOICES = [
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
        # Territories
        ('DC', 'District of Columbia'),
        ('AS', 'American Samoa'),
        ('GU', 'Guam'),
        ('MP', 'Northern Mariana Islands'),
        ('PR', 'Puerto Rico'),
        ('VI', 'U.S. Virgin Islands'),
        ('UM', 'U.S. Minor Outlying Islands'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200)
    addressline2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICES, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True, default='US')
    establish = models.DateField(blank=True, null=True)
    owner = models.CharField(max_length=200)

class Appointment(models.Model):
    STATE_CHOICES = [
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
        # Territories
        ('DC', 'District of Columbia'),
        ('AS', 'American Samoa'),
        ('GU', 'Guam'),
        ('MP', 'Northern Mariana Islands'),
        ('PR', 'Puerto Rico'),
        ('VI', 'U.S. Virgin Islands'),
        ('UM', 'U.S. Minor Outlying Islands'),
    ]

    STATUS_CHOICES = [
        ('request', 'Request'),
        ('scheduled', 'scheduled'),
        ('completed', 'Completed'),
        ('followup', 'Follow Up'),
    ]

    MEDIA_CHOICES = [
        ('zoom', 'Zoom'),
        ('teams', 'Microsoft Teams'),
        ('meet', 'Google Meet'),
        ('skype', 'Skype'),
        ('webex', 'Webex by Cisco'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=500)
    addressline2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICES, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True, default='US')
    appointment = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='request',)
    meetingUrl = models.URLField(blank=True, null=True)
    meetingDate = models.DateField(blank=True, null=True)
    meetingTime = models.TimeField(blank=True, null=True)
    meetingMedia = models.CharField(max_length=100,choices=MEDIA_CHOICES,default='zoom')
    zoom_slot = models.ForeignKey('ZoomAvailableSlot', on_delete=models.SET_NULL, blank=True, null=True, related_name='appointments')
    zoom_meeting_id = models.CharField(max_length=255, blank=True, null=True)
    zoom_meeting_url = models.URLField(blank=True, null=True)
    zoom_meeting_password = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Appointment for {self.name} on {self.meetingDate} at {self.meetingTime}"

class VideoDirect(models.Model):
    title = models.CharField(max_length=100, help_text="Enter the title of the video")
    description = models.TextField(blank=True, help_text="Optional: Add a brief description")
    video = models.FileField(upload_to='videos/', help_text="Upload your video file")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ZoomCredentials(models.Model):
    app_name = models.CharField(max_length=255, default='wealthProZoomApp')
    account_id = models.CharField(max_length=255, default='Sn2rpXqFRmC7AitP028Xmg')
    client_id = models.CharField(max_length=255, default='FC0NGNG7QfyRU7yLXHCrMw')
    client_secret = models.CharField(max_length=255, default='68kBbdAS49mzxtvQebGl1BM5fzN6AgBp')
    secret_token = models.CharField(max_length=255, default='Hapqqa_CRN2HzdT0R-kgiw')
    verification_token = models.CharField(max_length=255, default='TdcWSKzkSV6J3PBjo1qVpQ')
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.app_name

    class Meta:
        verbose_name_plural = "Zoom Credentials"

class ZoomAvailableSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting_id = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.end_time.strftime('%H:%M')}"

# Insurance Calculator Models
class InsuranceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class, e.g., 'fa-heart' for health")
    
    def __str__(self):
        return self.name

class InsuranceBaseRate(models.Model):
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.CASCADE, related_name='base_rates')
    min_age = models.IntegerField(default=0)
    max_age = models.IntegerField(default=100)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('ANY', 'Any')], default='ANY')
    base_monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    rate_per_thousand = models.DecimalField(max_digits=10, decimal_places=2, help_text="Additional rate per $1,000 of coverage")
    
    class Meta:
        unique_together = ('insurance_type', 'min_age', 'max_age', 'gender')
        
    def __str__(self):
        if self.gender == 'ANY':
            return f"{self.insurance_type.name}: Ages {self.min_age}-{self.max_age}"
        else:
            return f"{self.insurance_type.name}: {self.gender} Ages {self.min_age}-{self.max_age}"

class CSOMortalityTable(models.Model):
    """2017 CSO Mortality Table for accurate life insurance calculations"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    SMOKER_STATUS_CHOICES = [
        ('NS', 'Non-smoker'),
        ('SM', 'Smoker'),
        ('ANY', 'Any'),
    ]
    
    age = models.IntegerField(help_text="Age of the insured")
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    smoker_status = models.CharField(max_length=5, choices=SMOKER_STATUS_CHOICES, default='ANY')
    mortality_rate = models.DecimalField(max_digits=10, decimal_places=6, help_text="Annual mortality rate per 1,000 individuals")
    table_version = models.CharField(max_length=10, default="2017 CSO", help_text="Version of the CSO table")
    
    class Meta:
        unique_together = ('age', 'gender', 'smoker_status', 'table_version')
        verbose_name = "CSO Mortality Table Entry"
        verbose_name_plural = "CSO Mortality Table Entries"
    
    def __str__(self):
        return f"{self.table_version}: {self.gender} Age {self.age} ({self.get_smoker_status_display()}) - {self.mortality_rate}"

class InsuranceRiskFactor(models.Model):
    """Model for additional risk factors affecting insurance premiums"""
    FACTOR_TYPE_CHOICES = [
        ('LIFE', 'Life Insurance'),
        ('HEALTH', 'Health Insurance'),
        ('AUTO', 'Auto Insurance'),
        ('HOME', 'Home Insurance'),
    ]
    
    name = models.CharField(max_length=100, help_text="Name of the risk factor")
    factor_type = models.CharField(max_length=10, choices=FACTOR_TYPE_CHOICES)
    description = models.TextField(help_text="Description of how this factor affects premiums")
    
    class Meta:
        unique_together = ('name', 'factor_type')
    
    def __str__(self):
        return f"{self.name} ({self.get_factor_type_display()})"

class RiskFactorValue(models.Model):
    """Values for different risk factors"""
    risk_factor = models.ForeignKey(InsuranceRiskFactor, on_delete=models.CASCADE, related_name='values')
    value_name = models.CharField(max_length=100, help_text="The condition or value (e.g., 'Smoker', 'High Blood Pressure')")
    multiplier = models.DecimalField(max_digits=5, decimal_places=3, help_text="Multiplier applied to base premium (e.g., 1.5 for 50% increase)")
    
    def __str__(self):
        return f"{self.risk_factor.name}: {self.value_name} ({self.multiplier}x)"

class InsuranceInvestmentReturn(models.Model):
    """Model to store return and maturity data for insurance policies"""
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.CASCADE, related_name='investment_returns')
    term_years = models.IntegerField(help_text="Policy term in years (e.g., 10, 15, 20)")
    annual_return_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual return rate percentage (e.g., 5.25 for 5.25%)")
    guaranteed_return = models.BooleanField(default=False, help_text="Whether the return rate is guaranteed or estimated")
    tax_benefits = models.BooleanField(default=True, help_text="If the policy provides tax benefits")
    maturity_bonus_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Additional bonus percentage at maturity")
    
    # Adding more detailed investment projections
    conservative_return_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Conservative scenario return rate")
    aggressive_return_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Aggressive scenario return rate")
    historical_performance = models.TextField(blank=True, help_text="Description of historical performance")
    
    class Meta:
        unique_together = ('insurance_type', 'term_years')
        
    def __str__(self):
        return f"{self.insurance_type.name}: {self.term_years} years at {self.annual_return_rate}%"

class StateRateAdjustment(models.Model):
    """Model to store state-specific insurance rate adjustments"""
    STATE_CHOICES = [
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
        ('DC', 'District of Columbia'),
    ]
    
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.CASCADE, related_name='state_adjustments')
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    rate_multiplier = models.DecimalField(max_digits=5, decimal_places=3, default=1.0, 
                                          help_text="Multiplier applied to base premium rates for this state (e.g., 1.2 for 20% higher)")
    description = models.TextField(blank=True, help_text="Optional explanation for the rate adjustment")
    
    class Meta:
        unique_together = ('insurance_type', 'state')
        verbose_name = "State Rate Adjustment"
        verbose_name_plural = "State Rate Adjustments"
    
    def __str__(self):
        return f"{self.insurance_type.name} - {self.get_state_display()}: {self.rate_multiplier}x"

class StateRegulation(models.Model):
    """Model to store specific state insurance regulations"""
    state = models.CharField(max_length=2, choices=StateRateAdjustment.STATE_CHOICES)
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.CASCADE, related_name='state_regulations')
    min_coverage_required = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, 
                                               help_text="Minimum coverage amount required by state law")
    special_requirements = models.TextField(blank=True, help_text="Special requirements or disclosures for this state")
    filing_requirements = models.TextField(blank=True, help_text="Filing requirements for this insurance type in this state")
    
    class Meta:
        unique_together = ('state', 'insurance_type')
        
    def __str__(self):
        return f"{self.get_state_display()} - {self.insurance_type.name} Regulations"

class DisclaimerText(models.Model):
    """Model for storing legal disclaimers for the calculator"""
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.CASCADE, related_name='disclaimers')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    last_updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.insurance_type.name} - {self.title}"

class SiteSettings(models.Model):
    """Model to store global site settings that can be updated from admin"""
    site_name = models.CharField(max_length=200, default="Next Generation Wealth Pro")
    site_tagline = models.CharField(max_length=200, default="Wealth Management")
    
    # Contact Information
    address = models.CharField(max_length=200, default="123 Street, New York, USA")
    phone = models.CharField(max_length=20, default="+012 345 67890")
    email = models.EmailField(default="info@nextgenwealthpro.com")
    
    # About Us Content
    about_us_short = models.TextField(default="Next Generation Wealth Pro provides comprehensive wealth management services.")
    about_us_full = models.TextField(blank=True)
    
    # Social Media Links
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    
    # SEO Settings
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    
    # Analytics and Tracking
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    # Company Info
    established_year = models.PositiveIntegerField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='images/', blank=True, null=True)
    favicon = models.ImageField(upload_to='images/', blank=True, null=True)
    
    # Footer Content
    footer_text = models.TextField(blank=True)
    
    # Cache Settings - time in seconds
    cache_timeout = models.PositiveIntegerField(default=3600)
    
    # Email Settings
    email_host = models.CharField(max_length=200, default="smtp.gmail.com", 
                                 help_text="SMTP server hostname (e.g., email-smtp.us-east-1.amazonaws.com for Amazon SES)")
    email_port = models.PositiveIntegerField(default=587,
                                           help_text="SMTP server port (587 for TLS, 465 for SSL)")
    email_use_tls = models.BooleanField(default=True,
                                      help_text="Use TLS for secure email transmission")
    email_use_ssl = models.BooleanField(default=False,
                                      help_text="Use SSL instead of TLS (don't enable both)")
    email_host_user = models.CharField(max_length=200, default="",
                                     help_text="SMTP username or IAM SMTP user for Amazon SES")
    email_host_password = models.CharField(max_length=200, default="",
                                        help_text="SMTP password or IAM SMTP password for Amazon SES")
    default_from_email = models.EmailField(default="info@nextgenwealthpro.com",
                                         help_text="Default sender email address (must be verified in Amazon SES)")
    contact_email = models.EmailField(default="contact@nextgenwealthpro.com",
                                    help_text="Email address to receive contact form submissions (must be verified)")
    email_provider = models.CharField(max_length=100, default="smtp",
                                    choices=[
                                        ('smtp', 'Standard SMTP'),
                                        ('ses', 'Amazon SES'),
                                        ('mailgun', 'Mailgun'),
                                        ('sendgrid', 'SendGrid'),
                                    ],
                                    help_text="Email service provider")
    aws_region = models.CharField(max_length=50, default="us-east-1",
                                choices=[
                                    ('us-east-1', 'US East (N. Virginia)'),
                                    ('us-east-2', 'US East (Ohio)'),
                                    ('us-west-1', 'US West (N. California)'),
                                    ('us-west-2', 'US West (Oregon)'),
                                    ('af-south-1', 'Africa (Cape Town)'),
                                    ('ap-east-1', 'Asia Pacific (Hong Kong)'),
                                    ('ap-south-1', 'Asia Pacific (Mumbai)'),
                                    ('ap-northeast-3', 'Asia Pacific (Osaka)'),
                                    ('ap-northeast-2', 'Asia Pacific (Seoul)'),
                                    ('ap-southeast-1', 'Asia Pacific (Singapore)'),
                                    ('ap-southeast-2', 'Asia Pacific (Sydney)'),
                                    ('ap-northeast-1', 'Asia Pacific (Tokyo)'),
                                    ('ca-central-1', 'Canada (Central)'),
                                    ('eu-central-1', 'Europe (Frankfurt)'),
                                    ('eu-west-1', 'Europe (Ireland)'),
                                    ('eu-west-2', 'Europe (London)'),
                                    ('eu-south-1', 'Europe (Milan)'),
                                    ('eu-west-3', 'Europe (Paris)'),
                                    ('eu-north-1', 'Europe (Stockholm)'),
                                    ('me-south-1', 'Middle East (Bahrain)'),
                                    ('sa-east-1', 'South America (São Paulo)'),
                                ],
                                help_text="AWS region for Amazon SES (if using SES)")
    
    # Map Configuration
    google_maps_embed_url = models.URLField(
        default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.9663095343016!2d-74.00425882426698!3d40.71116937132799!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25a23e28c1191%3A0x49f75d3281df052a!2s150%20Park%20Row%2C%20New%20York%2C%20NY%2010007%2C%20USA!5e0!3m2!1sen!2sbg!4v1685637930992!5m2!1sen!2sbg",
        help_text="Google Maps embed URL for contact page"
    )
    
    # Business Hours
    business_hours_weekdays = models.CharField(max_length=100, default="9:00 AM - 5:00 PM", 
                                             help_text="Business hours for weekdays")
    business_hours_saturday = models.CharField(max_length=100, default="By appointment", 
                                             help_text="Business hours for Saturday")
    business_hours_sunday = models.CharField(max_length=100, default="Closed", 
                                           help_text="Business hours for Sunday")
    
    # Security Settings
    enable_csrf_protection = models.BooleanField(default=True, 
                                               help_text="Enable CSRF protection in production")
    enable_secure_cookies = models.BooleanField(default=True, 
                                              help_text="Enable secure cookies in production")
    enable_ssl_redirect = models.BooleanField(default=True, 
                                            help_text="Enable SSL redirect in production")
    
    # Create timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return f"Site Settings - {self.site_name}"
    
    def save(self, *args, **kwargs):
        # Ensure there's only one instance of site settings
        if SiteSettings.objects.exists() and not self.pk:
            raise ValueError("There can only be one SiteSettings instance")
        
        # Clear settings cache when saving
        from main.settings_registry import clear_settings_cache
        clear_settings_cache()
        
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create site settings"""
        settings, created = cls.objects.get_or_create()
        return settings











