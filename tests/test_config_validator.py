from pype.config_validator import *
from mock import MagicMock
from mock import patch


def nononeconfigvalidator_ok_test():

    assert NoNoneConfigValidator(None).validate({})

def nononeconfigvalidator_ko_test():

    assert not NoNoneConfigValidator().validate(None)


def containskeyconfigvalidator_ok_test():

    assert ContainsKeyConfigValidator({KEY_VALUE:"ok"}).validate({"ok":True})

def containskeyconfigvalidator_ko_test():

    assert not ContainsKeyConfigValidator({KEY_VALUE:"ok"}).validate({"ko":True})

def containskeysconfigvalidator_ok_test():

    assert ContainsKeysConfigValidator({KEYS_LIST:["ok1","ok2"]}).validate({"ok1":True,"ok2":True})

    assert ContainsKeysConfigValidator({KEYS_LIST:["ok1"]}).validate({"ok1":True,"ok2":True})
