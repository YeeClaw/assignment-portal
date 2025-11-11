from typing import Literal
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
    all_dates: list[datetime]|None # This is my best guess
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
    intra_group_peer_reviews: bool
    group_category_id: int
    needs_grading_count: int
    needs_grading_count_by_section: list[dict]|None
    position: int
    post_to_sis: bool|None
    integration_id: str|None
    integration_data: dict|None
    points_possible: float
    submission_types: list[str]
    has_submitted_submission: bool
    grading_type: Literal[
        "pass_fail", 
        "percent", 
        "letter_grade", 
        "gpa_scale", 
        "points"
    ]
    grading_standard_id: int
    published: bool
    unpublished: bool
    only_visible_to_overrides: bool
    locked_for_user: bool
    lock_info: LockInfo|None
    lock_explanation: str
    quiz_id: int|None
    anonymous_submissions: bool|None
    discussion_topic: dict|None # If needed, make DiscussionTopic model
    freeze_on_copy: bool|None
    frozen: bool|None
    # Can only be string literals. Specify if needed
    frozen_attributes: list[str]
    submission: dict|None # Submission object. Make as needed
    use_rubric_for_grading: bool|None
    rubric_settings: dict|None
    rubric: list[RubricCriteria|RubricRating]|None
    assignment_visibility: list[int]|None
    overrides: dict|None
    omit_from_final_grade: bool|None
    hide_in_gradebook: bool|None
    moderated_grading: bool
    grader_count: int
    final_grader_id: int|None
    grader_comments_visible_to_graders: bool
    graders_anonymous_to_graders: bool
    grader_names_visible_to_final_grade: bool
    anonymous_grading: bool
    allowed_attempts: int
    post_manually: bool
    score_statistics: ScoreStatistic|None
    can_submit: bool|None
    ab_guid: list[str]
    annotatable_attachment_id: int|None
    anonymize_students: bool|None
    require_lockdown_browser: bool|None
    important_dates: bool|None
    muted: bool|None
    anonymous_peer_reviews: bool
    anonymous_instructor_annotations: bool

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
