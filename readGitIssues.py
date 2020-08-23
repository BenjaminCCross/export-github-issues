from github import Github
import csv 
from dotenv import load_dotenv
load_dotenv()
import os


ACCESS_TOKEN=os.getenv("OATH_TOKEN")

g = Github(ACCESS_TOKEN)
repo = g.get_repo(os.getenv("PREF_REPO"))

repoLabelsList = []
for label in repo.get_labels():
            repoLabelsList.append(label.name)

# Collect issues regardless of state
open_issues = repo.get_issues(state="open")
closed_issues = repo.get_issues(state="closed")
issues = [open_issues, closed_issues]

fieldnames = ['Issue Number', 'Title', 'Milestone', 'Comments', 'Closed At']
fieldnamesWithLabels = fieldnames + repoLabelsList

with open('issuelist.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnamesWithLabels)
    writer.writeheader()

    for issues_list in issues:
        for issue in issues_list:

            # convert milestone to name or NA
            milestoneObject = issue.milestone
            if not milestoneObject is None:
                milestone = milestoneObject.title
            else:
                milestone = "NA"

            # store issueFieldVals
            issueFieldVals = [str(issue.number), str(issue.title), str(milestone), str(issue.comments), str(issue.closed_at)]

            # convert field name and val to dict
            fieldDict = {fieldnames[i]: issueFieldVals[i] for i in range(len(issueFieldVals))}

            # convert labels to name list
            labelsList = []
            for label in issue.get_labels():
                labelsList.append(label.name)

            # Create dict for if label is present for issue
            hasLabels = {}
            for label in repoLabelsList:
                if label in labelsList:
                    hasLabels[label] = 1
                else:
                    hasLabels[label] = 0

            # Create row dict and add fields to row
            row = {}
            row.update(fieldDict)
            row.update(hasLabels)
            
            writer.writerow(row)

