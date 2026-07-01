"""Seed MITRE ATT&CK techniques into the local database."""

import argparse
import json
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models.technique import Technique


SAMPLE_TECHNIQUES = [
    {"id": "T1566", "name": "Phishing", "tactic": "Initial Access", "description": "Adversaries send phishing messages to gain access to victim systems.", "reference": "https://attack.mitre.org/techniques/T1566"},
    {"id": "T1059", "name": "Command and Scripting Interpreter", "tactic": "Execution", "description": "Adversaries may abuse command and script interpreters to execute commands.", "reference": "https://attack.mitre.org/techniques/T1059"},
    {"id": "T1059.001", "name": "PowerShell", "tactic": "Execution", "description": "PowerShell is a powerful interactive command-line interface and scripting environment included in the Windows operating system.", "reference": "https://attack.mitre.org/techniques/T1059/001"},
    {"id": "T1078", "name": "Valid Accounts", "tactic": "Defense Evasion", "description": "Adversaries may obtain and use credentials of existing accounts.", "reference": "https://attack.mitre.org/techniques/T1078"},
    {"id": "T1078.002", "name": "Domain Accounts", "tactic": "Defense Evasion", "description": "Adversaries may obtain and use credentials of a domain account.", "reference": "https://attack.mitre.org/techniques/T1078/002"},
    {"id": "T1003", "name": "OS Credential Dumping", "tactic": "Credential Access", "description": "Adversaries may attempt to dump credentials to obtain account login and credential material.", "reference": "https://attack.mitre.org/techniques/T1003"},
    {"id": "T1047", "name": "Windows Management Instrumentation", "tactic": "Execution", "description": "Adversaries may abuse WMI to execute commands.", "reference": "https://attack.mitre.org/techniques/T1047"},
    {"id": "T1053", "name": "Scheduled Task/Job", "tactic": "Execution", "description": "Adversaries may abuse task scheduling functionality to facilitate execution.", "reference": "https://attack.mitre.org/techniques/T1053"},
    {"id": "T1086", "name": "PowerShell", "tactic": "Execution", "description": "PowerShell scripts may be used to perform a number of actions.", "reference": "https://attack.mitre.org/techniques/T1086"},
    {"id": "T1098", "name": "Account Manipulation", "tactic": "Persistence", "description": "Adversaries may manipulate accounts to maintain access.", "reference": "https://attack.mitre.org/techniques/T1098"},
    {"id": "T1105", "name": "Ingress Tool Transfer", "tactic": "Command and Control", "description": "Adversaries may transfer tools or other files between systems.", "reference": "https://attack.mitre.org/techniques/T1105"},
    {"id": "T1110", "name": "Brute Force", "tactic": "Credential Access", "description": "Adversaries may use brute-force techniques to gain access.", "reference": "https://attack.mitre.org/techniques/T1110"},
    {"id": "T1133", "name": "External Remote Services", "tactic": "Initial Access", "description": "Adversaries may leverage external remote services to access systems.", "reference": "https://attack.mitre.org/techniques/T1133"},
    {"id": "T1190", "name": "Exploit Public-Facing Application", "tactic": "Initial Access", "description": "Adversaries may exploit weaknesses in public-facing software.", "reference": "https://attack.mitre.org/techniques/T1190"},
    {"id": "T1203", "name": "Exploitation for Client Execution", "tactic": "Execution", "description": "Adversaries may exploit software vulnerabilities to execute arbitrary code.", "reference": "https://attack.mitre.org/techniques/T1203"},
    {"id": "T1210", "name": "Exploitation of Remote Services", "tactic": "Lateral Movement", "description": "Adversaries may take advantage of trust relationships to move laterally.", "reference": "https://attack.mitre.org/techniques/T1210"},
    {"id": "T1486", "name": "Data Encrypted for Impact", "tactic": "Impact", "description": "Adversaries may encrypt data on target systems to interrupt availability.", "reference": "https://attack.mitre.org/techniques/T1486"},
    {"id": "T1490", "name": "Inhibit System Recovery", "tactic": "Impact", "description": "Adversaries may delete or remove built-in data recovery components.", "reference": "https://attack.mitre.org/techniques/T1490"},
    {"id": "T1496", "name": "Data Manipulation", "tactic": "Impact", "description": "Adversaries may manipulate data to influence decision-making.", "reference": "https://attack.mitre.org/techniques/T1496"},
    {"id": "T1562", "name": "Impair Defenses", "tactic": "Defense Evasion", "description": "Adversaries may maliciously modify components of defenses.", "reference": "https://attack.mitre.org/techniques/T1562"},
    {"id": "T1567", "name": "Exfiltration Over Web Service", "tactic": "Exfiltration", "description": "Adversaries may exfiltrate data using web services.", "reference": "https://attack.mitre.org/techniques/T1567"},
    {"id": "T1570", "name": "Lateral Tool Transfer", "tactic": "Lateral Movement", "description": "Adversaries may transfer tools or files between systems.", "reference": "https://attack.mitre.org/techniques/T1570"},
    {"id": "T1573", "name": "Encrypted Channel", "tactic": "Command and Control", "description": "Adversaries may communicate using encrypted channels to avoid detection.", "reference": "https://attack.mitre.org/techniques/T1573"},
    {"id": "T1588", "name": "Obtain Capabilities", "tactic": "Resource Development", "description": "Adversaries may buy or steal capabilities to support operations.", "reference": "https://attack.mitre.org/techniques/T1588"},
]


def seed_techniques(db: Session, techniques: list[dict]) -> dict:
    added = 0
    skipped = 0
    items = []
    for item in techniques:
        existing = db.get(Technique, item["id"])
        if existing:
            skipped += 1
            continue
        obj = Technique(**item)
        db.add(obj)
        added += 1
        items.append(obj)
    db.commit()
    return {"added": added, "skipped": skipped, "techniques": [t.id for t in items]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed MITRE ATT&CK techniques")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate tables before seeding")
    args = parser.parse_args()

    if args.reset:
        Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        result = seed_techniques(db, SAMPLE_TECHNIQUES)
        print(json.dumps(result, indent=2))
    finally:
        db.close()


if __name__ == "__main__":
    main()
