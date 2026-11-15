
import json

from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from bug_hunter.models import Question


class Command(BaseCommand):
    help = "Import Code Detective questions from JSON"

    def handle(self, *args, **options):

        file_path = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "questions.json"
        )

        if not file_path.exists():
            raise CommandError(
                f"Question file not found: {file_path}"
            )

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                questions = json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            raise CommandError(f"Cannot read question file: {error}")

        if not isinstance(questions, list):
            raise CommandError("JSON must contain a list of questions.")

        created_count = 0
        updated_count = 0

        required_fields = {
            "language",
            "difficulty",
            "title",
            "question_text",
            "buggy_code",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_option",
            "explanation",
        }

        with transaction.atomic():

            for index, item in enumerate(questions, start=1):

                if not isinstance(item, dict):
                    raise CommandError(
                        f"Question {index} must be an object."
                    )

                missing = required_fields - item.keys()

                if missing:
                    raise CommandError(
                        f"Question {index} missing fields: "
                        f"{', '.join(sorted(missing))}"
                    )

                language = item["language"]
                difficulty = item["difficulty"]
                correct_option = item["correct_option"]

                if language not in dict(Question.LANGUAGE_CHOICES):
                    raise CommandError(
                        f"Question {index}: Invalid language."
                    )

                if difficulty not in dict(Question.DIFFICULTY_CHOICES):
                    raise CommandError(
                        f"Question {index}: Invalid difficulty."
                    )

                if correct_option not in dict(Question.OPTION_CHOICES):
                    raise CommandError(
                        f"Question {index}: Invalid correct option."
                    )

                defaults = {
                    key: item[key]
                    for key in required_fields
                    if key not in {"language", "difficulty", "title"}
                }

                defaults.update({
                    "points": item.get("points", 10),
                    "is_published": item.get("is_published", True),
                })

                question, created = Question.objects.update_or_create(
                    language=language,
                    difficulty=difficulty,
                    title=item["title"],
                    defaults=defaults,
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete! Created: {created_count}, "
                f"Updated: {updated_count}, Total: {len(questions)}"
            )
        )
