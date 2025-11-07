import requests
import logging

from constants import BASE_URL, TOKEN
from utils import Course, convert_to_utc_datetime
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def get_current_courses() -> list[Course]:
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
    logger.debug(f"Response: {[course.model_dump_json() for course in current_courses]}")
    return current_courses
