"""
envparse is a simple utility to parse environment variables.
"""
from __future__ import unicode_literals

import json as pyjson
import logging
import os
import re
import urllib.parse as urlparse

logger = logging.getLogger(__file__)


class ConfigurationError(Exception):
    pass


# Cannot rely on None since it may be desired as a return value.
NOTSET = type(str("NoValue"), (object,), {})


def shortcut(cast):
    def method(self, var, *args, **kwargs):
        return self.__call__(var, cast=cast, *args, **kwargs)

    return method


class Env(object):
    """
    Lookup and cast environment variables with optional schema.
    Usage:::
        env = Env()
        env('foo')
        env.bool('bar')
        # Create env with a schema
        env = Env(MAIL_ENABLED=bool, SMTP_LOGIN=(str, 'DEFAULT'))
        if env('MAIL_ENABLED'):
            ...
    """

    BOOLEAN_TRUE_STRINGS = ("true", "on", "ok", "y", "yes", "1")

    def __init__(self, **schema):
        self.schema = schema

    def __call__(self, var, default=None, cast=None):
        """
        Return value for given environment variable.
        :param var: Name of variable.
        :param default: If var not present in environ, return this instead.
        :param cast: Type or callable to cast return value as.
        :param subcast: Subtype or callable to cast return values as (used for
                        nested structures).
        :param force: force to cast to type even if default is set.
        :param preprocessor: callable to run on pre-casted value.
        :param postprocessor: callable to run on casted value.
        :returns: Value from environment or default (if set).
        """
        logger.debug("Get '%s' casted as '%s'/'%s' with default '%s'", var, cast)

        if var in self.schema:
            params = self.schema[var]
            if isinstance(params, dict):
                if cast is None:
                    cast = params.get("cast", cast)
            else:
                if cast is None:
                    cast = params
        # Default cast is `str` if it is not specified. Most types will be
        # implicitly strings so reduces having to specify.
        cast = str if cast is None else cast

        try:
            value = os.environ[var]
        except KeyError:
            if default is NOTSET:
                error_msg = "Environment variable '{}' not set.".format(var)
                raise ConfigurationError(error_msg)
            else:
                value = default

        if value != default:
            value = self.cast(value, cast)

        return value

    @classmethod
    def cast(cls, value, cast=str):
        """
        Parse and cast provided value.
        :param value: Stringed value.
        :param cast: Type or callable to cast return value as.
        :returns: Value of type `cast`.
        """
        if cast is bool:
            value = value.lower() in cls.BOOLEAN_TRUE_STRINGS
        elif cast is float:
            # Clean string
            float_str = re.sub(r"[^\d,\.]", "", value)
            # Split to handle thousand separator for different locales, i.e.
            # comma or dot being the placeholder.
            parts = re.split(r"[,\.]", float_str)
            if len(parts) == 1:
                float_str = parts[0]
            else:
                float_str = "{0}.{1}".format("".join(parts[0:-1]), parts[-1])
            value = float(float_str)

        try:
            return cast(value)
        except ValueError as error:
            raise ConfigurationError(*error.args)

    # Shortcuts
    bool = shortcut(bool)
    dict = shortcut(dict)
    float = shortcut(float)
    int = shortcut(int)
    list = shortcut(list)
    set = shortcut(set)
    str = shortcut(str)
    tuple = shortcut(tuple)
    json = shortcut(pyjson.loads)
    url = shortcut(urlparse.urlparse)


# Convenience object if no schema is required.
env = Env()
