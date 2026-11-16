
def examination_context(request):

    assigned_classes = []

    if request.user.is_authenticated and not request.user.is_superuser:
        from .models import ClassAccess

        accesses = (
            ClassAccess.objects
            .select_related("academic_class")
            .filter(
                student=request.user,
                academic_class__is_active=True
            )
            .order_by("academic_class__name")
        )

        assigned_classes = [
            access.academic_class
            for access in accesses
        ]

    return {
        "examination_classes": assigned_classes
    }
