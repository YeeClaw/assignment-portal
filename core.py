import requests
import logging
import utils

from constants import BASE_URL, TOKEN
from models import Course, Assignment

logger = logging.getLogger(__name__)


def get_current_courses() -> list[Course]:
    """
    Collect all active courses for the token owner.
    :return: A dictionary of courses in accordance to Canvas schema
    """
    endpoint = f"{BASE_URL}/v1/users/self/courses"
    params = {"include[]": "term"}
    params['enrollement_state'] = "active"
    params['per_page'] = "100"
    headers = {"Authorization": f"Bearer {TOKEN}"}

    response = requests.get(endpoint, params=params, headers=headers)
    logger.debug(response.json())
    logger.debug(response.headers)

    if response.status_code != 200:
        raise RuntimeError(
            "Ran into an error when collecting active courses! "
            f"Responded with status: {response.status_code}"
        )
    
    all_courses = [Course.model_validate(item) for item in response.json()]
    if logger.getEffectiveLevel() == logging.DEBUG:
        for course in all_courses:
            logger.debug(f"Picked up course: {course.name}")

    current_courses = list(filter(utils.current_course_filter, all_courses))

    logger.info("Collected active courses!")
    logger.debug(f"Response: {[course.model_dump_json() for course in current_courses]}")
    return current_courses


def get_course_weekly_assignments(course_id: str) -> list[Assignment]:
    """
    Will return all assignments due in a 7 day timeframe.
    :param course_id: String representing the course ID to get
    assignments for.
    :return: A list of Pydantic Assignment models.
    """
    endpoint = f"{BASE_URL}/v1/courses/{course_id}/assignments"
    return []
