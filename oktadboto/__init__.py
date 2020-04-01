import subprocess
import logging

from boto3 import Session
from botocore.session import get_session
from datetime import timedelta, datetime, timezone
from botocore.credentials import RefreshableCredentials
from functools import wraps

logger = logging.getLogger(__name__)

AWS_SESSION_TOKEN = "AWS_SESSION_TOKEN"
AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"


def oktad_command(profile):
    return ["oktad", profile, "--", "env"]


def get_oktad_credentials(profile, expiration):
    # execute shell command and capture output
    logger.warning(
        "Getting fresh AWS credentials from Oktad for profile {}!".format(profile)
    )
    completed_process = subprocess.run(
        oktad_command(profile), check=True, capture_output=True, encoding="utf-8"
    )

    if completed_process.returncode != 0:
        raise RuntimeError("Oktad Process failed: {}".format(completed_process))

    aws_vars = {}
    for line in completed_process.stdout.splitlines():
        vals = line.split("=", maxsplit=1)
        if len(vals) == 2 and vals[0] in [
            AWS_SESSION_TOKEN,
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY,
        ]:
            aws_vars[vals[0]] = vals[1]

    if len(aws_vars) != 3:
        raise RuntimeError(
            "Failed to capture the AWS tokens from Oktad: {}".format(completed_process)
        )

    return {
        "access_key": aws_vars[AWS_ACCESS_KEY_ID],
        "secret_key": aws_vars[AWS_SECRET_ACCESS_KEY],
        "token": aws_vars[AWS_SESSION_TOKEN],
        "expiry_time": (datetime.now(timezone.utc) + expiration).isoformat(),
    }


def oktadboto_session(profile, expiration=timedelta(minutes=50), region="us-east-1"):
    @wraps(get_oktad_credentials)
    def wrap_refresh():
        return get_oktad_credentials(profile, expiration)

    session_credentials = RefreshableCredentials.create_from_metadata(
        metadata=wrap_refresh(), refresh_using=wrap_refresh, method="sts-assume-role",
    )

    session = get_session()
    session._credentials = session_credentials
    session.set_config_variable("region", region)
    return Session(botocore_session=session)
