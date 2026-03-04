import subprocess
import os
import re
import random

STATES = [
    'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado',
    'connecticut', 'delaware', 'florida', 'georgia', 'hawaii', 'idaho',
    'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana',
    'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota',
    'mississippi', 'missouri', 'montana', 'nebraska', 'nevada',
    'new-hampshire', 'new-jersey', 'new-mexico', 'new-york',
    'north-carolina', 'north-dakota', 'ohio', 'oklahoma', 'oregon',
    'pennsylvania', 'rhode-island', 'south-carolina', 'south-dakota',
    'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington',
    'west-virginia', 'wisconsin', 'wyoming'
]

OUT_DIR = "final_output/10_practice_tests"
os.makedirs(OUT_DIR, exist_ok=True)
DATE_STR = "2026-03-04"

def parse_facts(text):
    data = {}
    def extract(pattern, default=""):
        m = re.search(pattern, text)
        return m.group(1).strip() if m else default

    title_m = re.search(r"Book Title:\s+(.*?)\n---", text, re.DOTALL)
    data['title'] = " ".join(title_m.group(1).strip().split()) if title_m else ""
    
    data['state'] = extract(r"State:\s+(.*?)\n")
    data['curriculum_name'] = extract(r"Curriculum Name:\s+(.*?)\n")
    data['curriculum_acronym'] = extract(r"Curriculum Acronym:\s+(.*?)\n")
    data['exam_name'] = extract(r"Exam Name:\s+(.*?)\n")
    data['exam_acronym'] = extract(r"Exam Acronym:\s+(.*?)\n")
    data['total_topics'] = extract(r"Total Topics:\s+(\d+)")
    
    ch_m = re.search(r"Total Chapters:\s+\d+\n+(.*?)\n---", text, re.DOTALL)
    chapters = []
    if ch_m:
        lines = ch_m.group(1).strip().split('\n')
        chapters = [line.strip() for line in lines if line.strip() and "Topics:" not in line and "Chapters:" not in line]
    data['chapters'] = chapters
    return data

def generate_html(data):
    intros = [
        f"<p><b>{data['title']}</b> is your complete solution for standardized math preparation. With 300 unique questions spread over 10 full-length exams, it's designed to build student confidence and highlight areas needing review.</p>",
        f"<p>Give your students the edge they need with <b>{data['title']}</b>. It features 10 comprehensive assessment tests (30 questions each) with fully explained answers, making it the perfect tool for uncovering gaps in their Grade 7 math knowledge.</p>",
        f"<p>Get ready for testing season with <b>{data['title']}</b>. This resource provides 300 targeted practice problems arranged into 10 full-length tests, ensuring your students have the repetitions they need to succeed.</p>",
        f"<p><b>{data['title']}</b> offers exactly what students need before the big test: realistic, rigorous practice. Featuring 10 exams and complete step-by-step explanations, it removes the guesswork from test prep.</p>",
        f"<p>Stop stressing over assessment prep. <b>{data['title']}</b> brings you 10 complete practice tests to systematically build students' skills and stamina across every Grade 7 math topic.</p>"
    ]
    
    features_heads = ["What's Inside", "Here's What You're Getting", "What You'll Find", "A Quick Look Inside", "Features at a Glance"]
    features_opts = [
        "<li>✅ 10 full-length practice exams containing 30 questions each</li>",
        "<li>✅ 300 total problems covering every major grade-level concept</li>",
        "<li>✅ Detailed step-by-step answer explanations for every single question</li>",
        "<li>✅ Realistic test formats mirroring actual state exams</li>",
        "<li>✅ Answer grids and simple scoring rubrics included</li>",
        "<li>✅ Score trackers built in to help students monitor their own progress</li>",
        "<li>✅ Colorful, engaging page layouts with diagrams and a cheerful owl mascot</li>",
        "<li>✅ 100% print-and-go — absolutely no prep work required</li>"
    ]
    
    curr_opts = []
    if data['curriculum_name'] not in ("(not available)", "") and data['curriculum_name'].lower() != "none":
        curr_opts.append(f"<p>This resource isn't generic. It's built from the ground up to match the <b>{data['curriculum_name']} ({data['curriculum_acronym']})</b> for <b>{data['state']}</b>.</p>")
        curr_opts.append(f"<p>Carefully aligned to <b>{data['state']}'s</b> expectations, this book strictly follows the requirements of the <b>{data['curriculum_acronym']}</b> standards.</p>")
    else:
        curr_opts.append(f"<p>This book is perfectly aligned to the specific Grade 7 math standards for <b>{data['state']}</b>. Your students only practice what they actually need to know.</p>")
        curr_opts.append(f"<p>Written specifically with <b>{data['state']}</b> classrooms in mind, ensuring a perfect match for state-level expectations.</p>")

    if data['exam_name'] not in ("(none)", "") and data['exam_name'] != "(not available)":
        curr_opts[-1] += f" It's the ideal preparation tool for the <b>{data['exam_name']} ({data['exam_acronym']})</b>."

    curr_heads = [f"Made for {data['state']}", "State Standards Aligned", f"Written for {data['state']}", f"Matches {data['state']}'s Standards"]

    use_heads = ["Who's This For?", "Great For", "Works Well For", "Who'll Get the Most Out of This", "Perfect For"]
    use_cases = [
        "<li>✅ State exam preparation and building testing stamina</li>",
        "<li>✅ Weekly classroom test-prep sessions leading up to the final</li>",
        "<li>✅ Homework assignments where students use the key to self-correct</li>",
        "<li>✅ Focused tutoring sessions to drill weak concept areas</li>",
        "<li>✅ Homeschool benchmarking and standardized assessment practice</li>",
        "<li>✅ End-of-year summer review to solidify math mastery</li>"
    ]

    series_heads = ["Want More?", "Looking for More?", "Check Out the Full Series", "The Rest of the Series"]
    series_opts = [
        "<li>✅ <b>All-in-One</b> — The complete resource with full lessons, worked examples, and practice for every topic</li>",
        "<li>✅ <b>Study Guide</b> — A concise review of key concepts, essential examples, and quick practice</li>",
        "<li>✅ <b>Workbook</b> — Hundreds of scaffolded practice problems organized by topic for extra practice</li>",
        "<li>✅ <b>Step-by-Step Guide</b> — A guided approach with clear, numbered instructions so students learn at their own pace</li>",
        "<li>✅ <b>Math in 30 Days</b> — A structured daily plan that covers the full curriculum in one month</li>",
        "<li>✅ <b>Quizzes</b> — Quick 15-minute assessments for every topic to track progress</li>",
        "<li>✅ <b>Puzzles & Brain Teasers</b> — Curriculum-aligned games, riddles, and challenges that make math fun</li>",
        "<li>✅ <b>Worksheets</b> — Standalone printable activities for any topic, ready to use in any order</li>"
    ]

    ch_heads = ["All Topics Covered", "What's Covered", f"All {data['total_topics']} Topics, Broken Down", "Here's the Breakdown", "Chapter by Chapter"]
    
    closing_opts = [
        "<p>Set your students up for success when assessment time arrives.</p>\n<p><b>Grab these 10 Practice Tests today and watch their confidence grow!</b></p>",
        "<p>Don't leave test scores to chance. Give them the rigorous repetitions they need.</p>\n<p><b>Add these 10 Practice Tests to your classroom toolkit today!</b></p>",
        "<p>Testing season doesn't have to be stressful when students know exactly what to expect.</p>\n<p><b>Download these 10 Practice Tests now and start preparing!</b></p>",
        "<p>Help your class walk into their exams feeling fully prepared and confident.</p>\n<p><b>Get your copy of these 10 Practice Tests today!</b></p>"
    ]

    # Sections construction
    random.shuffle(features_opts)
    s_intro = random.choice(intros)
    s_features = f"<p></p>\n<p><b>{random.choice(features_heads)}</b></p>\n<ul>\n" + "\n".join(features_opts[:8]) + "\n</ul>"

    ch_head = random.choice(ch_heads)
    format_type = random.choice(["list", "table"])
    ch_html = f"<p></p>\n<p><b>{ch_head}</b></p>\n"
    if format_type == "list":
        ch_html += "<ul>\n"
        for c in data['chapters']:
            parts = c.split("—")
            if len(parts) == 2:
                ch_html += f"  <li><b>{parts[0].strip()}</b> — {parts[1].strip()}</li>\n"
            else:
                ch_html += f"  <li>{c}</li>\n"
        ch_html += "</ul>"
    else:
        ch_html += "<table>\n  <tbody>\n"
        for c in data['chapters']:
            parts = c.split("—")
            if len(parts) == 2:
                ch_html += f"    <tr>\n      <td><b>{parts[0].strip()}</b></td>\n      <td>{parts[1].strip()}</td>\n    </tr>\n"
            else:
                ch_html += f"    <tr>\n      <td colspan='2'>{c}</td>\n    </tr>\n"
        ch_html += "  </tbody>\n</table>"
    s_chapters = ch_html

    s_curr = f"<p></p>\n<p><b>{random.choice(curr_heads)}</b></p>\n" + random.choice(curr_opts)
    
    random.shuffle(use_cases)
    s_use = f"<p></p>\n<p><b>{random.choice(use_heads)}</b></p>\n<ul>\n" + "\n".join(use_cases) + "\n</ul>"

    s_series = f"<p></p>\n<p><b>{random.choice(series_heads)}</b></p>\n<ul>\n" + "\n".join(series_opts) + "\n</ul>"

    s_close = f"<p></p>\n{random.choice(closing_opts)}"

    # Mix order
    blocks = [s_chapters, s_curr, s_use]
    random.shuffle(blocks)
    
    final_output = s_intro + "\n" + s_features + "\n" + "\n".join(blocks) + "\n" + s_series + "\n" + s_close + "\n\n"

    footer = """★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★

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

    return final_output + footer

def main():
    for state in STATES:
        print(f"Generating for {state}...")
        cmd = f"python3 .agents/skills/writing-tpt-description/scripts/get_book_facts.py 10_practice_tests {state}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Failed to get facts for {state}")
            continue
        
        facts = parse_facts(res.stdout)
        html = generate_html(facts)
        
        filepath = os.path.join(OUT_DIR, f"{state}_tpt_{DATE_STR}.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
    print("Done generating all 50 descriptions.")

if __name__ == "__main__":
    main()