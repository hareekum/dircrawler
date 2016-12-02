# -*- coding: utf-8 -*-

"""
dircrawler.transformers

This module contains some transformers used for transforming a filepath
"""

import hashlib


class AbstractTransformer(object):
    """Interface for file transformers"""

    def transform(self, *args, **kwargs):
        raise NotImplementedError


class MD5Transformer(AbstractTransformer):
    """Class for transforming a file path to the file's MD5 hash"""

    def transform(self, filepath, blocksize=65536):
        hasher = hashlib.md5()
        with open(filepath) as fh:
            buf = fh.read()
            hasher.update(buf)
        return hasher.hexdigest()


class FirstLineTransformer(AbstractTransformer):
    """Class for transforming a file path to the file's first line"""

    def transform(self, filepath):
        with open(filepath) as fh:
            line = fh.readline()
        return line
