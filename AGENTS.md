# TSC-CRM — Odoo 18 CRM Module

Custom CRM module for Odoo 18, built from `TSC-CRM_requirement_v1.1.docx`.

## Project State

- **Phase**: Initialization — no Odoo modules created yet
- **Odoo version**: 18 (latest)
- **Requirement doc**: `TSC-CRM_requirement_v1.1.docx` (root)

## Quick Commands

```bash
# Install Odoo 18 (if not present)
pip install odoo

# Start Odoo dev server with custom addons path
odoo --addons-path=addons,/path/to/odoo/addons -d tsc_crm -i tsc_crm --dev=xmlrpc

# Run Odoo shell
odoo shell -d tsc_crm

# Upgrade module after changes
odoo -d tsc_crm -u tsc_crm

# Run Python tests
python -m pytest addons/tsc_crm/tests/

# Lint Python
ruff check addons/tsc_crm/
ruff format addons/tsc_crm/
```

## Module Structure

```
addons/
  tsc_crm/
    __init__.py
    __manifest__.py
    models/
      __init__.py
      crm_lead.py
    views/
      crm_lead_views.xml
    security/
      ir.model.access.csv
    data/
    tests/
      __init__.py
      test_crm_lead.py
```

## Odoo 18 Conventions

- **Python**: Follow odoo/odoo coding style (2-space indent in XML, 4-space in Python)
- **Models**: Inherit `models.Model`, use `_name`, `_description`, `_inherit`
- **Views**: XML with `<record>` tags, form/tree/kanban/search views
- **Security**: Define `ir.model.access.csv` + record rules in `security/`
- **Manifest**: `__manifest__.py` with `depends`, `data`, `license` keys
- **License**: Use `LGPL-3` or `OEEL-1` per Odoo standards
- **Fields**: Use `fields.Char`, `fields.Selection`, `fields.Many2one`, etc.
- **No direct SQL** unless performance-critical; use ORM API
- **Naming**: model `crm.lead` → view `crm_lead_view_form`, tree `crm_lead_view_tree`

## Skills

Available in `.opencode/skill/` — use `skill({ name: "..." })` to load:
- `project-init` — initialize project context files
- `verification-before-completion` — verify before marking done
- `planning-and-task-breakdown` — break work into tasks
- `test-driven-development` — TDD workflow
- `code-review-and-quality` — review checklist

## Rules

- Read `TSC-CRM_requirement_v1.1.docx` before implementing any feature
- Follow Odoo ORM patterns — no raw SQL without justification
- Every model needs `ir.model.access.csv` entry
- Write tests in `tests/` directory
- Run linter before commit
- Reference `.opencode/AGENTS.md` for agent behavioral rules
