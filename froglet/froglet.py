###############################################################
#
# Froglet - A Python client for Frog - v0.2
#       By Herman Slatman
#       https://hermanslatman.nl
#
#       Licensed under GPLv3
#
# Original work from:
#
# PyNLPl - Frog Client - Version 1.4.1
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#
#       Derived from code by Rogier Kraf
#
###############################################################

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from sys import version
import json
import socket

class Froglet(object):
    def __init__(self, host="localhost", port=12345, server_encoding="utf-8",
                 returnall=True, timeout=120.0, ner=False):
        """Create a client connecting to a Frog or Tadpole server."""
        self.buffsize = 4096
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(timeout)
        self.socket.connect((host, int(port)))
        self.server_encoding = server_encoding
        self.returnall = returnall


    def process(self, input_data, source_encoding="utf-8", return_unicode=True, oldfrog=False, format=u"plain"):
        """Receives input_data in the form of a str or unicode object,
            passes this to the server, with proper consideration for the encodings,
            (word,pos,lemma,morphology), each of these is a proper unicode object
            unless return_unicode is set to False, in which case raw strings will be returned.
            Return_unicode is no longer optional, it is fixed to True,
            parameter is still there only for backwards-compatibility."""
        if isinstance(input_data, list) or isinstance(input_data, tuple):
            input_data = " ".join(input_data)


        #decode (or preferably do this in an earlier stage)
        input_data = check_unicode(input_data, source_encoding)
        input_data = input_data.strip(' \t\n')

        to_send = input_data.encode(self.server_encoding) + b'\r\n'
        if not oldfrog:
            to_send += b'EOT\r\n'
        self.socket.sendall(to_send) #send to socket in desired encoding
        output = []

        done = False
        while not done:
            data = b""
            while not data or data[-1] != b'\n':
                moredata = self.socket.recv(self.buffsize)
                if not moredata:
                    break
                data += moredata


            data = check_unicode(data, self.server_encoding)


            for line in data.strip(' \t\r\n').split('\n'):
                if line == "READY":
                    done = True
                    break
                elif line:
                    line = line.split('\t') #split on tab
                    if len(line) > 4 and line[0].isdigit(): #first column is token number
                        if line[0] == '1' and output:
                            if self.returnall:
                                output.append((None,) * 10)
                            else:
                                output.append((None,) * 5)
                        fields = line[1:]
                        token_number = int(line[0])
                        named_entity = chunk = confidence = token_number_head = dependency_type = ""
                        word, lemma, morph, pos = fields[0:4]
                        if len(fields) > 4:
                            confidence = float(fields[4])
                        if len(fields) > 5:
                            named_entity = fields[5]
                        if len(fields) > 6:
                            chunk = fields[6]
                        if len(fields) > 7:
                            token_number_head = int(fields[7])
                        if len(fields) > 8:
                            dependency_type = fields[8]

                        if len(fields) < 5:
                            raise Exception("Can't process response line from Frog: ", repr(line),
                                            " got unexpected number of fields ",
                                            str(len(fields) + 1))

                        if self.returnall:
                            output.append((token_number, word, lemma, morph, pos, confidence, named_entity, chunk, token_number_head, dependency_type))
                        else:
                            output.append((token_number, word, lemma, morph, pos))

        if format == u"json":
            # return the output in json format: first create dict
            dict_tokens = create_dict(output)

            # then create the json dump
            json_tokens = create_json(dict_tokens)

            return json_tokens
        elif format == u"dict":
            # return the output in dict format
            dict_tokens = create_dict(output)

            return dict_tokens
        else:
            return output


    def process_aligned(self, input_data, source_encoding="utf-8", return_unicode=True):
        output = self.process(input_data, source_encoding, return_unicode)
        outputwords = [x[0] for x in output]
        inputwords = input_data.strip(' \t\n').split(' ')
        alignment = align(inputwords, outputwords)
        for i, _ in enumerate(inputwords):
            targetindex = alignment[i]
            if targetindex == None:
                if self.returnall:
                    yield (None,) * 10
                else:
                    yield (None,) * 5
            else:
                yield output[targetindex]

    def __del__(self):
        self.socket.close()


def create_dict(processed_tokens):
    """Creates a Python dict describing the entire Frog output.
    
    Returns a dict object containing mappings to dicts describing a token.

    :param processed_tokens: tokens processed by Frog
    :type processed_tokens: list
    """
    result = {}
    for item in processed_tokens:
        # every item is a tuple, consisting of token number, token, lemmatized, etcetera (5 or 10 tuple)
        # we process one line separately now...
        # so, every token is supposed to be part of 1 sentence
        item_dict = {}

        token_number, word, lemma, morph, pos = item[:5]
        item_dict['token_number'] = token_number # raw token number is set (Frog is 1-indexed)
        item_dict['word'] = word
        item_dict['lemma'] = lemma
        item_dict['morph'] = morph
        item_dict['pos'] = pos

        if len(item) == 10:
            confidence, named_entity, chunk, token_number_head, dependency_type = item[5:]
            item_dict['confidence'] = confidence
            item_dict['named_entity'] = named_entity
            item_dict['chunk'] = chunk
            item_dict['token_number_head'] = token_number_head
            item_dict['dependency_type'] = dependency_type

        # processing the item is complete; add it to the result
        # the key is the token number minus 1, because 0-indexing is much nicer...
        result[int(token_number) - 1] = item_dict

    # adding some stats / diagnostics
    result['length'] = len(processed_tokens)

    return result


def create_json(processed_tokens):
    """Returns json dump of tokens in dict.

    :param processed_tokens: tokens processed by Frog
    :type processed_tokens: dict
    """
    # processing done; return result as json, sort the keys
    return json.dumps(processed_tokens, sort_keys=True)



def align(inputwords, outputwords):
    """For each inputword, provides the index of the outputword"""
    alignment = []
    cursor = 0
    for inputword in inputwords:
        if len(outputwords) > cursor and outputwords[cursor] == inputword:
            alignment.append(cursor)
            cursor += 1
        elif len(outputwords) > cursor+1 and outputwords[cursor+1] == inputword:
            alignment.append(cursor+1)
            cursor += 2
        else:
            alignment.append(None)
            cursor += 1
    return alignment

def check_unicode(string, encoding='utf-8', errors='strict'):
    #ensure string is properly unicode.. wrapper for python 2.6/2.7,
    if version < '3':
        #ensure the object is unicode
        if isinstance(string, unicode):
            return string
        else:
            return unicode(string, encoding, errors=errors)
    else:
        #will work on byte arrays
        if isinstance(string, str):
            return string
        else:
            return str(string, encoding, errors=errors)
