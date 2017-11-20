import babel from 'rollup-plugin-babel';

export default {
  input: 'assets/js/lazy-image.js',
  output: {
    file: 'dist/js/lazy-image.web.js',
    format: 'umd',
    name: 'lazyImage'
  },
  plugins: [
    babel({
      exclude: 'node_modules/**' // only transpile our source code
    })
  ]
};
