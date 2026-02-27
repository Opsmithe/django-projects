"""
File Upload Utility Module for Tennis Club Application

This module provides helper functions for handling file uploads including:
- Custom file path generation
- File validation (size, format)
- Image processing and optimization
- File cleanup utilities

Author: Tennis Club Development Team
Date: 2026
"""

import os
from django.core.exceptions import ValidationError
from django.conf import settings
from PIL import Image
import uuid


def member_profile_picture_path(instance, filename):
    """
    Generate a custom file path for member profile pictures.
    
    This function is used by Django's FileField/ImageField to determine
    where uploaded files should be stored.
    
    Args:
        instance: The model instance (Names object)
        filename: Original filename from upload
        
    Returns:
        str: Path where file will be saved
        
    Example:
        Input: filename="john_photo.jpg"
        Output: "profile_pics/john-doe/uuid_john_photo.jpg"
        
    File Structure:
        media/
        └── profile_pics/
            ├── john-doe/
            │   └── abc123_photo.jpg
            └── jane-smith/
                └── def456_photo.jpg
    """
    # Get file extension
    ext = filename.split('.')[-1]
    
    # Generate unique filename using UUID to prevent conflicts
    # UUID ensures that even if two users upload "photo.jpg", they won't conflict
    unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
    
    # Create path: profile_pics/member-slug/unique_filename.ext
    # Using slug ensures organized folder structure per member
    return os.path.join(
        'profile_pics',
        instance.slug if instance.slug else 'temp',
        unique_filename
    )


def validate_image_file(file):
    """
    Validate uploaded image file for size and format.
    
    This function checks:
    1. File size (must be under 5MB)
    2. File extension (must be jpg, jpeg, png, gif, or webp)
    3. File is actually an image (not just renamed)
    
    Args:
        file: UploadedFile object from Django form
        
    Raises:
        ValidationError: If file doesn't meet requirements
        
    Example:
        >>> from django.core.files.uploadedfile import SimpleUploadedFile
        >>> file = SimpleUploadedFile("test.jpg", b"file_content")
        >>> validate_image_file(file)  # Passes if valid
    """
    # Check file size (5MB limit)
    max_size = 5 * 1024 * 1024  # 5MB in bytes
    if file.size > max_size:
        raise ValidationError(
            f'File size must be under 5MB. Your file is {file.size / (1024*1024):.2f}MB.'
        )
    
    # Check file extension
    ext = os.path.splitext(file.name)[1].lower()
    allowed_extensions = getattr(
        settings, 
        'ALLOWED_IMAGE_EXTENSIONS', 
        ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    )
    
    if ext not in allowed_extensions:
        raise ValidationError(
            f'File type "{ext}" is not allowed. '
            f'Allowed types: {", ".join(allowed_extensions)}'
        )
    
    # Verify file is actually an image by trying to open it
    try:
        # PIL will raise an exception if file is not a valid image
        img = Image.open(file)
        img.verify()  # Verify it's a valid image
        
        # Reset file pointer after verification
        # This is important because verify() reads the file
        file.seek(0)
        
    except Exception as e:
        raise ValidationError(
            f'Invalid image file. Please upload a valid image. Error: {str(e)}'
        )


def optimize_uploaded_image(image_path, max_width=800, max_height=800, quality=85):
    """
    Optimize uploaded image by resizing and compressing.
    
    This function:
    1. Opens the image
    2. Resizes if larger than max dimensions (maintains aspect ratio)
    3. Compresses to reduce file size
    4. Saves optimized version
    
    Args:
        image_path (str): Path to the image file
        max_width (int): Maximum width in pixels (default: 800)
        max_height (int): Maximum height in pixels (default: 800)
        quality (int): JPEG quality 1-100 (default: 85)
        
    Returns:
        bool: True if optimization successful, False otherwise
        
    Example:
        >>> optimize_uploaded_image('/media/profile_pics/john/photo.jpg')
        True
        
    Note:
        - Maintains aspect ratio when resizing
        - Converts RGBA images to RGB (for JPEG compatibility)
        - Original file is replaced with optimized version
    """
    try:
        # Open image
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if necessary (for JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Calculate new dimensions maintaining aspect ratio
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Save optimized image
        img.save(image_path, optimize=True, quality=quality)
        
        return True
        
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return False


def delete_old_profile_picture(instance):
    """
    Delete old profile picture when uploading a new one.
    
    This prevents accumulation of unused files on the server.
    
    Args:
        instance: Model instance with profile_picture field
        
    Returns:
        bool: True if file was deleted, False otherwise
        
    Example:
        >>> member = Names.objects.get(id=1)
        >>> delete_old_profile_picture(member)
        True
        
    Note:
        - Checks if file exists before attempting deletion
        - Silently fails if file doesn't exist (already deleted)
        - Does not delete default avatar
    """
    try:
        # Get old instance from database
        old_instance = instance.__class__.objects.get(pk=instance.pk)
        
        # Check if old instance has a profile picture
        if old_instance.profile_picture:
            old_file = old_instance.profile_picture
            
            # Check if it's not the default avatar
            if 'default_avatar' not in old_file.name:
                # Check if file exists
                if os.path.isfile(old_file.path):
                    # Delete the file
                    os.remove(old_file.path)
                    return True
                    
    except instance.__class__.DoesNotExist:
        # New instance, no old file to delete
        pass
    except Exception as e:
        print(f"Error deleting old profile picture: {e}")
        
    return False


def get_file_size_display(size_in_bytes):
    """
    Convert file size in bytes to human-readable format.
    
    Args:
        size_in_bytes (int): File size in bytes
        
    Returns:
        str: Human-readable file size
        
    Example:
        >>> get_file_size_display(1024)
        '1.00 KB'
        >>> get_file_size_display(1048576)
        '1.00 MB'
        >>> get_file_size_display(500)
        '500 bytes'
    """
    if size_in_bytes < 1024:
        return f"{size_in_bytes} bytes"
    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.2f} KB"
    else:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"


def create_thumbnail(image_path, thumbnail_size=(150, 150)):
    """
    Create a thumbnail version of an image.
    
    Args:
        image_path (str): Path to original image
        thumbnail_size (tuple): Thumbnail dimensions (width, height)
        
    Returns:
        str: Path to thumbnail file, or None if failed
        
    Example:
        >>> create_thumbnail('/media/profile_pics/john/photo.jpg')
        '/media/profile_pics/john/thumb_photo.jpg'
        
    Note:
        - Thumbnail is saved in same directory as original
        - Filename is prefixed with 'thumb_'
        - Maintains aspect ratio
    """
    try:
        img = Image.open(image_path)
        img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        
        # Generate thumbnail path
        directory = os.path.dirname(image_path)
        filename = os.path.basename(image_path)
        thumb_filename = f"thumb_{filename}"
        thumb_path = os.path.join(directory, thumb_filename)
        
        # Save thumbnail
        img.save(thumb_path, optimize=True, quality=85)
        
        return thumb_path
        
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return None
