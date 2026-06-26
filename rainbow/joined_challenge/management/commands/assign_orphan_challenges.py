from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from joined_challenge.models import JoinedChallenge


class Command(BaseCommand):
    help = (
        "Assign a user (looked up by email) to every joined challenge that "
        "currently has no user associated with it."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "email",
            help="Email of the user to assign to the orphan challenges.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only show how many challenges would be updated, without saving.",
        )

    def handle(self, *args, **options):
        email = options["email"]
        dry_run = options["dry_run"]

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CommandError(f"No user found with email '{email}'.")

        orphans = JoinedChallenge.objects.filter(user__isnull=True)
        count = orphans.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("No challenges without a user found."))
            return

        if dry_run:
            self.stdout.write(
                f"[dry-run] Would assign {count} challenge(s) to {user.email}."
            )
            return

        updated = orphans.update(user=user)
        self.stdout.write(
            self.style.SUCCESS(f"Assigned {updated} challenge(s) to {user.email}.")
        )
