from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
import random





CHALLENGES = [
    # PYTHON
    {
        "title": "Find the Second Largest Number",
        "category": "Python",
        "level": "Easy",
        "description": "List madhil second largest number shodha.",
        "starter_code": "numbers = [10, 25, 8, 40, 15]\n\n# Write your code here",
        "hint": "Largest number ani second largest number track kara.",
    },
    {
        "title": "Count Even and Odd Numbers",
        "category": "Python",
        "level": "Easy",
        "description": "List madhil even ani odd numbers vegale count kara.",
        "starter_code": "numbers = [12, 7, 25, 8, 14, 31]\n\n# Write your code here",
        "hint": "Modulo operator (%) vapra.",
    },
    {
        "title": "Reverse a String",
        "category": "Python",
        "level": "Easy",
        "description": "String reverse karun print kara.",
        "starter_code": 'text = "developer"\n\n# Write your code here',
        "hint": "String slicing kiwa loop vaprun paha.",
    },
    {
        "title": "Check Palindrome",
        "category": "Python",
        "level": "Easy",
        "description": "String palindrome aahe ka te check kara.",
        "starter_code": 'word = "madam"\n\n# Write your code here',
        "hint": "Original string ani reversed string compare kara.",
    },
    {
        "title": "Count Vowels",
        "category": "Python",
        "level": "Easy",
        "description": "String madhil vowels chi sankhya moja.",
        "starter_code": 'text = "programming language"\n\n# Write your code here',
        "hint": "a, e, i, o, u ya characters check kara.",
    },
    {
        "title": "Remove Duplicates",
        "category": "Python",
        "level": "Easy",
        "description": "List madhun duplicate values remove kara.",
        "starter_code": "numbers = [1, 2, 2, 3, 4, 4, 5]\n\n# Write your code here",
        "hint": "Set kiwa new list vaprun paha.",
    },
    {
        "title": "Find the Factorial",
        "category": "Python",
        "level": "Easy",
        "description": "Given number cha factorial calculate kara.",
        "starter_code": "number = 5\n\n# Write your code here",
        "hint": "Loop kiwa recursion vapra.",
    },
    {
        "title": "Check Prime Number",
        "category": "Python",
        "level": "Medium",
        "description": "Given number prime aahe ka te check kara.",
        "starter_code": "number = 29\n\n# Write your code here",
        "hint": "2 pasun number chya square root paryant divisibility check kara.",
    },
    {
        "title": "Find Common Elements",
        "category": "Python",
        "level": "Easy",
        "description": "Don lists madhil common elements shodha.",
        "starter_code": "a = [1, 2, 3, 4]\nb = [3, 4, 5, 6]\n\n# Write your code here",
        "hint": "Set intersection kiwa loop vapra.",
    },
    {
        "title": "Character Frequency",
        "category": "Python",
        "level": "Medium",
        "description": "String madhil pratyek character kiti vela aala te moja.",
        "starter_code": 'text = "programming"\n\n# Write your code here',
        "hint": "Dictionary madhye character counts store kara.",
    },
    {
        "title": "Find Missing Number",
        "category": "Python",
        "level": "Medium",
        "description": "1 te n madhil list madhye missing number shodha.",
        "starter_code": "numbers = [1, 2, 4, 5, 6]\n\n# Write your code here",
        "hint": "Expected sum ani actual sum madhil difference paha.",
    },
    {
        "title": "Merge Two Dictionaries",
        "category": "Python",
        "level": "Easy",
        "description": "Don dictionaries ekatra merge kara.",
        "starter_code": 'a = {"name": "Rohan"}\nb = {"role": "Developer"}\n\n# Write your code here',
        "hint": "Dictionary unpacking kiwa update() vapra.",
    },
    {
        "title": "Sort Without sort()",
        "category": "Python",
        "level": "Medium",
        "description": "Built-in sort() na vaparta numbers sort kara.",
        "starter_code": "numbers = [5, 2, 9, 1, 7]\n\n# Write your code here",
        "hint": "Bubble sort algorithm implement kara.",
    },
    {
        "title": "Flatten a Nested List",
        "category": "Python",
        "level": "Hard",
        "description": "Nested list la single-level list madhye convert kara.",
        "starter_code": "items = [[1, 2], [3, 4], [5, 6]]\n\n# Write your code here",
        "hint": "Nested loops vapra.",
    },
    {
        "title": "Find the Most Frequent Element",
        "category": "Python",
        "level": "Medium",
        "description": "List madhye sarvat jast vela yenara element shodha.",
        "starter_code": "numbers = [1, 2, 2, 3, 2, 4, 3]\n\n# Write your code here",
        "hint": "Frequency dictionary tayar kara.",
    },

    # DJANGO
    {
        "title": "Create a Django Model",
        "category": "Django",
        "level": "Easy",
        "description": "Student name, email ani age store karanara model tayar kara.",
        "starter_code": "from django.db import models\n\n# Create Student model here",
        "hint": "models.Model inherit kara ani CharField, EmailField, IntegerField vapra.",
    },
    {
        "title": "Create a Django View",
        "category": "Django",
        "level": "Easy",
        "description": "Simple HTTP response return karanara view lihा.",
        "starter_code": "from django.http import HttpResponse\n\n# Create your view here",
        "hint": "HttpResponse use kara.",
    },
    {
        "title": "Create a URL Pattern",
        "category": "Django",
        "level": "Easy",
        "description": "Home view la root URL sobat connect kara.",
        "starter_code": "from django.urls import path\n\n# Add URL pattern here",
        "hint": "path('', views.home, name='home') pattern vapra.",
    },
    {
        "title": "Create a Model Form",
        "category": "Django",
        "level": "Medium",
        "description": "Student model sathi ModelForm tayar kara.",
        "starter_code": "from django import forms\n\n# Create StudentForm here",
        "hint": "Meta class madhye model ani fields define kara.",
    },
    {
        "title": "Filter Active Records",
        "category": "Django",
        "level": "Easy",
        "description": "Active students database madhun retrieve kara.",
        "starter_code": "from .models import Student\n\n# Write ORM query here",
        "hint": "filter() method vapra.",
    },
    {
        "title": "Create a Login Protected View",
        "category": "Django",
        "level": "Medium",
        "description": "Login required aslela view tayar kara.",
        "starter_code": "from django.contrib.auth.decorators import login_required\n\n# Create protected view here",
        "hint": "login_required decorator vapra.",
    },
    {
        "title": "Handle POST Request",
        "category": "Django",
        "level": "Medium",
        "description": "POST request madhun form data access kara.",
        "starter_code": "def student_create(request):\n    # Handle POST request\n    pass",
        "hint": "request.method ani request.POST check kara.",
    },
    {
        "title": "Count Database Records",
        "category": "Django",
        "level": "Easy",
        "description": "Student table madhil total records moja.",
        "starter_code": "from .models import Student\n\n# Count students",
        "hint": "QuerySet cha count() method vapra.",
    },
    {
        "title": "Get Latest Record",
        "category": "Django",
        "level": "Medium",
        "description": "Database madhil latest student record retrieve kara.",
        "starter_code": "from .models import Student\n\n# Get latest record",
        "hint": "latest() kiwa order_by() vapra.",
    },
    {
        "title": "Create a Custom Manager",
        "category": "Django",
        "level": "Hard",
        "description": "Active students retrieve karanara custom manager tayar kara.",
        "starter_code": "from django.db import models\n\n# Create custom manager",
        "hint": "models.Manager extend kara.",
    },

    # SQL
    {
        "title": "Select All Students",
        "category": "SQL",
        "level": "Easy",
        "description": "Students table madhil sarva records retrieve kara.",
        "starter_code": "SELECT ______ FROM students;",
        "hint": "All columns select karanyasathi wildcard vapra.",
    },
    {
        "title": "Find Students Above Age 18",
        "category": "SQL",
        "level": "Easy",
        "description": "Age 18 peksha jast aslele students shodha.",
        "starter_code": "SELECT * FROM students\nWHERE ______;",
        "hint": "WHERE clause madhye comparison operator vapra.",
    },
    {
        "title": "Sort Students by Name",
        "category": "SQL",
        "level": "Easy",
        "description": "Students alphabetical order madhye display kara.",
        "starter_code": "SELECT * FROM students\nORDER BY ______;",
        "hint": "ORDER BY name ASC vaprun paha.",
    },
    {
        "title": "Count Total Students",
        "category": "SQL",
        "level": "Easy",
        "description": "Table madhil students chi total sankhya moja.",
        "starter_code": "SELECT ______(*) FROM students;",
        "hint": "Aggregate function COUNT vapra.",
    },
    {
        "title": "Find Duplicate Emails",
        "category": "SQL",
        "level": "Medium",
        "description": "Duplicate email addresses shodha.",
        "starter_code": "SELECT email, COUNT(*)\nFROM students\nGROUP BY email\n______;",
        "hint": "GROUP BY nantar HAVING vapra.",
    },
    {
        "title": "Join Two Tables",
        "category": "SQL",
        "level": "Medium",
        "description": "Students ani courses tables join kara.",
        "starter_code": "SELECT *\nFROM students\n______ courses\nON students.course_id = courses.id;",
        "hint": "INNER JOIN vapra.",
    },
    {
        "title": "Find Maximum Salary",
        "category": "SQL",
        "level": "Easy",
        "description": "Employees table madhil maximum salary shodha.",
        "starter_code": "SELECT ______(salary)\nFROM employees;",
        "hint": "MAX() aggregate function vapra.",
    },
    {
        "title": "Update Student Email",
        "category": "SQL",
        "level": "Medium",
        "description": "Specific student cha email update kara.",
        "starter_code": "UPDATE students\nSET email = 'new@example.com'\nWHERE ______;",
        "hint": "Unique ID vaprun WHERE condition lava.",
    },

    # JAVASCRIPT
    {
        "title": "Create a Counter",
        "category": "JavaScript",
        "level": "Easy",
        "description": "Button click kelyavar counter increase kara.",
        "starter_code": "let count = 0;\n\n// Increase count on button click",
        "hint": "addEventListener() vapra.",
    },
    {
        "title": "Find Largest Array Value",
        "category": "JavaScript",
        "level": "Easy",
        "description": "Array madhil largest number shodha.",
        "starter_code": "const numbers = [12, 45, 7, 89, 23];\n\n// Write your code",
        "hint": "Math.max() kiwa loop vapra.",
    },
    {
        "title": "Filter Adult Users",
        "category": "JavaScript",
        "level": "Easy",
        "description": "Age 18 kiwa tyapeksha jast aslele users filter kara.",
        "starter_code": "const users = [\n  {name: 'A', age: 17},\n  {name: 'B', age: 22}\n];",
        "hint": "Array filter() method vapra.",
    },
    {
        "title": "Convert String to Uppercase",
        "category": "JavaScript",
        "level": "Easy",
        "description": "String uppercase madhye convert kara.",
        "starter_code": "const message = 'hello developer';\n\n// Write your code",
        "hint": "toUpperCase() method vapra.",
    },
    {
        "title": "Calculate Array Sum",
        "category": "JavaScript",
        "level": "Medium",
        "description": "Array madhil numbers chi sum calculate kara.",
        "starter_code": "const numbers = [10, 20, 30, 40];\n\n// Write your code",
        "hint": "reduce() method vapra.",
    },
    {
        "title": "Validate an Email",
        "category": "JavaScript",
        "level": "Medium",
        "description": "Basic email validation function tayar kara.",
        "starter_code": "function validateEmail(email) {\n    // Write your logic\n}",
        "hint": "Includes check kiwa regular expression vapra.",
    },
    {
        "title": "Remove Duplicate Array Values",
        "category": "JavaScript",
        "level": "Medium",
        "description": "Array madhun duplicate values remove kara.",
        "starter_code": "const values = [1, 2, 2, 3, 4, 4];\n\n// Write your code",
        "hint": "Set vaprun paha.",
    },
    {
        "title": "Create a Promise",
        "category": "JavaScript",
        "level": "Medium",
        "description": "Resolve ani reject use karun Promise tayar kara.",
        "starter_code": "const task = new Promise((resolve, reject) => {\n    // Write your logic\n});",
        "hint": "Promise constructor madhye callback function asto.",
    },

    # DSA
    {
        "title": "Linear Search",
        "category": "DSA",
        "level": "Easy",
        "description": "Array madhye target element search kara.",
        "starter_code": "numbers = [4, 8, 15, 16, 23]\ntarget = 15\n\n# Write your code",
        "hint": "Pratyek element sequentially check kara.",
    },
    {
        "title": "Binary Search",
        "category": "DSA",
        "level": "Medium",
        "description": "Sorted array madhye binary search implement kara.",
        "starter_code": "numbers = [2, 5, 8, 12, 16, 23]\ntarget = 16\n\n# Write your code",
        "hint": "Low, high ani mid pointers maintain kara.",
    },
    {
        "title": "Bubble Sort",
        "category": "DSA",
        "level": "Medium",
        "description": "Bubble sort algorithm implement kara.",
        "starter_code": "numbers = [5, 1, 4, 2, 8]\n\n# Write your code",
        "hint": "Adjacent elements compare ani swap kara.",
    },
    {
        "title": "Check Balanced Parentheses",
        "category": "DSA",
        "level": "Medium",
        "description": "Brackets balanced aahet ka te check kara.",
        "starter_code": 'expression = "{[()]}"\n\n# Write your code',
        "hint": "Stack data structure vapra.",
    },
    {
        "title": "Two Sum Problem",
        "category": "DSA",
        "level": "Medium",
        "description": "Target sum denari don elements chi pair shodha.",
        "starter_code": "numbers = [2, 7, 11, 15]\ntarget = 9\n\n# Write your code",
        "hint": "Dictionary madhye previously seen values store kara.",
    },
    {
        "title": "Find Maximum Subarray Sum",
        "category": "DSA",
        "level": "Hard",
        "description": "Contiguous subarray madhil maximum sum shodha.",
        "starter_code": "numbers = [-2, 1, -3, 4, -1, 2, 1]\n\n# Write your code",
        "hint": "Kadane's algorithm study kara.",
    },
    {
        "title": "Reverse a Linked List",
        "category": "DSA",
        "level": "Hard",
        "description": "Singly linked list reverse kara.",
        "starter_code": "# Define a linked list node\n# Reverse the linked list",
        "hint": "Previous, current ani next pointers vapra.",
    },
    {
        "title": "Implement a Stack",
        "category": "DSA",
        "level": "Medium",
        "description": "Push, pop ani peek operations aslela stack tayar kara.",
        "starter_code": "class Stack:\n    def __init__(self):\n        # Initialize stack\n        pass",
        "hint": "Python list vaprun operations implement kara.",
    },
    {
        "title": "Find First Non-Repeating Character",
        "category": "DSA",
        "level": "Medium",
        "description": "String madhil pahila non-repeating character shodha.",
        "starter_code": 'text = "aabbcde"\n\n# Write your code',
        "hint": "Character frequency count kara ani original order check kara.",
    },
    {
        "title": "Merge Two Sorted Arrays",
        "category": "DSA",
        "level": "Medium",
        "description": "Don sorted arrays merge karun sorted result tayar kara.",
        "starter_code": "a = [1, 3, 5]\nb = [2, 4, 6]\n\n# Write your code",
        "hint": "Two pointer technique vapra.",
    },
]


THOUGHTS = [
    {
        "quote": "First, solve the problem. Then, write the code.",
        "author": "Developer Principle",
        "description": "Problem samajlyashivay code lihayla suruvat karu naka.",
    },
    {
        "quote": "Debugging is twice as hard as writing the code in the first place.",
        "author": "Programming Principle",
        "description": "Code simple ani readable thevne mahatvache aahe.",
    },
    {
        "quote": "Small steps every day lead to big results.",
        "author": "Developer Mindset",
        "description": "Consistency hi long-term learning chi key aahe.",
    },
    {
        "quote": "An error is not a failure. It is information.",
        "author": "Developer Mindset",
        "description": "Error message vachun problem chi root cause shodha.",
    },
    {
        "quote": "The best way to learn programming is by writing programs.",
        "author": "Learning Principle",
        "description": "Tutorial baghnyapeksha practical coding la priority dya.",
    },
    {
        "quote": "Readable code is easier to maintain than clever code.",
        "author": "Clean Code Principle",
        "description": "Dusrya developer la samjel asa code liha.",
    },
    {
        "quote": "A good developer keeps asking why.",
        "author": "Developer Mindset",
        "description": "Fakt code kay karto nahi, tar kasa ani ka karto he samjun ghya.",
    },
    {
        "quote": "Every bug you fix makes you a better problem solver.",
        "author": "Developer Mindset",
        "description": "Debugging madhun practical experience milto.",
    },
    {
        "quote": "Build projects to turn knowledge into experience.",
        "author": "Project Principle",
        "description": "Shikalelela concept project madhye implement kara.",
    },
    {
        "quote": "Do not memorize solutions. Understand the logic.",
        "author": "Learning Principle",
        "description": "Logic samajla tar navin problems solve karta yetat.",
    },
    {
        "quote": "Consistency beats occasional intensity.",
        "author": "Learning Principle",
        "description": "Roj thodi practice karne upyogi tharte.",
    },
    {
        "quote": "Your code should explain itself.",
        "author": "Clean Code Principle",
        "description": "Meaningful names ani simple functions vapra.",
    },
    {
        "quote": "A project is proof of what you can build.",
        "author": "Career Principle",
        "description": "Portfolio madhye complete ani working projects dakhva.",
    },
    {
        "quote": "Learn the fundamentals before chasing tools.",
        "author": "Learning Principle",
        "description": "Strong fundamentals mule frameworks shikne sope hote.",
    },
    {
        "quote": "Do not fear breaking code. Learn to fix it.",
        "author": "Developer Mindset",
        "description": "Safe environment madhye experiment kara.",
    },
]


LEARNING_TIPS = [
    {
        "title": "Read the Error Message",
        "description": "Error cha type, file name ani line number adhi check kara.",
        "category": "Debugging",
    },
    {
        "title": "Practice Without Looking",
        "description": "Example samjun ghetlyanantar code na baghta punha lihun paha.",
        "category": "Practice",
    },
    {
        "title": "Use Meaningful Names",
        "description": "Variables ani functions la tyanchya purpose nusar names dya.",
        "category": "Clean Code",
    },
    {
        "title": "Make Small Commits",
        "description": "Git madhye related changes sathi meaningful commits kara.",
        "category": "Git",
    },
    {
        "title": "Understand HTTP Methods",
        "description": "GET, POST, PUT, PATCH ani DELETE yanche differences samjun ghya.",
        "category": "Backend",
    },
    {
        "title": "Learn SQL Joins",
        "description": "INNER JOIN, LEFT JOIN ani related table queries practice kara.",
        "category": "Database",
    },
    {
        "title": "Use Django ORM Carefully",
        "description": "filter(), get(), exclude() ani select_related() samjun ghya.",
        "category": "Django",
    },
    {
        "title": "Test Your API",
        "description": "Success sobat invalid input ani permission cases pan test kara.",
        "category": "API",
    },
    {
        "title": "Keep Functions Small",
        "description": "Ek function ek specific responsibility handle karel asa design kara.",
        "category": "Clean Code",
    },
    {
        "title": "Learn List Comprehensions",
        "description": "Python madhye readable list comprehensions lihinyacha sarav kara.",
        "category": "Python",
    },
    {
        "title": "Understand Git Branches",
        "description": "Feature development sathi branches vaprayla shika.",
        "category": "Git",
    },
    {
        "title": "Protect Secret Keys",
        "description": "SECRET_KEY, passwords ani API keys GitHub var upload karu naka.",
        "category": "Security",
    },
    {
        "title": "Use Pagination",
        "description": "Large API responses pagination ne manageable kara.",
        "category": "API",
    },
    {
        "title": "Validate User Input",
        "description": "Server-side validation shivay user input trust karu naka.",
        "category": "Security",
    },
    {
        "title": "Write Reusable Code",
        "description": "Repeated logic reusable functions kiwa classes madhye theva.",
        "category": "Clean Code",
    },
    {
        "title": "Understand Database Indexes",
        "description": "Indexes query performance improve karu shaktat, pan unnecessary indexes avoid kara.",
        "category": "Database",
    },
]


DAILY_GOALS = [
    "Aaj ek Python problem swatah solve kara.",
    "Django madhye ek ORM query practice kara.",
    "Ek REST API endpoint samjun ghya.",
    "GitHub var ek meaningful commit kara.",
    "SQL madhil 5 queries practice kara.",
    "Ek JavaScript array method implement kara.",
    "Aadhi kelelya project madhil ek bug fix kara.",
    "Ek Django model ani migration practice kara.",
    "Ek API Postman madhye test kara.",
    "Ek coding concept swatahchya shabdat explain kara.",
    "15 minutes DSA problem solving kara.",
    "Ek function refactor karun readable banva.",
    "Ek official documentation page vacha.",
    "Project README madhye setup instructions improve kara.",
    "Ek small feature complete kara ani test kara.",
]


@login_required(login_url="login")
def home(request):
    challenge = random.choice(CHALLENGES)
    thought = random.choice(THOUGHTS)
    tip = random.choice(LEARNING_TIPS)
    daily_goal = random.choice(DAILY_GOALS)

    context = {
        "challenge": challenge,
        "thought": thought,
        "tip": tip,
        "daily_goal": daily_goal,
        "challenge_count": len(CHALLENGES),
        "thought_count": len(THOUGHTS),
        "tip_count": len(LEARNING_TIPS),
    }

    return render(request, "documentation/home.html", context)


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
