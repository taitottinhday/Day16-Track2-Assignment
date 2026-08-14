# Cost safety status

Final status after the Day 16 run:

- Terraform destroyed all 16 lab resources.
- VM count: 0.
- Persistent disk count: 0.
- reserved/external address count: 0.
- Cloud NAT/router, load balancer, forwarding rule, and custom VPC count: 0.
- Terraform state resource count: 0.
- Cloud Billing is unlinked from the project: `billingEnabled = false`.

The 100,000 VND budget is an alert, not a hard spending cap. Google documents that budgets do not automatically prevent usage or billing. Billing was therefore disabled after the lab to stop future billable Google Cloud usage in this project.

The required lab architecture is not a fully Free Tier architecture. It uses an `e2-medium`, SSD disk, Cloud NAT, and an external HTTP Load Balancer. Google's Compute Engine Free Tier is limited to an eligible `e2-micro` VM and other product-specific limits. Do not run `terraform apply` again unless you intentionally re-enable Billing and accept short-lived lab charges.

Official references:

- https://cloud.google.com/billing/docs/how-to/budgets
- https://cloud.google.com/billing/docs/how-to/modify-project
- https://cloud.google.com/free/docs/free-cloud-features

Billing reports can be delayed. Usage incurred before Billing was disabled can still appear later; disabling Billing prevents new billable usage but does not erase already-incurred charges.
