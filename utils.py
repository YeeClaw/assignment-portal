from pydantic import BaseModel


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


class Term(BaseModel):
    id: int
    name: str
    start_at: str
    end_at: str
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
    start_at: str
    default_view: str
    enrollment_term_id: int
    is_public: bool
    grading_standard_id: int
    root_account_id: int
    uuid: str
    license: str
    grade_passback_settings: str|None = None
    end_at: str
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
    course_format: str
    restrict_enrollments_to_course_dates: bool
