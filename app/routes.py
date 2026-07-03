import json
import re
from datetime import datetime, timezone
from functools import wraps

from flask import (
    Blueprint,
    Response,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.logic_engine import analyze_project
from app.models import (
    Character,
    ContactMessage,
    Event,
    Faction,
    Feedback,
    Project,
    Relation,
    User,
    WishlistEntry,
)


main = Blueprint("main", __name__)
RELATION_TYPES = [
    "hates",
    "allied_with",
    "member_of",
    "loyal_to",
    "participated_in",
    "rules",
    "located_in",
]
RELATION_TYPE_LABELS = {
    "hates": "Hates",
    "allied_with": "Allied with",
    "member_of": "Member of",
    "loyal_to": "Loyal to",
    "participated_in": "Participated in",
    "rules": "Rules",
    "located_in": "Located in",
}
RELATION_TYPE_HELPERS = {
    "hates": "Usually character -> character.",
    "allied_with": "Usually character/faction -> character/faction.",
    "member_of": "Usually character -> faction.",
    "loyal_to": "Usually character/faction -> character/faction.",
    "participated_in": "Usually character/faction -> event.",
    "rules": "Usually character/faction -> faction/location-like entity.",
    "located_in": "Usually character/faction/event -> event or location-like entity.",
}
USER_ROLES = [
    "Writer",
    "Game Master",
    "Worldbuilder",
    "Screenwriter",
    "Game Developer",
    "Narrative Designer",
    "Other",
]


@main.before_app_request
def restrict_routes_during_wishlist_mode():
    """Keep the pre-launch site focused while retaining admin access."""
    if not current_app.config.get("WISHLIST_MODE", False):
        return None

    endpoint = request.endpoint or ""
    if endpoint in {"static", "main.index", "main.wishlist", "main.login", "main.logout"}:
        return None

    if endpoint.startswith("main.admin_") and current_user.is_authenticated and current_user.is_admin:
        return None

    return redirect(url_for("main.wishlist"))


def admin_required(view):
    # For local testing, set a user's is_admin field to True in a Flask shell and commit the change.
    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapped_view


def get_project_or_404_for_current_user(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    return project


def project_access_required(view):
    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwargs):
        get_project_or_404_for_current_user(kwargs["project_id"])
        return view(*args, **kwargs)

    return wrapped_view


@main.route("/")
def index():
    if current_app.config.get("WISHLIST_MODE", False):
        return redirect(url_for("main.wishlist"))
    return render_template("index.html")


@main.route("/wishlist", methods=["GET", "POST"])
def wishlist():
    def render_wishlist():
        joined_email = request.args.get("email", "").strip().lower()
        joined_entry = None
        if request.args.get("joined") == "1" and joined_email:
            joined_entry = WishlistEntry.query.filter_by(email=joined_email).first()
        wishlist_position = None
        wishlist_reference = None
        if joined_entry:
            wishlist_position = WishlistEntry.query.filter(
                WishlistEntry.id <= joined_entry.id
            ).count()
            wishlist_reference = f"ZR-{joined_entry.id:04d}"

        return render_template(
            "wishlist.html",
            wishlist_roles=USER_ROLES,
            wishlist_count=WishlistEntry.query.count(),
            recent_wishlist_entries=WishlistEntry.query.order_by(
                WishlistEntry.created_at.desc()
            )
            .limit(3)
            .all(),
            joined_entry=joined_entry,
            wishlist_position=wishlist_position,
            wishlist_reference=wishlist_reference,
        )

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        name = request.form.get("name", "").strip()
        role = request.form.get("role", "").strip()
        message = request.form.get("message", "").strip()

        if not email:
            flash("Please enter your email address.", "danger")
            return render_wishlist()

        if WishlistEntry.query.filter_by(email=email).first():
            flash("You are already on the Zirel wishlist.", "info")
            return redirect(url_for("main.wishlist", joined=1, email=email))

        if role and role not in USER_ROLES:
            role = None

        entry = WishlistEntry(
            email=email,
            name=name or None,
            role=role or None,
            message=message or None,
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("main.wishlist", joined=1, email=email))

    return render_wishlist()


@main.route("/terms")
def terms():
    return render_template("terms.html")


@main.route("/privacy")
def privacy():
    return render_template("privacy.html")


@main.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")


@main.route("/legal")
def legal():
    return render_template("legal.html")


@main.route("/faq")
def faq():
    return render_template("faq.html")


@main.route("/whitepaper")
def whitepaper():
    return render_template("whitepaper.html")


@main.route("/roadmap")
def roadmap():
    return render_template("roadmap.html")


@main.route("/beta")
def beta():
    return render_template("beta.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.projects"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        role = request.form.get("role", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        terms_agreed = request.form.get("terms_agreed") == "accepted"

        if not username or not email or not password or not confirm_password:
            flash("All registration fields are required.", "danger")
            return render_template("register.html")
        if role not in USER_ROLES:
            flash("Please select what describes you best.", "danger")
            return render_template("register.html")
        if not terms_agreed:
            flash("Please agree to the Terms of Service and Privacy Policy.", "danger")
            return render_template("register.html")
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")
        if User.query.filter_by(username=username).first():
            flash("That username is already in use.", "danger")
            return render_template("register.html")
        if User.query.filter_by(email=email).first():
            flash("That email address is already registered.", "danger")
            return render_template("register.html")

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        flash("Welcome to Zirel.", "success")
        return redirect(url_for("main.projects"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_app.config.get("WISHLIST_MODE", False):
            if current_user.is_admin:
                return redirect(url_for("main.admin_dashboard"))
            return redirect(url_for("main.wishlist"))
        return redirect(url_for("main.projects"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        login_user(user)
        flash("Welcome back.", "success")
        if current_app.config.get("WISHLIST_MODE", False):
            if user.is_admin:
                return redirect(url_for("main.admin_dashboard"))
            return redirect(url_for("main.wishlist"))
        return redirect(url_for("main.projects"))

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.index"))


@main.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        role = request.form.get("role", "").strip()
        message = request.form.get("message", "").strip()
        valid_roles = [
            "Writer",
            "Game Master",
            "World-builder",
            "Game Developer",
            "Screenwriter",
            "Other",
        ]

        if not message:
            flash("Feedback message is required.", "danger")
            return render_template("feedback.html")

        if role not in valid_roles:
            role = "Other"

        db.session.add(
            Feedback(
                name=name or None,
                email=email or None,
                role=role,
                message=message,
            )
        )
        db.session.commit()

        flash("Thank you for your feedback.", "success")
        return redirect(url_for("main.feedback"))

    return render_template("feedback.html")


@main.route("/feedback/list")
@admin_required
def feedback_list():
    # This route is for local MVP use only and should be protected before public deployment.
    return redirect(url_for("main.admin_feedback"))


@main.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        reason = request.form.get("reason", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()
        valid_reasons = [
            "General question",
            "Beta access",
            "Bug report",
            "Collaboration",
            "Business / partnership",
            "Other",
        ]

        if not email or not message:
            flash("Email and message are required.", "danger")
            return render_template("contact.html")

        if reason not in valid_reasons:
            reason = "Other"

        db.session.add(
            ContactMessage(
                name=name or None,
                email=email,
                reason=reason,
                subject=subject or None,
                message=message,
            )
        )
        db.session.commit()

        flash("Your message has been sent. Thank you.", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html")


@main.route("/contact/list")
@admin_required
def contact_list():
    # This route is for local MVP use only and should be protected before public deployment.
    return redirect(url_for("main.admin_contact"))


@main.route("/admin")
@admin_required
def admin_dashboard():
    stats = {
        "users": User.query.count(),
        "projects": Project.query.count(),
        "characters": Character.query.count(),
        "factions": Faction.query.count(),
        "events": Event.query.count(),
        "relations": Relation.query.count(),
        "feedback": Feedback.query.count(),
        "contact": ContactMessage.query.count(),
        "wishlist": WishlistEntry.query.count(),
    }
    return render_template(
        "admin_dashboard.html",
        stats=stats,
        feedback_entries=Feedback.query.order_by(Feedback.created_at.desc()).limit(5).all(),
        contact_messages=ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all(),
        users=User.query.order_by(User.created_at.desc()).limit(5).all(),
    )


@main.route("/admin/feedback")
@admin_required
def admin_feedback():
    entries = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template("admin_feedback.html", feedback_entries=entries)


@main.route("/admin/contact")
@admin_required
def admin_contact():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin_contact.html", contact_messages=messages)


@main.route("/admin/users")
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin_users.html", users=users)


@main.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot delete your own admin account while logged in.", "danger")
        return redirect(url_for("main.admin_users"))
    if user.is_admin and User.query.filter_by(is_admin=True).count() <= 1:
        flash("You cannot delete the last admin account.", "danger")
        return redirect(url_for("main.admin_users"))

    db.session.delete(user)
    db.session.commit()
    flash("User account deleted.", "success")
    return redirect(url_for("main.admin_users"))


@main.route("/admin/wishlist")
@admin_required
def admin_wishlist():
    entries = WishlistEntry.query.order_by(WishlistEntry.created_at.desc()).all()
    return render_template("admin_wishlist.html", wishlist_entries=entries)


@main.route("/admin/wishlist/<int:entry_id>/delete", methods=["POST"])
@admin_required
def admin_delete_wishlist_entry(entry_id):
    entry = WishlistEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Wishlist entry deleted.", "success")
    return redirect(url_for("main.admin_wishlist"))


@main.route("/admin/feedback/<int:feedback_id>/delete", methods=["POST"])
@admin_required
def admin_delete_feedback(feedback_id):
    entry = Feedback.query.get_or_404(feedback_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Feedback message deleted.", "success")
    return redirect(url_for("main.admin_feedback"))


@main.route("/admin/contact/<int:message_id>/delete", methods=["POST"])
@admin_required
def admin_delete_contact_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash("Contact message deleted.", "success")
    return redirect(url_for("main.admin_contact"))


@main.route("/projects")
@login_required
def projects():
    project_query = Project.query
    if not current_user.is_admin:
        project_query = project_query.filter(Project.user_id == current_user.id)
    all_projects = project_query.order_by(Project.created_at.desc()).all()
    project_stats = {
        "worlds": len(all_projects),
        "characters": sum(len(project.characters) for project in all_projects),
        "relations": sum(len(project.relations) for project in all_projects),
        "events": sum(len(project.events) for project in all_projects),
    }
    return render_template(
        "projects.html",
        projects=all_projects,
        project_stats=project_stats,
    )


@main.route("/projects/import", methods=["GET", "POST"])
@login_required
def import_project():
    if request.method == "POST":
        uploaded_file = request.files.get("import_file")

        if not uploaded_file or uploaded_file.filename == "":
            flash("Unsupported file. Please choose a Zirel JSON export file.", "warning")
            return render_template("import_project.html")

        if not uploaded_file.filename.lower().endswith(".json"):
            flash("Unsupported file. Please upload a .json file.", "warning")
            return render_template("import_project.html")

        try:
            export_data = json.load(uploaded_file)
        except json.JSONDecodeError:
            flash("Invalid JSON. Please upload a valid Zirel export file.", "danger")
            return render_template("import_project.html")

        validation_error = validate_project_import(export_data)
        if validation_error:
            flash(validation_error, "danger")
            return render_template("import_project.html")

        try:
            project = create_project_from_import(export_data)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Import failed. Please check the file and try again.", "danger")
            return render_template("import_project.html")

        flash("Project imported successfully.", "success")
        return redirect(url_for("main.project_detail", project_id=project.id))

    return render_template("import_project.html")


@main.route("/projects/<int:project_id>")
@project_access_required
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    warning_count = len(analyze_project(project))
    return render_template(
        "project_detail.html",
        project=project,
        warning_count=warning_count,
    )


@main.route("/projects/<int:project_id>/export/json")
@project_access_required
def export_project_json(project_id):
    project = Project.query.get_or_404(project_id)
    export_data = build_project_export(project)
    filename = build_export_filename(project.name)
    json_body = json.dumps(export_data, indent=2, ensure_ascii=False)

    return Response(
        json_body,
        mimetype="application/json",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
        },
    )


@main.route("/projects/<int:project_id>/warnings")
@project_access_required
def warnings(project_id):
    project = Project.query.get_or_404(project_id)
    project_warnings = analyze_project(project)
    warning_summary = {
        "total": len(project_warnings),
        "high": sum(warning.get("severity") == "high" for warning in project_warnings),
        "medium": sum(
            warning.get("severity") == "medium" for warning in project_warnings
        ),
        "low": sum(warning.get("severity") == "low" for warning in project_warnings),
    }
    if warning_summary["total"] == 0:
        warning_summary["status"] = "Consistent for now"
    elif warning_summary["high"]:
        warning_summary["status"] = "Needs attention"
    else:
        warning_summary["status"] = "Review recommended"
    return render_template(
        "warnings.html",
        project=project,
        warnings=project_warnings,
        warning_summary=warning_summary,
    )


@main.route("/projects/<int:project_id>/graph")
@project_access_required
def graph(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template("graph.html", project=project)


@main.route("/projects/<int:project_id>/graph/data")
@project_access_required
def graph_data(project_id):
    project = Project.query.get_or_404(project_id)
    nodes = []
    node_ids = set()
    node_labels = {}

    for character in project.characters:
        node_id = build_graph_node_id("character", character.id)
        nodes.append(
            {
                "data": {
                    "id": node_id,
                    "label": character.name,
                    "type": "character",
                }
            }
        )
        node_ids.add(node_id)
        node_labels[node_id] = character.name

    for faction in project.factions:
        node_id = build_graph_node_id("faction", faction.id)
        nodes.append(
            {
                "data": {
                    "id": node_id,
                    "label": faction.name,
                    "type": "faction",
                }
            }
        )
        node_ids.add(node_id)
        node_labels[node_id] = faction.name

    for event in project.events:
        node_id = build_graph_node_id("event", event.id)
        nodes.append(
            {
                "data": {
                    "id": node_id,
                    "label": event.name,
                    "type": "event",
                }
            }
        )
        node_ids.add(node_id)
        node_labels[node_id] = event.name

    edges = []
    for relation in project.relations:
        source = build_graph_node_id(relation.source_type, relation.source_id)
        target = build_graph_node_id(relation.target_type, relation.target_id)

        if source not in node_ids or target not in node_ids:
            continue

        edges.append(
            {
                "data": {
                    "id": f"relation-{relation.id}",
                    "source": source,
                    "target": target,
                    "label": relation.relation_type,
                    "relation_type": relation.relation_type,
                    "description": relation.description or "",
                    "source_label": node_labels[source],
                    "target_label": node_labels[target],
                }
            }
        )

    return jsonify({"nodes": nodes, "edges": edges})


@main.route("/projects/create", methods=["GET", "POST"])
@login_required
def create_project():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Project name is required.", "danger")
            return render_template("create_project.html")

        project = Project(user=current_user, name=name, description=description)
        db.session.add(project)
        db.session.commit()

        flash("Project created.", "success")
        return redirect(url_for("main.projects"))

    return render_template("create_project.html")


@main.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
@project_access_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Project name is required.", "danger")
            return render_template("create_project.html", project=project, is_edit=True)

        project.name = name
        project.description = description
        db.session.commit()

        flash("Project updated.", "success")
        return redirect(url_for("main.project_detail", project_id=project.id))

    return render_template("create_project.html", project=project, is_edit=True)


@main.route("/projects/<int:project_id>/delete", methods=["POST"])
@project_access_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()

    flash("Project deleted.", "success")
    return redirect(url_for("main.projects"))


@main.route("/projects/<int:project_id>/characters")
@project_access_required
def characters(project_id):
    project = Project.query.get_or_404(project_id)
    project_characters = Character.query.filter_by(project_id=project.id).order_by(
        Character.name.asc()
    ).all()
    character_stats = {
        "total": len(project_characters),
        "alive": sum(character.status == "alive" for character in project_characters),
        "dead": sum(character.status == "dead" for character in project_characters),
        "unknown": sum(character.status == "unknown" for character in project_characters),
    }
    return render_template(
        "characters.html",
        project=project,
        characters=project_characters,
        character_stats=character_stats,
    )


@main.route("/projects/<int:project_id>/characters/create", methods=["GET", "POST"])
@project_access_required
def create_character(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "unknown")
        birth_year = parse_optional_int(request.form.get("birth_year", ""))
        death_year = parse_optional_int(request.form.get("death_year", ""))

        if not name:
            flash("Character name is required.", "danger")
            return render_template("create_character.html", project=project)

        if status not in ["alive", "dead", "unknown"]:
            status = "unknown"

        character = Character(
            project=project,
            name=name,
            description=description,
            status=status,
            birth_year=birth_year,
            death_year=death_year,
        )
        db.session.add(character)
        db.session.commit()

        flash("Character created.", "success")
        return redirect(url_for("main.characters", project_id=project.id))

    return render_template("create_character.html", project=project)


@main.route(
    "/projects/<int:project_id>/characters/<int:character_id>/edit",
    methods=["GET", "POST"],
)
@project_access_required
def edit_character(project_id, character_id):
    project = Project.query.get_or_404(project_id)
    character = get_project_character(project.id, character_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "unknown")
        birth_year = parse_optional_int(request.form.get("birth_year", ""))
        death_year = parse_optional_int(request.form.get("death_year", ""))

        if not name:
            flash("Character name is required.", "danger")
            return render_template(
                "create_character.html",
                project=project,
                character=character,
                is_edit=True,
            )

        if status not in ["alive", "dead", "unknown"]:
            status = "unknown"

        character.name = name
        character.description = description
        character.status = status
        character.birth_year = birth_year
        character.death_year = death_year
        db.session.commit()

        flash("Character updated.", "success")
        return redirect(url_for("main.characters", project_id=project.id))

    return render_template(
        "create_character.html",
        project=project,
        character=character,
        is_edit=True,
    )


@main.route(
    "/projects/<int:project_id>/characters/<int:character_id>/delete",
    methods=["POST"],
)
@project_access_required
def delete_character(project_id, character_id):
    project = Project.query.get_or_404(project_id)
    character = get_project_character(project.id, character_id)
    delete_relations_for_entity(project.id, "character", character.id)
    db.session.delete(character)
    db.session.commit()

    flash("Character deleted.", "success")
    return redirect(url_for("main.characters", project_id=project.id))


@main.route("/projects/<int:project_id>/characters/bulk-delete", methods=["POST"])
@project_access_required
def bulk_delete_characters(project_id):
    project = Project.query.get_or_404(project_id)
    character_ids = parse_id_list(request.form.getlist("character_ids"))

    if not character_ids:
        flash("No characters selected.", "warning")
        return redirect(url_for("main.characters", project_id=project.id))

    characters_to_delete = Character.query.filter(
        Character.project_id == project.id,
        Character.id.in_(character_ids),
    ).all()

    for character in characters_to_delete:
        delete_relations_for_entity(project.id, "character", character.id)
        db.session.delete(character)

    db.session.commit()
    flash("Selected characters deleted.", "success")
    return redirect(url_for("main.characters", project_id=project.id))


@main.route("/projects/<int:project_id>/characters/delete-all", methods=["POST"])
@project_access_required
def delete_all_characters(project_id):
    project = Project.query.get_or_404(project_id)
    characters_to_delete = Character.query.filter_by(project_id=project.id).all()

    for character in characters_to_delete:
        delete_relations_for_entity(project.id, "character", character.id)
        db.session.delete(character)

    db.session.commit()
    flash("All characters deleted.", "success")
    return redirect(url_for("main.characters", project_id=project.id))


@main.route("/projects/<int:project_id>/factions")
@project_access_required
def factions(project_id):
    project = Project.query.get_or_404(project_id)
    project_factions = Faction.query.filter_by(project_id=project.id).order_by(
        Faction.name.asc()
    ).all()
    faction_stats = {
        "total": len(project_factions),
        "active": sum(faction.destroyed_year is None for faction in project_factions),
        "destroyed": sum(faction.destroyed_year is not None for faction in project_factions),
    }
    return render_template(
        "factions.html",
        project=project,
        factions=project_factions,
        faction_stats=faction_stats,
    )


@main.route("/projects/<int:project_id>/factions/create", methods=["GET", "POST"])
@project_access_required
def create_faction(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        created_year = parse_optional_int(request.form.get("created_year", ""))
        destroyed_year = parse_optional_int(request.form.get("destroyed_year", ""))

        if not name:
            flash("Faction name is required.", "danger")
            return render_template("create_faction.html", project=project)

        faction = Faction(
            project=project,
            name=name,
            description=description,
            created_year=created_year,
            destroyed_year=destroyed_year,
        )
        db.session.add(faction)
        db.session.commit()

        flash("Faction created.", "success")
        return redirect(url_for("main.factions", project_id=project.id))

    return render_template("create_faction.html", project=project)


@main.route(
    "/projects/<int:project_id>/factions/<int:faction_id>/edit",
    methods=["GET", "POST"],
)
@project_access_required
def edit_faction(project_id, faction_id):
    project = Project.query.get_or_404(project_id)
    faction = get_project_faction(project.id, faction_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        created_year = parse_optional_int(request.form.get("created_year", ""))
        destroyed_year = parse_optional_int(request.form.get("destroyed_year", ""))

        if not name:
            flash("Faction name is required.", "danger")
            return render_template(
                "edit_faction.html",
                project=project,
                faction=faction,
            )

        faction.name = name
        faction.description = description
        faction.created_year = created_year
        faction.destroyed_year = destroyed_year
        db.session.commit()

        flash("Faction updated.", "success")
        return redirect(url_for("main.factions", project_id=project.id))

    return render_template("edit_faction.html", project=project, faction=faction)


@main.route(
    "/projects/<int:project_id>/factions/<int:faction_id>/delete",
    methods=["POST"],
)
@project_access_required
def delete_faction(project_id, faction_id):
    project = Project.query.get_or_404(project_id)
    faction = get_project_faction(project.id, faction_id)
    delete_relations_for_entity(project.id, "faction", faction.id)
    db.session.delete(faction)
    db.session.commit()

    flash("Faction deleted.", "success")
    return redirect(url_for("main.factions", project_id=project.id))


@main.route("/projects/<int:project_id>/factions/bulk-delete", methods=["POST"])
@project_access_required
def bulk_delete_factions(project_id):
    project = Project.query.get_or_404(project_id)
    faction_ids = parse_id_list(request.form.getlist("faction_ids"))

    if not faction_ids:
        flash("No factions selected.", "warning")
        return redirect(url_for("main.factions", project_id=project.id))

    factions_to_delete = Faction.query.filter(
        Faction.project_id == project.id,
        Faction.id.in_(faction_ids),
    ).all()

    for faction in factions_to_delete:
        delete_relations_for_entity(project.id, "faction", faction.id)
        db.session.delete(faction)

    db.session.commit()
    flash("Selected factions deleted.", "success")
    return redirect(url_for("main.factions", project_id=project.id))


@main.route("/projects/<int:project_id>/factions/delete-all", methods=["POST"])
@project_access_required
def delete_all_factions(project_id):
    project = Project.query.get_or_404(project_id)
    factions_to_delete = Faction.query.filter_by(project_id=project.id).all()

    for faction in factions_to_delete:
        delete_relations_for_entity(project.id, "faction", faction.id)
        db.session.delete(faction)

    db.session.commit()
    flash("All factions deleted.", "success")
    return redirect(url_for("main.factions", project_id=project.id))


@main.route("/projects/<int:project_id>/events")
@project_access_required
def events(project_id):
    project = Project.query.get_or_404(project_id)
    project_events = Event.query.filter_by(project_id=project.id).order_by(
        Event.year.asc(),
        Event.name.asc(),
    ).all()
    event_years = [event.year for event in project_events if event.year is not None]
    event_stats = {
        "total": len(project_events),
        "earliest": min(event_years) if event_years else None,
        "latest": max(event_years) if event_years else None,
    }
    return render_template(
        "events.html",
        project=project,
        events=project_events,
        event_stats=event_stats,
    )


@main.route("/projects/<int:project_id>/events/create", methods=["GET", "POST"])
@project_access_required
def create_event(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        year = parse_optional_int(request.form.get("year", ""))
        location = request.form.get("location", "").strip()

        if not name:
            flash("Event name is required.", "danger")
            return render_template("create_event.html", project=project)

        event = Event(
            project=project,
            name=name,
            description=description,
            year=year,
            location=location,
        )
        db.session.add(event)
        db.session.commit()

        flash("Event created.", "success")
        return redirect(url_for("main.events", project_id=project.id))

    return render_template("create_event.html", project=project)


@main.route(
    "/projects/<int:project_id>/events/<int:event_id>/edit",
    methods=["GET", "POST"],
)
@project_access_required
def edit_event(project_id, event_id):
    project = Project.query.get_or_404(project_id)
    event = get_project_event(project.id, event_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        year = parse_optional_int(request.form.get("year", ""))
        location = request.form.get("location", "").strip()

        if not name:
            flash("Event name is required.", "danger")
            return render_template("edit_event.html", project=project, event=event)

        event.name = name
        event.description = description
        event.year = year
        event.location = location
        db.session.commit()

        flash("Event updated.", "success")
        return redirect(url_for("main.events", project_id=project.id))

    return render_template("edit_event.html", project=project, event=event)


@main.route(
    "/projects/<int:project_id>/events/<int:event_id>/delete",
    methods=["POST"],
)
@project_access_required
def delete_event(project_id, event_id):
    project = Project.query.get_or_404(project_id)
    event = get_project_event(project.id, event_id)
    delete_relations_for_entity(project.id, "event", event.id)
    db.session.delete(event)
    db.session.commit()

    flash("Event deleted.", "success")
    return redirect(url_for("main.events", project_id=project.id))


@main.route("/projects/<int:project_id>/events/bulk-delete", methods=["POST"])
@project_access_required
def bulk_delete_events(project_id):
    project = Project.query.get_or_404(project_id)
    event_ids = parse_id_list(request.form.getlist("event_ids"))

    if not event_ids:
        flash("No events selected.", "warning")
        return redirect(url_for("main.events", project_id=project.id))

    events_to_delete = Event.query.filter(
        Event.project_id == project.id,
        Event.id.in_(event_ids),
    ).all()

    for event in events_to_delete:
        delete_relations_for_entity(project.id, "event", event.id)
        db.session.delete(event)

    db.session.commit()
    flash("Selected events deleted.", "success")
    return redirect(url_for("main.events", project_id=project.id))


@main.route("/projects/<int:project_id>/events/delete-all", methods=["POST"])
@project_access_required
def delete_all_events(project_id):
    project = Project.query.get_or_404(project_id)
    events_to_delete = Event.query.filter_by(project_id=project.id).all()

    for event in events_to_delete:
        delete_relations_for_entity(project.id, "event", event.id)
        db.session.delete(event)

    db.session.commit()
    flash("All events deleted.", "success")
    return redirect(url_for("main.events", project_id=project.id))


@main.route("/projects/<int:project_id>/relations")
@project_access_required
def relations(project_id):
    project = Project.query.get_or_404(project_id)
    project_relations = Relation.query.filter_by(project_id=project.id).order_by(
        Relation.id.desc()
    ).all()
    relation_stats = {
        "total": len(project_relations),
        "characters": sum(
            relation.source_type == "character" or relation.target_type == "character"
            for relation in project_relations
        ),
        "factions": sum(
            relation.source_type == "faction" or relation.target_type == "faction"
            for relation in project_relations
        ),
        "events": sum(
            relation.source_type == "event" or relation.target_type == "event"
            for relation in project_relations
        ),
    }
    relation_rows = [
        {
            "relation": relation,
            "source_name": resolve_entity_name(
                project.id,
                relation.source_type,
                relation.source_id,
            ),
            "target_name": resolve_entity_name(
                project.id,
                relation.target_type,
                relation.target_id,
            ),
        }
        for relation in project_relations
    ]
    return render_template(
        "relations.html",
        project=project,
        relation_rows=relation_rows,
        relation_stats=relation_stats,
        relation_type_labels=RELATION_TYPE_LABELS,
    )


@main.route("/projects/<int:project_id>/relations/create", methods=["GET", "POST"])
@project_access_required
def create_relation(project_id):
    project = Project.query.get_or_404(project_id)
    entity_choices = get_entity_choices(project.id)
    grouped_entity_choices = get_grouped_entity_choices(project.id)

    if request.method == "POST":
        source = parse_entity_choice(request.form.get("source_entity", ""))
        target = parse_entity_choice(request.form.get("target_entity", ""))
        relation_type = request.form.get("relation_type", "")
        description = request.form.get("description", "").strip()

        if not source or not target or relation_type not in RELATION_TYPES:
            flash("Source, relation type, and target are required.", "danger")
            return render_template(
                "create_relation.html",
                project=project,
                entity_choices=entity_choices,
                grouped_entity_choices=grouped_entity_choices,
                relation_types=RELATION_TYPES,
                relation_type_labels=RELATION_TYPE_LABELS,
                relation_type_helpers=RELATION_TYPE_HELPERS,
            )

        source_type, source_id = source
        target_type, target_id = target
        if not entity_exists(project.id, source_type, source_id) or not entity_exists(
            project.id,
            target_type,
            target_id,
        ):
            flash("Selected entities must belong to this project.", "danger")
            return render_template(
                "create_relation.html",
                project=project,
                entity_choices=entity_choices,
                grouped_entity_choices=grouped_entity_choices,
                relation_types=RELATION_TYPES,
                relation_type_labels=RELATION_TYPE_LABELS,
                relation_type_helpers=RELATION_TYPE_HELPERS,
            )

        relation = Relation(
            project=project,
            source_type=source_type,
            source_id=source_id,
            relation_type=relation_type,
            target_type=target_type,
            target_id=target_id,
            description=description,
        )
        db.session.add(relation)
        db.session.commit()

        flash("Relation created.", "success")
        return redirect(url_for("main.relations", project_id=project.id))

    return render_template(
        "create_relation.html",
        project=project,
        entity_choices=entity_choices,
        grouped_entity_choices=grouped_entity_choices,
        relation_types=RELATION_TYPES,
        relation_type_labels=RELATION_TYPE_LABELS,
        relation_type_helpers=RELATION_TYPE_HELPERS,
    )


@main.route("/projects/<int:project_id>/relations/bulk-delete", methods=["POST"])
@project_access_required
def bulk_delete_relations(project_id):
    project = Project.query.get_or_404(project_id)
    relation_ids = parse_id_list(request.form.getlist("relation_ids"))

    if not relation_ids:
        flash("No relations selected.", "warning")
        return redirect(url_for("main.relations", project_id=project.id))

    relations_to_delete = Relation.query.filter(
        Relation.project_id == project.id,
        Relation.id.in_(relation_ids),
    ).all()

    for relation in relations_to_delete:
        db.session.delete(relation)

    db.session.commit()
    flash("Selected relations deleted.", "success")
    return redirect(url_for("main.relations", project_id=project.id))


@main.route("/projects/<int:project_id>/relations/delete-all", methods=["POST"])
@project_access_required
def delete_all_relations(project_id):
    project = Project.query.get_or_404(project_id)
    Relation.query.filter_by(project_id=project.id).delete()
    db.session.commit()

    flash("All relations deleted.", "success")
    return redirect(url_for("main.relations", project_id=project.id))


@main.route(
    "/projects/<int:project_id>/relations/<int:relation_id>/edit",
    methods=["GET", "POST"],
)
@project_access_required
def edit_relation(project_id, relation_id):
    project = Project.query.get_or_404(project_id)
    relation = get_project_relation(project.id, relation_id)
    entity_choices = get_entity_choices(project.id)
    grouped_entity_choices = get_grouped_entity_choices(project.id)

    if request.method == "POST":
        source = parse_entity_choice(request.form.get("source_entity", ""))
        target = parse_entity_choice(request.form.get("target_entity", ""))
        relation_type = request.form.get("relation_type", "")
        description = request.form.get("description", "").strip()

        if not source or not target or relation_type not in RELATION_TYPES:
            flash("Source, relation type, and target are required.", "danger")
            return render_template(
                "edit_relation.html",
                project=project,
                relation=relation,
                entity_choices=entity_choices,
                grouped_entity_choices=grouped_entity_choices,
                relation_types=RELATION_TYPES,
                relation_type_labels=RELATION_TYPE_LABELS,
                relation_type_helpers=RELATION_TYPE_HELPERS,
            )

        source_type, source_id = source
        target_type, target_id = target
        if not entity_exists(project.id, source_type, source_id) or not entity_exists(
            project.id,
            target_type,
            target_id,
        ):
            flash("Selected entities must belong to this project.", "danger")
            return render_template(
                "edit_relation.html",
                project=project,
                relation=relation,
                entity_choices=entity_choices,
                grouped_entity_choices=grouped_entity_choices,
                relation_types=RELATION_TYPES,
                relation_type_labels=RELATION_TYPE_LABELS,
                relation_type_helpers=RELATION_TYPE_HELPERS,
            )

        relation.source_type = source_type
        relation.source_id = source_id
        relation.relation_type = relation_type
        relation.target_type = target_type
        relation.target_id = target_id
        relation.description = description
        db.session.commit()

        flash("Relation updated.", "success")
        return redirect(url_for("main.relations", project_id=project.id))

    return render_template(
        "edit_relation.html",
        project=project,
        relation=relation,
        entity_choices=entity_choices,
        grouped_entity_choices=grouped_entity_choices,
        relation_types=RELATION_TYPES,
        relation_type_labels=RELATION_TYPE_LABELS,
        relation_type_helpers=RELATION_TYPE_HELPERS,
    )


@main.route(
    "/projects/<int:project_id>/relations/<int:relation_id>/delete",
    methods=["POST"],
)
@project_access_required
def delete_relation(project_id, relation_id):
    project = Project.query.get_or_404(project_id)
    relation = get_project_relation(project.id, relation_id)
    db.session.delete(relation)
    db.session.commit()

    flash("Relation deleted.", "success")
    return redirect(url_for("main.relations", project_id=project.id))


def get_project_character(project_id, character_id):
    return Character.query.filter_by(id=character_id, project_id=project_id).first_or_404()


def get_project_faction(project_id, faction_id):
    return Faction.query.filter_by(id=faction_id, project_id=project_id).first_or_404()


def get_project_event(project_id, event_id):
    return Event.query.filter_by(id=event_id, project_id=project_id).first_or_404()


def get_project_relation(project_id, relation_id):
    return Relation.query.filter_by(id=relation_id, project_id=project_id).first_or_404()


def get_entity_choices(project_id):
    choices = []
    characters = Character.query.filter_by(project_id=project_id).order_by(
        Character.name.asc()
    )
    factions = Faction.query.filter_by(project_id=project_id).order_by(Faction.name.asc())
    events = Event.query.filter_by(project_id=project_id).order_by(Event.name.asc())

    for character in characters:
        choices.append(
            {
                "value": f"character:{character.id}",
                "label": f"character: {character.name}",
            }
        )
    for faction in factions:
        choices.append(
            {
                "value": f"faction:{faction.id}",
                "label": f"faction: {faction.name}",
            }
        )
    for event in events:
        choices.append(
            {
                "value": f"event:{event.id}",
                "label": f"event: {event.name}",
            }
        )

    return choices


def get_grouped_entity_choices(project_id):
    grouped_choices = {
        "Characters": [],
        "Factions": [],
        "Events": [],
    }

    characters = Character.query.filter_by(project_id=project_id).order_by(
        Character.name.asc()
    )
    factions = Faction.query.filter_by(project_id=project_id).order_by(Faction.name.asc())
    events = Event.query.filter_by(project_id=project_id).order_by(Event.name.asc())

    for character in characters:
        grouped_choices["Characters"].append(
            {
                "value": f"character:{character.id}",
                "label": character.name,
            }
        )
    for faction in factions:
        grouped_choices["Factions"].append(
            {
                "value": f"faction:{faction.id}",
                "label": faction.name,
            }
        )
    for event in events:
        grouped_choices["Events"].append(
            {
                "value": f"event:{event.id}",
                "label": event.name,
            }
        )

    return grouped_choices


def resolve_entity_name(project_id, entity_type, entity_id):
    entity = get_entity(project_id, entity_type, entity_id)
    if not entity:
        return f"{entity_type}: Unknown"
    return entity.name


def get_entity(project_id, entity_type, entity_id):
    model_by_type = {
        "character": Character,
        "faction": Faction,
        "event": Event,
    }
    model = model_by_type.get(entity_type)
    if not model:
        return None
    return model.query.filter_by(id=entity_id, project_id=project_id).first()


def entity_exists(project_id, entity_type, entity_id):
    return get_entity(project_id, entity_type, entity_id) is not None


def build_project_export(project):
    return {
        "app_name": "Zirel",
        "export_version": "1.0",
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": isoformat_or_none(project.created_at),
        },
        "characters": [
            {
                "id": character.id,
                "name": character.name,
                "description": character.description,
                "status": character.status,
                "birth_year": character.birth_year,
                "death_year": character.death_year,
            }
            for character in project.characters
        ],
        "factions": [
            {
                "id": faction.id,
                "name": faction.name,
                "description": faction.description,
                "created_year": faction.created_year,
                "destroyed_year": faction.destroyed_year,
            }
            for faction in project.factions
        ],
        "events": [
            {
                "id": event.id,
                "name": event.name,
                "description": event.description,
                "year": event.year,
                "location": event.location,
            }
            for event in project.events
        ],
        "relations": [
            {
                "id": relation.id,
                "source_type": relation.source_type,
                "source_id": relation.source_id,
                "source_label": resolve_export_entity_label(
                    project.id,
                    relation.source_type,
                    relation.source_id,
                ),
                "relation_type": relation.relation_type,
                "target_type": relation.target_type,
                "target_id": relation.target_id,
                "target_label": resolve_export_entity_label(
                    project.id,
                    relation.target_type,
                    relation.target_id,
                ),
                "description": relation.description,
            }
            for relation in project.relations
        ],
        "warnings": analyze_project(project),
    }


def resolve_export_entity_label(project_id, entity_type, entity_id):
    entity = get_entity(project_id, entity_type, entity_id)
    if not entity:
        return "Missing entity"
    return entity.name


def build_export_filename(project_name):
    slug = re.sub(r"[^a-z0-9]+", "-", project_name.lower()).strip("-")
    if not slug:
        slug = "project"
    return f"{slug}-export.json"


def isoformat_or_none(value):
    if value is None:
        return None
    return value.isoformat()


def validate_project_import(export_data):
    if not isinstance(export_data, dict):
        return "Invalid JSON. The file must contain a Zirel export object."

    app_name = export_data.get("app_name")
    if app_name is not None and app_name != "Zirel":
        return "Invalid JSON. This does not look like a Zirel export."

    project_data = export_data.get("project")
    if not isinstance(project_data, dict):
        return "Missing project data."

    for key in ["characters", "factions", "events", "relations"]:
        if key in export_data and not isinstance(export_data[key], list):
            return f"Invalid JSON. {key} must be a list."

    return None


def create_project_from_import(export_data):
    project_data = export_data["project"]
    project_name = str(project_data.get("name") or "Imported Project").strip()
    if not project_name:
        project_name = "Imported Project"

    project = Project(
        user=current_user,
        name=f"{project_name} (Imported)",
        description=project_data.get("description") or "",
    )
    db.session.add(project)
    db.session.flush()

    id_maps = {
        "character": {},
        "faction": {},
        "event": {},
    }

    import_characters(project, export_data.get("characters", []), id_maps["character"])
    import_factions(project, export_data.get("factions", []), id_maps["faction"])
    import_events(project, export_data.get("events", []), id_maps["event"])
    import_relations(project, export_data.get("relations", []), id_maps)

    return project


def import_characters(project, characters, id_map):
    for item in characters:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            continue

        status = item.get("status") or "unknown"
        if status not in ["alive", "dead", "unknown"]:
            status = "unknown"

        character = Character(
            project=project,
            name=name,
            description=item.get("description") or "",
            status=status,
            birth_year=coerce_optional_int(item.get("birth_year")),
            death_year=coerce_optional_int(item.get("death_year")),
        )
        db.session.add(character)
        db.session.flush()
        remember_imported_id(id_map, item.get("id"), character.id)


def import_factions(project, factions, id_map):
    for item in factions:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            continue

        faction = Faction(
            project=project,
            name=name,
            description=item.get("description") or "",
            created_year=coerce_optional_int(item.get("created_year")),
            destroyed_year=coerce_optional_int(item.get("destroyed_year")),
        )
        db.session.add(faction)
        db.session.flush()
        remember_imported_id(id_map, item.get("id"), faction.id)


def import_events(project, events, id_map):
    for item in events:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            continue

        event = Event(
            project=project,
            name=name,
            description=item.get("description") or "",
            year=coerce_optional_int(item.get("year")),
            location=item.get("location") or "",
        )
        db.session.add(event)
        db.session.flush()
        remember_imported_id(id_map, item.get("id"), event.id)


def import_relations(project, relations, id_maps):
    for item in relations:
        if not isinstance(item, dict):
            continue

        source_type = item.get("source_type")
        target_type = item.get("target_type")
        relation_type = item.get("relation_type")

        if source_type not in id_maps or target_type not in id_maps:
            continue
        if relation_type not in RELATION_TYPES:
            continue

        source_id = get_imported_id(id_maps[source_type], item.get("source_id"))
        target_id = get_imported_id(id_maps[target_type], item.get("target_id"))
        if source_id is None or target_id is None:
            continue

        relation = Relation(
            project=project,
            source_type=source_type,
            source_id=source_id,
            relation_type=relation_type,
            target_type=target_type,
            target_id=target_id,
            description=item.get("description") or "",
        )
        db.session.add(relation)


def remember_imported_id(id_map, old_id, new_id):
    if old_id is None:
        return
    id_map[old_id] = new_id
    id_map[str(old_id)] = new_id


def get_imported_id(id_map, old_id):
    if old_id in id_map:
        return id_map[old_id]
    return id_map.get(str(old_id))


def coerce_optional_int(value):
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_entity_choice(value):
    if ":" not in value:
        return None
    entity_type, entity_id = value.split(":", 1)
    if entity_type not in ["character", "faction", "event"]:
        return None
    try:
        return entity_type, int(entity_id)
    except ValueError:
        return None


def parse_id_list(values):
    ids = []
    for value in values:
        try:
            ids.append(int(value))
        except ValueError:
            continue
    return ids


def delete_relations_for_entity(project_id, entity_type, entity_id):
    Relation.query.filter(
        Relation.project_id == project_id,
        (
            (Relation.source_type == entity_type)
            & (Relation.source_id == entity_id)
        )
        | (
            (Relation.target_type == entity_type)
            & (Relation.target_id == entity_id)
        ),
    ).delete(synchronize_session=False)


def build_graph_node_id(entity_type, entity_id):
    return f"{entity_type}-{entity_id}"


def parse_optional_int(value):
    value = value.strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None
