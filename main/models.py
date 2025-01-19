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

class VideoDirect(models.Model):
    title = models.CharField(max_length=100, help_text="Enter the title of the video")
    description = models.TextField(blank=True, help_text="Optional: Add a brief description")
    video = models.FileField(upload_to='videos/', help_text="Upload your video file")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title











