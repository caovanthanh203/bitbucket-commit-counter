import requests, dateutil.parser
import json

baseUrlv2 = "https://bitbucket.org/api/2.0"
baseUrlv1 = "https://bitbucket.org/api/1.0"

username = ""
password = ""
role = "contributor" #admin, contributor, member, owner
year = 2020

totalCommits = 0
totalAdd = 0
totalRemove = 0
overallAdd = 0
overallRemove = 0
commitCount = 0
commits = []

print ("")
print ("Stats for {year}".format(year=year))
print ("")

r = requests.get("{base}/repositories?role={role}".format(base=baseUrlv2, role=role),
	auth=(username, password))

repos = r.json()

while 'next' in repos:
	for repo in repos["values"]:
		commitLink = repo["links"]["commits"]["href"]
		repoSlug = repo["slug"]
		# print(repoSlug)
		# continue
		r = requests.get(commitLink,
		auth=(username, password))

		c = r.json()
		commits.extend(c['values'])

		while 'next' in c:
			# print("next page")
			r = requests.get("{next}".format(next=c['next']), 
				auth=(username, password))
			c = r.json()
			commits.extend(c['values'])

		for commit in commits:
			# print("count commit")
			commitDate = dateutil.parser.parse(commit['date'])
			if commitDate.year == year:
				commitCount += 1

		print ("Total commits in {user}/{repo}: {count}".format(user=username, repo=repoSlug, count=commitCount))	
		totalCommits += commitCount	
		#reset counters
		commitCount = 0
		commits = []
	r = requests.get("{next}".format(next=repos['next']), auth=(username, password))
	repos = r.json()

print ("")
print ("Total commits: {count}".format(count=totalCommits))