import os
import sys
import subprocess
import re
import random
from datetime import datetime

states = [
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado", 
    "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho", 
    "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", 
    "maine", "maryland", "massachusetts", "michigan", "minnesota", 
    "mississippi", "missouri", "montana", "nebraska", "nevada", 
    "new-hampshire", "new-jersey", "new-mexico", "new-york", 
    "north-carolina", "north-dakota", "ohio", "oklahoma", "oregon", 
    "pennsylvania", "rhode-island", "south-carolina", "south-dakota", 
    "tennessee", "texas", "utah", "vermont", "virginia", "washington", 
    "west-virginia", "wisconsin", "wyoming"
]

TODAY = datetime.now().strftime("%Y-%m-%d")

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

def parse_facts(text):
    facts = {}
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith('Book Title:'): facts['Book Title'] = line.split(':', 1)[1].strip()
        elif line.startswith('State:'): facts['State'] = line.split(':', 1)[1].strip()
        elif line.startswith('Curriculum Name:'): facts['Curriculum Name'] = line.split(':', 1)[1].strip()
        elif line.startswith('Curriculum Acronym:'): facts['Curriculum Acronym'] = line.split(':', 1)[1].strip()
        elif line.startswith('Exam Name:'): facts['Exam Name'] = line.split(':', 1)[1].strip()
        elif line.startswith('Exam Acronym:'): facts['Exam Acronym'] = line.split(':', 1)[1].strip()
        elif line.startswith('Total Topics:'): facts['Total Topics'] = line.split(':', 1)[1].strip()

    def get_bullet_section(regex_pattern):
        match = re.search(regex_pattern, text, re.DOTALL)
        if match:
            # Split by bullet point
            return [x.strip() for x in match.group(1).split('•') if x.strip()]
        return []

    # Regex for chapters: Between Total Chapters: X and --- FEATURES
    ch_match = re.search(r'Total Chapters:.*?\n(.*?)--- FEATURES', text, re.DOTALL)
    if ch_match:
        facts['Chapters'] = [x.strip() for x in ch_match.group(1).split('\n') if x.strip()]
    else:
        facts['Chapters'] = []

    facts['Features'] = get_bullet_section(r'--- FEATURES.*?---\n(.*?)--- USE CASES')
    facts['Use Cases'] = get_bullet_section(r'--- USE CASES.*?---\n(.*?)--- SERIES CROSS-SELL')
    facts['Cross-Sell'] = get_bullet_section(r'--- SERIES CROSS-SELL.*?---\n(.*?)--- DESIGN')
    
    return facts

def generate_description(state, facts):
    title = facts.get('Book Title', 'Grade 7 Math Workbook')
    state_name = facts.get('State', state.replace('-', ' ').title())
    curr_name = facts.get('Curriculum Name', '')
    curr_acronym = facts.get('Curriculum Acronym', '')
    exam_name = facts.get('Exam Name', '')
    exam_acronym = facts.get('Exam Acronym', '')
    topic_count_raw = facts.get('Total Topics', 'all')
    
    features = facts.get('Features', [])
    use_cases = facts.get('Use Cases', [])
    cross_sell = facts.get('Cross-Sell', [])
    chapters = facts.get('Chapters', [])

    # Randomizing Headings
    feature_headings = ["Here's What You're Getting", "What's Inside", "What You'll Find", "A Quick Look Inside", "Inside the Workbook", "Workbook Features"]
    chapter_headings = [f"All {topic_count_raw} Topics, Covered", "What's Covered", "Chapter Breakdown", "Topics Included", "Here's the Breakdown", "What Students Will Learn"]
    curriculum_headings = [f"Made for {state_name}", "Curriculum Alignment", f"Written for {state_name}", f"Aligned to {state_name}'s Standards", "State Standards Alignment"]
    test_prep_headings = ["Ready for the Exam", "Get Ready for the Test", "Built-In Test Prep", "When Test Day Comes", "Test Prep Made Easy", f"Built-In {exam_acronym} Prep" if exam_acronym else "Test Prep Built In"]
    use_cases_headings = ["Who's This For?", "Great For", "Works Well For", "Who'll Get the Most Out of This", "How to Use This"]
    series_headings = ["Want More?", "Looking for More?", "Need Lessons Too?", "Check Out the Full Series", "More Resources for Your Classroom"]

    random.shuffle(feature_headings)
    random.shuffle(chapter_headings)
    random.shuffle(curriculum_headings)
    random.shuffle(test_prep_headings)
    random.shuffle(use_cases_headings)
    random.shuffle(series_headings)

    # 1. Opening
    openings = [
        f"<p><b>{title}</b></p>\\n<p>This workbook is your go-to resource for practicing every Grade 7 math skill. It offers organized, focused problems that help students master the concepts they need.</p>",
        f"<p><b>{title}</b></p>\\n<p>Simplify your math instruction with a structured, comprehensive workbook. It provides all the practice students need to build confidence and fluency in Grade 7 math.</p>",
        f"<p><b>{title}</b></p>\\n<p>Give your students the structured practice they deserve. This workbook covers every topic for the year and supports sustained learning.</p>",
        f"<p><b>{title}</b></p>\\n<p>An organized approach to practicing Grade 7 math. Use this workbook to reinforce skills day by day.</p>"
    ]
    
    # Process Features
    f_list = []
    for f in features:
        if f: f_list.append(f"<li>✅ {f}</li>")
    
    # Always include design features
    f_list.append("<li>✅ Colorful pages with illustrations, diagrams, and a friendly owl mascot</li>")
    f_list.append("<li>✅ Answer key with explanations included</li>")
    f_list.append("<li>✅ Print and go / no prep needed</li>")
    
    f_list_str = "\\n".join(f_list)
    opening_html = f"{random.choice(openings)}\\n<p></p>\\n<p><b>{feature_headings[0]}</b></p>\\n<ul>\\n{f_list_str}\\n</ul>\\n"

    # 2. Chapters
    ch_list_arr = []
    for ch in chapters:
        if ch:
            if '—' in ch:
                parts = ch.split('—', 1)
                ch_list_arr.append(f"<li>✅ <b>{parts[0].strip()}</b> — {parts[1].strip()}</li>")
            else:
                ch_list_arr.append(f"<li>✅ {ch}</li>")
    ch_list = "\\n".join(ch_list_arr)
    chapter_html = f"<p></p>\\n<p><b>{chapter_headings[0]}</b></p>\\n<ul>\\n{ch_list}\\n</ul>\\n"

    # 3. Curriculum
    if curr_name and curr_name.lower() not in ["(none)", "(not available)"]:
        curr_text = f"<b>{curr_name} ({curr_acronym})</b>"
    else:
        curr_text = f"<b>{state_name}'s specific Grade 7 math standards</b>"

    curriculum_intros = [
        f"This book was carefully developed to align with {curr_text}.",
        f"I wrote this specifically for <b>{state_name}</b> to follow {curr_text}.",
        f"You don't need to guess if this matches your lessons — it is completely aligned to {curr_text}.",
        f"Built to match {curr_text} so you can teach with confidence."
    ]
    curriculum_html = f"<p></p>\\n<p><b>{curriculum_headings[0]}</b></p>\\n<p>{random.choice(curriculum_intros)}</p>\\n"

    # 4. Exam / Test Prep
    exam_html = ""
    if exam_name and exam_name.lower() not in ["(none)", "(not available)"]:
        exam_text = f"<b>{exam_name} ({exam_acronym})</b>"
        exam_intros = [
            f"If your students are taking the {exam_text}, this workbook gives them the targeted practice they need to do their best.",
            f"Getting ready for the {exam_text}? The practice problems here build the exact skills tested on exam day.",
            f"This resource is perfect for helping students prepare for the {exam_text} in the spring."
        ]
        exam_html = f"<p></p>\\n<p><b>{test_prep_headings[0]}</b></p>\\n<p>{random.choice(exam_intros)}</p>\\n"

    # 5. Use Cases
    uc_list = []
    for uc in use_cases:
        if uc: uc_list.append(f"<li>✅ {uc}</li>")
    uc_list_str = "\\n".join(uc_list)
    use_cases_html = f"<p></p>\\n<p><b>{use_cases_headings[0]}</b></p>\\n<ul>\\n{uc_list_str}\\n</ul>\\n"

    # 6. Series Cross-Sell
    cross_sell_items = []
    for cs in cross_sell:
        if not cs: continue
        if "—" in cs:
            parts = cs.split("—", 1)
            book_type = parts[0].strip()
            desc = parts[1].strip()
            cross_sell_items.append(f"<li>✅ <b>{book_type}</b> — {desc}</li>")
        else:
            cross_sell_items.append(f"<li>✅ {cs}</li>")
            
    cs_list = "\\n".join(cross_sell_items)
    series_html = f"<p></p>\\n<p><b>{series_headings[0]}</b></p>\\n<ul>\\n{cs_list}\\n</ul>\\n"

    # 7. CTA
    ctas = [
        f"<p>Get the practice resource that actually makes a difference.</p>\\n<p><b>Grab your copy today!</b></p>",
        f"<p>Set your students up for success with structured, daily practice.</p>\\n<p><b>Download the workbook now.</b></p>",
        f"<p>You don't need to spend hours searching for the right practice problems.</p>\\n<p><b>Add this workbook to your teaching toolkit today!</b></p>",
        f"<p>Provide your students with the rigorous practice they need.</p>\\n<p><b>Get started right away!</b></p>"
    ]
    cta_html = f"<p></p>\\n{random.choice(ctas)}\\n<p></p>\\n"

    # Assemble everything with random order for inner sections
    sections = [chapter_html, curriculum_html, use_cases_html, series_html]
    if exam_html:
        sections.append(exam_html)
        
    random.shuffle(sections)
    
    final_content = opening_html.strip() + "\\n\\n" + "\\n\\n".join(s.strip() for s in sections) + "\\n\\n" + cta_html.strip() + "\\n\\n" + footer
    
    return final_content.strip()

for state in states:
    print(f"Processing {state}...")
    cmd = ["python3", ".agents/skills/writing-tpt-description/scripts/get_book_facts.py", "workbook", state]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to get facts for {state}: {result.stderr}")
        continue
        
    facts = parse_facts(result.stdout)
    desc = generate_description(state, facts)
    
    filepath = f"final_output/workbook/{state}_tpt_{TODAY}.html"
    with open(filepath, "w") as f:
        f.write(desc)

print("Done generating all workbook descriptions.")
