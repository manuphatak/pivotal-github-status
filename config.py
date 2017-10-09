import os

PIVOTAL_ACCESS_TOKEN = os.environ['PIVOTAL_ACCESS_TOKEN']
GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
SECRET_KEY = os.environ['SECRET_KEY']

MANAGED_LABELS = ('unstarted', 'started', 'finished', 'delivered', 'rejected',
                  'accepted')
DNS_WHITELIST = ('app01.pivotaltracker.com', 'app02.pivotaltracker.com',
                 'app03.pivotaltracker.com', 'app04.pivotaltracker.com',
                 'localhost')
