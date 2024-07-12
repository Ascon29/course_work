import os

ROOT_DIR = os.path.dirname(__file__)

LOGS_DIR = os.path.join(ROOT_DIR, "logs")
DATA_DIR = os.path.join(ROOT_DIR, "data")

LOGS_UTILS_DIR = os.path.join(LOGS_DIR, "utils.log")
LOGS_VIEWS_DIR = os.path.join(LOGS_DIR, "views.log")
LOGS_SERVICES_DIR = os.path.join(LOGS_DIR, "services.log")
LOGS_REPORTS_DIR = os.path.join(LOGS_DIR, "reports.log")
