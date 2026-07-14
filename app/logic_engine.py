from app.models import Character, Event, Faction


STRONGLY_MUTUAL_TYPES = {
    "allied_with",
    "friends_with",
    "siblings_with",
    "married_to",
    "rivals_with",
    "enemies_with",
    "partners_with",
    "trades_with",
    "at_war_with",
    "related_to",
    "connected_to",
}

INVERSE_RELATION_TYPES = {
    "parent_of", "child_of", "teacher_of", "student_of", "mentor_of", "mentored_by",
    "leader_of", "led_by", "member_of", "has_member", "rules", "ruled_by", "owns",
    "owned_by", "serves", "served_by", "employs", "employed_by", "created", "created_by",
    "located_in", "contains", "participated_in", "has_participant", "descendant_of",
    "ancestor_of", "successor_to", "predecessor_to", "founded", "founded_by", "born_in",
    "birthplace_of", "died_in", "death_place_of", "precedes", "follows", "part_of",
    "includes", "guardian_of", "protected_by",
}


def analyze_project(project):
    warnings = []
    relations = list(project.relations)
    relation_keys = set()
    for relation in relations:
        relation_keys.add(
            (
                relation.source_type,
                relation.source_id,
                relation.relation_type,
                relation.target_type,
                relation.target_id,
            )
        )
        if relation.direction_mode == "mutual":
            relation_keys.add(
                (
                    relation.target_type,
                    relation.target_id,
                    relation.relation_type,
                    relation.source_type,
                    relation.source_id,
                )
            )
        elif relation.direction_mode == "inverse" and relation.inverse_relation_type:
            relation_keys.add(
                (
                    relation.target_type,
                    relation.target_id,
                    relation.inverse_relation_type,
                    relation.source_type,
                    relation.source_id,
                )
            )

    for relation in relations:
        source = resolve_entity(project, relation.source_type, relation.source_id)
        target = resolve_entity(project, relation.target_type, relation.target_id)

        if relation.relation_type == "participated_in":
            check_participation_timeline(warnings, source, target)

        if (
            relation.source_type == "character"
            and relation.target_type == "character"
            and relation.relation_type == "hates"
        ):
            reverse_hate = (
                "character",
                relation.target_id,
                "hates",
                "character",
                relation.source_id,
            )
            if reverse_hate not in relation_keys and source and target:
                warnings.append(
                    build_warning(
                        warning_type="one_sided_hostility",
                        category="Relationships",
                        severity="low",
                        title="Hostility is one-sided",
                        message=f"{source.name} hates {target.name}, but {target.name} does not hate {source.name}.",
                        explanation="A hatred relation exists in only one direction. This may be intentional, but mutual hostility often needs an opposite relation to make the conflict clear.",
                        suggestions=[
                            f"Add a hates relation from {target.name} to {source.name}.",
                            "If the hostility is intentionally one-sided, explain why in the relation description.",
                            "Consider whether another relation type better describes the target's response.",
                        ],
                    )
                )

        if relation.relation_type in STRONGLY_MUTUAL_TYPES and relation.direction_mode == "one_way" and source and target:
            warnings.append(
                build_warning(
                    warning_type="mutual_type_is_one_way",
                    category="Relationships",
                    severity="low",
                    title="Mutual relation is stored as one-way",
                    message=f"{source.name} is {relation.relation_type.replace('_', ' ')} {target.name}, but the relation is visible in one direction only.",
                    explanation="This relation type usually describes a shared connection. One-way may be intentional, but it can make the graph and entity views imply an uneven relationship.",
                    suggestions=[
                        "Change the direction mode to Mutual if both sides share the same relation.",
                        "Keep One-way if the asymmetry is intentional and explain it in the relation notes.",
                        "Use an inverse pair if each side describes the connection differently.",
                    ],
                )
            )

        if relation.relation_type in INVERSE_RELATION_TYPES and relation.direction_mode == "mutual" and source and target:
            warnings.append(
                build_warning(
                    warning_type="directional_type_is_mutual",
                    category="Relationships",
                    severity="medium",
                    title="Directional relation is marked mutual",
                    message=f"{source.name} and {target.name} share the same “{relation.relation_type.replace('_', ' ')}” label in both directions.",
                    explanation="This type normally changes meaning when read backwards. Mutual mode can incorrectly describe both entities as having the same role.",
                    suggestions=[
                        "Change the direction mode to Inverse pair.",
                        "Add the correct reverse label, such as parent/child or teacher/student.",
                        "Keep Mutual only if this custom world intentionally gives both sides the same role.",
                    ],
                )
            )

    reciprocal_seen = set()
    for relation in relations:
        if relation.direction_mode != "one_way":
            continue
        reverse = next(
            (
                candidate
                for candidate in relations
                if candidate.id != relation.id
                and candidate.direction_mode == "one_way"
                and candidate.relation_type == relation.relation_type
                and candidate.source_type == relation.target_type
                and candidate.source_id == relation.target_id
                and candidate.target_type == relation.source_type
                and candidate.target_id == relation.source_id
            ),
            None,
        )
        pair = tuple(sorted((relation.id, reverse.id))) if reverse else None
        if not reverse or pair in reciprocal_seen:
            continue
        reciprocal_seen.add(pair)
        source = resolve_entity(project, relation.source_type, relation.source_id)
        target = resolve_entity(project, relation.target_type, relation.target_id)
        if source and target:
            warnings.append(
                build_warning(
                    warning_type="duplicate_reciprocal_relations",
                    category="Structure",
                    severity="low",
                    title="Two one-way relations can be simplified",
                    message=f"{source.name} and {target.name} have matching “{relation.relation_type.replace('_', ' ')}” relations in both directions.",
                    explanation="Two separate rows describe the same symmetric connection. A single Mutual relation is easier to edit, delete, export, and inspect.",
                    suggestions=[
                        "Keep one relation, change it to Mutual, and delete the duplicate reverse row.",
                        "Keep both one-way rows if their notes or meanings are intentionally different.",
                    ],
                )
            )

    check_internal_faction_conflicts(warnings, project)
    return warnings


def check_participation_timeline(warnings, source, target):
    if not source or not target or not isinstance(target, Event) or target.year is None:
        return

    if isinstance(source, Character):
        if source.death_year is not None and source.death_year < target.year:
            warnings.append(
                build_warning(
                    warning_type="dead_character_after_death",
                    category="Timeline",
                    severity="high",
                    title="Dead character appears after death",
                    message=f"{source.name} died in {source.death_year} but participates in {target.name} in {target.year}.",
                    explanation="A character appears in an event that happens after their recorded death year. This may break the internal chronology of the world.",
                    suggestions=[
                        "Change the character's death year.",
                        "Change the event year.",
                        "If this is intentional, explain it in the relation description, for example: ghost, flashback, memory, legend, or resurrection.",
                    ],
                )
            )

        if source.birth_year is not None and source.birth_year > target.year:
            warnings.append(
                build_warning(
                    warning_type="character_before_birth",
                    category="Timeline",
                    severity="high",
                    title="Character appears before birth",
                    message=f"{source.name} was born in {source.birth_year} but participates in {target.name} in {target.year}.",
                    explanation="A character is linked to an event that occurs before their recorded birth year. This usually signals a timeline mismatch.",
                    suggestions=[
                        "Change the character's birth year.",
                        "Change the event year.",
                        "If the relation is symbolic or ancestral, clarify that in the relation description.",
                    ],
                )
            )

    if isinstance(source, Faction):
        if source.destroyed_year is not None and source.destroyed_year < target.year:
            warnings.append(
                build_warning(
                    warning_type="destroyed_faction_after_destruction",
                    category="Timeline",
                    severity="high",
                    title="Destroyed faction appears after destruction",
                    message=f"{source.name} was destroyed in {source.destroyed_year} but participates in {target.name} in {target.year}.",
                    explanation="A faction is connected to an event that happens after the faction's destroyed year. This may make the political or historical timeline inconsistent.",
                    suggestions=[
                        "Change the faction's destroyed year.",
                        "Change the event year.",
                        "If remnants, heirs, or successor groups are involved, create a separate faction or explain it in the relation description.",
                    ],
                )
            )


def check_internal_faction_conflicts(warnings, project):
    member_relations = [
        relation
        for relation in project.relations
        if relation.source_type == "character"
        and relation.relation_type == "member_of"
        and relation.target_type == "faction"
    ]
    loyalty_relations = [
        relation
        for relation in project.relations
        if relation.source_type == "faction"
        and relation.relation_type == "loyal_to"
        and relation.target_type == "character"
    ]
    hate_keys = {
        (relation.source_id, relation.target_id)
        for relation in project.relations
        if relation.source_type == "character"
        and relation.relation_type == "hates"
        and relation.target_type == "character"
    }

    for member_relation in member_relations:
        for loyalty_relation in loyalty_relations:
            if member_relation.target_id != loyalty_relation.source_id:
                continue

            character_id = member_relation.source_id
            leader_id = loyalty_relation.target_id
            if (character_id, leader_id) not in hate_keys:
                continue

            character = resolve_entity(project, "character", character_id)
            faction = resolve_entity(project, "faction", member_relation.target_id)
            leader = resolve_entity(project, "character", leader_id)
            if not character or not faction or not leader:
                continue

            warnings.append(
                build_warning(
                    warning_type="internal_faction_conflict",
                    category="Politics",
                    severity="medium",
                    title="Faction member hates faction's loyalty target",
                    message=f"{character.name} is a member of {faction.name}, but {faction.name} is loyal to {leader.name}, whom {character.name} hates.",
                    explanation="A character belongs to a faction whose loyalty points toward someone that character hates. This may be a rich source of drama, but it can also indicate a missing explanation.",
                    suggestions=[
                        "Add notes explaining why the character remains in the faction.",
                        "Change the character's faction membership or hatred relation if one is outdated.",
                        "Add another relation that explains the tension, such as coercion, rivalry, secret loyalty, or political necessity.",
                    ],
                )
            )


def build_warning(
    warning_type,
    category,
    severity,
    title,
    message,
    explanation,
    suggestions,
):
    return {
        "type": warning_type,
        "category": category,
        "severity": severity,
        "title": title,
        "message": message,
        "explanation": explanation,
        "suggestions": suggestions,
    }


def resolve_entity(project, entity_type, entity_id):
    if entity_type == "character":
        return find_by_id(project.characters, entity_id)
    if entity_type == "faction":
        return find_by_id(project.factions, entity_id)
    if entity_type == "event":
        return find_by_id(project.events, entity_id)
    return None


def find_by_id(entities, entity_id):
    for entity in entities:
        if entity.id == entity_id:
            return entity
    return None
