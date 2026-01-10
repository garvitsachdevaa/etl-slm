# scripts/template_rules.py

TEMPLATE_RULES = {
    "template_01_explicit_relation": {
        "allow_relations": True,
        "allow_abstain": False,
        "min_confidence": 0.9,
        "max_confidence": 1.0,
    },
    "template_02_implicit_relation": {
        "allow_relations": True,
        "allow_abstain": True,
        "min_confidence": 0.6,
        "max_confidence": 0.85,
    },
    "template_03_abstain": {
        "allow_relations": False,
        "allow_abstain": True,
    },
    "template_04_mixed_format": {
        "allow_relations": True,
        "allow_abstain": True,
        "min_confidence": 0.6,
        "max_confidence": 1.0,
    },
    "template_05_roles_attributes": {
        "allow_relations": False,
        "allow_abstain": True,
    },
    "template_06_table_like": {
        "allow_relations": True,
        "allow_abstain": True,
        "min_confidence": 0.7,
        "max_confidence": 1.0,
    },
    "template_07_long_context": {
        "allow_relations": True,
        "allow_abstain": True,
        "min_confidence": 0.7,
        "max_confidence": 1.0,
    },
    "template_08_visual_context": {
        "allow_relations": True,
        "allow_abstain": True,
        "min_confidence": 0.7,
        "max_confidence": 1.0,
    },
    "template_09_noisy_ocr": {
        "allow_relations": True,
        "allow_abstain": True,
        "min_confidence": 0.5,
        "max_confidence": 0.75,
    },
    "template_10_conflicting_info": {
        "allow_relations": False,
        "allow_abstain": True,
    },
    "template_11_user_commentary": {
        "allow_relations": False,
        "allow_abstain": True,
    },
}
