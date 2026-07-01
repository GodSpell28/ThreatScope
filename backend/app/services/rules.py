from typing import List, Dict, Any
from app.models.rule import DetectionRule, RuleType


def summarize_rule(rule: DetectionRule) -> Dict[str, Any]:
    return {
        "id": rule.id,
        "name": rule.name,
        "rule_type": rule.rule_type.value,
        "content_length": len(rule.content or ""),
        "status": rule.status,
    }


def validate_sigma(rule: DetectionRule) -> Dict[str, Any]:
    content = rule.content or ""
    return {
        "valid": "title:" in content and "detection:" in content,
        "rule_type": rule.rule_type.value,
    }


def validate_yara(rule: DetectionRule) -> Dict[str, Any]:
    content = rule.content or ""
    return {
        "valid": "rule " in content and "condition:" in content,
        "rule_type": rule.rule_type.value,
    }


def validate_rule(rule: DetectionRule) -> Dict[str, Any]:
    if rule.rule_type == RuleType.sigma:
        return validate_sigma(rule)
    if rule.rule_type == RuleType.yara:
        return validate_yara(rule)
    return {"valid": False, "reason": "unsupported rule type"}
