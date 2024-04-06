from src.passgen.distributor.payload_distributor import Client


def test_client():
    client_a = Client("127.0.0.1", 8001)
    assert client_a.sliding_window_multiplier == 1
    client_a.decrement_sliding_window()
    assert client_a.sliding_window_multiplier == 1
    client_a.decrement_sliding_window()
    client_a.decrement_sliding_window()
    client_a.decrement_sliding_window()
    client_a.decrement_sliding_window()
    assert client_a.sliding_window_multiplier == 1
    client_a.increment_sliding_window()
    assert client_a.sliding_window_multiplier == 2
    client_a.increment_sliding_window()
    assert client_a.sliding_window_multiplier == 4
    client_a.increment_sliding_window()
    assert client_a.sliding_window_multiplier == 8
    client_a.decrement_sliding_window()
    assert client_a.sliding_window_multiplier == 4
    client_a.decrement_sliding_window()
    assert client_a.sliding_window_multiplier == 2
    client_a.decrement_sliding_window()
    assert client_a.sliding_window_multiplier == 1
    client_a.decrement_sliding_window()
    assert client_a.sliding_window_multiplier == 1
    client_a.decrement_sliding_window()
    client_a.decrement_sliding_window()
    client_a.decrement_sliding_window()
    client_a.decrement_sliding_window()
    assert client_a.sliding_window_multiplier == 1
