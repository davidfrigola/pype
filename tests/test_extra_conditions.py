
from pype.extra_conditions import *
from mock import MagicMock
from mock import patch


""" RegexCondition tests """
def init_ok_RegexCondition_test():

    condition = RegexCondition({"value":".*"})


def init_fail_RegexCondition_test():

    try:
        condition = RegexCondition({"value-no":".*"})
    except:
        pass
