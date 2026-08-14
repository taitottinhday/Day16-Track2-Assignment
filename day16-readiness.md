# Day 16 readiness — 2A202601979

- Cloud path chính: GCP, CPU-only LightGBM.
- Cloud identity: `gcloud` và Application Default Credentials đã xác thực; thông tin nhận dạng được giữ ngoài Git.
- Billing: đã liên kết để chạy Lab, sau đó đã ngắt khỏi project sau khi destroy (`billingEnabled = false`).
- Budget alert: 100.000 VND/tháng; cảnh báo ở 50%, 90% và 100%.
- CLI: Google Cloud CLI hoạt động và project đã được chọn.
- Terraform: v1.15.8; `init`, `fmt -check`, `validate`, `plan`, `apply` đều thành công.
- Local: Python 3.11, Git, curl và Docker hoạt động; `make` còn pending cho Day 18 và không chặn Day 16.
- Secrets: `.env`, state, `.tfvars`, SSH keys và credentials đều bị loại khỏi Git.
- GPU quota: không cần cho luồng bắt buộc; `gpu_count = 0`.
- Fallback: CPU `e2-medium`, đã chạy benchmark thành công.
- Hugging Face: không dùng trong luồng CPU; GPU/vLLM là phần tùy chọn.
