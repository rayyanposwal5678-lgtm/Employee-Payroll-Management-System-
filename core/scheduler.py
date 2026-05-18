"""
EPMS Background Scheduler
Uses APScheduler to run automated tasks while the Django server is active.

Jobs:
  1. Auto Attendance  - Runs daily at 8:00 AM on weekdays
  2. Auto Payroll     - Runs on the 1st of every month at 12:01 AM
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management import call_command

logger = logging.getLogger(__name__)

def run_auto_attendance():
    """Calls the auto_attendance management command."""
    logger.info("[Scheduler] Running automated daily attendance...")
    call_command('auto_attendance')

def run_auto_payroll():
    """Calls the auto_payroll management command."""
    logger.info("[Scheduler] Running automated monthly payroll generation...")
    call_command('auto_payroll')

def start():
    """Initializes and starts the background scheduler."""
    scheduler = BackgroundScheduler()

    # Job 1: Auto Attendance — Every weekday at 8:00 AM
    scheduler.add_job(
        run_auto_attendance,
        trigger=CronTrigger(day_of_week='mon-fri', hour=8, minute=0),
        id='auto_attendance_daily',
        name='Daily Auto Attendance (Mon-Fri 8:00 AM)',
        replace_existing=True,
    )

    # Job 2: Auto Payroll — 1st of every month at 12:01 AM
    scheduler.add_job(
        run_auto_payroll,
        trigger=CronTrigger(day=1, hour=0, minute=1),
        id='auto_payroll_monthly',
        name='Monthly Auto Payroll (1st at 00:01)',
        replace_existing=True,
    )

    scheduler.start()
    logger.info("[Scheduler] Background scheduler started successfully.")
    logger.info(f"[Scheduler] Registered jobs: {[job.name for job in scheduler.get_jobs()]}")
