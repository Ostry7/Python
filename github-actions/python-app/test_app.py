from utils import get_status_code
from unittest.mock import patch

def test_status_code():
    with patch("utils.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        assert get_status_code("https://example.com") == 200
