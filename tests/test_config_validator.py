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


def containskeysconfigvalidator_ko_test():

    assert not ContainsKeysConfigValidator({KEYS_LIST:["ok1","ok3"]}).validate({"ok1":True,"ok2":True})

    assert not ContainsKeysConfigValidator({KEYS_LIST:["ok3"]}).validate({"ok1":True,"ok2":True})


def containskeyinstanceofconfigvalidator_ok_test():

    assert ContainsKeyAndInstanceConfigValidator({"list":type([])}).validate({"list":["item1","item2"]})

def containskeyinstanceofconfigvalidator_ko_test():

    assert not ContainsKeyAndInstanceConfigValidator({"list":type([])}).validate({"list":"item1","list2":"item2"})

    assert not ContainsKeyAndInstanceConfigValidator({"list":type([])}).validate({"list1":"item1","list2":"item2"})





