"""
file_builder
~~~~~~~~~~~~~

Houses the declaration of :py:class:`FileBuilder` along with supporting
classes, functions, and attributes.
"""

__author__ = 'Andrew van Herick'
__copyright__ = \
    'Unpublished Copyright (c) 2020 Andrew van Herick. All Rights Reserved.'
__license__ = 'Apache Software License 2.0'

import errno
import os
from abc import ABC, abstractmethod

from inceptiontools.archetype_parameters import ArchetypeParameters
from inceptiontools.archetype_resource_builder import ArchetypeResourceBuilder
from inceptiontools.constants import UNIMPLEMENTED_ABSTRACT_METHOD_ERROR


class FileBuilder(ArchetypeResourceBuilder, ABC):
    """
    This abstract base provides a common interface for building files for an
    an :py:class:`inceptiontools.Archetype`.  It provides 'template-method'
    implementations of the methods, :py:meth:`path` and:py:method:`incept`
    which rely on subclass implementations to determine a subpath under the
    project root directory, as well as how to render file content,
    both from a :py:class:`inceptiontools.ArchetypeParameters`.
    """

    def _path(self, root_dir, params):
        return os.path.join(root_dir, self.subpath(params))

    def path(self, root_dir: str, params: ArchetypeParameters) -> str:
        """
        Uses the implementation of :py:meth:`subpath` to determine the
        absolute path to the file saved by :py:meth:`incept`.
        :param root_dir: the root directory argument for
        :py:meth:`incept`
        :param params: the parameters argument for :py:meth:`incept`
        :return: the path
        """
        return self._path(root_dir, params)

    def build(self, root_dir: str, params: ArchetypeParameters) -> None:
        """
        Renders and saves the content generated by :py:meth:`render` to the
        location under `root_dir` determined by the _result of
        :py:meth:``subpath``.
        :param root_dir: the root directory under which the file should be
        saved
        :param params: the parameters used to determine the saved file
        content and possibly the subpath under the root directory
        :return: :py:const:`None`
        ..:note: this method has dependencies on the implementations of
        :py:meth:`render` and :py:meth:`subpath`
        """
        content = self.render(params)

        p = self._path(root_dir, params)
        try:
            os.makedirs(os.path.dirname(p))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

        with open(p, 'w') as f:
            f.write(content)

    @abstractmethod
    def subpath(self, params: ArchetypeParameters) -> str:
        """
        Subclasses are required to implement this method.  Implementations
        of this method should return the subpath, under the root directory,
        of the file to be saved by :py:meth:`incept`.
        :param params: the :py:class `ArchetypeParameters` to use as context
        when creating the subpath, e.g., when storing files whose sub-path
        might be determined by the package name.
        :return: the subpath
        """
        raise UNIMPLEMENTED_ABSTRACT_METHOD_ERROR

    @abstractmethod
    def render(self, params: ArchetypeParameters) -> str:
        """
        Subclasses are required to implement this method.  Implementations
        of this method should return the content of the file to be saved by
        :py:meth:`incept`.
        :param params: the :py:class:`ArchetypeParameters` to use as context
        when building the content
        :return: the content of the file to be saved by
        :py:meth:`incept`
        """
        raise UNIMPLEMENTED_ABSTRACT_METHOD_ERROR
