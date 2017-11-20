# Django Lazy Image

`django-lazy-image` is a small Django utility that allows you to render images lazily on the frontend to minimise initial page load.

## Installation

To install `django-lazy-image` just run:

```cli
pip install django-lazy-image
```

## Requirements

* Jinja2
* Django >= 1.11 (It's only been tested on 1.11 but i'm pretty sure it will work on 1.8+)
* [Django Jinja](https://github.com/niwinz/django-jinja)

## Configuration

Add `django_lazy_image` to your `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'django_lazy_image',
    ...
]
```

Then there are 2 ways to use the static files with Django:

### NPM (The preferred way)

You can simply do

```cli
npm install django-lazy-image
```

or

```cli
yarn add django-lazy-image
```

Then include the Javascript / CSS as a module

**file.js**
```javascript
import LazyImage from 'django-lazy-image';

// Only run the below code if the page has a lazy image instance
const lazyImage = document.querySelector('.js-LazyImage')
if (lazyImage) {
  // Collect all the lazy images on the page
  const lazyImages = document.querySelectorAll('.js-LazyImage')
  // Set up our IntersectionObserver callback
  const callback = (entries, observer) => {
    Array.from(entries).forEach((entry, index) => {
      // If any of the images have come in to view, activate them sequentially
      if (entry.isIntersecting) {
        window.setTimeout(() => {
          new LazyImage({ el: entry.target })
          observer.unobserve(entry.target)
        }, 150 * index)
      }
    })
  }
  const observer = new IntersectionObserver(callback, {
    threshold: 0.4
  })
  Array.from(lazyImages).forEach(image => observer.observe(image))
}
```

**file.css**
```css
@import 'django-lazy-image/dist/css/lazy-image.css';
```

### Django Static
Somewhere in your `base.html` add:

```html
{{ static('django_lazy_image/css/lazy-image.css') }}
{{ static('django_lazy_image/js/lazy-image.js') }}
```

You can then use the `lazyImage` function that is on the global object

```javascript
var images = [].slice.call(document.querySelectorAll('.js-LazyImage'))
images.forEach(function (el) {
  var image = window.lazyImage(el)
  ...
})
```
