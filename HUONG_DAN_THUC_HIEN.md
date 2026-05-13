# Hướng dẫn chạy và thực hiện bài SonarQube

File này hướng dẫn từng bước để bạn thực hiện bài **Continuous Code Quality with SonarQube** và chuẩn bị đầy đủ minh chứng nộp bài.

## 1. Mục tiêu bài làm

Bạn cần chứng minh rằng project có:

- SonarQube server chạy local bằng Docker.
- Project SonarQube được tạo thủ công.
- File `sonar-project.properties`.
- Test coverage bằng `pytest-cov`.
- SonarQube analysis chạy thành công.
- GitHub Actions workflow `.github/workflows/sonarqube.yml`.
- Quality Gate được cấu hình và enforced.
- Ít nhất 5 code issues được phân tích và sửa.
- Screenshot Quality Gate pass và fail.
- README có hướng dẫn setup.

## 2. Cài dependencies local

Trong thư mục project, chạy:

```bash
python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```
```

## 3. Chạy test và tạo coverage report

```bash
pytest --cov=src --cov-report=xml --cov-report=term-missing --junitxml=test-results.xml
```

Sau khi chạy xong, cần có:

```text
coverage.xml
test-results.xml
```

Nếu test pass và coverage trên 80%, bạn đã đáp ứng phần coverage.

## 4. Chạy SonarQube bằng Docker

Chạy lệnh đúng theo đề:

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -v sonarqube_data:/opt/sonarqube/data \
  sonarqube:2026.1-community
```

Đợi 1-2 phút, sau đó mở:

```text
http://localhost:9000
```

Đăng nhập mặc định:

```text
Username: admin
Password: admin
```

Sau đó đổi password admin.

Nếu cần xem log:

```bash
docker logs -f sonarqube
```

## 5. Tạo project trong SonarQube

Trong giao diện SonarQube:

1. Chọn tạo project mới.
2. Chọn manual setup.
3. Đặt project key:

```text
SonarQube-Code-Quality
```

4. Đặt project name:

```text
SonarQube Code Quality
```

5. Generate token.
6. Copy token và lưu lại cẩn thận.

Không chụp lộ token.

## 6. Kiểm tra file sonar-project.properties

Project đã có file:

```text
sonar-project.properties
```

Nội dung chính:

```properties
sonar.projectKey=SonarQube-Code-Quality
sonar.projectName=SonarQube Code Quality
sonar.sources=src
sonar.tests=tests
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml
```

Nếu bạn dùng project key khác trong SonarQube, hãy sửa lại dòng:

```properties
sonar.projectKey=...
```

cho trùng với project key thật.

## 7. Chạy local SonarQube analysis

Trước tiên tạo coverage:

```bash
pytest --cov=src --cov-report=xml --cov-report=term-missing
```

Nếu bạn dùng macOS hoặc Windows Docker Desktop:

```bash
MSYS_NO_PATHCONV=1 docker run --rm \
-e SONAR_HOST_URL="http://host.docker.internal:9000" \
-e SONAR_TOKEN="<YOUR_TOKEN>" \
-v "/$(pwd):/usr/src" \
-w /usr/src \
sonarsource/sonar-scanner-cli \
-Dsonar.projectBaseDir=/usr/src

```

Sau khi chạy xong, quay lại dashboard SonarQube để xem kết quả.

Bạn cần chụp screenshot:

- Project dashboard.
- Metrics: bugs, vulnerabilities, code smells, coverage, duplications.
- Quality Gate status.

## 7.1 Troubleshooting (Git Bash + Docker Desktop)

Neu gap loi `401 Unauthorized`:

```text
Failed to query server version ... HTTP 401 Unauthorized
```

Token SonarQube khong hop le. Hay tao token moi trong SonarQube va thay lai `SONAR_TOKEN`.

Neu gap loi `Project root configuration file: NONE`, kiem tra volume mount:

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "/$(pwd):/usr/src" sonarsource/sonar-scanner-cli ls -la /usr/src
```

Output phai co file `sonar-project.properties`.

## 8. Tạo Quality Gate custom

Trong SonarQube:

```text
Quality Gates -> Create
```

Đặt tên ví dụ:

```text
Custom Python Quality Gate
```

Thêm điều kiện:

| Metric | Operator | Value |
|---|---|---|
| New Bugs | is greater than | 0 |
| New Vulnerabilities | is greater than | 0 |
| New Code Coverage | is less than | 80 |
| New Duplicated Lines (%) | is greater than | 3 |

Nói cách khác, yêu cầu mong muốn là:

```text
New Bugs = 0
New Vulnerabilities = 0
New Code Coverage >= 80%
New Duplicated Lines <= 3%
```

Sau đó apply Quality Gate này cho project `SonarQube-Code-Quality`.

## 9. Tạo screenshot Quality Gate fail

Code cuối cùng trong `src/` đang là code sạch để pass. Để tạo minh chứng fail, bạn dùng file lỗi mẫu:

```text
examples/issues_before.py
```

Copy vào source để SonarQube phân tích:

```bash
cp examples/issues_before.py src/sonarqube_code_quality/issues_before.py
```

Chạy lại test coverage:

```bash
pytest --cov=src --cov-report=xml --cov-report=term-missing
```

Chạy lại SonarQube scanner:

```bash
MSYS_NO_PATHCONV=1 docker run --rm \
  -e SONAR_HOST_URL="http://host.docker.internal:9000" \
  -e SONAR_TOKEN="<YOUR_TOKEN>" \
  -v "/$(pwd):/usr/src" \
  -w /usr/src \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectBaseDir=/usr/src
```


Sau đó chụp screenshot Quality Gate fail hoặc issues mới được phát hiện.

## 10. Sửa lỗi để Quality Gate pass

Xóa file lỗi vừa copy:

```bash
rm src/sonarqube_code_quality/issues_before.py
```

Chạy lại:

```bash
pytest --cov=src --cov-report=xml --cov-report=term-missing
MSYS_NO_PATHCONV=1 docker run --rm \
  -e SONAR_HOST_URL="http://host.docker.internal:9000" \
  -e SONAR_TOKEN="<YOUR_TOKEN>" \
  -v "/$(pwd):/usr/src" \
  -w /usr/src \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectBaseDir=/usr/src
```

Chụp screenshot Quality Gate pass.

Các lỗi đã sửa được mô tả trong:

```text
docs/ISSUE_FIXES.md
```

## 11. Cấu hình GitHub Actions

Workflow đã có sẵn:

```text
.github/workflows/sonarqube.yml
```

Workflow này:

- Chạy khi push vào `main`.
- Chạy khi mở pull request vào `main`.
- Chạy Black và Ruff.
- Chạy pytest coverage.
- Chạy SonarQube scan.
- Check Quality Gate.
- Fail nếu Quality Gate fail.

## 12. Tạo GitHub secrets

Vào GitHub repo:

```text
Settings -> Secrets and variables -> Actions -> New repository secret
```

Tạo:

```text
SONAR_TOKEN
```

Giá trị là token từ SonarQube.

Tạo tiếp:

```text
SONAR_HOST_URL
```

Nếu dùng self-hosted runner trên máy đang chạy SonarQube:

```text
http://localhost:9000
```

Nếu dùng URL public/tunnel:

```text
https://your-sonarqube-url
```

## 13. Lưu ý quan trọng về GitHub Actions

Nếu SonarQube chạy local ở `localhost:9000`, GitHub-hosted runner như `ubuntu-latest` sẽ không truy cập được.

Vì vậy file workflow đang dùng:

```yaml
runs-on: self-hosted
```

Bạn cần cài GitHub self-hosted runner trên máy của bạn.

Cách làm:

1. Vào GitHub repository.
2. Chọn `Settings`.
3. Chọn `Actions`.
4. Chọn `Runners`.
5. Chọn `New self-hosted runner`.
6. Làm theo hướng dẫn GitHub hiển thị cho hệ điều hành của bạn.
7. Start runner.
8. Push code để workflow chạy.

Nếu giảng viên cho phép dùng SonarCloud hoặc bạn expose SonarQube ra public URL, bạn có thể đổi:

```yaml
runs-on: self-hosted
```

thành:

```yaml
runs-on: ubuntu-latest
```

## 14. Cài SonarLint để lấy bonus

Nếu muốn lấy bonus +10:

1. Mở VS Code hoặc PyCharm.
2. Cài extension/plugin SonarLint.
3. Connect SonarLint tới SonarQube server.
4. Bind project với project key `SonarQube-Code-Quality`.
5. Chụp screenshot SonarLint đã connected và đang phân tích project.

## 15. Checklist screenshot cần nộp

Bạn nên chuẩn bị các screenshot sau:

```text
1. Docker container SonarQube đang chạy
2. SonarQube dashboard sau khi setup
3. Project SonarQube đã được tạo
4. Local analysis thành công
5. Coverage report trong SonarQube
6. Issues before fixing
7. Bảng hoặc file docs/ISSUE_FIXES.md
8. Quality Gate Failed
9. Quality Gate Passed
10. GitHub Actions workflow chạy thành công
11. Repository secrets đã cấu hình, không lộ giá trị
12. SonarLint connected nếu làm bonus
```

## 16. Cách push lên GitHub

```bash
git init
git add .
git commit -m "Initial SonarQube code quality assignment"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

## 17. Những gì cần nộp

Nộp:

```text
1. GitHub repository URL
2. Source code có sonar-project.properties
3. .github/workflows/sonarqube.yml
4. README.md
5. HUONG_DAN_THUC_HIEN.md
6. Screenshot SonarQube dashboard
7. Screenshot Quality Gate pass
8. Screenshot Quality Gate fail
9. Screenshot GitHub Actions workflow
10. Documentation before/after: docs/ISSUE_FIXES.md
11. Screenshot SonarLint nếu làm bonus
```
