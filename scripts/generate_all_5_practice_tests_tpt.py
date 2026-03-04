import os
import subprocess
import re
import random
from datetime import datetime

STATES = [
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut",
    "delaware", "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa",
    "kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan",
    "minnesota", "mississippi", "missouri", "montana", "nebraska", "nevada", "new-hampshire",
    "new-jersey", "new-mexico", "new-york", "north-carolina", "north-dakota", "ohio", "oklahoma",
    "oregon", "pennsylvania", "rhode-island", "south-carolina", "south-dakota", "tennessee",
    "texas", "utah", "vermont", "virginia", "washington", "west-virginia", "wisconsin", "wyoming"
]

BOOK_TYPE = "5_practice_tests"
DATE_STR = datetime.now().strftime("%Y-%m-%d")
OUT_DIR = f"final_output/{BOOK_TYPE}"
os.makedirs(OUT_DIR, exist_ok=True)

FOOTER = """★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★

<p>
  Looking for more <b>Grade 7 Math</b> resources? Visit my
  <a href="https://www.teacherspayteachers.com/store/viewmath" target="_blank"><b>TPT store</b></a>
  for engaging, classroom-ready materials from <b>View Math</b> — a math education company dedicated to helping students succeed.
</p>

<p>
  Explore more teaching tools and learning materials at
  <a href="https://www.viewmath.com" target="_blank"><b>ViewMath.com</b></a>.
</p>

<p>
  Questions or suggestions? Reach out at
  <a href="mailto:dr.nazari@viewmath.com">dr.nazari@viewmath.com</a>.
</p>

<p>
  <b>Follow me</b> to catch new releases — all <b>50% off</b> for the first 24 hours!
</p>

<p>
  <b>– Dr. A. Nazari</b>
</p>"""

def parse_facts(state_slug):
    cmd = ["python3", ".agents/skills/writing-tpt-description/scripts/get_book_facts.py", BOOK_TYPE, state_slug]
    result = subprocess.run(cmd, capture_output=True, text=True)
    out = result.stdout
    
    data = {"chapters": [], "features": [], "use_cases": [], "series": []}
    
    def extract_line(prefix):
        m = re.search(rf"{prefix}\s+(.*)", out)
        return m.group(1).strip() if m else ""
        
    data["title"] = extract_line("Book Title:")
    # Some titles break onto two lines in the output if terminal wrapped it, so let's get it robustly.
    # Actually wait, terminal wrapping in subprocess.run shouldn't occur unless the script itself wraps it.
    # Let's fix wrapping by removing newlines before parsing or just grab via regex
    # Wait, the script output shows "Book Title:      5 North Carolina NC EOG Grade 7 Math Practice Tests: Extra P\nractice for Test Day"
    # That means the script is printing fixed widths. Let's handle it by reading lines.
    
    lines = out.split('\n')
    current_section = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("Book Title:"):
            data["title"] = re.sub(r'\s+', ' ', line.split("Book Title:")[1].strip())
            # check the next line to see if it's continuing (doesn't start with --- or Key:)
            if i+1 < len(lines) and not ":" in lines[i+1] and not lines[i+1].startswith("---"):
                data["title"] += lines[i+1].strip()
        elif line.startswith("State:"):
            data["state"] = line.split("State:")[1].strip()
        elif line.startswith("Curriculum Name:"):
            data["curriculum"] = line.split("Curriculum Name:")[1].strip()
        elif line.startswith("Curriculum Acronym:"):
            data["curr_acronym"] = line.split("Curriculum Acronym:")[1].strip()
        elif line.startswith("Exam Name:"):
            data["exam_name"] = line.split("Exam Name:")[1].strip()
        elif line.startswith("Exam Acronym:"):
            data["exam_acronym"] = line.split("Exam Acronym:")[1].strip()
        elif line.startswith("Total Topics:"):
            data["total_topics"] = line.split("Total Topics:")[1].strip()
        elif line.startswith("Total Chapters:"):
            data["total_chapters"] = line.split("Total Chapters:")[1].strip()
        elif line.startswith("--- CHAPTERS & TOPICS ---"):
            current_section = "chapters"
        elif line.startswith("--- FEATURES (for this book type) ---"):
            current_section = "features"
        elif line.startswith("--- USE CASES ---"):
            current_section = "use_cases"
        elif line.startswith("--- SERIES CROSS-SELL (other books to mention) ---"):
            current_section = "series"
        elif line.startswith("--- DESIGN & QUALITY"):
            current_section = "design"
        elif line.startswith("---") or line.startswith("==="):
            continue
        elif line:
            if current_section == "chapters" and "topics" in line:
                data["chapters"].append(line)
            elif current_section == "features" and line.startswith("•"):
                data["features"].append(line.replace("•", "").strip())
            elif current_section == "features" and not line.startswith("•") and data["features"]:
                data["features"][-1] += " " + line.strip()
            elif current_section == "use_cases" and line.startswith("•"):
                data["use_cases"].append(line.replace("•", "").strip())
            elif current_section == "use_cases" and not line.startswith("•") and data["use_cases"]:
                data["use_cases"][-1] += " " + line.strip()
            elif current_section == "series" and line.startswith("•"):
                data["series"].append(line.replace("•", "").strip())
            elif current_section == "series" and not line.startswith("•") and data["series"]:
                data["series"][-1] += " " + line.strip()
                
    return data

def generate_html(data):
    # Variety for opening
    openings = [
        f"<p>Get your students ready for test day with five full-length practice tests covering the entire Grade 7 math curriculum. With 150 realistic practice problems and full step-by-step explanations, this resource gives students exactly what they need to build confidence.</p>",
        f"<p>Five full practice exams mean plenty of opportunities to prepare. This resource includes 150 carefully crafted math problems to help your Grade 7 students feel completely ready for test day.</p>",
        f"<p>Make test prep straightforward and effective. Here are 5 complete, full-length practice tests packed with 150 questions and detailed answer explanations to guide your students to success.</p>",
        f"<p>Stop searching for dependable test prep. This practical resource delivers 5 full-length practice exams with 150 questions designed specifically for Grade 7 mathematics, complete with step-by-step solutions.</p>",
        f"<p>Give your students the edge they need with 150 realistic practice problems divided into 5 full-length tests. Every single answer is fully explained so mistakes become learning opportunities.</p>"
    ]
    
    # Variety for Feature Headings
    feat_headings = [
        "<b>Here's What You're Getting</b>",
        "<b>What's Inside</b>",
        "<b>A Quick Look Inside</b>",
        "<b>What You'll Find in This Book</b>",
        "<b>The Highlights</b>"
    ]
    
    # Variety for Test Prep Headings
    test_headings = [
        "<b>Built-In Test Prep</b>",
        "<b>When Test Day Comes</b>",
        "<b>Realistic Exam Practice</b>",
        "<b>True-to-Life Testing Scenarios</b>",
        "<b>Ready for the Big Test</b>"
    ]
    
    # Variety for Use Case Headings
    uc_headings = [
        "<b>Who's This For?</b>",
        "<b>Great For</b>",
        "<b>Works Well For</b>",
        "<b>Who Will Get the Most Out of This</b>",
        "<b>Perfect For</b>"
    ]
    
    # Variety for Curriculum Headings
    curr_headings = [
        f"<b>Made for {data['state']}</b>",
        f"<b>Follows {data.get('curr_acronym', 'State')} Standards</b>",
        f"<b>Written for {data['state']}</b>",
        f"<b>Matches {data['state']}'s Standards</b>",
        f"<b>Crafted Specifically for {data['state']}</b>"
    ]
    
    # Variety for Series Headings
    series_headings = [
        "<b>Want More?</b>",
        "<b>Looking for More Resources?</b>",
        "<b>Check Out the Full Series</b>",
        f"<b>More {data['state']} Resources</b>",
        "<b>Need Lessons Too?</b>"
    ]
    
    # Section: Opening
    opening_html = f"<p><b>{data['title']}</b></p>\n{random.choice(openings)}"
    
    # Section: Features
    feats = data["features"][:]
    # Ensure they are rephrased simply or just kept as is with checkmarks
    random.shuffle(feats)
    # Add mandatory design features
    design_feats = [
        "Colorful pages with illustrations, diagrams, and a friendly owl mascot",
        "Complete answer key with full explanations for every problem",
        "Print and go format — absolutely no prep needed on your part"
    ]
    feats.extend(design_feats)
    random.shuffle(feats)
    
    feat_html = f"<p></p>\n<p>{random.choice(feat_headings)}</p>\n<ul>\n"
    for f in feats:
        feat_html += f"  <li>✅ {f}</li>\n"
    feat_html += "</ul>"
    
    # Section: Chapters & Topics
    chap_headings_options = [
        "<b>All Topics Covered</b>",
        "<b>What's Covered</b>",
        f"<b>{data.get('total_topics', 'All')} Topics, {data.get('total_chapters', 'Several')} Chapters</b>",
        "<b>Here's the Breakdown</b>",
        "<b>Inside the Chapters</b>"
    ]
    
    chap_html = f"<p></p>\n<p>{random.choice(chap_headings_options)}</p>\n"
    chap_html += f"<p>This resource covers all {data.get('total_topics', '56')} Grade 7 math topics:</p>\n<ul>\n"
    for c in data["chapters"]:
        # "Chapter 1: Ratios... — 6 topics" -> "<b>Ch. 1: Ratios...</b> — 6 topics"
        parts = c.split(" — ")
        if len(parts) == 2:
            chap_name = parts[0].replace("Chapter", "Ch.")
            topics = parts[1]
            chap_html += f"  <li><b>{chap_name}</b> — {topics}</li>\n"
        else:
            chap_html += f"  <li>{c}</li>\n"
    chap_html += "</ul>"
    
    # Section: Curriculum
    curr_html = f"<p></p>\n<p>{random.choice(curr_headings)}</p>\n"
    curr_text = f"This isn't just a generic resource. It's built directly from the ground up for <b>{data['state']}</b>. "
    if data.get("curriculum", "(not available)") != "(not available)":
        curr_text += f"It matches the <b>{data['curriculum']}</b> (<b>{data.get('curr_acronym', '')}</b>) perfectly. "
    curr_html += f"<p>{curr_text.strip()}</p>"
    
    # Section: Exam / Test Prep
    exam_html = ""
    if data.get("exam_name") and data.get("exam_name") != "(none)":
        exam_html = f"<p></p>\n<p>{random.choice(test_headings)}</p>\n"
        exam_html += f"<p>Get your students ready for the <b>{data['exam_name']}</b> (<b>{data.get('exam_acronym', '')}</b>). These practice tests simulate real testing conditions so students know what to expect when it matters most.</p>"
    
    # Section: Use Cases
    uc_html = f"<p></p>\n<p>{random.choice(uc_headings)}</p>\n<ul>\n"
    ucs = data["use_cases"][:]
    random.shuffle(ucs)
    for u in ucs:
        uc_html += f"  <li>✅ {u}</li>\n"
    uc_html += "</ul>"
    
    # Section: Series Cross-Sell
    series_html = f"<p></p>\n<p>{random.choice(series_headings)}</p>\n<ul>\n"
    ser = data["series"][:]
    random.shuffle(ser)
    for s in ser:
        # Example s: "All-in-One — The complete resource..."
        parts = s.split(" — ")
        if len(parts) == 2:
            title = parts[0]
            desc = parts[1]
            series_html += f"  <li>✅ <b>{title}</b> — {desc}</li>\n"
        else:
            series_html += f"  <li>✅ {s}</li>\n"
    series_html += "</ul>"
    
    # Section: Closing CTA
    closing_options = [
        f"<p></p>\n<p>Help your students walk into their exams feeling completely prepared. The structured practice and thorough answer explanations provide everything they need.</p>\n<p><b>Grab these {data['state']} practice tests today and make your test prep stress-free!</b></p>",
        f"<p></p>\n<p>Don't let test anxiety slow your students down. Consistent, realistic practice builds the confidence required for mastering Grade 7 math.</p>\n<p><b>Add this resource to your cart today and start practicing tomorrow!</b></p>",
        f"<p></p>\n<p>There's no substitute for authentic practice when test day approaches. These 5 tests lay the groundwork for a successful end-of-year review.</p>\n<p><b>Download your practice tests and give your students the best preparation possible!</b></p>",
        f"<p></p>\n<p>Preparing for state tests doesn't have to mean reinventing the wheel. Use these fully mapped exams to ensure every standard is covered.</p>\n<p><b>Get the 5 practice tests now and set your students up for success!</b></p>"
    ]
    closing_html = random.choice(closing_options)
    
    # Assembly: Shuffle middle sections for uniqueness
    middle_sections = [feat_html, chap_html, curr_html, uc_html, series_html]
    if exam_html:
        middle_sections.append(exam_html)
        
    random.shuffle(middle_sections)
    
    content = opening_html + "\n\n" + "\n\n".join(middle_sections) + "\n\n" + closing_html + "\n\n" + FOOTER
    
    return content

for state in STATES:
    if state == "north-carolina":
        continue # Already generated
    print(f"Generating for {state}...")
    data = parse_facts(state)
    html_content = generate_html(data)
    
    filepath = os.path.join(OUT_DIR, f"{state}_tpt_{DATE_STR}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

print("All done!")
