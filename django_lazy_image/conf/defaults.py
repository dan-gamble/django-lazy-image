from django.conf import settings

# The default quality settings passed to Sorl
LAZY_IMAGE_DEFAULT_QUALITY_OPTIONS = {
    'normal': 60,
    'webp': 80,
}
LAZY_IMAGE_DEFAULT_QUALITY = LAZY_IMAGE_DEFAULT_QUALITY_OPTIONS['normal']

# This is the namespace you gave the package in your urls.py
LAZY_IMAGE_URL_NAMESPACE = 'assets'

# This is the file model that Sorl is expecting to create a thumbnail from
LAZY_IMAGE_FILE_MODEL = 'media.File'

# Do you want the lazy images to server webp where possible?
LAZY_IMAGE_ENABLE_WEBP = True
