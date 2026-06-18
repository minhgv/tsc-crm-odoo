# TSC CRM — Implementation Plan

> **Created**: 2026-06-17
> **Status**: Draft — Pending Review
> **Based on**: Audit report of TSC-CRM_requirement_v1.1.docx vs current codebase

---

## Executive Summary

Module hiện tại có **9 models** nhưng **8/10 feature chưa implement** và **3 dangling references** (tsc.service, tsc.package, tsc.package.level) sẽ crash module khi install. Plan này chia thành **7 phases**, mỗi phase có thể review và approve riêng.

---

## Phase 1: Fix Blocking Issues — Service/Package Models

> **Priority**: CRITICAL — Module không thể load nếu thiếu 3 models này
> **Estimated Effort**: 1-2 ngày
> **Dependencies**: None

### Mục tiêu
Tạo 3 models thiếu để fix dangling references trong `order_line.py`, đồng thời build feature Service/Package Management đầy đủ.

### 1.1 Model `tsc.service`

```
File: models/service.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Tên dịch vụ (required) |
| code | Char | Mã dịch vụ (unique) |
| service_type | Selection | direct / project |
| description | Text | Mô tả |
| logo | Image | Logo dịch vụ |
| banner | Image | Banner |
| video_url | Char | Link video giới thiệu |
| target_customer | Selection | individual / business / government / all |
| value_proposition | Text | Giá trị mang lại |
| policies | Text | Chính sách |
| channel | Selection | online / offline / both |
| active | Boolean | Default True |
| package_ids | One2many | → tsc.package |
| sequence | Integer | Thứ tự hiển thị |

**Views**: form, tree, kanban, search
**Security**: ACL cho admin, manager, staff_business
**Tests**: CRUD, name_get, search

### 1.2 Model `tsc.package`

```
File: models/package.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Tên gói cước (required) |
| code | Char | Mã gói (unique) |
| service_id | Many2one → tsc.service | Dịch vụ cha |
| package_type | Selection | one_time / cycle |
| trial_days | Integer | Thời gian dùng thử |
| validity_days | Integer | Thời hạn sử dụng |
| setup_fee | Float | Phí triển khai/lắp đặt |
| description | Text | Mô tả |
| logo | Image | Logo |
| image_ids | One2many → ir.attachment | Hình ảnh/video |
| notes | Text | Ghi chú |
| level_ids | One2many → tsc.package.level | Các level giá |
| active | Boolean | Default True |
| is_combo | Boolean | Là gói combo |
| combo_service_ids | Many2many → tsc.service | Dịch vụ trong combo |
| sequence | Integer | Thứ tự |

**Views**: form, tree, kanban, search (filter by service)
**Security**: ACL cho admin, manager, staff_business
**Tests**: CRUD, combo logic, price computation

### 1.3 Model `tsc.package.level`

```
File: models/package_level.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Tên level (VD: HDD, SSD) |
| package_id | Many2one → tsc.package | Gói cước cha |
| price | Float | Giá (Kip/tháng) |
| description | Text | Mô tả |
| sequence | Integer | Thứ tự |

**Views**: Inline trong package form
**Security**: Theo package
**Tests**: CRUD, price levels

### 1.4 Files cần tạo/sửa

| Action | File |
|--------|------|
| CREATE | `models/service.py` |
| CREATE | `models/package.py` |
| CREATE | `models/package_level.py` |
| EDIT | `models/__init__.py` — thêm import |
| CREATE | `views/service_views.xml` |
| CREATE | `views/package_views.xml` |
| EDIT | `security/ir.model.access.csv` — thêm ACLs |
| EDIT | `__manifest__.py` — thêm views vào data |
| CREATE | `tests/test_service.py` |
| CREATE | `tests/test_package.py` |

### 1.5 Acceptance Criteria

- [ ] `tsc.service`, `tsc.package`, `tsc.package.level` models exist và register thành công
- [ ] `tsc.order.line` Many2one fields không còn dangling reference
- [ ] CRUD views cho service và package hoạt động
- [ ] ACLs đúng cho từng role
- [ ] Tests pass
- [ ] Module install thành công trên Odoo 18

---

## Phase 2: Contract Management

> **Priority**: CAO — Cần cho flow nghiệp vụ cốt lõi (Bước 4: Ký hợp đồng)
> **Estimated Effort**: 2-3 ngày
> **Dependencies**: Phase 1 (cần service/package cho order line)

### Mục tiêu
Tạo model `tsc.contract` quản lý hợp đồng, tích hợp VOffice signing và document scan.

### 2.1 Model `tsc.contract`

```
File: models/contract.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Số hợp đồng (auto sequence) |
| lead_id | Many2one → crm.lead | Đơn hàng liên kết |
| partner_id | Many2one → res.partner | Khách hàng |
| contract_date | Date | Ngày ký |
| start_date | Date | Ngày hiệu lực |
| end_date | Date | Ngày hết hạn |
| state | Selection | draft / pending_sign / signed / active / expired / cancelled |
| signed_file | Binary | File scan hợp đồng đã ký |
| voffice_doc_id | Char | ID tài liệu trên VOffice |
| voffice_status | Selection | none / pending / signed / rejected |
| notes | Text | Ghi chú |
| amount_total | Float | Tổng giá trị hợp đồng |

**Workflow states**:
```
draft → pending_sign → signed → active → expired
                  ↘ cancelled
```

### 2.2 VOffice Integration

- Button "Send to VOffice" → gọi VOffice API upload document
- Button "Check Status" → polling VOffice status
- Webhook receiver (nếu cần) để cập nhật trạng thái tự động
- Reference: `.mimocode/skills/voffice/SKILL.md` cho API patterns

### 2.3 Document Scan

- Upload file scan qua Binary field
- Hỗ trợ PDF, image (JPG, PNG)
- Link đến `ir.attachment` để manage files

### 2.4 Files cần tạo/sửa

| Action | File |
|--------|------|
| CREATE | `models/contract.py` |
| EDIT | `models/__init__.py` |
| CREATE | `views/contract_views.xml` |
| EDIT | `security/ir.model.access.csv` |
| EDIT | `__manifest__.py` |
| CREATE | `tests/test_contract.py` |

### 2.5 Acceptance Criteria

- [ ] Contract CRUD hoạt động
- [ ] Workflow states đúng (draft → pending_sign → signed → active)
- [ ] Upload scan file hoạt động
- [ ] VOffice integration stub hoạt động (tối thiểu create + status check)
- [ ] Dashboard hiển thị contract stats
- [ ] ACLs đúng cho roles
- [ ] Tests pass

---

## Phase 3: Invoice & Payment

> **Priority**: CAO — Cần cho flow thanh toán (Bước 5)
> **Estimated Effort**: 3-4 ngày
> **Dependencies**: Phase 2 (contract → invoice)

### Mục tiêu
Tạo `tsc.invoice` và `tsc.payment` models, tích hợp Unipay/uMoney.

### 3.1 Model `tsc.invoice`

```
File: models/invoice.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Số hóa đơn (auto sequence) |
| contract_id | Many2one → tsc.contract | Hợp đồng |
| partner_id | Many2one → res.partner | Khách hàng |
| invoice_date | Date | Ngày xuất |
| due_date | Date | Ngày đến hạn |
| state | Selection | draft / posted / paid / cancelled / refund |
| amount_untaxed | Float | Thành tiền |
| vat_rate | Float | Tỷ lệ VAT (%) |
| vat_amount | Float | Số tiền VAT |
| wht_rate | Float | Tỷ lệ WHT (%) |
| wht_amount | Float | Số tiền WHT |
| amount_total | Float | Tổng cộng |
| invoice_line_ids | One2many → tsc.invoice.line | Chi tiết |
| payment_ids | One2many → tsc.payment | Các khoản thanh toán |
| notes | Text | Ghi chú |

### 3.2 Model `tsc.invoice.line`

```
File: models/invoice_line.py
```

| Field | Type | Description |
|-------|------|-------------|
| invoice_id | Many2one → tsc.invoice | Hóa đơn |
| order_line_id | Many2one → tsc.order.line | Order line |
| description | Char | Mô tả |
| quantity | Float | Số lượng |
| unit_price | Float | Đơn giá |
| amount | Float | Thành tiền |

### 3.3 Model `tsc.payment`

```
File: models/payment.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Mã giao dịch |
| invoice_id | Many2one → tsc.invoice | Hóa đơn |
| partner_id | Many2one → res.partner | Khách hàng |
| amount | Float | Số tiền |
| payment_method | Selection | unipay / umoney / cash / bank_transfer |
| payment_date | DateTime | Ngày thanh toán |
| state | Selection | draft / pending / confirmed / failed / refunded |
| transaction_id | Char | Mã giao dịch外部 |
| notes | Text | Ghi chú |

### 3.4 Unipay/uMoney Integration

- Button "Create Payment" → tạo payment record
- Unipay: QR payment, mobile balance
- uMoney: ví/bank
- Stub API calls (chưa connect thật, nhưng interface sẵn sàng)

### 3.5 Files cần tạo/sửa

| Action | File |
|--------|------|
| CREATE | `models/invoice.py` |
| CREATE | `models/invoice_line.py` |
| CREATE | `models/payment.py` |
| EDIT | `models/__init__.py` |
| CREATE | `views/invoice_views.xml` |
| CREATE | `views/payment_views.xml` |
| EDIT | `security/ir.model.access.csv` |
| EDIT | `__manifest__.py` |
| CREATE | `tests/test_invoice.py` |
| CREATE | `tests/test_payment.py` |

### 3.6 Acceptance Criteria

- [ ] Invoice CRUD + workflow states hoạt động
- [ ] Payment CRUD + workflow states hoạt động
- [ ] Invoice lines auto-calculate totals
- [ ] VAT/WHT calculation đúng (kết hợp Phase 4)
- [ ] Dashboard hiển thị invoice/payment stats
- [ ] Payment method stub sẵn sàng
- [ ] Tests pass

---

## Phase 4: VAT/WHT & Exchange Rate

> **Priority**: TRUNG BÌNH — Cần cho tính giá/hoá đơn
> **Estimated Effort**: 1-2 ngày
> **Dependencies**: Phase 3 (invoice dùng VAT/WHT)

### Mục tiêu
Tạo config models cho VAT, WHT, và tỷ giá BCEL.

### 4.1 Model `tsc.vat`

```
File: models/vat.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Mô tả |
| rate | Float | Tỷ lệ VAT (%) |
| date_from | Date | Có hiệu lực từ |
| date_to | Date | Có hiệu lực đến |
| active | Boolean | Default True |

### 4.2 Model `tsc.wht`

```
File: models/wht.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Mô tả |
| rate | Float | Tỷ lệ WHT (%) |
| date_from | Date | Có hiệu lực từ |
| date_to | Date | Có hiệu lực đến |
| active | Boolean | Default True |

### 4.3 Model `tsc.exchange.rate`

```
File: models/exchange_rate.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Ngày tỷ giá |
| currency_from | Char | Từ tiền tệ (USD, THB, ...) |
| currency_to | Char | Đến tiền tệ (LAK) |
| rate | Float | Tỷ giá |
| source | Char | Nguồn (BCEL) |
| date | Date | Ngày áp dụng |

**Cron job**: Hàng ngày fetch tỷ giá từ BCEL
- URL: https://www.bcel.com.la/bcel/exchange-rate.html?lang=en
- Nếu ngày không có tỷ giá (T7, CN) → dùng tỷ giá ngày gần nhất

### 4.4 Files cần tạo/sửa

| Action | File |
|--------|------|
| CREATE | `models/vat.py` |
| CREATE | `models/wht.py` |
| CREATE | `models/exchange_rate.py` |
| EDIT | `models/__init__.py` |
| CREATE | `views/vat_views.xml` |
| CREATE | `views/wht_views.xml` |
| CREATE | `views/exchange_rate_views.xml` |
| CREATE | `data/vat_data.xml` — mẫu VAT rates |
| CREATE | `data/wht_data.xml` — mẫu WHT rates |
| EDIT | `security/ir.model.access.csv` |
| EDIT | `__manifest__.py` |
| CREATE | `tests/test_vat.py` |
| CREATE | `tests/test_exchange_rate.py` |

### 4.5 Acceptance Criteria

- [ ] VAT/WHT config CRUD hoạt động
- [ ] Tính VAT/WHT theo thời điểm xuất invoice đúng
- [ ] Exchange rate CRUD hoạt động
- [ ] Cron job fetch BCEL rate (stub/test mode)
- [ ] Fallback ngày không có tỷ giá (T7/CN)
- [ ] Data mẫu VAT/WHT load đúng
- [ ] Tests pass

---

## Phase 5: Commission & Discounts/Promotions

> **Priority**: TRUNG BÌNH — Cần cho kinh doanh
> **Estimated Effort**: 2-3 ngày
> **Dependencies**: Phase 1 (service/package), Phase 3 (invoice/payment)

### Mục tiêu
Tạo commission config và discount/promotion system.

### 5.1 Model `tsc.commission`

```
File: models/commission.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Tên quy tắc |
| service_id | Many2one → tsc.service | Dịch vụ (blank = all) |
| package_id | Many2one → tsc.package | Gói cước (blank = all) |
| commission_type | Selection | percentage / fixed |
| rate | Float | Tỷ lệ hoa hồng (%) hoặc số tiền cố định |
| min_revenue | Float | Doanh thu tối thiểu (revenue tier) |
| max_revenue | Float | Doanh thu tối đa |
| target_type | Selection | all / am_province / agency / staff / management |
| date_from | Date | Có hiệu lực từ |
| date_to | Date | Có hiệu lực đến |
| active | Boolean | Default True |

### 5.2 Model `tsc.commission.detail`

```
File: models/commission_detail.py
```

| Field | Type | Description |
|-------|------|-------------|
| commission_id | Many2one → tsc.commission | Quy tắc |
| employee_id | Many2one → hr.employee | Nhân viên |
| order_id | Many2one → crm.lead | Đơn hàng |
| amount | Float | Số tiền hoa hồng |
| state | Selection | draft / confirmed / paid |
| confirmed_date | Date | Ngày xác nhận |

### 5.3 Model `tsc.discount`

```
File: models/discount.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Tên chương trình |
| discount_type | Selection | percentage / fixed |
| value | Float | Giá trị giảm |
| service_id | Many2one → tsc.service | Dịch vụ (blank = all) |
| package_id | Many2one → tsc.package | Gói cước (blank = all) |
| min_quantity | Integer | Số lượng tối thiểu |
| date_from | Date | Bắt đầu |
| date_to | Date | Kết thúc |
| active | Boolean | Default True |
| max_uses | Integer | Số lần dùng tối đa (0 = unlimited) |
| used_count | Integer | Đã dùng |

### 5.4 Files cần tạo/sửa

| Action | File |
|--------|------|
| CREATE | `models/commission.py` |
| CREATE | `models/commission_detail.py` |
| CREATE | `models/discount.py` |
| EDIT | `models/__init__.py` |
| CREATE | `views/commission_views.xml` |
| CREATE | `views/discount_views.xml` |
| EDIT | `security/ir.model.access.csv` |
| EDIT | `__manifest__.py` |
| CREATE | `tests/test_commission.py` |
| CREATE | `tests/test_discount.py` |

### 5.5 Acceptance Criteria

- [ ] Commission config CRUD hoạt động
- [ ] Commission calculation theo tier đúng
- [ ] Discount config CRUD hoạt động
- [ ] Auto-apply discount trên order line khi đúng điều kiện
- [ ] max_uses tracking
- [ ] Commission detail tracking per employee
- [ ] Tests pass

---

## Phase 6: SLA Config & Notifications

> **Priority**: TRUNG BÌNH — Mở rộng từ partial hiện tại
> **Estimated Effort**: 2-3 ngày
> **Dependencies**: Phase 1 (order flow), Phase 5 (KPI context)

### Mục tiêu
Hoàn thiện SLA configuration và thêm SMS/Email notifications.

### 6.1 Model `tsc.sla.config`

```
File: models/sla_config.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Tên stage |
| stage_key | Selection | created / assigned / accepted / surveying / confirm / contract / paid |
| time_limit | Float | Thời gian giới hạn |
| time_unit | Selection | minutes / hours / days |
| apply_type | Selection | full_24h / business_hours |
| business_start | Float | Giờ bắt đầu (VD: 8) |
| business_end | Float | Giờ kết thúc (VD: 17) |
| auto_action | Selection | none / auto_assign_admin / notify |
| service_id | Many2one → tsc.service | Áp dụng cho dịch vụ (blank = all) |
| region_id | Many2one → tsc.region | Áp dụng cho khu vực (blank = all) |
| active | Boolean | Default True |

### 6.2 Model `tsc.sla.violation`

```
File: models/sla_violation.py
```

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Mô tả |
| lead_id | Many2one → crm.lead | Đơn hàng vi phạm |
| sla_config_id | Many2one → tsc.sla.config | Config bị vi phạm |
| violation_date | DateTime | Thời điểm vi phạm |
| action_taken | Text | Hành động đã thực hiện |
| resolved | Boolean | Đã xử lý |

### 6.3 Notification Templates

Tạo `mail.template` records trong `data/notification_templates.xml`:

| Template | Loại | Kích hoạt |
|----------|------|-----------|
| Order Created | Email + SMS | Khi tạo order |
| Order Assigned | Email + SMS | Khi gán đơn |
| Order Reassigned | Email + SMS | Khi chuyển đơn |
| SLA Warning | Email | Khi sắp hết hạn SLA |
| SLA Violated | Email + SMS | Khi quá SLA |
| Task Assigned | Email | Khi gán task kỹ thuật |
| Task Completed | Email | Khi hoàn thành task |

### 6.4 Auto-assign Logic

```python
# Trong crm_lead.py hoặc scheduled action
def _cron_check_sla(self):
    """Check all active leads for SLA violations"""
    # 1. Find leads past SLA deadline
    # 2. Log violation in tsc.sla.violation
    # 3. Execute auto_action (reassign to admin, send notification)
    # 4. Mark KPI impact
```

### 6.5 Files cần tạo/sửa

| Action | File |
|--------|------|
| CREATE | `models/sla_config.py` |
| CREATE | `models/sla_violation.py` |
| EDIT | `models/__init__.py` |
| EDIT | `models/crm_lead.py` — thêm SLA check logic |
| CREATE | `views/sla_config_views.xml` |
| CREATE | `views/sla_violation_views.xml` |
| EDIT | `views/crm_lead_views.xml` — thêm SLA info |
| CREATE | `data/notification_templates.xml` |
| CREATE | `data/sla_data.xml` — mẫu SLA config |
| EDIT | `security/ir.model.access.csv` |
| EDIT | `__manifest__.py` |
| CREATE | `tests/test_sla.py` |

### 6.6 Acceptance Criteria

- [ ] SLA config CRUD hoạt động
- [ ] SLA violation tracking hoạt động
- [ ] Notification templates tạo đúng format
- [ ] Auto-assign admin khi quá SLA
- [ ] Scheduled action check SLA hàng giờ
- [ ] Lead form hiển thị SLA info đầy đủ
- [ ] Tests pass

---

## Phase 7: Permission Gaps & Final Integration

> **Priority**: THẤP — Hoàn thiện sau khi tất cả features done
> **Estimated Effort**: 1-2 ngày
> **Dependencies**: Phase 1-6 (cần tất cả models để set permission đúng)

### Mục tiêu
Fix permission gaps và final integration.

### 7.1 Permission Fixes

| Issue | Fix |
|-------|-----|
| `group_tsc_admin` không imply manager | Thêm `implied_ids` = manager |
| `group_tsc_staff_cc` không có ACL | Thêm ACL cho customer care |
| Không có record rules cho crm.lead | Thêm rules scope theo region/team |
| Không có record rules cho technical.task | Thêm rules scope theo assigned_to/team |
| `tsc.role` trên hr.employee không link res.groups | Thêm logic sync hoặc remove redundancy |

### 7.2 New Record Rules

```xml
<!-- Lead: staff thấy leads của mình/team/region -->
<record id="rule_lead_staff" model="ir.rule">
    <field name="name">Staff sees own/team leads</field>
    <field name="model_id" ref="model_crm_lead"/>
    <field name="domain_force">[
        '|',
        ('user_id', '=', user.id),
        ('user_id', 'in', user.sale_team_id.member_ids.ids)
    ]</field>
    <field name="groups" eval="[(4, ref('group_tsc_staff_business'))]"/>
</record>

<!-- Lead: manager thấy tất cả leads trong region -->
<record id="rule_lead_manager" model="ir.rule">
    <field name="name">Manager sees all leads</field>
    <field name="model_id" ref="model_crm_lead"/>
    <field name="domain_force">[(1, '=', 1)]</field>
    <field name="groups" eval="[(4, ref('group_tsc_manager'))]"/>
</record>

<!-- Technical task: staff thấy tasks assigned to自己 -->
<record id="rule_task_staff" model="ir.rule">
    <field name="name">Staff sees own tasks</field>
    <field name="model_id" ref="model_tsc_technical_task"/>
    <field name="domain_force">[
        '|',
        ('assigned_to.user_id', '=', user.id),
        ('assigned_by.user_id', '=', user.id)
    ]</field>
    <field name="groups" eval="[(4, ref('group_tsc_staff_technical'))]"/>
</record>
```

### 7.3 Files cần sửa

| Action | File |
|--------|------|
| EDIT | `security/tsc_security.xml` — fix group hierarchy |
| EDIT | `security/ir.model.access.csv` — thêm ACLs |
| CREATE | `security/tsc_record_rules.xml` — thêm record rules |
| EDIT | `__manifest__.py` — thêm record rules file |

### 7.4 Acceptance Criteria

- [ ] Admin imply Manager permissions
- [ ] Customer Care group có quyền đọc cơ bản
- [ ] Record rules cho leads, tasks hoạt động
- [ ] Staff chỉ thấy data của mình/team
- [ ] Manager thấy tất cả data
- [ ] Admin override mọi thứ
- [ ] Integration test: toàn bộ module hoạt động đồng bộ
- [ ] `ruff check` passes
- [ ] All tests pass

---

## Execution Order & Dependencies

```
Phase 1 (Service/Package) ──→ Phase 2 (Contract) ──→ Phase 3 (Invoice/Payment)
                                                        ↓
                                              Phase 4 (VAT/WHT/Exchange)
                                                        ↓
                                              Phase 5 (Commission/Discount)
                                                        ↓
                                              Phase 6 (SLA/Notifications)
                                                        ↓
                                              Phase 7 (Permissions/Final)
```

**Parallel opportunities**:
- Phase 4 (VAT/WHT) có thể chạy song song với Phase 2 (Contract)
- Phase 6 (SLA) có thể chạy song song với Phase 5 (Commission)

---

## Estimated Total Effort

| Phase | Days |
|-------|------|
| Phase 1: Service/Package | 1-2 |
| Phase 2: Contract | 2-3 |
| Phase 3: Invoice/Payment | 3-4 |
| Phase 4: VAT/WHT/Exchange | 1-2 |
| Phase 5: Commission/Discount | 2-3 |
| Phase 6: SLA/Notifications | 2-3 |
| Phase 7: Permissions/Final | 1-2 |
| **Total** | **12-19 ngày** |

---

## Risk & Notes

1. **Phase 1 là blocker** — Không thể implement bất kỳ feature nào khác nếu Service/Package models chưa tạo
2. **VOffice integration** cần API token và test environment — stub sẵn sàng nhưng cần config thật
3. **Unipay/uMoney** similarly cần API credentials — stub interface sẵn sàng
4. **BCEL exchange rate** scraping có thể thay đổi format — cần fallback mechanism
5. **Notification SMS** cần SMS gateway config — template sẵn sàng nhưng sending cần provider

---

## Review Checklist

- [ ] Phân tích lại priority — có feature nào nên lên/down không?
- [ ] Kiểm tra effort estimate — có realistic không?
- [ ] Xác nhận dependency order — có bottleneck nào không?
- [ ] Quyết định VOffice/Unipay stub vs real API
- [ ] Xác nhận naming convention cho models
- [ ] Review field list cho từng model — thiếu/giết field nào?
