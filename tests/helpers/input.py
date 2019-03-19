import io

from pytest_mock import MockFixture


def set_stdin_value(mocker: MockFixture, value: str):
    input_mock = io.StringIO(value)
    input_mock.name = "mocked_stdin"
    mocker.patch("sys.stdin", input_mock)
