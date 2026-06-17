# TSC-CRM User Stories

## Module 1: `tsc_crm` — Core CRM

### US-1.1: Tạo Order mới
**As a** Sales Staff, **I want to** tạo order mới với thông tin khách hàng và dịch vụ, **so that** tôi có thể theo dõi quá trình xử lý.

**Acceptance Criteria:**
- Order tự động tạo mã (`tsc_order_id`) theo sequence `ORD-XXXX`
- Chọn region, loại dịch vụ (direct/project), loại KH (individual/business/government), nguồn (miniapp/cms)
- Thêm order lines với service, package, số lượng, đơn giá, giảm giá
- Tổng order tự động tính (`tsc_order_total = sum(line.total_price)`)
- Trạng thái mặc định: Created

**Test Cases:**
```
TC-1.1.1: Tạo order với order lines — verify tsc_order_id auto-generated
TC-1.1.2: Thêm 3 order lines — verify tsc_order_total = sum(total_price)
TC-1.1.3: Tạo order không có region — verify order vẫn tạo được
TC-1.1.4: Kiểm tra sequence không trùng nhau
```

### US-1.2: Giao việc Order (Assignment)
**As a** Manager, **I want to** giao order cho nhân viên, **so that** order được xử lý kịp thời.

**Acceptance Criteria:**
- Click "Assign" → chọn employee → order chuyển sang stage "Assigned"
- Mỗi lần assign/reassign tạo log trong `tsc.order.assignment`
- Log ghi: assigned_from, assigned_to, assigned_by, reason (auto/manual/reassign/override)
- Message post vào chatter khi assign

**Test Cases:**
```
TC-1.2.1: Assign order cho employee — verify stage = "Assigned", assignment log tạo
TC-1.2.2: Reassign sang employee khác — verify log reason = "reassign"
TC-1.2.3: Kiểm tra chatter có message assignment
TC-1.2.4: Assign không chọn employee — verify ValidationError
```

### US-1.3: Workflow 7 trạng thái
**As a** Sales Staff, **I want to** chuyển order qua các trạng thái, **so that** tôi theo dõi tiến trình.

**Acceptance Criteria:**
- 7 stages: Created → Assigned → Accepted → Surveying → Confirm → Contract → Paid
- Mỗi stage chuyển tạo message trong chatter
- `tsc_stage_key` tự động map từ stage_id

**Test Cases:**
```
TC-1.3.1: Chuyển qua tất cả 7 stages — verify tsc_stage_key đúng
TC-1.3.2: Xác nhận order (action_confirm_order) — verify stage = "Confirm"
TC-1.3.3: Chuyển sang Survey — verify stage = "Survey / Consultation"
```

### US-1.4: Tạo Technical Task
**As a** Sales Staff, **I want to** tạo task kỹ thuật cho nhân viên kỹ thuật, **so that** khảo sát/triển khai được thực hiện.

**Acceptance Criteria:**
- Task có 6 trạng thái: Draft → Assigned → Accepted → In Progress → Done → Cancelled
- Phải chọn assigned_to trước khi assign
- Task overdue khi deadline đã qua và task chưa done/cancelled
- Task type: survey/implementation/maintenance

**Test Cases:**
```
TC-1.4.1: Tạo task → assign → accept → start → done — verify full workflow
TC-1.4.2: Assign task không chọn employee — verify ValidationError
TC-1.4.3: Tạo task với deadline quá hạn — verify is_overdue = True
TC-1.4.4: Cancel task → reset về draft — verify state = "draft"
```

### US-1.5: Quản lý Region hierarchy
**As a** Admin, **I want to** quản lý cấu trúc tổ chức theo vùng, **so that** phân quyền và phân công theo khu vực.

**Acceptance Criteria:**
- Region hierarchy: parent/child, self-referential
- name_get hiển thị "Parent / Child"
- Code unique, có thể active/inactive

**Test Cases:**
```
TC-1.5.1: Tạo region parent + child — verify name_get = "Parent / Child"
TC-1.5.2: Tạo region với code trùng — verify unique constraint
TC-1.5.3: Deactivate region parent — verify child vẫn tồn tại
```

### US-1.6: Dashboard tổng quan
**As a** Manager, **I want to** xem dashboard tổng quan, **so that** tôi biết tình hình kinh doanh.

**Acceptance Criteria:**
- Hiển thị: total orders, overdue orders, stage stats, region stats
- Hiển thị: pending/overdue/done tasks
- Button dẫn đến danh sách chi tiết

**Test Cases:**
```
TC-1.6.1: Tạo 5 orders — verify total_orders = 5
TC-1.6.2: Tạo order overdue — verify overdue_orders tăng
TC-1.6.3: Click "All Orders" — verify mở đúng window
```

---

## Module 2: `tsc_crm_auth` — Authentication

### US-2.1: Đăng nhập bằng OTP
**As a** Customer, **I want to** đăng nhập bằng số điện thoại + OTP, **so that** tôi không cần nhớ password.

**Acceptance Criteria:**
- Gửi OTP 6 chữ số, hết hạn sau 5 phút
- Verify OTP: đúng mã, đúng phone, đúng purpose
- Sai OTP 3 lần → OTP hết hiệu lực
- API: POST /api/auth/otp/send, /otp/verify

**Test Cases:**
```
TC-2.1.1: Gửi OTP — verify code 6 digits, record tạo
TC-2.1.2: Verify đúng OTP — verify state = "verified"
TC-2.1.3: Verify sai OTP 3 lần — verify state = "expired"
TC-2.1.4: Verify OTP hết hạn 5 phút — verify returns False
TC-2.1.5: Verify OTP sai phone — verify returns False
```

### US-2.2: Đăng ký tài khoản Customer
**As a** Customer, **I want to** đăng ký tài khoản qua OTP, **so that** tôi có thể sử dụng dịch vụ.

**Acceptance Criteria:**
- Nhập name, phone, email, password, OTP
- OTP phải verified trước khi đăng ký
- Tạo res.partner + res.users với tsc_user_type = 'customer'
- API: POST /api/auth/register

**Test Cases:**
```
TC-2.2.1: Đăng ký thành công — verify user tạo với tsc_user_type = 'customer'
TC-2.2.2: Đăng ký sai OTP — verify ValidationError
TC-2.2.3: Đăng ký phone trùng — verify user mới tạo riêng
```

### US-2.3: Đăng nhập bằng LaoID
**As an** Employee, **I want to** đăng nhập bằng LaoID SSO, **so that** tôi dùng chung tài khoản công ty.

**Acceptance Criteria:**
- Redirect đến LaoID SSO URL
- Callback: lấy access_token → lấy profile → find or create user
- User type = 'employee', login = 'laoid_{id}'
- Login log ghi nhận mọi login attempt

**Test Cases:**
```
TC-2.3.1: LaoID profile mới — verify user tạo với tsc_lao_id, tsc_user_type = 'employee'
TC-2.3.2: LaoID profile cũ — verify user update tên, không tạo mới
TC-2.3.3: LaoID profile không có tên — verify fallback sang username
TC-2.3.4: Login log ghi nhận success/failure
```

### US-2.4: Quản lý Login Log
**As a** Admin, **I want to** xem lịch sử đăng nhập, **so that** tôi kiểm soát bảo mật.

**Acceptance Criteria:**
- Log: user, login_type (backend/otp/laoid), state (success/failed), ip, user_agent, timestamp
- Chỉ admin mới xem được

**Test Cases:**
```
TC-2.4.1: Tạo login log backend — verify fields đầy đủ
TC-2.4.2: Tạo login log failed với failure_reason — verify lưu đúng
```

---

## Module 3: `tsc_crm_service` — Service Catalog

### US-3.1: Quản lý Service
**As a** Admin, **I want to** quản lý danh sách dịch vụ, **so that** khách hàng biết dịch vụ nào khả dụng.

**Acceptance Criteria:**
- Service có: code, name, logo, icon, banner, slogan, description, policy
- Target customer: individual/business/government
- Distribution channel: online/offline/both
- Service type: direct/project
- Có packages liên kết

**Test Cases:**
```
TC-3.1.1: Tạo service với đầy đủ fields — verify lưu đúng
TC-3.1.2: Service code trùng — verify unique constraint
TC-3.1.3: Thêm package vào service — verify package_ids cập nhật
```

### US-3.2: Quản lý Package
**As a** Admin, **I want to** quản lý gói cước cho mỗi dịch vụ, **so that** khách hàng có nhiều lựa chọn.

**Acceptance Criteria:**
- Package type: per_use/cycle
- Có levels (products) với giá khác nhau
- deployment_fee, trial_days, validity_days
- Package thuộc về 1 service

**Test Cases:**
```
TC-3.2.1: Tạo package cycle với 2 levels — verify level_ids đúng
TC-3.2.2: Package per_use — verify package_type = 'per_use'
TC-3.2.3: Package có trial_days — verify trial_days lưu đúng
```

### US-3.3: Tạo Combo
**As a** Admin, **I want to** tạo combo dịch vụ, **so that** khách hàng mua gói ưu đãi.

**Acceptance Criteria:**
- Combo chứa nhiều lines, mỗi line = service + package + quantity + price
- Total price tự động tính

**Test Cases:**
```
TC-3.3.1: Tạo combo 2 services — verify total_price = sum(line prices)
TC-3.3.2: Combo trống — verify total_price = 0
```

### US-3.4: Quản lý Promotion
**As a** Admin, **I want to** tạo chương trình khuyến mãi, **so that** thúc đẩy bán hàng.

**Acceptance Criteria:**
- Promo type: fixed/percentage
- Scope: order_line/package/service
- Date range: from → to (phải từ ≤ đến)
- Value >= 0, percentage <= 100

**Test Cases:**
```
TC-3.4.1: Tạo promo fixed 100K — verify value = 100000
TC-3.4.2: Tạo promo percentage 10% — verify value = 10.0
TC-3.4.3: Date from > date to — verify ValidationError
TC-3.4.4: Percentage > 100 — verify ValidationError
TC-3.4.5: Value âm — verify ValidationError
```

### US-3.5: Quản lý Discount Policy
**As a** Admin, **I want to** cấu hình chính sách chiết khấu cho agent, **so that** hoa hồng đúng chính sách.

**Acceptance Criteria:**
- Discount type: revenue/order_count
- Discount mode: fixed/percentage
- Scope: all_agents/specific_agent (phải chọn agency)
- Date range validation

**Test Cases:**
```
TC-3.5.1: Policy all_agents percentage — verify lưu đúng
TC-3.5.2: Policy specific_agent không chọn agency — verify ValidationError
TC-3.5.3: Percentage > 100 — verify ValidationError
```

---

## Module 4: `tsc_crm_workflow` — Workflow & Billing

### US-4.1: Quản lý Hợp đồng
**As a** Sales Staff, **I want to** tạo và quản lý hợp đồng, **so that** ký kết được theo dõi.

**Acceptance Criteria:**
- Contract states: Draft → Pending Sign → Signed → Scanned → Active → Expired/Terminated
- Auto-generate contract code (CT-XXXX)
- Có template, audit log, approved_by, performance_state
- Upload signed file

**Test Cases:**
```
TC-4.1.1: Tạo contract — verify code auto-generated, state = draft
TC-4.1.2: Submit → Sign → Scan → Activate — verify full flow
TC-4.1.3: Terminate contract — verify state = 'terminated'
TC-4.1.4: Verify audit log ghi nhận mọi actions
TC-4.1.5: Chọn template — verify template_id lưu đúng
```

### US-4.2: Quản lý Hóa đơn
**As a** Finance Staff, **I want to** tạo hóa đơn với VAT/WHT, **so that** quyết toán chính xác.

**Acceptance Criteria:**
- Invoice states: Draft → Posted → Paid → Cancelled/Refunded
- Auto-calculate: VAT = subtotal * rate/100, WHT = subtotal * rate/100
- Total = subtotal + VAT - WHT
- Invoice lines: description, qty, unit_price, amount

**Test Cases:**
```
TC-4.2.1: Tạo invoice subtotal 1M, VAT 7% — verify VAT = 70K
TC-4.2.2: Invoice với WHT 5% — verify total = 1M + 70K - 50K = 1.02M
TC-4.2.3: Post → Pay → verify state transitions
TC-4.2.4: Cancel invoice — verify state = 'cancelled'
TC-4.2.5: Thêm 2 invoice lines — verify amount = qty * unit_price
```

### US-4.3: Quản lý Thanh toán
**As a** Finance Staff, **I want to** ghi nhận thanh toán, **so that** theo dõi thu tiền.

**Acceptance Criteria:**
- 6 payment methods: wallet/bank/QR/mobile/umoney/cash
- Confirm payment → invoice tự chuyển sang "Paid"
- Auto-generate payment code (PAY-XXXX)

**Test Cases:**
```
TC-4.3.1: Tạo payment QR — verify code auto-generated
TC-4.3.2: Confirm payment — verify invoice.state = 'paid'
TC-4.3.3: Fail payment — verify payment.state = 'failed', invoice không đổi
TC-4.3.4: Tất cả 6 payment methods — verify tạo được
```

### US-4.4: Cấu hình VAT/WHT/Exchange Rate
**As a** Admin, **I want to** cấu hình thuế và tỷ giá, **so that** hóa đơn đúng quy định.

**Acceptance Criteria:**
- VAT/WHT: name, rate, date range
- Exchange rate: date, buy_rate, sell_rate, source (BCEL)
- Weekend logic: T7/CN dùng tỷ giá ngày gần nhất

**Test Cases:**
```
TC-4.4.1: Tạo VAT config 7% — verify rate = 7.0
TC-4.4.2: Tạo exchange rate ngày 14/6 và 17/6 — query ngày 15/6 (T7) → verify dùng rate ngày 14/6
TC-4.4.3: Query exchange rate ngày 20/6 (sau 17/6) → verify dùng rate ngày 17/6
```

### US-4.5: Tích hợp VOffice
**As a** Sales Staff, **I want to** gửi hợp đồng lên VOffice để ký, **so that** ký số được thực hiện.

**Acceptance Criteria:**
- Config: api_url, api_user, api_password
- Upload document → Send and sign → Check status
- Ký xong → contract tự chuyển sang "Signed", file signed lưu về
- Bị reject → ghi lý do vào error_message

**Test Cases:**
```
TC-4.5.1: Tạo VOffice config — verify connection fields
TC-4.5.2: VOffice sign record — verify status = 'draft'
TC-4.5.3: Upload + send — verify status = 'sent'
TC-4.5.4: Published → verify contract signed, signed_file lưu về
TC-4.5.5: Rejected → verify error_message có lý do
```

---

## Module 5: `tsc_crm_commission` — Commission

### US-5.1: Cấu hình Commission Rules
**As a** Admin, **I want to** cấu hình quy tắc hoa hồng, **so that** tính tự động khi có thanh toán.

**Acceptance Criteria:**
- Commission type: percentage/fixed
- Target group: am/agency/staff/management
- Có thể filter theo service, package, agency
- Min/max revenue range

**Test Cases:**
```
TC-5.1.1: Rule percentage 5% cho agency — verify rate = 5.0
TC-5.1.2: Rule fixed 100K cho staff — verify rate = 100000
TC-5.1.3: Tất cả target groups — verify tạo được
```

### US-5.2: Tính Commission tự động
**As a** Finance Staff, **I want to** commission tự tính khi invoice paid, **so that** hoa hồng đúng hạn.

**Acceptance Criteria:**
- Gọi `compute_commission(invoice)` khi invoice paid
- Percentage: amount = subtotal * rate / 100
- Fixed: amount = rate
- Tạo commission record với state = 'draft'

**Test Cases:**
```
TC-5.2.1: Invoice 1M, rule 5% — verify commission = 50K
TC-5.2.2: Invoice 1M, rule fixed 100K — verify commission = 100K
TC-5.2.3: Invoice chưa paid — verify không tạo commission
TC-5.2.4: Approve → Pay — verify state transitions
```

---

## Module 6: `tsc_crm_admin` — Administration

### US-6.1: Quản lý Organization hierarchy
**As a** Admin, **I want to** quản lý cấu trúc tổ chức 4 cấp, **so that** phân quyền theo đơn vị.

**Acceptance Criteria:**
- 4 cấp: TSC (HQ) → tỉnh → mường → bản
- 3 khối: Business / Technical / CC
- name_get hiển thị hierarchical

**Test Cases:**
```
TC-6.1.1: Tạo 4 cấp hierarchy — verify parent/child relationships
TC-6.1.2: name_get cấp 3 — verify "TSC / Vientiane / Saysettha"
TC-6.1.3: Tất cả divisions — verify business/technical/cc
```

### US-6.2: Quản lý Role & Permission
**As a** Admin, **I want to** phân quyền chi tiết, **so that** mỗi role có đúng quyền.

**Acceptance Criteria:**
- Role: name, code, permissions
- Permission: name, code, model, operation (CRUD)
- Mapping: role ↔ permission (unique constraint)
- Phase 1: Admin/Manager/Staff

**Test Cases:**
```
TC-6.2.1: Tạo role + permission + map — verify permission_ids cập nhật
TC-6.2.2: Map trùng role+permission — verify unique constraint error
TC-6.2.3: Permission với operation CRUD — verify 4 operations
```

---

## Module 7: `tsc_crm_integration` — Integration

### US-7.1: Quản lý Notification Templates
**As a** Admin, **I want to** cấu hình mẫu thông báo, **so that** thông báo tự động gửi.

**Acceptance Criteria:**
- Channel: sms/email/push
- Trigger: new_order, order_assigned, order_transferred, order_overdue, contract_signed, invoice_created, payment_received
- Template có subject, body

**Test Cases:**
```
TC-7.1.1: Tạo template SMS cho new_order — verify lưu đúng
TC-7.1.2: Tất cả trigger events — verify 7 triggers
TC-7.1.3: Notification log states: pending/sent/failed — verify tạo được
```

### US-7.2: Frontend — Xem dịch vụ
**As a** Customer, **I want to** xem danh sách dịch vụ trên web, **so that** tôi biết TSC cung cấp gì.

**Acceptance Criteria:**
- GET /services — hiển thị danh sách active services
- GET /services/<id> — chi tiết service, packages, levels
- Không cần đăng nhập

**Test Cases:**
```
TC-7.2.1: Truy cập /services — verify hiển thị services active
TC-7.2.2: Truy cập /services/999 — verify 404
TC-7.2.3: Xem chi tiết service — verify packages hiển thị
```

### US-7.3: Frontend — Tạo Order
**As a** Customer, **I want to** tạo order từ web, **so that** tôi không cần gọi điện.

**Acceptance Criteria:**
- GET /order/create — form chọn service, region, notes
- Cần đăng nhập
- POST tạo order trong CRM

**Test Cases:**
```
TC-7.3.1: Truy cập /order/create — verify form hiển thị
TC-7.3.2: Chưa đăng nhập — verify redirect login
```

### US-7.4: Frontend — Xem Invoice
**As a** Customer, **I want to** xem hóa đơn trên web, **so that** tôi kiểm tra thanh toán.

**Acceptance Criteria:**
- GET /invoice/<code> — hiển thị invoice details, lines, totals
- Cần đăng nhập

**Test Cases:**
```
TC-7.4.1: Truy cập /invoice/INV-0001 — verify invoice details
TC-7.4.2: Invoice không tồn tại — verify 404
```

---

## Cross-Cutting: i18n

### US-8.1: Đa ngôn ngữ
**As a** User, **I want to** chuyển đổi ngôn ngữ, **so that** tôi dùng bằng tiếng mình hiểu.

**Acceptance Criteria:**
- Hỗ trợ: English (default), Lao (lo), Vietnamese (vi)
- Field labels, selection labels, view strings đều translate
- Mỗi module có .pot + lo.po + vi.po

**Test Cases:**
```
TC-8.1.1: Switch sang Vietnamese — verify menu "Services" → "Dịch vụ"
TC-8.1.2: Switch sang Lao — verify labels hiển thị Lao
TC-8.1.3: Kiểm tra .pot có đầy đủ strings
```

---

## Tổng kết

| Module | User Stories | Test Cases |
|--------|-------------|------------|
| tsc_crm | 6 | 21 |
| tsc_crm_auth | 4 | 14 |
| tsc_crm_service | 5 | 16 |
| tsc_crm_workflow | 5 | 22 |
| tsc_crm_commission | 2 | 7 |
| tsc_crm_admin | 2 | 6 |
| tsc_crm_integration | 4 | 10 |
| i18n | 1 | 3 |
| **Total** | **29** | **99** |
