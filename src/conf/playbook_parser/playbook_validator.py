from src.conf.playbook_parser.playbook_objects import Playbook
from src.conf.playbook_parser.playbook_parser import PlaybookParser
from src.conf.playbook_parser.playbook_values import TruthyValue
from src.conf.playbook_parser.utils.exceptions import NonUniqueProfileIdError, MultipleHostSelectorError, \
    MoreOrLessThanASingleOptionSelectedError


class PlaybookValidator:
    @staticmethod
    def validate_profiles(playbook: Playbook):
        """ Validate that all profiles contain unique a profile_id """
        profile_ids = []
        for profile in playbook.profiles:
            profile_ids.append(profile.profile_id)
        contains_duplicates = any(profile_ids.count(item) > 1 for item in profile_ids)
        if contains_duplicates:
            raise NonUniqueProfileIdError("Found non-unique profile_id across playbooks")

    @staticmethod
    def validate_use_groups_or_list(playbook: Playbook):
        for profile in playbook.profiles:
            if not TruthyValue.only_one_is_truthy(profile.hosts.use_list,profile.hosts.use_group):
                raise MultipleHostSelectorError("Use either list or group")

    @staticmethod
    def validate_use_one_itertools_function(playbook: Playbook):
        for profile in playbook.profiles:
            iter_funcs = [
                profile.password_generator.itertools_func.permutations,
                profile.password_generator.itertools_func.combinations,
                profile.password_generator.itertools_func.combinations_with_replacement,
                profile.password_generator.itertools_func.cartesian_product
            ]
            if not TruthyValue.only_one_is_truthy(*iter_funcs):
                raise MoreOrLessThanASingleOptionSelectedError(
                    "You selected zero or more than one option in a profile, where a single selected option was expected")

    @staticmethod
    def validate_password_source(playbook: Playbook):
        """ Validates that either output.generator or output.file is set, but not both """  # noqa
        for profile in playbook.profiles:
            password_sources = [
                profile.password_generator.password_source.generator,
                profile.password_generator.password_source.file,
            ]
            if not TruthyValue.only_one_is_truthy(*password_sources):
                raise MoreOrLessThanASingleOptionSelectedError(
                    "You selected zero or more than one option in a profile, where a single selected option was expected")


if __name__ == '__main__':
    PlaybookValidator.validate_profiles(PlaybookParser.create_playbook())
    PlaybookValidator.validate_use_groups_or_list(PlaybookParser.create_playbook())
    PlaybookValidator.validate_use_one_itertools_function(PlaybookParser.create_playbook())
    PlaybookValidator.validate_password_source(PlaybookParser.create_playbook())
