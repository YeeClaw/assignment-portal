import logging
import requests

from datetime import datetime, timezone
from constants import BASE_URL, TOKEN
from models import Course

logger = logging.getLogger(__name__)


def validate_environment() -> None:
    """
    Will raise runtime errors if any required environment variables are found
    to be missing, falsy, or generally invalid.
    """
    from constants import TOKEN, DOMAIN
    if not TOKEN:
        raise RuntimeError("No Canvas token found in environment!")
    if not DOMAIN:
        raise RuntimeError("No Canvas domain found in environment!")    


def convert_to_utc_datetime(string_date: str) -> datetime:
    basic_datetime = datetime.strptime(string_date, "%Y-%m-%dT%H:%M:%SZ")
    datetime_with_tz = basic_datetime.replace(tzinfo=timezone.utc)

    return datetime_with_tz


def test_api_access() -> None:
    """
    Will hit the user generated tokens Canvas endpoint to ensure that there 
    is authorized access.
    """
    endpoint = f"{BASE_URL}/v1/users/self/user_generated_tokens"
    logger.debug(f"Qualified endpoint: {endpoint}")

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    logger.debug(f"Headers: {headers}")

    response = requests.get(endpoint, headers=headers)
    logger.debug(response.json())

    if response.status_code != 200:
        raise RuntimeError(
            "Unable to authenticate with Canvas. "
            f"Status: {response.status_code}"
        )
    else:
        logger.info("Authenticated with Canvas API!")


def set_log_level(log_level: str) -> None:
    """
    Set the log level of the script.
    """
    log_level = log_level.upper()
    root_logger = logging.getLogger()

    match log_level:
        case "DEBUG":
            root_logger.setLevel(logging.DEBUG)
        case "INFO":
            logger.setLevel(logging.INFO)
        case "WARNING":
            root_logger.setLevel(logging.WARNING)
        case "ERROR":
            root_logger.setLevel(logging.ERROR)
        case _:
            root_logger.setLevel(logging.INFO)


def current_course_filter(course: Course) -> bool:
    if not course.term.start_at or not course.term.end_at:
        return False

    term_start = convert_to_utc_datetime(course.term.start_at)
    logger.debug(f"Term start (UTC): {term_start}")
    term_end = convert_to_utc_datetime(course.term.end_at)
    logger.debug(f"Term end (UTC): {term_end}")

    # Get current UTC time
    utc_now = datetime.now(timezone.utc)
    logger.debug(f"Now (UTC): {utc_now}")

    if term_start <= utc_now <= term_end:
        return True
    return False
