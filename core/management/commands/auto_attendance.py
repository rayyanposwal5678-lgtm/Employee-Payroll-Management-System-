import datetime
from django.core.management.base import BaseCommand
from core.models import Employee, Attendance

class Command(BaseCommand):
    help = 'Automatically marks all active employees as Present for the current day.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting daily automated attendance...")
        
        active_employees = Employee.objects.filter(status='Active')
        today = datetime.date.today()
        
        # Don't mark attendance automatically on weekends (Saturday/Sunday)
        if today.weekday() in [5, 6]:
            self.stdout.write(self.style.WARNING("Today is a weekend. Automated attendance skipped."))
            return
            
        count = 0
        skipped_count = 0
        
        for emp in active_employees:
            # Check if attendance already logged (perhaps user did it manually)
            attendance, created = Attendance.objects.get_or_create(
                employee=emp,
                date=today,
                defaults={'status': 'Present'}
            )
            
            if created:
                count += 1
            else:
                skipped_count += 1
                
        self.stdout.write(self.style.SUCCESS(f'Automated Attendance Complete: Marked {count} present. Skipped {skipped_count} (already recorded).'))
