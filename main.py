import argparse
import core
import utils
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from argparse import Namespace

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def main(args: 'Namespace'):
    utils.set_log_level(args.log_level)
    utils.validate_environment()

    utils.test_api_access()
    courses = core.get_current_courses()
    weekly_tasks = core.get_weekly_tasks()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A simple Canvas to Anytype integration"
    )
    parser.add_argument('-l', '--log-level', type=str, default='INFO',
                        help='Options include: DEBUG, INFO, WARNING, ERROR')

    main(parser.parse_args())
