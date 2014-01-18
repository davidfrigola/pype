
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

def init_ok_ContainsTextCondition_test():

    pass


def init_fail_ContainsTextCondition_test():

    pass

def evaluate_true_ContainsTextCondition_test():

    containsTextCondition = ContainsTextCondition({"value":"test"})

    assert containsTextCondition.evaluate(BaseItem(None,"This is a test value that evaluates to true"))

def evaluate_false_ContainsTextCondition_test():

    containsTextCondition = ContainsTextCondition({"value":"falsetest"})

    assert not containsTextCondition.evaluate(BaseItem(None,"This is a test value that evaluates to true"))


def evaluate_false_AlreadyProcessedCondition():

    condition = AlreadyProcessedCondition({})

    assert not condition.evaluate(BaseItem(None,"any value"))

def evaluate_true_AlreadyProcessedCondition():
    pass

