import IST


def test_generate_random_array():
    """Simple test with valid imports."""
    arr = IST.generate_random_array(-2, 7, 20)
    assert len(arr) == 20 and min(arr) >= -2 and max(arr) <= 7

def test_get_key_from_array():
    """Test that key is in array."""
    arr = range(10)
    key = IST.get_key_from_array(arr)
    assert key in arr

