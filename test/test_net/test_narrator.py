from src.net.terminal.narrator import Narrator


class TestNarrator:
    @classmethod
    def setup_class(cls) -> None:
        cls.narrator = Narrator()

    def test_message_content(self, capfd) -> None:
        def message_assertion(func, msg) -> None:
            func(msg)
            captured = capfd.readouterr()
            assert msg in captured.out

        message_assertion(self.narrator.debug, "Debugging message details")
        message_assertion(self.narrator.info, "Informational message")
        message_assertion(self.narrator.success, "Success message - something went right")
        message_assertion(self.narrator.warning, "Warning message - take notice of this")
        message_assertion(self.narrator.error, "Error message - watch out, something went wrong!")
        message_assertion(self.narrator.critical, "Critical message - this is critical")

    # TODO: Finish tests
    def test_logging_with_disabled_colors(self) -> None:
        pass

    def test_logging_with_enabled_colors(self) -> None:
        pass

    def test_log_level_filtering(self) -> None:
        pass

    def test_hostname_resolution(self) -> None:
        pass
