from django.contrib import admin
from django.utils.html import mark_safe, format_html
from .models import Videos, HomeInfoSection, HomeSliderImage, Team, FooterSection, ServicesSection, Appointment, BusinessContact, Contactus, VideoDirect


admin.site.register(Videos)
admin.site.register(FooterSection)

# Register your models here.

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'phone', 'email', 'agentNo', 'profile_image')
    list_filter = ['name', 'designation']

    def profile_image(self, obj):
        if obj.profileUrl:
            return mark_safe(f"<img src='{obj.profileUrl.url}' width='100' height='100' />")
        return "No Image"

    profile_image.short_description = "Profile Image"

@admin.register(HomeInfoSection)
class HomeInfoSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'imgAltText', 'profile_image')  # Use 'profile_image' here to display the method
    list_filter = ['title']

    def profile_image(self, obj):
        if obj.imgUrl:  # Check for the correct field name, assuming 'imgUrl' stores the image
            return mark_safe(f"<img src='{obj.imgUrl.url}' width='100' height='100' />")
        return "No Image"

    profile_image.short_description = "Profile Img"

@admin.register(HomeSliderImage)
class HomeSliderImageAdmin(admin.ModelAdmin):
    list_display = ('profile_image','sliderImageAltText','sliderImageUrl')
    list_filter = ['sliderImageAltText']

    def profile_image(self, obj):
        if obj.sliderImageUrl:  # Check for the correct field name, assuming 'imgUrl' stores the image
            return mark_safe(f"<img src='{obj.sliderImageUrl.url}' width='300' height='300' />")
        return "No Image"

    profile_image.short_description = "Profile Img"

@admin.register(ServicesSection)
class ServicesSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc' , 'imgUrl' , 'profile_image' )
    list_filter = ['title']
    def profile_image(self, obj):
        if obj.imgUrl:  # Check for the correct field name, assuming 'imgUrl' stores the image
            return mark_safe(f"<img src='{obj.imgUrl.url}' width='300' height='300' />")
        return "No Image"

    profile_image.short_description = "Profile Img"

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone','address','appointment','meetingUrl','meetingDate','meetingTime','meetingMedia','status')
    list_filter = ['name','appointment','meetingDate','meetingMedia','status']

@admin.register(BusinessContact)
class BusinessContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone')
    list_filter = ['name','email']

@admin.register(Contactus)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone','address','state','status')
    list_filter = ['name','status','state']

@admin.register(VideoDirect)
class VideoDirectAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'video_preview')

    def video_preview(self, obj):
        if obj.video:
            # Embed a video player in the admin panel
            return format_html(
                '<video width="320" height="240" controls>'
                '<source src="{}" type="video/mp4">'
                'Your browser does not support the video tag.'
                '</video>',
                obj.video.url
            )
        return "No video uploaded"

    video_preview.short_description = "Video Preview"



