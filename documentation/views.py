from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404


@login_required(login_url="login")
def home(request):
    return render(request, "documentation/home.html")

def python_topic(request, topic):
    allowed_topics = {
        "introduction": "introduction.html",
        "installation": "installation.html",
        "syntax": "syntax.html",
        "comments": "comments.html",
        "variables": "variables.html",
        "data-types": "data-types.html",
        "type-casting": "type-casting.html",
        "input-output": "input-output.html",
        "operators": "operators.html",
        "strings": "strings.html",
        "string-methods": "string-methods.html",
        "lists": "lists.html",
        "tuples": "tuples.html",
        "sets": "sets.html",
        "dictionaries": "dictionaries.html",
        "conditions": "conditions.html",
        "loops": "loops.html",
        "loop-control": "loop-control.html",
        "functions": "functions.html",
        "arguments": "arguments.html",
        "lambda": "lambda.html",
        "modules": "modules.html",
        "exceptions": "exceptions.html",
        "file-handling": "file-handling.html",
        "oops": "oops.html",
        "inheritance": "inheritance.html",
        "polymorphism": "polymorphism.html",
        "practice": "practice.html",
    }

    template = allowed_topics.get(topic)

    if not template:
        from django.http import Http404
        raise Http404("Topic not found")

    return render(request, f"documentation/python/{template}")

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def python_index(request):
    return render(
        request,
        "documentation/python/index.html"
    )
    
    

def html_topic(request, topic):
    allowed_topics = {
        "introduction": "introduction.html",
        "structure": "structure.html",
        "elements": "elements.html",
        "attributes": "attributes.html",
        "headings-paragraphs": "headings-paragraphs.html",
        "links": "links.html",
        "images": "images.html",
        "lists": "lists.html",
        "tables": "tables.html",
        "forms": "forms.html",
        "input-types": "input-types.html",
        "semantic-html": "semantic-html.html",
        "audio-video": "audio-video.html",
        "iframes": "iframes.html",
        "html-entities": "html-entities.html",
        "html5-features": "html5-features.html",
        "seo-basics": "seo-basics.html",
        "accessibility": "accessibility.html",
        "projects": "projects.html",
        "practice": "practice.html",
    }

    template = allowed_topics.get(topic)

    if not template:
        from django.http import Http404
        raise Http404("HTML Topic not found")

    return render(request, f"documentation/html/{template}")


@login_required(login_url="login")
def html_index(request):
    return render(
        request,
        "documentation/html/index.html"
    )
    
    



def css_topic(request, topic):
    allowed_topics = {
        "introduction": "introduction.html",
        "syntax": "syntax.html",
        "ways-to-add-css": "ways-to-add-css.html",
        "selectors": "selectors.html",
        "colors-backgrounds": "colors-backgrounds.html",
        "text-properties": "text-properties.html",
        "fonts": "fonts.html",
        "units": "units.html",
        "box-model": "box-model.html",
        "margin-padding": "margin-padding.html",
        "borders-outlines": "borders-outlines.html",
        "width-height": "width-height.html",
        "display": "display.html",
        "position": "position.html",
        "flexbox": "flexbox.html",
        "grid": "grid.html",
        "pseudo-classes": "pseudo-classes.html",
        "pseudo-elements": "pseudo-elements.html",
        "transitions-transforms": "transitions-transforms.html",
        "animations": "animations.html",
        "shadows-gradients": "shadows-gradients.html",
        "overflow-z-index": "overflow-z-index.html",
        "responsive-design": "responsive-design.html",
        "media-queries": "media-queries.html",
        "variables": "variables.html",
        "specificity-inheritance": "specificity-inheritance.html",
        "best-practices": "best-practices.html",
        "projects": "projects.html",
        "practice": "practice.html",
    }

    template = allowed_topics.get(topic)

    if not template:
        from django.http import Http404
        raise Http404("CSS Topic not found")

    return render(
        request,
        f"documentation/css/{template}"
    )


@login_required(login_url="login")
def css_index(request):
    return render(
        request,
        "documentation/css/index.html"
    )

def javascript_index(request):
    return render(request, "documentation/javascript/index.html")


@login_required(login_url="login")
def javascript_topic(request, topic):

    allowed_topics = {
        "introduction": "introduction.html",
        "syntax": "syntax.html",
        "ways-to-add-javascript": "ways-to-add-javascript.html",
        "variables": "variables.html",
        "data-types": "data-types.html",
        "operators": "operators.html",
        "input-output": "input-output.html",
        "conditions": "conditions.html",
        "loops": "loops.html",
        "functions": "functions.html",
        "arrow-functions": "arrow-functions.html",
        "arrays": "arrays.html",
        "array-methods": "array-methods.html",
        "strings": "strings.html",
        "objects": "objects.html",
        "object-methods": "object-methods.html",
        "dom": "dom.html",
        "dom-selectors": "dom-selectors.html",
        "dom-manipulation": "dom-manipulation.html",
        "events": "events.html",
        "form-validation": "form-validation.html",
        "es6": "es6.html",
        "spread-rest": "spread-rest.html",
        "higher-order-methods": "higher-order-methods.html",
        "json": "json.html",
        "local-storage": "local-storage.html",
        "async-javascript": "async-javascript.html",
        "promises": "promises.html",
        "fetch-api": "fetch-api.html",
        "projects": "projects.html",
    }

    template = allowed_topics.get(topic)

    if not template:
        from django.http import Http404
        raise Http404("JavaScript Topic not found")

    return render(request, f"documentation/javascript/{template}")


# =====================================
# DJANGO DOCUMENTATION
# =====================================

def django_index(request):
    return render(request, "documentation/django/index.html")


@login_required(login_url="login")
def django_topic(request, topic):

    allowed_topics = {
        "introduction": "introduction.html",
        "installation": "installation.html",
        "project-structure": "project-structure.html",
        "mvt-architecture": "mvt-architecture.html",
        "urls-and-views": "urls-and-views.html",
        "templates": "templates.html",
        "static-files": "static-files.html",
        "models": "models.html",
        "django-orm": "django-orm.html",
        "migrations": "migrations.html",
        "forms": "forms.html",
        "modelforms": "modelforms.html",
        "crud-operations": "crud-operations.html",
        "authentication": "authentication.html",
        "login-logout": "login-logout.html",
        "admin-panel": "admin-panel.html",
        "sessions-and-cookies": "sessions-and-cookies.html",
        "model-relationships": "model-relationships.html",
        "file-image-upload": "file-image-upload.html",
        "class-based-views": "class-based-views.html",
        "middleware": "middleware.html",
        "messages-framework": "messages-framework.html",
        "pagination-search": "pagination-search.html",
        "security": "security.html",
        "testing": "testing.html",
        "deployment": "deployment.html",
    }

    template = allowed_topics.get(topic)

    if not template:
        from django.http import Http404
        raise Http404("Django Topic not found")

    return render(
        request,
        f"documentation/django/{template}"
    )
    
# ==========================================
# DJANGO REST FRAMEWORK NOTES
# ==========================================

def drf_index(request):
    return render(
        request,
        "documentation/drf/index.html"
    )


def drf_topic(request, topic):

    topics = [
        "introduction",
        "django-vs-drf",
        "rest-api-basics",
        "json",
        "http-methods",
        "http-status-codes",
        "installation",
        "first-api",
        "serializers",
        "model-serializer",
        "serialization",
        "deserialization",
        "api-views",
        "function-based-views",
        "request-response",
        "crud-api",
        "url-routing",
        "generic-views",
        "mixins",
        "concrete-generic-views",
        "viewsets",
        "routers",
        "authentication",
        "permissions",
        "token-authentication",
        "jwt-authentication",
        "pagination",
        "filtering",
        "searching",
        "ordering",
        "throttling",
        "relationships",
        "file-upload-api",
        "api-testing",
        "api-deployment",
    ]

    if topic not in topics:
        raise Http404("Topic not found")

    return render(
        request,
        f"documentation/drf/{topic}.html"
    )
