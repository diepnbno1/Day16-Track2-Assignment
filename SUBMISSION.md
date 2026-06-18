# Day16 Track 2 Lab Submission

Ho ten: Nguyễn Bách Điệp
Ma hoc vien: 2A202600535

## Phuong an thuc hien

AWS GPU quota `Running On-Demand G and VT instances` chua duoc duyet, request tang quota len 4 vCPU van o trang thai `Case Opened`, nen bai lam su dung phuong an CPU fallback voi LightGBM theo README AWS.

Tai khoan AWS chi cho phep Free Tier instance, nen `r5.2xlarge` bi AWS tu choi. Thuc nghiem duoc chay tren `t3.micro`, nhung van dung Terraform de tao VPC, private subnet, NAT Gateway, Application Load Balancer, IAM role va EC2 CPU node. Truy cap node thong qua AWS Systems Manager.

## Ket qua benchmark

- Dataset: Kaggle `mlg-ulb/creditcardfraud`
- File du lieu: `creditcard.csv`
- So dong: 284,807
- Model: LightGBM binary classifier
- Training time: 3.2048s
- Best iteration: 19
- AUC-ROC: 0.949838
- Accuracy: 0.996032
- F1-score: 0.429293
- Precision: 0.285235
- Recall: 0.867347
- Inference latency 1 row: 1.3343 ms
- Inference throughput 1000 rows: 458,910.32 rows/s

## Cau truc repo

- `evidence/screenshots/`: anh minh chung.
- `results/`: ket qua benchmark va output Terraform/EC2.
- `reports/`: bao cao ngan.
- `terraform/`: ma nguon Terraform va benchmark script.
- `deliverables/`: file zip nop bai.

## Minh chung

- `evidence/screenshots/01_gpu_quota_case_opened.jpg`: GPU quota bang 0 va request 4 vCPU dang `Case Opened`.
- `evidence/screenshots/02_ec2_cpu_instance_running.jpg`: EC2 CPU node dang chay.
- `evidence/screenshots/03_benchmark_result_json.jpg`: ket qua `benchmark_result.json`.
- `evidence/screenshots/04_benchmark_terminal_output.jpg`: log LightGBM benchmark.
- `evidence/screenshots/05_ssm_run_command_success.jpg`: AWS Systems Manager command thanh cong.
- `evidence/screenshots/06_aws_billing_services.jpg`: AWS Billing/Bills.

## File chinh

- `terraform/`: ma nguon Terraform da chinh cho CPU fallback.
- `terraform/benchmark.py`: benchmark LightGBM.
- `results/benchmark_result.json`: metrics day du.
- `results/benchmark_stdout.txt`: output benchmark.
- `reports/cpu_fallback_report.md`: bao cao ngan.
- `deliverables/day16_cpu_fallback_submission.zip`: goi nop bai.
