# -*- coding: utf-8 -*-
#
# phys_pkg.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Interface to a physical OPC package, either a zip archive or directory"""

import os


class BlobCollection(dict):
    """
    Structures a set of blobs, like a set of files in an OPC package.
    It can add and retrieve items by URI (relative path, roughly) and can
    also retrieve items by uri_tail, the trailing portion of the URI.
    """


class PhysPkg(object):
    """
    Provides read and write services for packages on the filesystem. Suitable
    for use with OPC packages in either Zip or expanded directory form.
    |PhysPkg| objects are iterable, generating a (uri, blob) 2-tuple for each
    item in the package.
    """
    def __init__(self, blobs, root_uri):
        super(PhysPkg, self).__init__()
        self._blobs = blobs
        self._root_uri = root_uri

    def __iter__(self):
        """
        Generate a (uri, blob) 2-tuple for each of the items in the package.
        """
        return iter(self._blobs.items())

    @staticmethod
    def read(path):
        """
        Return a |PhysPkg| instance loaded with contents of OPC package at
        *path*, where *path* can be either a regular zip package or a
        directory containing an expanded package.
        """
        if os.path.isdir(path):
            return DirPhysPkg.read(path)
        else:
            return ZipPhysPkg.read(path)

    @property
    def root_uri(self):
        return self._root_uri  # pragma: no cover


class DirPhysPkg(PhysPkg):
    """
    An OPC physical package that has been expanded into individual files in
    a directory structure that mirrors the pack URI.
    """
    def __init__(self, blobs, root_uri):
        super(DirPhysPkg, self).__init__(blobs, root_uri)

    @classmethod
    def read(cls, pkg_dir):
        """
        Return a |BlobCollection| instance loaded from *pkg_dir*.
        """
        return cls(None, None)


class ZipPhysPkg(PhysPkg):
    """
    An OPC physical package in the typically encountered form, a zip archive.
    """
    def __init__(self, blobs, root_uri):
        super(ZipPhysPkg, self).__init__(blobs, root_uri)

    @classmethod
    def read(cls, pkg_zip_path):
        """
        Return a |BlobCollection| instance loaded from *pkg_zip_path*.
        """
        return cls(None, None)
