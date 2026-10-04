# Day 16 — Báo cáo benchmark LightGBM

- Họ và tên: **Lê Văn Tài**
- MSSV: **2A202602464**

1. Tôi chọn **Google Cloud Platform (GCP)**, region/zone `us-central1` / `us-central1-a`, máy `e2-medium`, source commit `61257f8` cộng các thay đổi cục bộ trong working tree.
2. Tôi tải `mlg-ulb/creditcardfraud` bằng Kaggle Legacy API Key trên VM; dataset có 284.807 dòng, 31 cột và 492 giao dịch gian lận.
3. Dữ liệu được chia stratified 60% train / 20% validation / 20% test với seed 16; validation dùng early stopping, test chỉ đánh giá cuối.
4. Load dữ liệu mất **2.213283 giây**; training mất **2.916045 giây**; best iteration là **68**.
5. AUC **0.976848**, Accuracy **0.999508**, F1 **0.847826**, Precision **0.906977**, Recall **0.795918** trên tập test; AUC dùng xác suất dự đoán.
6. Latency một dòng là **0.898412 ms**; throughput batch 1.000 dòng là **369092.763 dòng/giây**; dùng median, warm-up nằm ngoài phép đo.
7. CPU/RAM/Network được quan sát **sau** benchmark lúc `2026-10-04 04:01:10 UTC`: CPU snapshot 33.3% user/66.7% idle, RAM 3.8 GiB tổng và 486 MiB đã dùng; bằng chứng: `submission/resource_snapshot_after.txt` và ảnh `submission/screenshots/02_resource_snapshot.png`.
8. Trang Welcome của project hiển thị **₫7.791.151 credit, ₫0 đã dùng, hết hạn 2027-01-02**; Payment overview cũng hiển thị khoản manual payment credit **−₫800.000**. Đã chạy `terraform destroy -auto-approve` sau benchmark: Terraform xác nhận **16 resources destroyed**; `terraform state list` rỗng và kiểm tra GCP sau destroy không còn VM, forwarding rule hay mạng `ai-vpc` của lab (mạng `default` mặc định của project vẫn còn).

>
