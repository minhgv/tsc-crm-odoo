# KẾ HOẠCH DỰ KIẾN TRIỂN KHAI TSC-CRM

## 1. Requirement & Design

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 1.1 | Chốt mô hình triển khai | |
| 1.2 | Sequence/flow diagram và tài liệu giải pháp | |

## 2. Service Management: Khai báo và quản lý dịch vụ

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 2.1 | Thông tin cơ bản | Service Code, Service Name, Service Type, Logo, Icon, Banner, Hình ảnh/video giới thiệu |
| 2.2 | Nội dung giới thiệu | Slogan, Description, Benefit, Policy |
| 2.3 | Kênh bán | MiniApp, Website |
| 2.4 | Các trạng thái dịch vụ | Pending/Active/Inactive. Admin chuyển trạng thái. Khi Active→Inactive phải inactive tất cả package trước |

## 3. Package Management: Khai báo và quản lý gói cước, Product trong gói cước

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 3.1 | Thông tin cơ bản | Package Code, Package Name, Logo, Mô tả, Hình ảnh/video giới thiệu |
| 3.2 | Product và giá | Một gói cước có 1 hoặc nhiều Product, mỗi Product có mức giá khác nhau. Phí triển khai, lắp đặt |
| 3.3 | Chu kỳ gói cước (Loại gói cước) | Theo lần, Theo chu kỳ (Ngày/tuần/tháng/3 tháng/6 tháng/9 tháng/1 năm), Thời gian dùng thử |
| 3.4 | Các trạng thái của gói cước | Pending/Active/Inactive. Admin chuyển trạng thái |

## 4. Combo Product: Khai báo và quản lý dịch vụ, gói cước combo

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 4.1 | Tạo Combo | Chọn nhiều Service, Package để tạo thành dịch vụ/gói cước combo |

## 5. ORDER & WORKFLOW Management: Quản lý giao dịch

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 5.1 | Tạo Order | Một order có 1 hoặc nhiều line, mỗi line tương ứng 1 dịch vụ/gói cước |
| 5.2 | Order Assignment (Giao việc) | Hệ thống tự động giao cho Sales staff. Quá hạn → auto assign Admin. Admin/quản lý giao việc |
| 5.3 | Workflow Tracking (Status) | Created → Assigned (Sale staff) → Accepted (Sale staff) → Surveying (optional, Technical staff) → Confirm → Contract → Paid |
| 5.4 | Technical Task | Admin/Sales staff tạo task, giao cho Technical staff |
| 5.5 | SLA Tracking | Thời gian tiếp nhận, Khảo sát/Tư vấn, Triển khai, Hợp đồng, Thanh toán |

## 6. Customer Management: Quản lý khách hàng

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 6.1 | Profile khách hàng | Tên, Mã khách hàng, Email, Phone number, Địa chỉ, Loại KH (Cá nhân/hộ kinh doanh, Doanh nghiệp, Tổ chức chính phủ) |
| 6.2 | Lịch sử giao dịch | Lịch sử đăng ký dịch vụ, hợp đồng, thanh toán/hóa đơn |

## 7. KPI Management: Admin cấu hình các tham số SLA

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 7.1 | Các tham số | Thời gian tiếp nhận (từ KH order hoặc nhắc nhở gia hạn), Thời gian Khảo sát/Tư vấn, Triển khai, Hợp đồng, Thanh toán |

## 8. Contract Management: Quản lý hợp đồng (Phase 1 chỉ upload file)

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 8.1 | Thông tin cơ bản | |
| 8.2 | Commercial & Billing | Tính "giá trị hợp đồng" & báo cáo tài chính |
| 8.3 | Performance | Trạng thái: chưa triển khai / đang triển khai-thanh toán / đã hoàn thành |
| 8.4 | Trường quản trị & audit (Governance) | |
| 8.5 | Tạo hợp đồng | Hệ thống tự gen theo template và thông tin trên hệ thống |
| 8.6 | Contract Repository | Upload Scan, Download |

## 9. Promotion Management: Khai báo và quản lý khuyến mại

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 9.1 | Kiểu khuyến mại | Cố định số tiền, Tỷ lệ % theo giá gói |
| 9.2 | Phạm vi | Theo giao dịch (line), Theo gói cước, Theo dịch vụ |
| 9.3 | Thời hạn khuyến mại | From date to date |

## 10. Discount Policy: Khai báo và quản lý hoa hồng cho Agent, tỷ lệ chiết khấu

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 10.1 | Kiểu chiết khấu | Theo doanh thu, Theo số đơn hàng (order) |
| 10.2 | Mức chiết khấu | Cố định số tiền, Tỷ lệ % |
| 10.3 | Phạm vi | Chung cho tất cả Agent, Theo từng Agent cụ thể |

## 11. BILLING & PAYMENT

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 11.1 | Invoice | Invoice List, Invoice Detail |
| 11.2 | VAT | VAT History, Effective Date |
| 11.3 | WHT | WHT History, Effective Date |
| 11.4 | Exchange Rate | Daily Exchange Rate, Effective Date |
| 11.5 | Payment | Create Payment, Payment History |

## 12. ADMINISTRATION

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 12.1 | User Management | Login bằng Laoid. Danh sách, Thêm, Cập nhật, Khóa/Mở khóa User |
| 12.2 | Organization Management | Phòng ban: TSC → tỉnh → mường → bản. Khối: Kinh doanh / Kỹ thuật / CC |
| 12.3 | Role & Permission | Phase 1: Admin/Manager/Staff. Role, Permission, Mapping (assign permission for Role, User) |

## 13. Integration Hub: Phase 1 chỉ BCCS3 Connector

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 13.1 | ERP Connector | |
| 13.2 | BCCS3 Connector | Phase 1 |
| 13.3 | Unipay Connector | |
| 13.4 | ILP Connector | |

## 14. Notification Center: Phase 2

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 14.1 | SMS | |
| 14.2 | Email | |
| 14.3 | Push Notification | |
| 14.4 | Web Notification | |

## 15. Reporting & Dashboard: P1 làm một số báo cáo cơ bản

| TT | Nội dung | Chi tiết |
|----|----------|----------|
| 15.1 | Dashboard | |
| 15.2 | KPI | |
| 15.3 | Sales Report | |
| 15.4 | SLA Report | |
| 15.5 | Revenue Report | |
| 15.6 | Commission Report | |

## 16. API cho bên thứ 3

## 17. Portal
