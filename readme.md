# CoilSnakeTools

A small collection of command-line tools to view data from a [CoilSnake](https://github.com/pk-hack/CoilSnake/) project that is otherwise hard to view.

## Features

* .gifs of animations
* .gifs of swirls
* Icons on town maps
* Dump level stats

## Usage

```
coilsnaketools.py [--help] [--path PATH] --mode MODE [--output OUTPUT]

Options:
  -p, --path TEXT
      Path of a CoilSnake project. If blank, uses the current directory.
  -m, --mode [anim|swirl|level|townmap|all]
      Function to execute.  [required]
        anim: make .gifs of animations.
        swirl: make .gifs of swirls.
        level: make a .txt dump of level stats.
        townmap: make .pngs of icons on town maps.
        all: does every above function.
  -o, --output TEXT
      Output location. If blank, uses the current directory.
  --help
      Generate a help message and exit.
```

E.g.`coilsnaketools.py -p "C:\Some\Awesome\Project" -m townmap -o "C:\Some\Awesome\Output"`


## Dependencies

* click
* Pillow
* pyyaml