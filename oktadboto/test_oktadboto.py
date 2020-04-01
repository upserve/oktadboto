import unittest
from unittest.mock import patch, Mock
from datetime import timedelta, datetime
from boto3 import Session

from oktadboto import oktad_command, get_oktad_credentials, oktadboto_session

ENV_STR = (
    "VIRTUALENVWRAPPER_WORKON_CD=1\n"
    "LC_TERMINAL=iTerm2\n"
    "DISPLAY=/private/tmp/com.apple.launchd.HslUCXNu9T/org.macosforge.xquartz:0\n"
    "SECURITYSESSIONID=186a6\n"
    "COLORTERM=truecolor\n"
    "_=/usr/local/bin/oktad\n"
    "AWS_SESSION_TOKEN=FwoGZXIvYX__TOKEN__SKLknw==\n"
    "AWS_ACCESS_KEY_ID=ASIA__ACCESSS_KEY__GJON5\n"
    "AWS_SECRET_ACCESS_KEY=UDm6R__SECRET_KEY__7YsZ2mC/v\n"
)
METADATA = {
    "access_key": "ASIA__ACCESSS_KEY__GJON5",
    "expiry_time": "2020-01-01T00:30:00",
    "secret_key": "UDm6R__SECRET_KEY__7YsZ2mC/v",
    "token": "FwoGZXIvYX__TOKEN__SKLknw==",
}


class OktadBoto(unittest.TestCase):
    def test_oktad_command(self):
        self.assertEqual(
            oktad_command("foo_profile"), ["oktad", "foo_profile", "--", "env"]
        )

    @patch("oktadboto.subprocess.run")
    @patch("oktadboto.datetime")
    def test_get_oktad_credentials(self, mock_datetime, mock_subprocess_run):
        mock_subprocess_run.return_value = Mock(returncode=0, stdout=ENV_STR)
        mock_datetime.now.return_value = datetime(2020, 1, 1)
        self.assertDictEqual(
            METADATA, get_oktad_credentials("bar_profile", timedelta(minutes=30))
        )

    @patch("oktadboto.subprocess.run")
    def test_get_oktad_credentials_error(self, mock_subprocess_run):
        mock_subprocess_run.return_value = Mock(returncode=1)
        with self.assertRaises(RuntimeError):
            get_oktad_credentials("bar_profile", timedelta(minutes=30))

    @patch("oktadboto.get_oktad_credentials", return_value=METADATA)
    def test_oktadboto_session(self, mock_get_credentials):
        self.assertIsInstance(oktadboto_session("foo_bar_session"), Session)
