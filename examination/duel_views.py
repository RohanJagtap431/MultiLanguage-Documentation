import random
import secrets

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Q
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import ClassAccess, Subject, Question, DuelRoom

DUEL_QUESTIONS = 5


# ==================================================
# HELPERS
# ==================================================

def _get_user_class(user, class_id):
    """Student la ya class madhe access ahe ka te tapasa. Ahe tar AcademicClass return kara."""
    if not class_id or not str(class_id).isdigit():
        return None

    access = (
        ClassAccess.objects.select_related("academic_class")
        .filter(
            student=user,
            academic_class_id=class_id,
            academic_class__is_active=True,
        )
        .first()
    )
    return access.academic_class if access else None


def _duel_home_url(class_id):
    return f"{reverse('examination:duel_home')}?class={class_id}"


def _valid_mcq_ids(subject):
    return list(
        Question.objects.filter(
            subject=subject,
            question_type="mcq",
            is_active=True,
        )
        .annotate(
            option_count=Count("options", distinct=True),
            correct_count=Count(
                "options",
                filter=Q(options__is_correct=True),
                distinct=True,
            ),
        )
        .filter(option_count__gte=2, correct_count=1)
        .values_list("id", flat=True)
    )


def _new_code():
    while True:
        code = secrets.token_hex(3).upper()
        if not DuelRoom.objects.filter(code=code).exists():
            return code


def _get_room_for_player(request, code):
    room = DuelRoom.objects.select_related("subject").filter(code=code.upper()).first()
    if not room or not room.is_player(request.user):
        raise Http404("Room sapdla nahi.")
    return room


def _room_state(room, user):
    if room.status == "waiting":
        return "waiting"
    if room.status == "finished":
        return "finished"
    side = room.side(user)
    return "waiting_opponent" if getattr(room, f"{side}_done") else "playing"


# ==================================================
# HOME: ya class cha duel page
# ==================================================

@login_required
def duel_home(request):
    assigned_class = _get_user_class(request.user, request.GET.get("class"))

    if not assigned_class:
        messages.error(request, "Please select your class.")
        return redirect("examination:class_dashboard")

    subjects = Subject.objects.filter(
        academic_class=assigned_class,
        is_active=True,
    ).order_by("name")

    rooms = (
        DuelRoom.objects.filter(subject__academic_class=assigned_class)
        .filter(Q(host=request.user) | Q(guest=request.user))
        .exclude(status="finished")
        .select_related("subject")
        .order_by("-created_at")[:5]
    )

    return render(
        request,
        "examination/duel_home.html",
        {
            "assigned_class": assigned_class,
            "selected_class": assigned_class,
            "subjects": subjects,
            "rooms": rooms,
            "duel_questions": DUEL_QUESTIONS,
        },
    )


# ==================================================
# CREATE ROOM
# ==================================================

@login_required
@require_POST
def duel_create(request):
    assigned_class = _get_user_class(request.user, request.POST.get("class"))

    if not assigned_class:
        messages.error(request, "Please select your class.")
        return redirect("examination:class_dashboard")

    home_url = _duel_home_url(assigned_class.id)

    subject_id = request.POST.get("subject", "")
    if not subject_id.isdigit():
        messages.error(request, "Subject nivda.")
        return redirect(home_url)

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        academic_class=assigned_class,
        is_active=True,
    )

    ids = _valid_mcq_ids(subject)
    if len(ids) < DUEL_QUESTIONS:
        messages.error(
            request,
            f"{subject.name} sathi duel sathi pure prashna nahit "
            f"(required {DUEL_QUESTIONS}, available {len(ids)})."
        )
        return redirect(home_url)

    room = DuelRoom.objects.create(
        code=_new_code(),
        host=request.user,
        subject=subject,
        question_ids=random.sample(ids, DUEL_QUESTIONS),
    )
    return redirect("examination:duel_room", code=room.code)


# ==================================================
# JOIN ROOM (code takun)
# ==================================================

@login_required
@require_POST
def duel_join(request):
    assigned_class = _get_user_class(request.user, request.POST.get("class"))

    if not assigned_class:
        messages.error(request, "Please select your class.")
        return redirect("examination:class_dashboard")

    home_url = _duel_home_url(assigned_class.id)
    code = request.POST.get("code", "").strip().upper()

    with transaction.atomic():
        room = DuelRoom.objects.select_for_update().filter(code=code).first()

        if not room:
            messages.error(request, "Ha code chukicha ahe.")
            return redirect(home_url)

        if room.host_id == request.user.id or room.guest_id == request.user.id:
            return redirect("examination:duel_room", code=room.code)

        if room.status != "waiting" or room.guest_id is not None:
            messages.error(request, "Ya room madhe jagaa nahi.")
            return redirect(home_url)

        if room.subject.academic_class_id != assigned_class.id:
            messages.error(request, "Ha room ya class sathi nahi.")
            return redirect(home_url)

        room.guest = request.user
        room.status = "active"
        room.save(update_fields=["guest", "status"])

    return redirect("examination:duel_room", code=room.code)


# ==================================================
# ROOM PAGE
# ==================================================

@login_required
def duel_room(request, code):
    room = _get_room_for_player(request, code)
    side = room.side(request.user)
    state = _room_state(room, request.user)

    # Sidebar madhe yogya class highlight honyasathi
    room_class = room.subject.academic_class

    questions = []
    if state == "playing":
        qmap = {
            q.id: q
            for q in Question.objects.filter(id__in=room.question_ids).prefetch_related("options")
        }
        questions = [qmap[i] for i in room.question_ids if i in qmap]

    my_score = getattr(room, f"{side}_score")

    opp_side = "guest" if side == "host" else "host"
    opp_score = getattr(room, f"{opp_side}_score") if state == "finished" else None

    winner = None
    if state == "finished":
        if room.host_score > room.guest_score:
            winner = "host"
        elif room.guest_score > room.host_score:
            winner = "guest"
        else:
            winner = "draw"

    return render(
        request,
        "examination/duel_room.html",
        {
            "room": room,
            "assigned_class": room_class,
            "selected_class": room_class,
            "side": side,
            "state": state,
            "questions": questions,
            "my_score": my_score,
            "opp_score": opp_score,
            "winner": winner,
            "total": len(room.question_ids),
        },
    )


# ==================================================
# STATUS (polling, JSON)
# ==================================================

@login_required
def duel_status(request, code):
    room = _get_room_for_player(request, code)
    return JsonResponse({"state": _room_state(room, request.user)})


# ==================================================
# SUBMIT ANSWERS
# ==================================================

@login_required
@require_POST
def duel_submit(request, code):
    room = _get_room_for_player(request, code)

    with transaction.atomic():
        room = DuelRoom.objects.select_for_update().get(pk=room.pk)

        if room.status != "active":
            return redirect("examination:duel_room", code=room.code)

        side = room.side(request.user)
        done_field = f"{side}_done"

        if getattr(room, done_field):
            return redirect("examination:duel_room", code=room.code)

        score = 0
        for qid in room.question_ids:
            chosen = request.POST.get(f"q_{qid}", "")
            if not chosen.isdigit():
                continue
            question = Question.objects.filter(id=qid).first()
            if question and question.options.filter(id=int(chosen), is_correct=True).exists():
                score += 1

        setattr(room, f"{side}_score", score)
        setattr(room, done_field, True)

        if room.host_done and room.guest_done:
            room.status = "finished"

        room.save()

    return redirect("examination:duel_room", code=room.code)


# ==================================================
# DELETE ROOM (fakt host, fakt waiting room)
# ==================================================

@login_required
@require_POST
def duel_delete(request, code):
    room = DuelRoom.objects.select_related("subject").filter(code=code.upper()).first()

    if not room or room.host_id != request.user.id:
        raise Http404("Room sapdla nahi.")

    class_id = room.subject.academic_class_id
    home_url = _duel_home_url(class_id)

    if room.status != "waiting" or room.guest_id is not None:
        messages.error(request, "Opponent join jhalela room delete karta yet nahi.")
        return redirect(home_url)

    room.delete()
    messages.success(request, "Room delete jhala.")
    return redirect(home_url)