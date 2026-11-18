
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import (
    AcademicClass,
    Subject,
    ClassAccess,
    Topic,
    StudyNote,
    Exam,
    Question,
    MCQOption,
    AnswerKey,
    GeneratedPaper,
    ExamResult,
)

from .forms import ClassAccessForm


# ==================================================
# 1. ACADEMIC CLASS
# ==================================================

@admin.register(AcademicClass)
class AcademicClassAdmin(admin.ModelAdmin):

    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)


# ==================================================
# 2. SUBJECT
# ==================================================

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "academic_class",
        "subject_code",
        "is_active",
    )

    list_filter = ("academic_class", "is_active")
    search_fields = ("name", "subject_code")


# ==================================================
# 3. STUDENT CLASS ACCESS
# ==================================================

@admin.register(ClassAccess)
class ClassAccessAdmin(admin.ModelAdmin):

    form = ClassAccessForm

    list_display = (
        "get_student_name",
        "academic_class",
        "assigned_at",
    )
    
    @admin.display(description="Student Name")
    def get_student_name(self, obj):
        return obj.student.name

    list_filter = ("academic_class",)

    search_fields = (
        "student__name",
        "student__mobile_number",
    )


# ==================================================
# 4. TOPIC
# ==================================================

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "subject",
        "order",
        "is_active",
    )

    list_filter = (
        "subject__academic_class",
        "subject",
        "is_active",
    )

    search_fields = ("name",)


# ==================================================
# 5. STUDY NOTES
# ==================================================

@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "topic",
        "is_published",
        "created_at",
    )

    list_filter = (
        "is_published",
        "topic__subject",
    )

    search_fields = (
        "title",
        "content",
    )


# ==================================================
# 6. MCQ OPTIONS VALIDATION
# ==================================================

class MCQOptionInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()

        if any(self.errors):
            return

        question_type = self.instance.question_type

        active_options = [
            form.cleaned_data
            for form in self.forms
            if form.cleaned_data
            and not form.cleaned_data.get("DELETE", False)
            and form.cleaned_data.get("option_text")
        ]

        if question_type == "mcq":

            if len(active_options) != 4:
                raise ValidationError(
                    "MCQ question must have exactly 4 options."
                )

            correct_options = [
                option
                for option in active_options
                if option.get("is_correct")
            ]

            if len(correct_options) != 1:
                raise ValidationError(
                    "MCQ must have exactly 1 correct answer."
                )

        else:

            if active_options:
                raise ValidationError(
                    "Only MCQ questions can have options."
                )


# ==================================================
# 7. MCQ OPTIONS INLINE
# ==================================================

class MCQOptionInline(admin.TabularInline):

    model = MCQOption
    formset = MCQOptionInlineFormSet
    extra = 4
    min_num = 4
    max_num = 4


# ==================================================
# 8. ANSWER KEY INLINE
# ==================================================

class AnswerKeyInline(admin.StackedInline):

    model = AnswerKey
    extra = 0
    max_num = 1


# ==================================================
# 9. QUESTION BANK
# ==================================================

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "question_text",
        "subject",
        "topic",
        "question_type",
        "marks",
        "is_active",
    )

    list_filter = (
        "subject__academic_class",
        "subject",
        "question_type",
        "is_active",
    )

    search_fields = ("question_text",)

    inlines = [
        MCQOptionInline,
        AnswerKeyInline,
    ]


# ==================================================
# 10. MCQ OPTIONS
# ==================================================

@admin.register(MCQOption)
class MCQOptionAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "option_text",
        "is_correct",
    )

    list_filter = ("is_correct",)

    search_fields = (
        "option_text",
        "question__question_text",
    )


# ==================================================
# 11. ANSWER KEY
# ==================================================

@admin.register(AnswerKey)
class AnswerKeyAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "created_at",
    )

    search_fields = (
        "question__question_text",
    )


# ==================================================
# 12. EXAM CONFIGURATION
# ==================================================

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "subject",
        "total_marks",
        "duration_minutes",
        "is_published",
    )

    list_filter = (
        "subject__academic_class",
        "subject",
        "total_marks",
        "is_published",
    )

    search_fields = ("title",)


# ==================================================
# 13. GENERATED PAPERS
# ==================================================

@admin.register(GeneratedPaper)
class GeneratedPaperAdmin(admin.ModelAdmin):

    list_display = (
        "get_student_name",
        "exam",
        "started_at",
        "expires_at",
        "status",
    )

    @admin.display(description="Student Name")
    def get_student_name(self, obj):
        return obj.student.name

    list_filter = (
        "status",
        "exam",
    )

    search_fields = (
        "student__name",
        "student__mobile_number",
        "exam__title",
    )

    readonly_fields = (
        "selected_question_ids",
        "started_at",
        "submitted_at",
    )


# ==================================================
# 14. EXAM RESULTS
# ==================================================

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):

    list_display = (
        "get_student",
        "get_exam",
        "marks_obtained",
        "status",
        "submitted_at",
        "approved_at",
    )

    list_filter = ("status",)

    search_fields = (
        "generated_paper__student__name",
        "generated_paper__student__mobile_number",
        "generated_paper__exam__title",
    )

    readonly_fields = (
        "submitted_at",
        "approved_at",
    )

    @admin.display(description="Student Name")
    def get_student(self, obj):
        return obj.generated_paper.student.name

    @admin.display(description="Exam")
    def get_exam(self, obj):
        return obj.generated_paper.exam


from .models import DuelRoom


@admin.register(DuelRoom)
class DuelRoomAdmin(admin.ModelAdmin):
    list_display = ("code", "subject", "host", "guest", "status", "host_score", "guest_score", "created_at")
    list_filter = ("status", "subject__academic_class", "subject")
    search_fields = ("code", "host__name", "guest__name")
    readonly_fields = ("code", "question_ids", "created_at")
    actions = ["delete_selected_rooms"]

    @admin.action(description="Select केलेले duel rooms delete करा")
    def delete_selected_rooms(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} room(s) delete झाले.")