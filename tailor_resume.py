import pandas as pd
import os
import json
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="YOUR_API_KEY_HERE",
    azure_endpoint="https://alignment-test-1.openai.azure.com",
    api_version="2024-08-01-preview"
)

RESUME = """
Dominique (Xucen) ZHENG
Los Angeles, CA | (+1)213-827-4863 | xucenzhe@usc.edu | Linkedin | Seeking GTM/Growth roles
Summary: Growth & GTM operator focused on building early-stage distribution systems, running outbound experiments, and turning insights into pipeline.
Work Authorization: F1. OPT eligible Summer 2026. Sponsorship not required

PROJECTS
Alignment (Behavioral Infrastructure Tool) | Founder & Product Lead Jan.2026-Present
- Ran a fake-door GTM experiment to validate demand, converting early interest into 2 paying users as initial signal
- Reduced MVP scope to isolate a single activation trigger for measurable validation
- Ran structured qualitative testing (n=6); identified evaluation-stage drop-off and redesigned messaging layer to improve forward action rate
- Created structured messaging layers used to communicate product value across user touchpoints
- Led a 3-person cross-functional team to ship MVP within a 2-week sprint

Identity-Based Health Adoption Campaign | USC Public Health Mar.2026
- Designed identity-driven messaging strategy to improve vaccination adoption among digital-native audiences
- Developed GTM messaging hypothesis framing vaccination as peer-aligned identity behavior
- Proposed A/B test structure using descriptive norms messaging to reduce autonomy threat
- Selected by professor as an exemplary campaign; received rare 10/10 evaluation

SheLevelsUp | Founder and Product Lead Aug.2025-Jan.2026
- Built and validated a demand hypothesis based on proven creator mode
- Strategically pivoted after assessing validation speed and technology leverage

EDUCATION
University of Southern California, California, USA
M.E. Major in Integrated Design, Technology & Business, Expected May 2027
Core Courses: Communication & Persuasion, Marketing & Analytics for Start-ups, Finance for Entrepreneurship

Shanghai Jiao Tong University, Shanghai, China
B.A. Major in Visual Communication Design, Minor in Entrepreneurship, Graduated Jun 2025

INTERNSHIP EXPERIENCE
SEPHORA (SHANGHAI) COSMETICS CO., LTD. Shanghai, China
UX Design Intern Jul.2024-Oct.2024
- Audited end-to-end mobile flows and identified 20+ usability gaps impacting activation and engagement
- Delivered a competitor analysis to inform feature prioritization and differentiation strategy
- Partnered with PM to update Member Center visuals; A/B improved engagement time by 3% and reduced task error rate by 1%

Ciwei Internship Platform Shanghai, China
Visual Design Intern Jun.2023-Aug.2023
- Produced assets and marketing collateral for partner outreach and two exhibitions
- Supported early funnel experiments for event conversion

SKILLS & TOOLS
Language: English (Proficient, TOEFL 106); Chinese (Native)
GTM & Growth: funnel mapping, retention math, CAC LTV sensitivity, activation metrics, A/B testing, experiment design
Analytics: SQL (basic), Excel (pivot)
Tools: Figma, Notion, ChatGPT, Clay, CRM systems (basic), Unity, Arduino

HONORS
Excellent Project of SJTU Undergraduate Research Program 2023
Fourth place, Tencent Games Peace Cup College Developer Creation Competition 2022

EXTRACURRICULAR
TroyLabs Ignite Program, Participant 2026-Present
SJTU Student Union, Vice Minister 2022-2025
SJTU Students Career Development Union, Vice President 2021-2025
"""

ALLOWED_TOOLS = ["Zapier", "Clay", "Apollo", "HubSpot", "Notion", "Airtable", "Figma", "Salesforce", "Mixpanel", "Amplitude", "Segment"]

df = pd.read_csv(os.path.expanduser("~/job-search/shortlist_2026-04-07.csv"))
os.makedirs(os.path.expanduser("~/job-search/applications"), exist_ok=True)

for i, row in df.iterrows():
    company = str(row['公司名']).replace('/', '-').replace(' ', '_')
    title = str(row['职位']).replace('/', '-').replace(' ', '_')[:40]
    jd = str(row.get('description', ''))[:3000]
    
    prompt = f"""你是一个专业的求职顾问，帮候选人针对具体JD调整简历。

规则：
1. 只调整措辞和关键词，不捏造经历
2. 不使用破折号（—），用普通句子
3. Summary 第一句针对这个岗位改写
4. 如果JD提到以下工具，且候选人能快速学会，可以加入Skills：{', '.join(ALLOWED_TOOLS)}
5. 保持简洁，不要冗长
6. 输出完整简历文本，格式和原版一致

JD：
{jd}

原版简历：
{RESUME}

输出调整后的完整简历文本："""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.3
        )
        tailored = response.choices[0].message.content
        
        filename = f"2026-04-07_{company}_{title}_resume.txt"
        filepath = os.path.expanduser(f"~/job-search/applications/{filename}")
        with open(filepath, 'w') as f:
            f.write(tailored)
        print(f"[{i+1}/25] 完成: {company} - {title}")
    except Exception as e:
        print(f"[{i+1}/25] 错误: {e}")

print("\n全部完成！文件在 ~/job-search/applications/")
