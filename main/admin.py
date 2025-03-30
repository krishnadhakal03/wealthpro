from django.contrib import admin
from django.utils.html import mark_safe, format_html
from .models import Videos, HomeInfoSection, HomeSliderImage, Team, FooterSection, ServicesSection, Appointment, BusinessContact, Contactus, VideoDirect, ZoomCredentials, ZoomAvailableSlot, InsuranceType, InsuranceBaseRate, InsuranceInvestmentReturn, StateRateAdjustment, SiteSettings
import os
import datetime
import subprocess
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.urls import path, reverse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


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
    list_display = ('name', 'email', 'phone', 'appointment', 'status', 'has_zoom_meeting', 'meetingDate', 'meetingTime')
    list_filter = ('status', 'meetingDate')
    search_fields = ('name', 'email', 'phone', 'zoom_meeting_id')
    date_hierarchy = 'appointment'
    readonly_fields = ('zoom_meeting_id', 'zoom_meeting_url', 'zoom_meeting_password')
    
    def has_zoom_meeting(self, obj):
        return bool(obj.zoom_meeting_id)
    
    has_zoom_meeting.boolean = True
    has_zoom_meeting.short_description = 'Zoom'
    
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone', 'status')
        }),
        ('Address Information', {
            'fields': ('address', 'addressline2', 'city', 'state', 'zipcode', 'country')
        }),
        ('Appointment Details', {
            'fields': ('appointment', 'meetingMedia', 'meetingDate', 'meetingTime', 'meetingUrl')
        }),
        ('Zoom Details', {
            'fields': ('zoom_slot', 'zoom_meeting_id', 'zoom_meeting_url', 'zoom_meeting_password'),
            'classes': ('collapse',),
        }),
    )

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

@admin.register(ZoomCredentials)
class ZoomCredentialsAdmin(admin.ModelAdmin):
    list_display = ('app_name', 'client_id', 'token_expiry', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('app_name', 'account_id', 'client_id', 'client_secret')
        }),
        ('Tokens', {
            'fields': ('secret_token', 'verification_token', 'access_token', 'refresh_token', 'token_expiry')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(ZoomAvailableSlot)
class ZoomAvailableSlotAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'is_available', 'meeting_id', 'created_at')
    list_filter = ('is_available', 'start_time')
    search_fields = ('meeting_id',)
    date_hierarchy = 'start_time'
    readonly_fields = ('created_at',)

class ZoomAppointmentFilter(admin.SimpleListFilter):
    title = 'Zoom Appointment'
    parameter_name = 'has_zoom'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', 'Has Zoom Link'),
            ('no', 'No Zoom Link'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(zoom_meeting_id__isnull=True).exclude(zoom_meeting_id='')
        if self.value() == 'no':
            return queryset.filter(zoom_meeting_id__isnull=True) | queryset.filter(zoom_meeting_id='')

@admin.register(InsuranceType)
class InsuranceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(InsuranceBaseRate)
class InsuranceBaseRateAdmin(admin.ModelAdmin):
    list_display = ('insurance_type', 'min_age', 'max_age', 'gender', 'base_monthly_rate', 'rate_per_thousand')
    list_filter = ('insurance_type', 'gender')
    search_fields = ('insurance_type__name',)

@admin.register(InsuranceInvestmentReturn)
class InsuranceInvestmentReturnAdmin(admin.ModelAdmin):
    list_display = ('insurance_type', 'term_years', 'annual_return_rate', 'guaranteed_return', 'tax_benefits', 'maturity_bonus_percent')
    list_filter = ('insurance_type', 'guaranteed_return', 'tax_benefits')
    search_fields = ('insurance_type__name',)

@admin.register(StateRateAdjustment)
class StateRateAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('insurance_type', 'state', 'rate_multiplier', 'description')
    list_filter = ('insurance_type', 'state')
    search_fields = ('insurance_type__name', 'state')
    list_editable = ('rate_multiplier',)

def export_db_as_sqlite(modeladmin, request, queryset):
    """Create a downloadable dump of the entire database"""
    if not request.user.is_superuser:
        messages.error(request, "Only superusers can perform database backups.")
        return

    # Get the SQLite database path from settings
    db_path = settings.DATABASES['default']['NAME']
    if not os.path.exists(db_path):
        messages.error(request, f"Database file not found at {db_path}")
        return

    # Create a filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"wealthpro_db_backup_{timestamp}.sqlite"
    
    try:
        # For SQLite, we can just read the file directly
        with open(db_path, 'rb') as db_file:
            response = HttpResponse(db_file.read(), content_type='application/x-sqlite3')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            messages.success(request, "Database backup created successfully.")
            return response
    except Exception as e:
        messages.error(request, f"Failed to create database backup: {str(e)}")

export_db_as_sqlite.short_description = "Download database backup"

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'updated_at', 'get_backup_link')
    fieldsets = (
        ('Website Identity', {
            'fields': ('site_name', 'site_tagline', 'company_logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'email')
        }),
        ('About Us Content', {
            'fields': ('about_us_short', 'about_us_full')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url')
        }),
        ('SEO Settings', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Analytics & Tracking', {
            'fields': ('google_analytics_id',)
        }),
        ('Company Details', {
            'fields': ('established_year', 'footer_text')
        }),
        ('Email Configuration', {
            'fields': ('email_host', 'email_port', 'email_use_tls', 'email_use_ssl', 'email_host_user', 
                      'email_host_password', 'default_from_email', 'contact_email', 'email_provider', 'aws_region'),
            'classes': ('collapse',),
            'description': 'Email server settings for sending notifications and contact form submissions'
        }),
        ('Map Settings', {
            'fields': ('google_maps_embed_url',),
            'description': 'Google Maps embed URL for contact page'
        }),
        ('Business Hours', {
            'fields': ('business_hours_weekdays', 'business_hours_saturday', 'business_hours_sunday'),
            'description': 'Store hours displayed on the contact page'
        }),
        ('Security Settings', {
            'fields': ('enable_csrf_protection', 'enable_secure_cookies', 'enable_ssl_redirect'),
            'classes': ('collapse',),
            'description': 'Security settings for production environment'
        }),
        ('Cache Settings', {
            'fields': ('cache_timeout',),
            'classes': ('collapse',),
            'description': 'Caching duration in seconds'
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['refresh_settings_cache', 'export_db_as_sqlite']
    
    def refresh_settings_cache(self, request, queryset):
        from main.settings_registry import reload_settings
        reload_settings()
        self.message_user(request, "Settings cache has been refreshed.")
    
    refresh_settings_cache.short_description = "Refresh settings cache"
    
    def has_add_permission(self, request):
        # Check if a settings object already exists
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the settings object
        return False
    
    def save_model(self, request, obj, form, change):
        """When saving the model, refresh the settings cache"""
        super().save_model(request, obj, form, change)
        # Refresh settings in the registry
        from main.settings_registry import reload_settings
        reload_settings()
        self.message_user(request, "Settings saved and cache refreshed.")
    
    def get_backup_link(self, obj):
        """Add backup link to the admin list display"""
        if obj.pk:
            url = reverse('admin:main_sitesettings_backup')
            return format_html('<a href="{}" class="button" style="background-color: #28a745; color: white;">Database Backup</a>', url)
        return "-"
    get_backup_link.short_description = "Backup"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('backup/', self.admin_site.admin_view(self.backup_view), name='main_sitesettings_backup'),
        ]
        return custom_urls + urls
    
    def backup_view(self, request):
        """Custom view for database backup with a prominent button"""
        context = {
            **self.admin_site.each_context(request),
            'title': 'Database Backup',
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'has_permission': request.user.is_superuser,
        }
        
        if request.method == 'POST' and request.user.is_superuser:
            return export_db_as_sqlite(self, request, None)
        
        return TemplateResponse(request, 'admin/database_backup.html', context)



