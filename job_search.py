import csv
import pandas as pd
from jobspy import scrape_jobs
from datetime import datetime
import os

keywords = [
    "GTM intern", "Growth intern", "Product Growth intern",
    "Growth Marketing intern", "Product intern", "Business Development intern",
    "Partnerships intern",
    "Revenue Operations intern",
    "Strategy intern",
    "Market expansion intern"
]

os.makedirs(os.path.expanduser("~/job-search/raw"), exist_ok=True)

all_jobs = []

for keyword in keywords:
    print(f"搜索中: {keyword}...")
    try:
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed", "zip_recruiter"],
            search_term=keyword,
            location="United States",
            is_remote=True,
            hours_old=168,
            results_wanted=30,
            linkedin_fetch_description=True,
            country_indeed="USA"
        )
        all_jobs.append(jobs)
        print(f"  找到 {len(jobs)} 个职位")
    except Exception as e:
        print(f"  错误: {e}")

df = pd.concat(all_jobs, ignore_index=True)
df = df.drop_duplicates(subset=["job_url"])
today = datetime.now().strftime('%Y-%m-%d')
output = os.path.expanduser(f"~/job-search/raw/jobs_{today}.csv")
df.to_csv(output, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
print(f"\n完成！共 {len(df)} 个职位，已保存到 {output}")
