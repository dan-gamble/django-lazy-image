from django.apps import apps
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from sorl.thumbnail import get_thumbnail

from .conf import settings


class ImageView(RedirectView):
    # If they change the source image, we don't want to be showing the old image.
    # Sorl uses memcached to retrieve images with the same args, so this should
    # be pretty quick.
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        # kwargs:
        # {'name': 'the_image.jpg', 'model': 'news.Article', 'pk': '9', 'field': 'hero_image', 'width': '285', 'height': '400', 'format': 'webp', 'crop': 'None'}
        Model = apps.get_model(*kwargs['model'].split('.', 1))
        obj = Model.objects.get(pk=kwargs['pk'])
        image = getattr(obj, kwargs['field'])

        sorl_args = [
            image
        ]
        sorl_kwargs = {}

        dimensions = ''
        width = kwargs['width']
        height = kwargs['height']

        if width == 'auto':
            dimensions = 'x{}'.format(height)
        elif height == 'auto':
            dimensions = width
        else:
            dimensions = '{}x{}'.format(width, height)

            if 'crop' not in kwargs:
                kwargs['crop'] = 'center'

        sorl_args.append(dimensions)

        if kwargs['crop'].lower() != 'none':
            sorl_kwargs['crop'] = kwargs['crop']

        if kwargs['format'] != 'source':
            sorl_kwargs['format'] = kwargs['format'].upper()

        sorl_kwargs['quality'] = int(kwargs['quality'])

        return get_thumbnail(
            *sorl_args,
            **sorl_kwargs
        ).url



class OSMImageRefFieldImageView(RedirectView):
    # If they change the source image, we don't want to be showing the old image.
    # Sorl uses memcached to retrieve images with the same args, so this should
    # be pretty quick.
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        # kwargs:
        # {'pk': '9', 'width': '285', 'height': '400', 'format': 'webp', 'crop': 'None'}
        file_model = apps.get_model(*settings.LAZY_IMAGE_OSM_FILE_MODEL.split('.', 1))
        file_ = get_object_or_404(file_model, pk=kwargs['pk'])

        sorl_args = [
            file_.file,
        ]
        sorl_kwargs = {}

        dimensions = ''
        width = kwargs['width']
        height = kwargs['height']

        if width == 'auto':
            dimensions = 'x{}'.format(height)
        elif height == 'auto':
            dimensions = width
        else:
            dimensions = '{}x{}'.format(width, height)

            if 'crop' not in kwargs:
                kwargs['crop'] = 'center'

        sorl_args.append(dimensions)

        if kwargs['crop'].lower() != 'none':
            sorl_kwargs['crop'] = kwargs['crop']

        if kwargs['format'] != 'source':
            sorl_kwargs['format'] = kwargs['format'].upper()

        sorl_kwargs['quality'] = int(kwargs['quality'])

        return get_thumbnail(
            *sorl_args,
            **sorl_kwargs
        ).url
