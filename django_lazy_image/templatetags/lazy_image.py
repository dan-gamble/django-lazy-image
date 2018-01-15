# pylint: disable=too-complex, too-many-arguments, too-many-locals

import json

from django.core.urlresolvers import reverse
from django_jinja import library

from ..conf import settings


@library.global_function
def lazy_image(
        image, height=None, width=None, blur=True, max_width=1920, crop=None, show_small_image=True,
        quality=settings.LAZY_IMAGE_DEFAULT_QUALITY, webp=settings.LAZY_IMAGE_ENABLE_WEBP,
        responsive_sizes=None):
    user_sized = height and width
    reverse_url = '{}:thumbnail'.format(settings.LAZY_IMAGE_URL_NAMESPACE)

    if isinstance(quality, int):
        normal_quality = webp_quality = quality
    elif isinstance(quality, dict):
        try:
            normal_quality = quality['normal']
            webp_quality = quality['webp']
        except KeyError:
            normal_quality = settings.LAZY_IMAGE_DEFAULT_QUALITY_OPTIONS['normal']
            webp_quality = settings.LAZY_IMAGE_DEFAULT_QUALITY_OPTIONS['webp']

    if user_sized and not crop:
        crop = 'center'

    width, height, aspect_ratio = calculate_width_and_height(
        width, height, image, user_sized, max_width
    )

    responsize_aspects = {}

    if responsive_sizes:
        responsize_aspects['default'] = f'{aspect_ratio * 100}%'

        for key, value in responsive_sizes.items():
            sizes = calculate_width_and_height(
                value['width'],
                value['height'],
                image,
                True,
                max_width
            )
            responsize_aspects[key] = f'{sizes[2] * 100}%'

    # The aspect ratio will be used to size the image with a padding-bottom based element
    aspect_ratio_percentage = f'{aspect_ratio * 100}%'

    original_large_image_url = reverse(reverse_url, kwargs={
        'pk': image.pk,
        'width': width,
        'height': height,
        'format': 'source',
        'crop': crop,
        'quality': normal_quality,
    })

    original_large_image_url_2x = reverse(reverse_url, kwargs={
        'pk': image.pk,
        'width': width * 2,
        'height': height * 2,
        'format': 'source',
        'crop': crop,
        'quality': normal_quality,
    })

    webp_url = reverse(reverse_url, kwargs={
        'pk': image.pk,
        'width': width,
        'height': height,
        'format': 'webp',
        'crop': crop,
        'quality': webp_quality,
    }) if webp else None

    webp_url_2x = reverse(reverse_url, kwargs={
        'pk': image.pk,
        'width': width * 2,
        'height': height * 2,
        'format': 'webp',
        'crop': crop,
        'quality': webp_quality,
    }) if webp else None

    try:
        if webp:
            small_image_url = reverse(reverse_url, kwargs={
                'pk': image.pk,
                'width': int(round(width / 20)),
                'height': int(round(height / 20)),
                'format': 'webp',
                'crop': crop,
                'quality': 100,
            })
        else:
            small_image_url = reverse(reverse_url, kwargs={
                'pk': image.pk,
                'width': int(round(width / 20)),
                'height': int(round(height / 20)),
                'format': 'source',
                'crop': crop,
                'quality': 100,
            })
    except ValueError:
        # Guard against really tiny images, i.e. width / 20 results in 0.
        small_image_url = original_large_image_url

    return {
        'alt_text': image.alt_text or '',
        'aspect_ratio': aspect_ratio_percentage,
        'small_image_url': small_image_url,
        'original_large_image_url': original_large_image_url,
        'original_large_image_url_2x': original_large_image_url_2x,
        'webp': webp,
        'webp_url': webp_url,
        'webp_url_2x': webp_url_2x,
        'blur': blur,
        'show_small_image': show_small_image,
        'is_transparent': str(image.file).endswith('.png'),
        'responsive_aspects': json.dumps(responsize_aspects) if responsive_sizes else None,
    }


@library.global_function
@library.render_with('django_lazy_image/lazy-image.html')
def render_lazy_image(image, height=None, width=None, blur=True, max_width=1920, crop=None, show_small_image=True,
                      quality=settings.LAZY_IMAGE_DEFAULT_QUALITY_OPTIONS, webp=settings.LAZY_IMAGE_ENABLE_WEBP,
                      responsive_sizes=None):
    """
    Usage: {{ render_lazy_image(path.to.image) }}
    """

    return lazy_image(image, height, width, blur, max_width, crop, show_small_image, quality, webp, responsive_sizes)


def calculate_width_and_height(width, height, image, user_sized, max_width):
    # Ideally we will use the images uploaded sizes to get our aspect ratio but in certain circumstances, like cards,
    # we will use our own provided ones
    if not height:
        height = image.height

    if not width:
        width = image.width

    aspect_ratio = height / width if user_sized else image.height / image.width

    if width > max_width:
        width = max_width

    if width > height:
        height = int(width * aspect_ratio)

    return [width, height, aspect_ratio]
