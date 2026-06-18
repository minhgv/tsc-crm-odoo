# TSC-CRM — Odoo 18 CRM Module

Custom CRM module for Odoo 18, built from `TSC-CRM_requirement_v1.1.docx`.

## Project State

- **Phase**: Implementation Complete — 7 phases delivered
- **Odoo version**: 18 (latest)
- **Requirement doc**: `TSC-CRM_requirement_v1.1.docx` (root)
- **Tests**: 77 test cases passing

## Quick Commands

```bash
# Start Docker environment
docker compose up -d

# Update module
docker exec tsc-crm-odoo-odoo-1 odoo -d tsc_crm \
  --db_host=db --db_port=5432 --db_user=odoo --db_password=odoo \
  -u tsc_crm --stop-after-init --http-port=8070

# Run tests
docker exec tsc-crm-odoo-odoo-1 odoo -d tsc_crm \
  --db_host=db --db_port=5432 --db_user=odoo --db_password=odoo \
  --test-tags=tsc_crm --stop-after-init --http-port=8070

# Lint Python
ruff check addons/tsc_crm/models/ --ignore=F401
```

## Module Structure

```
addons/tsc_crm/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── crm_lead.py          # Order management, SLA, workflow
│   ├── crm_team.py          # Team with region
│   ├── hr_employee.py       # Employee roles/groups
│   ├── res_partner.py       # Customer info
│   ├── region.py            # Region hierarchy
│   ├── service.py           # Service catalog
│   ├── package.py           # Package management
│   ├── package_level.py     # Package pricing levels
│   ├── order_line.py        # Order line items
│   ├── order_assignment.py  # Assignment audit log
│   ├── technical_task.py    # Technical task workflow
│   ├── contract.py          # Contract management
│   ├── sign.py              # VOffice signing tracking
│   ├── invoice.py           # Invoice management
│   ├── invoice_line.py      # Invoice line items
│   ├── payment.py           # Payment management
│   ├── vat.py               # VAT config (time-based)
│   ├── wht.py               # WHT config (time-based)
│   ├── sla_violation.py     # SLA violation tracking
│   └── tsc_dashboard.py     # Dashboard stats
├── views/                   # 18 XML view files
├── security/
│   ├── tsc_security.xml     # Groups + record rules
│   └── ir.model.access.csv  # 56 ACL entries
├── data/
│   ├── crm_stage_data.xml   # CRM stages
│   └── notification_templates.xml  # 5 email templates
├── tests/                   # 18 test files, 77 tests
└── i18n/                    # Translations
```

## Implemented Features

| # | Feature | Status | Models |
|---|---------|--------|--------|
| 1 | Service/Package Management | ✅ | tsc.service, tsc.package, tsc.package.level |
| 2 | Contract Management | ✅ | tsc.contract, tsc.sign |
| 3 | Invoice/Payment | ✅ | tsc.invoice, tsc.invoice.line, tsc.payment |
| 4 | VAT/WHT | ✅ | tsc.vat, tsc.wht |
| 5 | Exchange Rate | ✅ | tsc.exchange.rate (in tsc_crm_workflow) |
| 6 | Commission | ✅ | tsc.commission (in tsc_crm_commission) |
| 7 | Discounts/Promotions | ✅ | tsc.discount (in tsc_crm_service) |
| 8 | SLA Config | ✅ | tsc.sla.config (in tsc_crm_workflow), tsc.sla.violation |
| 9 | Notifications | ✅ | 5 email templates |
| 10 | Role-based Permissions | ✅ | 5 groups, 56 ACLs, 8 record rules |

## Security Groups Hierarchy

```
group_tsc_admin (implies group_tsc_manager)
└── group_tsc_manager (implies group_tsc_staff_business)
    └── group_tsc_staff_business
group_tsc_staff_technical
group_tsc_staff_cc
```

## Odoo 18 Conventions

- **Python**: 4-space indent, follow odoo/odoo coding style
- **XML**: 2-space indent, `<record>` tags for views
- **Models**: Inherit `models.Model`, use `_name`, `_description`, `_inherit`
- **Security**: `ir.model.access.csv` + record rules in `security/`
- **Manifest**: `__manifest__.py` with `depends`, `data`, `license` keys
- **License**: `LGPL-3`
- **Fields**: Use `fields.Char`, `fields.Selection`, `fields.Many2one`, etc.
- **SQL Constraints**: Use `_sql_constraints` instead of `unique=True` on fields
- **Naming**: model `tsc.service` → view `tsc_service_view_form`, tree `tsc_service_view_tree`

## Rules

- Read `TSC-CRM_requirement_v1.1.docx` before implementing any feature
- Follow Odoo ORM patterns — no raw SQL without justification
- Every model needs `ir.model.access.csv` entry
- Write tests in `tests/` directory
- Run linter before commit
- Check for existing models in other modules before creating new ones
