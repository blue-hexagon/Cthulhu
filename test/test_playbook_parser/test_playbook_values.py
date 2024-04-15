from src.conf.playbook_parser.playbook_values import TruthyValue


def test_truthy__only_one_is_true():
    assert TruthyValue.only_one_is_truthy('yes', 'nay', 'no')
    assert TruthyValue.only_one_is_truthy('yes', 'no')
    assert TruthyValue.only_one_is_truthy('yes')
    assert not TruthyValue.only_one_is_truthy('no')
    assert not TruthyValue.only_one_is_truthy('nay', 'no')
    assert not TruthyValue.only_one_is_truthy('yes', 'nay', 'no', 'exactly')
    assert not TruthyValue.only_one_is_truthy('yes', 'exactly')
    assert not TruthyValue.only_one_is_truthy('yes', 'exactly', 'no')
