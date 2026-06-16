# TSC-CRM — Odoo 18 CRM Module

Hệ thống CRM tích hợp cho viễn thông và giải pháp số — TSC/Unitel.

## Tổng quan

Hệ thống CRM-TSC là nền tảng tích hợp CRM + Order + Workflow + Integration chuyên biệt cho dịch vụ viễn thông và giải pháp số. Xây dựng trên Odoo 18.

**Mục tiêu:**
- Quản lý dịch vụ, gói cước, khuyến mại và combo linh hoạt
- Vận hành quy trình khép kín: Order → Hợp đồng → Thanh toán → Hóa đơn
- Tính hoa hồng tự động cho đa đối tượng
- Tích hợp hệ sinh thái: Unipay, BCCS3, LaoID, VOffice

## Cấu trúc module

```
addons/
├── tsc_crm/              # Core: Lead, Order, Region, Employee, Dashboard
├── tsc_crm_service/      # Dịch vụ: Service, Package, Combo, Discount, Agency
├── tsc_crm_workflow/     # Quy trình: Contract, Invoice, Payment, VAT/WHT, SLA, VOffice
├── tsc_crm_auth/         # Xác thực: OTP, LaoID SSO, Customer Registration
├── tsc_crm_commission/   # Hoa hồng: Commission rules & auto-calculation
└── tsc_crm_integration/  # Tích hợp: Notification, Landing Page, External APIs
```

## Yêu cầu

- Python 3.10+
- Docker & Docker Compose
- Odoo 18 (hoặc dùng Docker image `odoo:18`)
- PostgreSQL 15

## Cài đặt

### Docker (Khuyến nghị)

```bash
# Clone repository
git clone https://github.com/minhgv/tsc-crm-odoo.git
cd tsc-crm-odoo

# Khởi động Odoo + PostgreSQL
docker compose up -d

# Truy cập Odoo
# URL:      http://localhost:8069
# Database: tsc_crm
# User:     odoo
# Password: odoo
```

### Cài đặt module

```bash
# Cài tất cả module
docker compose exec odoo odoo -d tsc_crm \
  -i tsc_crm,tsc_crm_service,tsc_crm_workflow,tsc_crm_auth,tsc_crm_commission,tsc_crm_integration \
  --stop-after-init

# Hoặc dùng script
./test-docker.sh install
```

### Cài đặt thủ công

```bash
pip install odoo

odoo --addons-path=addons,/path/to/odoo/addons \
  -d tsc_crm \
  -i tsc_crm,tsc_crm_service,tsc_crm_workflow,tsc_crm_auth \
  --dev=xmlrpc
```

## Sử dụng

### Lệnh Docker

```bash
./test-docker.sh up        # Khởi động
./test-docker.sh down      # Dừng
./test-docker.sh install   # Cài module
./test-docker.sh update    # Update module
./test-docker.sh test      # Chạy test
./test-docker.sh reset     # Reset DB và cài lại
./test-docker.sh logs      # Xem log
```

### Lệnh Odoo

```bash
# Update module
odoo -d tsc_crm -u tsc_crm_auth

# Chạy test
odoo -d tsc_crm --test-enable --stop-after-init

# Odoo shell
odoo shell -d tsc_crm
```

## Chức năng chính

### CRM Core (`tsc_crm`)
- Lead/Order management với auto-generated Order ID
- Region hierarchy (tỉnh → huyện → xã)
- SLA deadline & overdue tracking
- Order lines (service + package + quantity + price)
- Dashboard tổng quan

### Service Catalog (`tsc_crm_service`)
- Quản lý dịch vụ (Cloud Server, Camera, MicroData, IPLC, SMS...)
- Quản lý gói cước với nhiều level giá
- Combo nhiều dịch vụ
- Chiết khấu / Khuyến mại / Hoa hồng
- Quản lý đại lý (Agency)

### Workflow (`tsc_crm_workflow`)
- **Hợp đồng**: Draft → Pending Sign → Signed → Scanned → Active
- **Hóa đơn**: VAT/WHT tự động, exchange rate
- **Thanh toán**: Unipay, uMoney, QR, Cash
- **VOffice**: Gửi hợp đồng ký số, theo dõi trạng thái
- **SLA**: Cấu hình thời gian theo stage

### Authentication (`tsc_crm_auth`)
- **LaoID SSO**: Login bằng LaoID quốc gia
- **OTP**: Đăng nhập bằng mã OTP qua SMS
- **Đăng ký**: Customer registration tự động

### Commission (`tsc_crm_commission`)
- Rule hoa hồng theo service/package/agency
- Auto-calculate khi invoice thanh toán

### Integration (`tsc_crm_integration`)
- Notification (SMS/Email)
- Landing page management
- External API integration

## Cấu hình

### LaoID SSO

Vào **Settings > Technical > System Parameters**:

| Key | Value |
|-----|-------|
| `tsc.laoid.client_id` | OAuth client ID |
| `tsc.laoid.client_secret` | OAuth client secret |
| `tsc.laoid.callback_url` | `https://your-domain/auth/laoid/callback` |
| `tsc.laoid.environment` | `production` hoặc `uat` |

### VOffice

Vào **Configuration > VOffice > VOffice Configuration**:
- API URL: `https://crm.laoid.net/apis`
- Username / Password

### VAT / WHT

Vào **Configuration > VAT** và **Configuration > WHT**:
- Tỷ lệ VAT/WHT theo thời gian
- Ví dụ: VAT 7% (01/01-30/04), 10% (01/05-30/11), 7% (01/12-31/12)

### Tỷ giá

Vào **Configuration > Exchange Rates**:
- Cập nhật hàng ngày theo BCEL
- Tự động áp dụng theo ngày xuất hóa đơn

## Tests

```bash
# Chạy tất cả test
docker compose exec odoo odoo -d tsc_crm \
  -i tsc_crm,tsc_crm_service,tsc_crm_workflow,tsc_crm_auth \
  --test-enable --stop-after-init --no-http

# Hoặc
./test-docker.sh test
```

**85 test cases** covering:
- Region, Order Line, Lead, Team, Employee
- Service, Package, Combo, Discount, Agency
- Contract, Invoice, Payment, Config, VOffice
- OTP, Customer Registration, LaoID, Login Log

## License

LGPL-3
