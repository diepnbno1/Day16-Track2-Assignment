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

## Minh chung

- `GPU quota.JPG`: GPU quota bang 0 va request 4 vCPU dang `Case Opened`.
- `EC2 instance.JPG`: EC2 CPU node dang chay.
- `benchmark.JPG`: ket qua `benchmark_result.json`.
- `benchmark-2.JPG`: log LightGBM benchmark.
- `command ID.JPG`: AWS Systems Manager command thanh cong.
- `bill.JPG`: AWS Billing/Bills.

## File chinh

- `terraform/`: ma nguon Terraform da chinh cho CPU fallback.
- `terraform/benchmark.py`: benchmark LightGBM.
- `benchmark_result.json`: metrics day du.
- `benchmark_stdout.txt`: output benchmark.
- `cpu_fallback_report.md`: bao cao ngan.
