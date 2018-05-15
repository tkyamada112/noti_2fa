import slackweb
from github import Github
from robots import *
from users import *

github_token          = 'xxx'
incoming_webhooks_url = 'xxx'
organization_name     = 'xxx'

class Git:
    def Client(github_token):
        client = Github(github_token)
        return client

    def ListViolators(github_clinet):
        violators = []
        for member in github_client.get_organization(organization_name).get_members(filter_='2fa_disabled'):
            violators.append(member.login)
        return violators

def ignore_robots(robots, violators):
    for robot in robots:
        if robot in violators:
            violators.remove(robot)
    return violators

def gen_slack_users(violators, slackUsers):
    slack_users = []
    no_belong_users = []
    for violator in violators:
        if violator in slackUsers:
            slack_users.append(slackUsers[violator])
        elif violator not in slackUsers:
            no_belong_users.append(violator)
    return slack_users, no_belong_users

github_client    = Git.Client(github_token)
violators        = Git.ListViolators(github_client)
proper_violators = ignore_robots(robots, violators)

slack_users, no_belong_users = gen_slack_users(violators, slackUsers)
slack = slackweb.Slack(url=incoming_webhooks_url)

for user in slack_users:
    mention_user = " @" + user
    slack.notify(text=mention_user, username="SecureAuditer", icon_emoji=":umbrella:", link_names=1)
if len(slack_users) != 0:
    slack.notify(text="Check 2fa", username="SecureAuditer", icon_emoji=":umbrella:")

if len(no_belong_users) != 0:
    users_str = ','.join(no_belong_users)
    message = "Unregister user detected. => " + users_str
    slack.notify(text=message, username="SecureAuditer", icon_emoji=":umbrella:")
