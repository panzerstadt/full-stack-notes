# SASS / SCSS

## TODO: tutorials!
- https://medium.com/@thejasonfile/getting-started-with-sass-dedb271bdf5a
- https://tutorialzine.com/2016/01/learn-sass-in-15-minutes
- https://scotch.io/tutorials/getting-started-with-sass
- https://sass-lang.com/guide

## watch a scss file (autocompile into css)
> sass --watch input_file.scss output_file.css

### variables
- store colors, font stacks, or any css value you think you want to reuse
- use $ to turn it into a variable

```css
$font-stack: Helvetica, sans-serif;

$primary-color: #333;

body {
	font: 100% $font-stack;
	color: $primary-color;
}
```

### another note
