"""Fetch the GitHub contributions calendar for one user and save it as JSON.

Runs in GitHub Actions with the workflow's GITHUB_TOKEN. Standard library only.
If the request fails for any reason, it prints a warning and exits 0 without
writing the file, so the build continues and the site renders without the graph.

Usage: python3 scripts/fetch_contributions.py <login> <output.json>
"""
import json
import os
import sys
import urllib.request

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { date contributionCount contributionLevel }
        }
      }
    }
  }
}
"""


def main():
    login, out = sys.argv[1], sys.argv[2]
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("::warning::GITHUB_TOKEN not set; skipping GitHub activity")
        return
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "portfolio-build"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.load(resp)
        cal = body["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        days = [d for w in cal["weeks"] for d in w["contributionDays"]]
        if not days:
            raise ValueError("empty calendar")
    except Exception as exc:  # network error, auth error, GraphQL error, unexpected shape
        detail = body.get("errors") if "body" in locals() and isinstance(body, dict) else ""
        print(f"::warning::Could not fetch GitHub contributions ({exc!r} {detail}); skipping GitHub activity")
        return
    with open(out, "w", encoding="utf-8") as f:
        json.dump(cal, f)
    print(f"Fetched {cal['totalContributions']} contributions over {len(days)} days "
          f"({days[0]['date']} to {days[-1]['date']})")


if __name__ == "__main__":
    main()
