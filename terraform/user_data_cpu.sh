#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

echo "Starting CPU benchmark bootstrap"

dnf update -y
dnf install -y python3 python3-pip

mkdir -p /home/ec2-user/ml-benchmark
cat > /home/ec2-user/ml-benchmark/benchmark.py.b64 <<'EOF'
${benchmark_b64}
EOF
base64 -d /home/ec2-user/ml-benchmark/benchmark.py.b64 > /home/ec2-user/ml-benchmark/benchmark.py
rm -f /home/ec2-user/ml-benchmark/benchmark.py.b64
chown -R ec2-user:ec2-user /home/ec2-user/ml-benchmark

sudo -u ec2-user python3 -m pip install --user --upgrade pip
sudo -u ec2-user python3 -m pip install --user lightgbm scikit-learn pandas numpy

echo "CPU benchmark bootstrap complete"
