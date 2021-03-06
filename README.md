# Froglet - A client for contacting a Frog server.

## Synopsis

A Python client for contacting a Frog server. Frog is an integration of memory-based natural language processing (NLP) modules developed for the Dutch language by the University of Tilburg and Radboud University Nijmegen. This client provides a Python API for interacting with a Frog server to perform certain tasks on Dutch texts, including tokenization, lemmatization and NER tagging. More information about Frog can be found on https://languagemachines.github.io/frog/.

## Code Example

Assuming a Frog server is running at some IP address and known port. For now this suffices:

```
import froglet

# replace with specific hostname or IP and port
client = froglet.Froglet("<hostname/ip>", "<port>")

# default format is *plain*, which means a tuple is returned
for data in client.process("Dit is een voorbeeldbericht om te froggen!"):
    word, lemma, morph, pos = data[:4]
	print(word, lemma, morph, pos)
	
	# do some other awesome things with the response



# an example requesting dict output:
dict_tokens = client.process("Dit is een voorbeeldbericht om te froggen!", format="dict")

# dict_tokens contains the length key, which describes the number of tokens in the dict
# see the froglet code for explanation why
for i in xrange(dict_tokens['length']):
	print(dict_tokens[i])
	print(dict_tokens[i]['lemma'])



# another example, using json output:
json_string = client.process("Dit is een voorbeeldbericht om te froggen!", format="json")

# the json is in string format, ready to be saved or deserialized
import json
json_tokens = json.loads(json_string)

# the json_data is equivalent to the dict_tokens described before
# take care that due to deserialization the type information is lost (i.e. str(i))
for str(i) in xrange(int(json_tokens['length'])):
    print(json_tokens[i])
	print(json_tokens[i]['morph'])
```

## Motivation

A Python client for Frog already [exists](https://github.com/proycon/pynlpl/blob/master/clients/frogclient.py) which is created by [one of the creators](https://github.com/proycon) of Frog itself. That implementation relies on a bigger package for NLP tasks. This client does not rely on installation of the entire [PyNLPl](https://github.com/proycon/pynlpl), but initial code is basically extracted from the original. In addition to that, some future improvements and additions will be implemented. Also check out the roadmap.

## Installation

This package is available on [PyPI](https://pypi.python.org/). Installation can be performed via the usual command you use for installing Python packages.

## API Reference

TODO: nothing to see here yet.

## Tests

TODO: nothing to see here yet.

## Roadmap

  * Providing several output formats
  * Additional documentation
  * ~~Making available for distribution~~
  * Implement configuration management, e.g. using a .ini file
  * Asynchronous calls?
  * When contacting a Frog server on localhost, don't use the network, but use original Python bindings
  * A REPL, for fun
  
## Contributors

Feel free to fork and create fixes or additions. Shoot a PR when done.

## License

Licensed under GPLv3