from django.core.management.base import BaseCommand
import coverage

class Command(BaseCommand):
    help = 'Run tests with coverage'

    def handle(self, *args, **kwargs):
        cov = coverage.Coverage(source=['.'])
        cov.erase()
        cov.start()

        from django.test.utils import get_runner
        from django.conf import settings

        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        failures = test_runner.run_tests(['apps/users/tests', 'apps/reservations/tests', 'apps/ticketing/tests'])
        
        cov.stop()
        cov.save()
        
        self.stdout.write(self.style.SUCCESS('Generating coverage report'))
        cov.report()
        cov.html_report(directory='htmlcov')

        if failures:
            self.stdout.write(self.style.ERROR('Tests failed'))
            exit(1)
        else:
            self.stdout.write(self.style.SUCCESS('Tests passed'))
