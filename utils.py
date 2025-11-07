import logging
import requests

from pydantic import BaseModel
from datetime import datetime, timezone
from constants import BASE_URL, TOKEN

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


class Term(BaseModel):
    id: int
    name: str
    start_at: str|None
    end_at: str|None
    workflow_state: str
    grading_period_group_id: str|None
    created_at: str


class Enrollments(BaseModel):
    type: str
    role: str
    role_id: int
    user_id: int
    enrollment_state: str
    limit_privileges_to_course_section: bool


class Calendar(BaseModel):
    ics: str


class Course(BaseModel):
    id: int
    name: str
    course_code: str
    account_id: int
    created_at: str
    start_at: str|None
    default_view: str
    enrollment_term_id: int
    is_public: bool
    grading_standard_id: int|None
    root_account_id: int
    uuid: str
    license: str
    grade_passback_settings: str|None = None
    end_at: str|None
    public_syllabus: bool
    public_syllabus_to_auth: bool
    storage_quota_mb: int
    is_public_to_auth_users: bool
    homeroom_course: bool
    course_color: str|None
    friendly_name: str|None
    term: Term
    apply_assignment_group_weights: bool
    locale: str|None = None
    calendar: Calendar
    time_zone: str
    blueprint: bool
    template: bool
    enrollments: list[Enrollments]
    hide_final_grades: bool
    workflow_state: str
    course_format: str = ""
    restrict_enrollments_to_course_dates: bool
