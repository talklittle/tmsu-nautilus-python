# Obsolete

Superseded by [Rust version](https://github.com/talklittle/tmsu-nautilus-rs) which is faster and less buggy.

# TMSU Nautilus Extension

GNOME Nautilus extension for file tagging using [TMSU](https://github.com/oniony/TMSU/).

## Requirements

* Nautilus 3
* Gtk 3
* [TMSU](https://github.com/oniony/TMSU/) 0.6.1+

## Installation

Create the nautilus-python extensions directory:

    mkdir -p ~/.local/share/nautilus-python/extensions

Copy (or symlink) `tmsu_tags.py` into the extensions directory:

    cp tmsu_tags.py ~/.local/share/nautilus-python/extensions/tmsu_tags.py

Kill and restart Nautilus:

    nautilus -q

## Release notes

See [CHANGELOG.md](CHANGELOG.md) for changes between versions.

## License

[GNU General Public License version 3](COPYING.txt)
