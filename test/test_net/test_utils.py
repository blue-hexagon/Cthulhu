from src.net.util import Utils


class TestUtils:

    def test_get_ms_delay(self) -> None:
        utils = Utils()
        # @formatter:off
        assert int(utils.get_ms_delay("1s")) == 1 * utils.ms_to_sec
        assert int(utils.get_ms_delay("1m")) == 1 * utils.sec_to_min * utils.ms_to_sec
        assert int(utils.get_ms_delay("1h")) == 1 * utils.min_to_hour * utils.sec_to_min * utils.ms_to_sec
        assert int(utils.get_ms_delay("1d")) == 1 * utils.hour_to_day * utils.min_to_hour * utils.sec_to_min * utils.ms_to_sec
        assert (
            int(utils.get_ms_delay("1w"))
            == 1 * utils.day_to_week * utils.hour_to_day * utils.min_to_hour * utils.sec_to_min * utils.ms_to_sec
        )
        # @formatter:on
