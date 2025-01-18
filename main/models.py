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
