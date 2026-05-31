import pandas as pd
import os

df = pd.read_csv(os.path.expanduser("~/job-search/raw/jobs_2026-04-07.csv"))

# 填充空值
df['description'] = df['description'].fillna('')
df['title'] = df['title'].fillna('')
df['company'] = df['company'].fillna('')

def score_job(row):
    desc = str(row['description']).lower()
    title = str(row['title']).lower()
    score = 0
    reasons = []

    # 硬性过滤
    if 'no sponsorship' in desc and 'opt' not in desc and 'cpt' not in desc:
        return None, None
    if any(x in desc for x in ['2+ years', '3+ years', '2 years of experience', '3 years of experience']):
        return None, None
    if all(x in desc for x in ['cold call', 'quota']) and 'product' not in desc:
        return None, None

    # 打分
    if 'opt' in desc or 'sponsorship' not in desc:
        score += 30
        reasons.append('签证友好')
    if any(x in desc for x in ['early stage', 'series a', 'seed', 'startup', 'small team']):
        score += 20
        reasons.append('早期公司')
    if any(x in desc for x in ['experiment', 'growth', 'analytics', 'funnel', 'retention', 'activation', 'user behavior']):
        score += 20
        reasons.append('增长/实验')
    if any(x in desc for x in ['own', 'drive', 'lead', 'responsible for', 'manage']):
        score += 15
        reasons.append('有ownership')
    if any(x in desc for x in ['notion', 'clay', 'zapier', 'hubspot', 'apollo', 'figma', 'airtable']):
        score += 15
        reasons.append('工具匹配')

    return score, ', '.join(reasons)

results = []
for _, row in df.iterrows():
    score, reason = score_job(row)
    if score is not None:
        results.append({
            '公司名': row.get('company', ''),
            '职位': row.get('title', ''),
            '链接': row.get('job_url', ''),
            '分数': score,
            '入选理由': reason
        })

result_df = pd.DataFrame(results)
result_df = result_df.sort_values('分数', ascending=False).head(25)
output = os.path.expanduser("~/job-search/shortlist_2026-04-07.csv")
result_df.to_csv(output, index=False)
print(f"筛选完成，共 {len(result_df)} 个职位")
print(result_df[['公司名', '职位', '分数']].to_string())
