import os
import uuid
from flask import current_app, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


class FileService:
    """Service class for handling file operations."""
    
    THUMBNAIL_SIZE = (300, 300)
    BANNER_SIZE = (1200, 400)
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed."""
        return ('.' in filename and
                filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS'])
    
    @staticmethod
    def generate_filename(filename):
        """Generate unique filename while preserving extension."""
        if not filename:
            return None
        
        extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{extension}"
        return secure_filename(unique_filename)
    
    @staticmethod
    def save_file(file, subfolder='general'):
        """Save uploaded file and return filename."""
        if not file or not file.filename:
            return None
        
        if not FileService.allowed_file(file.filename):
            raise ValueError("File type not allowed")
        
        filename = FileService.generate_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        
        # Create directory if it doesn't exist
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        
        return f"uploads/{subfolder}/{filename}"
    
    @staticmethod
    def save_image(file, subfolder='images', resize_to=None):
        """Save image file (basic implementation without PIL)."""
        if not file or not file.filename:
            return None
        
        if not FileService.allowed_file(file.filename):
            raise ValueError("File type not allowed")
        
        filename = FileService.generate_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        
        # Create directory if it doesn't exist
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, filename)
        
        # Save file directly (without image processing for now)
        try:
            file.save(file_path)
        except Exception as e:
            raise ValueError(f"Error saving image: {str(e)}")
        
        return f"uploads/{subfolder}/{filename}"
    
    @staticmethod
    def save_product_image(file):
        """Save product image."""
        return FileService.save_image(file, 'products')
    
    @staticmethod
    def save_shop_banner(file):
        """Save shop banner image."""
        return FileService.save_image(file, 'banners')
    
    @staticmethod
    def delete_file(file_path):
        """Delete file from filesystem."""
        if not file_path:
            return False
        
        try:
            full_path = os.path.join(current_app.root_path, 'static', file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
        except Exception as e:
            current_app.logger.error(f"Error deleting file {file_path}: {str(e)}")
        
        return False
    
    @staticmethod
    def validate_image_upload(file):
        """Validate image upload before processing."""
        if not file:
            return False, "No file provided"
        
        if not file.filename:
            return False, "No filename provided"
        
        if not FileService.allowed_file(file.filename):
            return False, "File type not allowed"
        
        # Check file size (file.content_length may not be available)
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)
        
        max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
        if file_length > max_size:
            return False, f"File too large (max {max_size // (1024 * 1024)}MB)"
        
        return True, "Valid file"


# Global file service instance
file_service = FileService()