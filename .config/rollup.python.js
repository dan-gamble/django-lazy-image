import babel from 'rollup-plugin-babel';

export default {
  input: 'assets/js/lazy-image.js',
  output: {
    file: 'django_lazy_image/static/django_lazy_image/js/lazy-image.js',
    format: 'umd',
    name: 'lazyImage'
  },
  plugins: [
    babel({
      exclude: 'node_modules/**' // only transpile our source code
    })
  ]
};
