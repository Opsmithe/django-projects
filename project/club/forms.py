"""
Django Forms for Tennis Club Application

ModelForms automatically generate form fields based on model fields,
reducing code duplication and ensuring consistency between forms and models.
"""

from django import forms
from .models import Names


class MemberForm(forms.ModelForm):
    """
    Form for creating and editing club members.
    
    ModelForm automatically creates form fields for all model fields,
    including validation rules, field types, and help text.
    """
    
    # Override fields to make them explicitly required
    firstname = forms.CharField(
        max_length=250,
        required=True,
        label='First Name',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter first name',
            'required': True,
        }),
        error_messages={
            'required': 'First name is required.',
        }
    )
    
    lastname = forms.CharField(
        max_length=250,
        required=True,
        label='Last Name',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter last name',
            'required': True,
        }),
        error_messages={
            'required': 'Last name is required.',
        }
    )
    
    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'example@email.com',
            'required': True,
        }),
        error_messages={
            'required': 'Email address is required.',
            'invalid': 'Please enter a valid email address.',
        }
    )
    
    phoneNumber = forms.CharField(
        max_length=15,
        required=True,
        label='Phone Number',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '000-000-0000',
            'required': True,
        }),
        error_messages={
            'required': 'Phone number is required.',
        }
    )
    
    city = forms.CharField(
        max_length=250,
        required=True,
        label='City',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter city',
            'required': True,
        }),
        error_messages={
            'required': 'City is required.',
        }
    )
    
    location = forms.CharField(
        max_length=250,
        required=True,
        label='Location/Area',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter specific location/area',
            'required': True,
        }),
        error_messages={
            'required': 'Location is required.',
        }
    )
    
    # Profile picture field
    # FileInput widget renders as <input type="file">
    # ClearableFileInput adds a checkbox to clear existing file
    profile_picture = forms.ImageField(
        required=False,
        label='Profile Picture',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-file-input',
            'accept': 'image/*',  # Only accept image files
        }),
        help_text='Upload a profile picture (JPG, PNG, GIF, WEBP - Max 5MB)',
        error_messages={
            'invalid_image': 'Please upload a valid image file.',
        }
    )
    
    class Meta:
        model = Names  # The model this form is based on
        
        # Fields to include in the form
        fields = [
            'firstname',
            'lastname', 
            'email',
            'phoneNumber',
            'city',
            'location',
            'profile_picture',  # Add profile picture field
            'status',
        ]
        
        # Exclude auto-generated fields
        exclude = ['slug', 'date_joined', 'date_updated', 'date_started']
        
        # Help text for fields (optional)
        help_text = {
            'email': 'We will never share your email with anyone.',
            'phoneNumber': 'Format: 000-000-0000',
            'status': 'Have you played at our club yet?',
        }
        
        # Widget for status field
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
    
    def clean_firstname(self):
        """
        Validate firstname field.
        """
        firstname = self.cleaned_data.get('firstname')
        
        if not firstname or firstname.strip() == '':
            raise forms.ValidationError('First name cannot be empty.')
        
        # Check if it's the default value
        if firstname.lower() == 'unknown':
            raise forms.ValidationError('Please enter a valid first name.')
        
        # Check minimum length
        if len(firstname.strip()) < 2:
            raise forms.ValidationError('First name must be at least 2 characters.')
        
        return firstname.strip()
    
    def clean_lastname(self):
        """
        Validate lastname field.
        """
        lastname = self.cleaned_data.get('lastname')
        
        if not lastname or lastname.strip() == '':
            raise forms.ValidationError('Last name cannot be empty.')
        
        # Check if it's the default value
        if lastname.lower() == 'member':
            raise forms.ValidationError('Please enter a valid last name.')
        
        # Check minimum length
        if len(lastname.strip()) < 2:
            raise forms.ValidationError('Last name must be at least 2 characters.')
        
        return lastname.strip()
    
    def clean_city(self):
        """
        Validate city field.
        """
        city = self.cleaned_data.get('city')
        
        if not city or city.strip() == '':
            raise forms.ValidationError('City cannot be empty.')
        
        # Check if it's the default value
        if city.lower() == 'not specified':
            raise forms.ValidationError('Please enter a valid city.')
        
        return city.strip()
    
    def clean_location(self):
        """
        Validate location field.
        """
        location = self.cleaned_data.get('location')
        
        if not location or location.strip() == '':
            raise forms.ValidationError('Location cannot be empty.')
        
        # Check if it's the default value
        if location.lower() == 'not specified':
            raise forms.ValidationError('Please enter a valid location.')
        
        return location.strip()
    
    def clean_profile_picture(self):
        """
        Validate profile picture upload.
        
        Checks:
        1. File size (max 5MB)
        2. File format (jpg, png, gif, webp)
        3. File is actually an image
        
        Returns:
            UploadedFile: The validated image file
            
        Raises:
            ValidationError: If validation fails
        """
        profile_picture = self.cleaned_data.get('profile_picture')
        
        if profile_picture:
            # Import validation function
            from .file_utils import validate_image_file
            
            # Validate the image
            # This will raise ValidationError if invalid
            validate_image_file(profile_picture)
        
        return profile_picture
    
    def clean_email(self):
        """
        Custom validation for email field.
        
        This method is called automatically during form validation.
        Method name pattern: clean_<field_name>
        """
        email = self.cleaned_data.get('email')
        
        if not email or email.strip() == '':
            raise forms.ValidationError('Email address is required.')
        
        # Check if email already exists (for new members)
        if email:
            # Exclude current instance when editing
            existing = Names.objects.filter(email=email)
            if self.instance.pk:  # If editing existing member
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise forms.ValidationError(
                    'A member with this email already exists.'
                )
        
        return email.strip()
    
    def clean_phoneNumber(self):
        """
        Custom validation for phone number.
        
        Ensures phone number follows expected format.
        """
        phone = self.cleaned_data.get('phoneNumber')
        
        if not phone or phone.strip() == '':
            raise forms.ValidationError('Phone number is required.')
        
        # Check if it's the default value
        if phone == '000-000-0000':
            raise forms.ValidationError('Please enter a valid phone number.')
        
        if phone:
            # Remove common separators
            cleaned = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
            
            # Check if it's all digits and has reasonable length
            if not cleaned.isdigit():
                raise forms.ValidationError(
                    'Phone number should contain only digits and separators (-, spaces).'
                )
            
            if len(cleaned) < 10:
                raise forms.ValidationError(
                    'Phone number must be at least 10 digits.'
                )
        
        return phone.strip()
    
    def clean(self):
        """
        Global form validation.
        
        This method is called after all field-specific clean methods.
        Use it for validation that involves multiple fields.
        """
        cleaned_data = super().clean()
        firstname = cleaned_data.get('firstname')
        lastname = cleaned_data.get('lastname')
        
        # Example: Ensure first and last names are different
        if firstname and lastname:
            if firstname.lower() == lastname.lower():
                raise forms.ValidationError(
                    'First name and last name should be different.'
                )
        
        return cleaned_data


class MemberSearchForm(forms.Form):
    """
    Simple search form (not a ModelForm).
    
    This demonstrates a regular Django form for searching members.
    """
    
    search_query = forms.CharField(
        max_length=100,
        required=False,
        label='Search Members',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Search by name, city, or location...',
        })
    )
    
    status_filter = forms.ChoiceField(
        choices=[
            ('', 'All Statuses'),
            ('PL', 'Played'),
            ('NPL', 'Not Played'),
        ],
        required=False,
        label='Filter by Status',
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
