import re
import subprocess
import os

patch = subprocess.run(["git", "diff", "--unified=15000", "tests_questions_bank_2/"], capture_output=True, text=True).stdout
current_file = None
current_q = None
changed_qs = {} 

for line in patch.splitlines():
    if line.startswith("+++ b/"):
        current_file = line[6:]
        if current_file not in changed_qs:
            changed_qs[current_file] = set()
    elif line.startswith(r"\begin{practiceQuestion}") or line.startswith(r" \begin{practiceQuestion}"):
        m = re.search(r"\\begin\{practiceQuestion\}\{([^}]+)\}", line)
        if m:
            current_q = m.group(1)
    elif line.startswith("-") or line.startswith("+"):
        if not line.startswith("---") and not line.startswith("+++") and current_q and current_file:
            changed_qs[current_file].add(current_q)

# clear existing review data if any
data_file = "build/audit_review_data.json"
if os.path.exists(data_file):
    os.remove(data_file)

# Call build_audit_review.py for each
count = 0
for file, qs in changed_qs.items():
    if qs:
        print(f"Adding from {file}: {', '.join(qs)}")
        cmd = ["python3", "scripts/build_audit_review.py", "add", "--chapter", "Changed Questions", file] + list(qs)
        subprocess.run(cmd, check=True)
        count += 1

if count > 0:
    subprocess.run(["python3", "scripts/build_audit_review.py", "open"], check=True)
else:
    print("No changed questions found!")