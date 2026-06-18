# Day16 CPU Fallback Report

Ho ten: Nguyễn Bách Điệp
Ma hoc vien: 2A202600535

Do AWS GPU quota `Running On-Demand G and VT instances` chua duoc duyet, bai lab duoc thuc hien theo phuong an CPU fallback.
Tai khoan AWS hien chi cho tao instance Free Tier, nen `r5.2xlarge` bi AWS tu choi voi loi `instance type is not eligible for Free Tier`; vi vay thuc nghiem duoc chay tren `t3.micro`.
Ha tang van duoc tao bang Terraform: VPC rieng, private subnet, NAT Gateway, Application Load Balancer, IAM role va EC2 CPU node trong private subnet.
De truy cap node rieng, bai lam dung AWS Systems Manager thay cho Bastion EC2 de tranh vuot quota va khong mo SSH public.
Benchmark su dung LightGBM voi dataset Kaggle `mlg-ulb/creditcardfraud`, file `creditcard.csv` gom 284,807 giao dich thuc va 30 feature.
Ket qua: load data 2.8524s, training 3.2048s, best iteration 19, AUC-ROC 0.949838, accuracy 0.996032.
F1-score dat 0.429293, precision 0.285235, recall 0.867347.
Inference latency cho 1 dong la 1.3343 ms; throughput cho 1000 dong la 458,910.32 rows/s.
Ket qua chi tiet da duoc luu trong `results/benchmark_result.json`; log terminal nam trong `results/benchmark_stdout.txt`.
Sau khi chup man hinh va nop bai, can chay `terraform destroy` ngay de xoa NAT Gateway, ALB va EC2.
