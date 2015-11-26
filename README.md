# Froglet - A client for contacting a Frog server.

## Synopsis

A Python client for contacting a Frog server. Frog is an integration of memory-based natural language processing (NLP) modules developed for the Dutch language by the University of Tilburg and Radboud University Nijmegen. This client provides a Python API for interacting with a Frog server to perform certain tasks on Dutch texts, including tokenization, lemmatization and NER tagging. More information about Frog can be found on https://languagemachines.github.io/frog/.

## Code Example

TODO: nothing to see here yet.

## Motivation

A Python client for Frog already [exists](https://github.com/proycon/pynlpl/blob/master/clients/frogclient.py) which is created by [one of the creators](https://github.com/proycon) of Frog itself. That implementation relies on a bigger package for NLP tasks. This client does not rely on installation of the entire [PyNLPl](https://github.com/proycon/pynlpl), but initial code is basically extracted from the original. In addition to that, some future improvements and additions will be implemented. Also check out the roadmap.

## Installation

TODO: nothing to see here yet.

## API Reference

TODO: nothing to see here yet.

## Tests

TODO: nothing to see here yet.

## Roadmap

  * Asynchronous calls
  * Providing several output formats
  * Implement configuration management, e.g. using a .ini file
  * When contacting a Frog server on localhost, don't use the network, but use original Python bindings
  * A REPL, for fun
  
## Contributors

Feel free to fork and create fixes or additions. Shoot a PR when done.

## License

Licensed under GPLv3