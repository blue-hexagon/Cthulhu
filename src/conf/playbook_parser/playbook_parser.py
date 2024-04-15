from src.conf.path_manager import PathManager
from src.conf.playbook_parser.playbook_objects import Frame, Scheduler, Playbook, Profile, Hosts, PasswordGenerator, \
    ItertoolsFunc, Distributor, PasswordSource
from src.net.protocol.ops import OperationProxyFactory

import yaml


class PlaybookParser:

    @staticmethod
    def _parse_yaml_file_to_dataclasses(file_path):
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
            return yaml_data

    @staticmethod
    def create_playbook(yaml_filepath=PathManager().payload_profiles):
        yaml_data = PlaybookParser._parse_yaml_file_to_dataclasses(yaml_filepath)
        profiles = [PlaybookParser._create_profile(profile_data) for profile_data in yaml_data['payload_profiles']]
        return Playbook(profiles=profiles)

    @staticmethod
    def _create_profile(profile_data):
        profile_id = profile_data['profile']['profile_id']
        hosts = PlaybookParser._create_hosts(profile_data['profile']['hosts'])
        password_generator = PlaybookParser._create_password_generator(profile_data['profile']['password_generator'])
        distributor = PlaybookParser._create_distributor(profile_data['profile']['distributor'])
        frame_sequence = [PlaybookParser._create_frame(frame) for frame in profile_data['profile']['FrameSequence']]

        return Profile(profile_id=profile_id,
                       hosts=hosts,
                       password_generator=password_generator,
                       distributor=distributor,
                       FrameSequence=frame_sequence)

    @staticmethod
    def _create_hosts(hosts_data):
        return Hosts(use_group=hosts_data['use_group'],
                     groupnames=hosts_data['groupnames'],
                     use_list=hosts_data['use_list'],
                     clientlist=hosts_data['clientlist'])

    @staticmethod
    def _create_password_generator(password_data):
        # @formatter:off
        itertools_func = ItertoolsFunc(cartesian_product=password_data['itertools_func']['cartesian_product'],
                                       permutations=password_data['itertools_func']['permutations'],
                                       combinations=password_data['itertools_func']['combinations'],
                                       combinations_with_replacement=password_data['itertools_func']['combinations_with_replacement'])
        # @formatter:on
        password_source = PasswordSource(
            generator=password_data['password_source']['generator'],
            file=password_data['password_source']['file'],
            path=password_data['password_source']['path'],
        )
        return PasswordGenerator(itertools_func=itertools_func,
                                 password_source=password_source,
                                 wordlist_matrix=password_data['wordlist_matrix'],
                                 bruteforce_table=password_data['bruteforce_table'])

    @staticmethod
    def _create_distributor(distributor_data):
        scheduler = Scheduler(first_in_first_out=distributor_data['scheduler']['first_in_first_out'],
                              round_robin=distributor_data['scheduler']['round_robin'],
                              weighted_round_robin=distributor_data['scheduler']['weighted_round_robin'])

        return Distributor(sliding_window=distributor_data['sliding_window'],
                           sw_size_initial_bits=distributor_data['sw_size_initial_bits'],
                           sw_size_min_bit=distributor_data['sw_size_min_bit'],
                           sw_size_max_bits=distributor_data['sw_size_max_bits'],
                           scheduler=scheduler)

    @staticmethod
    def _create_frame(frame_data):
        operations = [PlaybookParser._create_operation(op) for op in frame_data['Frame']]
        return Frame(operations=operations)

    @staticmethod
    def _create_operation(operation_data):
        args = operation_data.get('args', [])
        return OperationProxyFactory(subclass_name=operation_data['ProtocolOperation'], args=args)




if __name__ == '__main__':
    playbook = PlaybookParser.create_playbook()
    print(playbook)
    # PlaybookValidator.validate_playbook()
