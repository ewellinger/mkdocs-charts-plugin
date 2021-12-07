# mkdocs-charts-plugin

Mkdocs plugin to create plots from data.

## Installation

```shell
pip3 install mkdocs-charts-plugin
```

## Usage


## Options

- `vega_width` (default `container`). If not set explicitly, update the vega-lite schema width with this setting (see [vegalite size](https://vega.github.io/vega-lite/docs/size.html))


# TODO:


## set width correctly 

check for mkdocs theme


## support data files located in `docs/` folder

we need a relative URL for the data

--> parse it in the fence_ function?
- is valid json
- convert to json
- look for .get('data').get('url')
- is absolute?
- some mkdocs function to get absolute url

- in the plugin docs, is the URL relative to mkdocs.yml or to `docs/` ?

## data path

find the mkdocs root path

## validator fences

- add a validator python function for is valid JSON

## plugin to include JS and set the markdown_extension also?



## Toggle dark mode

- theme, switch to dark mode with mkdocs-material

toggle themes
there's a refresh() function shown in the <script> source
https://vega.github.io/vega-themes/?renderer=canvas&theme=quartz

## Styling

- CSS for styling colors to use/match mkdocs-material ?

## More

- write docs
    - page on how it works
- promote the plugin
  - blogpost, twitter
  - plugin wiki
  - refer to it from table-reader
  - add to demo in print-site
- add plotly express backend also?
- examples with altair

# Credits 

https://github.com/koaning/justcharts
https://facelessuser.github.io/pymdown-extensions/extras/mermaid/
https://vega.github.io/vega-lite/docs/config.html
