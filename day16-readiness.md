# Day 16 readiness — Lê Văn Tài — 2A202602464

- [ ] Chọn đúng một cloud và xác nhận tài khoản cá nhân, Billing, quota/credit đang hoạt động.
- [ ] Kiểm tra CLI của cloud và Terraform trong WSL/Bash; dùng đúng Project ID hoặc profile của mình.
- [ ] Đã tạo/download Kaggle **Legacy API Key**; không commit `~/.kaggle/kaggle.json`.
- [ ] Đã chạy `terraform init`, `validate`, `plan`, `apply`, rồi SSH được vào compute node private theo nhánh đã chọn.
- [ ] Trên VM, chờ startup script hoàn tất và xác nhận `import lightgbm, sklearn, pandas, numpy` trả `OK`.
- [ ] Đã tải Kaggle `creditcard.csv` gốc và kiểm tra 284.807 dòng, 31 cột, 492 fraud rows.
- [ ] Đã chạy `benchmark.py`, lưu JSON mới, chụp terminal/tài nguyên/Billing của chính mình.
- [ ] Đã copy `benchmark.py` và JSON khỏi VM, `terraform destroy`, kiểm tra state/resource trống, rồi tạo `submission/` không có credentials/state/dataset.
