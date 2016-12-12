import logging
"""Watching utilities"""


class SubClassWatcher(type):
    """
    Metaclass that logs subclassing.
    """
    def __init__(cls, name, bases, cls_dict):
        if len(cls.mro()) > 2:
            logging.debug("{} was subclassed by {}".format(cls.__name__, name))
        super(SubClassWatcher, cls).__init__(name, bases, cls_dict)
