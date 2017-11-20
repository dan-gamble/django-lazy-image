(function (global, factory) {
	typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
	typeof define === 'function' && define.amd ? define(factory) :
	(global.lazyImage = factory());
}(this, (function () { 'use strict';

var classCallCheck = function (instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
};

var LazyImage = function LazyImage(_ref) {
  var _this = this;

  var el = _ref.el;
  classCallCheck(this, LazyImage);

  this.el = el;
  this.smallImage = this.el.querySelector('.img-Image_Image-small');
  this.image = this.el.querySelector('.img-Image_Image[data-src]');
  this.src = this.image.dataset.src.split(', ');
  this.supportsObjectFit = 'objectFit' in document.documentElement.style;
  this.loadedClass = 'img-Image_Image-loaded';

  if (this.supportsObjectFit) {
    this.image.addEventListener('load', function () {
      _this.image.classList.add(_this.loadedClass);
    });
    this.image.addEventListener('transitionend', function (evt) {
      if (evt.propertyName === 'opacity') {
        _this.smallImage.parentNode.removeChild(_this.smallImage);
      }
    });

    this.image.setAttribute('src', this.src.join(', '));
  } else {
    var div = document.createElement('div');
    div.className = 'img-Image_Image img-Image_Image-large img-Image_Image-noObjectFit ' + this.loadedClass;
    var imageUrl = window.devicePixelRatio >= 2 ? this.src[1] : this.src[0];
    div.style.backgroundImage = 'url(' + imageUrl + ')';
    this.image.parentNode.replaceChild(div, this.image);
  }
};

return LazyImage;

})));
