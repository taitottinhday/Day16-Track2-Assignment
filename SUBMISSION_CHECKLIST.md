# Checklist chạy và nộp riêng — Lê Văn Tài — 2A202602464

Repository này hiện có hướng dẫn chi tiết cho **nhánh GCP CPU**. Nếu bạn chọn Azure, dùng phần Azure trong `README_other_clouds.md` và thay các lệnh/chụp bằng bằng chứng Azure tương ứng. Các kết quả cũ từ bản clone đã bị loại bỏ; chỉ kết quả tạo trong tài khoản cloud của bạn mới được đặt vào `submission/`.

1. Trên laptop (WSL/Bash), dùng Google account và Project ID của bạn, bật API, rồi trong `terraform-gcp/` chạy `terraform init`, `terraform validate`, `terraform plan`, `terraform apply`. Giữ `TF_VAR_project_id="<PROJECT_ID>"` trong cùng terminal.
2. SSH bằng IAP theo `terraform output iap_ssh_command`. Chờ startup script: `sudo systemctl status google-startup-scripts.service --no-pager` và `sudo journalctl -b -u google-startup-scripts.service -n 60 --no-pager`. Chỉ tiếp tục khi log cho biết startup kết thúc thành công.
3. Trên VM, tạo `~/.kaggle/kaggle.json` bằng **Kaggle Legacy API Key**, đặt quyền `700` cho thư mục và `600` cho file, rồi chạy `kaggle datasets download -d mlg-ulb/creditcardfraud --unzip -p ~/ml-benchmark/`.
4. Copy `benchmark.py` từ repo vào `~/ml-benchmark/`, chạy `python3 benchmark.py`, rồi xác minh `python3 -m json.tool benchmark_result.json`. Script bắt buộc đúng dataset Kaggle 284.807 × 31 và sẽ dừng nếu file khác.
5. Khi benchmark đang chạy, chụp `top`, `free -h`, `ip -s link`; chụp Billing Reports có scope Project và ngày làm lab. Ghi rõ nếu Billing chưa cập nhật.
6. Trước khi destroy, tải `benchmark.py` và `benchmark_result.json` về `submission/` bằng `gcloud compute scp ... --tunnel-through-iap`. Copy `terraform-gcp/*.tf` và `terraform-gcp/user_data*.sh` vào `submission/infra/`; đặt ảnh do bạn chụp vào `submission/screenshots/`.
7. Điền số thực đo vào `DAY16_REPORT.md`, copy thành `submission/report.md`, sau đó chạy `terraform destroy` và `terraform state list`. Không nộp `.terraform/`, `*.tfstate*`, `*.tfvars`, credentials, SSH keys hoặc `creditcard.csv`.
