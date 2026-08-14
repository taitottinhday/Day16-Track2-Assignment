# Day 16 — GCP CPU LightGBM Benchmark Report

## Environment

- Cloud path: Google Cloud Platform
- Region/zone: `us-central1` / `us-central1-a`
- Compute: private `e2-medium` VM, 2 vCPU and approximately 4 GiB RAM
- Access: IAP TCP forwarding; the VM had no public IP
- GPU: disabled (`gpu_count = 0`)
- Model: LightGBM `LGBMClassifier`
- Dataset: ULB Credit Card Fraud Detection, 284,807 rows and 492 fraud rows
- Random seed: 42, stratified 80/20 train/test split

The first complete Terraform apply created 16 resources in approximately 222 seconds. The original Windows checkout converted the startup script to CRLF, so the Debian VM could not execute its shebang. The repository now contains `.gitattributes` to enforce LF for shell scripts. After the corrected VM was created, bootstrap completed successfully and installed LightGBM, scikit-learn, pandas, NumPy, and Kaggle CLI.

## Benchmark results

| Metric | Result |
|---|---:|
| Data load time | 2.458790 s |
| Training time | 8.709089 s |
| Best iteration | `null` (no early stopping configured) |
| AUC-ROC | 0.978262 |
| Accuracy | 0.999508 |
| Precision | 0.864583 |
| Recall | 0.846939 |
| F1-score | 0.855670 |
| One-row mean latency | 0.886496 ms |
| One-row p95 latency | 0.956513 ms |
| 1,000-row batch throughput | 69,087.214 rows/s |

The confusion matrix contained 56,851 true negatives, 13 false positives, 15 false negatives, and 83 true positives. Accuracy alone is misleading because fraud represents only 492 of 284,807 rows. Recall shows that the model found about 84.7% of the fraud cases in the test set, while precision shows that about 86.5% of fraud alerts were correct. AUC-ROC indicates strong ranking performance across thresholds.

During training, the VM reported 0% idle CPU and the Python process used approximately 94% CPU. RAM usage was about 657 MiB of 3.8 GiB, so CPU was the clearer bottleneck while memory had substantial headroom. Batch prediction achieved much higher throughput than repeated single-row prediction because setup and Python-call overhead were amortized across 1,000 rows.

Cloud resources that can contribute to cost even while the benchmark is idle include the VM, 30 GB SSD boot disk, Cloud NAT, and external HTTP Load Balancer. A monthly budget of 100,000 VND with 50%, 90%, and 100% thresholds was created. The billing console still showed 0 VND for this project during evidence capture because cloud cost reporting is delayed.

## Dataset acquisition note

Kaggle CLI authentication was not available on the machine. The run therefore fetched the same public ULB Credit Card Fraud dataset through OpenML. No Kaggle, Hugging Face, cloud credential, Terraform state, or private key is stored in Git.

## Evidence

- `artifacts/benchmark_result.json`: machine-readable benchmark metrics.
- `artifacts/benchmark_terminal_output.txt`: complete benchmark output from the VM.
- `artifacts/resource_snapshot.txt`: CPU, RAM, process, and network snapshot captured during training.
- `artifacts/gcp_vm_details.png`: running private compute instance.
- `artifacts/gcp_monitoring.png`: GCP CPU and network monitoring charts.
- `artifacts/gcp_billing_budget.png`: Billing budget and alert thresholds.
- `artifacts/terraform_destroy_output.txt`: Terraform destroy log (added after cleanup).
- `artifacts/post_destroy_verification.txt`: verification that billable lab resources no longer exist.
