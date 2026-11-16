
def examination_context(request):
    assigned_class = None

    if request.user.is_authenticated and not request.user.is_superuser:
        from .models import ClassAccess

        access = (
            ClassAccess.objects
            .select_related("academic_class")
            .filter(student=request.user)
            .first()
        )

        if access and access.academic_class.is_active:
            assigned_class = access.academic_class

    return {
        "examination_class": assigned_class
    }
