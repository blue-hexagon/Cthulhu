from src.net.banner import Banner


class TestCliBanner:

    def test_banner_prints(self, capsys) -> None:
        Banner()  # prints the banner
        captured = capsys.readouterr()
        print(captured.out)
        print(captured.err)
        assert "█" in captured.out, "Banner did not print correctly."
