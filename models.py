from pydantic import BaseModel
from datetime import datetime


class ExternalToolTagAttributes(BaseModel):
    url: str
    new_tab: bool
    resource_link_id: str

class LockInfo(BaseModel):
    asset_string: str
    unlock_at: datetime|None
    lock_at: datetime|None
    context_module: dict|None
    manually_locked: bool

class RubricRating(BaseModel):
    points: int
    id: str
    description: str
    long_description: str

class RubricCriteria(BaseModel):
    points: int
    id: str
    learning_outcome_id: str|None
    vendor_guid: str|None
    description: str
    long_description: str
    criterion_use_range: bool
    rating: RubricRating|None
    ignore_for_scoring: bool

class AssignmentDate(BaseModel):
    id: int|None # No id if "base" is present
    base: bool
    title: str
    due_at: datetime
    unlock_at: datetime
    lock_at: datetime

class TurnitinSettings(BaseModel):
    originality_report_visibility: str
    s_paper_check: bool
    internet_check: bool
    journal_check: bool
    exclude_biblio: bool
    exclude_quoted: bool
    exclude_small_matches_type: str
    exclude_small_matches_value: int

class NeedsGradingCount(BaseModel):
    section_id: str
    needs_grading_count: int

class ScoreStatistic(BaseModel):
    min: int
    max: int
    mean: int
    upper_q: int
    median: int
    lower_q: int

class Assignment(BaseModel):
    id: int
    name: str
    description: str
    created_at: str
    updated_at: str
    due_at: datetime|None
    lock_at: datetime|None
    unlock_at: datetime|None
    has_overrides: bool
    all_dates: list[datetime]|None
    course_id: int
    html_url: str
    submissions_download_url: str
    assignment_group_id: int
    due_date_required: bool
    allowed_extensions: list[str]
    max_name_length: int
    turnitin_enabled: bool|None
    vericite_enabled: bool|None
    turnitin_settings: TurnitinSettings|None
    grade_group_students_individually: bool
    external_tool_tag_attributes: ExternalToolTagAttributes|None
    peer_reviews: bool
    automatic_peer_reviews: bool
    peer_review_count: int|None
    peer_reviews_assign_at: datetime|None

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
