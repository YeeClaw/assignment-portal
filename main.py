from datetime import UTC, datetime, time, timezone, tzinfo
import requests
import logging
import argparse
import urmom

from constants import TOKEN, BASE_URL
from typing import TYPE_CHECKING
from utils import Course
if TYPE_CHECKING:
    from argparse import Namespace

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()


def main(args: 'Namespace'):
    from utils import validate_environment
    validate_environment()

    test_api_access()
    get_current_courses()


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


def get_current_courses() -> dict:
    """
    Collect all active courses for the token owner.
    :return: A dictionary of courses in accordance to Canvas schema
    """
    endpoint = f"{BASE_URL}/v1/courses"
    params = {"enrollement_state": "active", "include[]": "term"}
    headers = {"Authorization": f"Bearer {TOKEN}"}

    response = requests.get(endpoint, params=params, headers=headers)
    logger.debug(response.json())

    if response.status_code != 200:
        raise RuntimeError(
            "Ran into an error when collecting active courses! "
            f"Responded with status: {response.status_code}"
        )
    
    all_courses = [Course.model_validate(item) for item in response.json()]
    current_courses: list[Course] = []
    for course in all_courses:
        if not course.term.start_at or not course.term.end_at:
            continue
        # Convert terms to datetimes
        term_start = convert_to_utc_datetime(course.term.start_at)
        logger.debug(f"Term start (UTC): {term_start}")
        term_end = convert_to_utc_datetime(course.term.end_at)
        logger.debug(f"Term end (UTC): {term_end}")

        # Get current UTC time
        utc_now = datetime.now(timezone.utc)
        logger.debug(f"Now (UTC): {utc_now}")

        if term_start <= utc_now <= term_end:
            current_courses.append(course)

    logger.info("Collected active courses!")
    return response.json()


def convert_to_utc_datetime(string_date: str) -> datetime:
    basic_datetime = datetime.strptime(string_date, "%Y-%m-%dT%H:%M:%SZ")
    datetime_with_tz = basic_datetime.replace(tzinfo=timezone.utc)

    return datetime_with_tz


def set_log_level(log_level: str) -> None:
    """
    Set the log level of the script.
    """
    log_level = log_level.upper()

    match log_level:
        case "DEBUG":
            logger.setLevel(logging.DEBUG)
        case "INFO":
            logger.setLevel(logging.INFO)
        case "WARNING":
            logger.setLevel(logging.WARNING)
        case "ERROR":
            logger.setLevel(logging.ERROR)
        case _:
            logger.setLevel(logging.INFO)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A simple Canvas to Anytype integration"
    )
    parser.add_argument('-l', '--log-level', type=str, default='INFO',
                        help='Options include: DEBUG, INFO, WARNING, ERROR')
    args = parser.parse_args()

    set_log_level(args.log_level)

    main(args)
