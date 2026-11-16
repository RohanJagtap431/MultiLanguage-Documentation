
import json

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db import transaction

from examination.models import (
    Subject,
    Topic,
    Question,
    MCQOption,
    AnswerKey,
)


class Command(BaseCommand):
    help = "Import questions from a JSON file"

    def handle(self, *args, **options):

        file_path = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "c_programming_short_questions_30.json"
        )


#c_programming_questions.json
#c_programming_long_questions_20.json
#c_programming_short_questions_30.json


        if not file_path.exists():
            raise CommandError(
                f"JSON file not found: {file_path}"
            )

        try:
            with open(file_path, "r", encoding="utf-8-sig") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise CommandError(f"Invalid JSON: {error}")

        subject_name = data.get("subject")

        if not subject_name:
            raise CommandError("Subject name is missing.")

        try:
            subject = Subject.objects.get(name=subject_name)
        except Subject.DoesNotExist:
            raise CommandError(
                f"Subject not found: {subject_name}"
            )

        imported = 0
        skipped = 0

        try:
            with transaction.atomic():

                for item in data.get("questions", []):

                    topic_name = item.get("topic")

                    if not topic_name:
                        raise CommandError(
                            "A question is missing its topic."
                        )

                    topic, _ = Topic.objects.get_or_create(
                        subject=subject,
                        name=topic_name,
                        defaults={
                            "description": topic_name,
                            "is_active": True,
                        },
                    )

                    question_text = item.get("question_text")

                    if not question_text:
                        raise CommandError(
                            "Question text is missing."
                        )

                    if Question.objects.filter(
                        subject=subject,
                        question_text=question_text,
                    ).exists():
                        skipped += 1
                        continue

                    question = Question(
                        subject=subject,
                        topic=topic,
                        question_text=question_text,
                        question_type=item["question_type"],
                        marks=item["marks"],
                        is_active=True,
                    )

                    question.full_clean()
                    question.save()

                    if question.question_type == "mcq":

                        options_list = item.get("options", [])

                        if len(options_list) != 4:
                            raise CommandError(
                                f"MCQ must have exactly 4 options: "
                                f"{question_text}"
                            )

                        correct_count = sum(
                            1 for option in options_list
                            if option.get("is_correct")
                        )

                        if correct_count != 1:
                            raise CommandError(
                                f"MCQ must have exactly 1 correct option: "
                                f"{question_text}"
                            )

                        for option in options_list:
                            MCQOption.objects.create(
                                question=question,
                                option_text=option["option_text"],
                                is_correct=option["is_correct"],
                            )

                    answer_key = item.get("answer_key", {})

                    AnswerKey.objects.create(
                        question=question,
                        model_answer=answer_key.get(
                            "model_answer", ""
                        ),
                        marking_rubric=answer_key.get(
                            "marking_rubric", ""
                        ),
                        important_keywords=answer_key.get(
                            "important_keywords", ""
                        ),
                    )

                    imported += 1

        except (ValidationError, KeyError, TypeError) as error:
            raise CommandError(f"Import failed: {error}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed! Added: {imported}, "
                f"Skipped duplicates: {skipped}"
            )
        )
