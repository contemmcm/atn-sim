from abc import ABCMeta, abstractmethod


class AdsbForwarder(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def forward(self, message, time_of_arrival):
        raise NotImplementedError()

    @abstractmethod
    def __str__(self):
        raise NotImplementedError()
