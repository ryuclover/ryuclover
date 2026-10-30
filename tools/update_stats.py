"""Refresh the public profile statistics; then run render_profile.py."""
from datetime import datetime, timezone, timedelta
from pathlib import Path
import json
import subprocess

def api(*args):
    result=subprocess.run(['gh','api',*args],capture_output=True,text=True,encoding='utf-8',check=True)
    return json.loads(result.stdout)

user=api('users/ryuclover')
query='query { user(login: "ryuclover") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date weekday contributionCount } } } } } }'
calendar=api('graphql','-f','query='+query)['data']['user']['contributionsCollection']['contributionCalendar']
stats={
    'updated_at':datetime.now(timezone(timedelta(hours=-3))).date().isoformat(),
    'public_repos':user['public_repos'],
    'followers':user['followers'],
    'calendar':calendar,
}
dest=Path(__file__).resolve().parent/'profile_stats.json'
dest.write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print('Public statistics refreshed:',stats['updated_at'])
