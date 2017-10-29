# pivotal-github-status

Develop: [![Build Status](https://travis-ci.org/bionikspoon/pivotal-github-status.svg?branch=develop)](https://travis-ci.org/bionikspoon/pivotal-github-status)

Master: [![Build Status](https://travis-ci.org/bionikspoon/pivotal-github-status.svg?branch=master)](https://travis-ci.org/bionikspoon/pivotal-github-status)


## Planning Docs

### Problem Statement

* Information from Pivotal doesn't translate to GithHub
* __Pain Point__: need to know when to merge PRs (status:accepted)

### Solution

* [x] Service that tags Github PRs with current Pivotal Status
* [ ] __Bonus Points__: Track sprints as mile stones
* [ ] __Bonus Points__: Turn this solution into a deployable SaaS
* [ ] __Bonus Points__: For tagging position (ex: story is above "must have for release line")

### Implementation

* [x] A service will listen to Pivotal hooks for changes and use Github's API to make changes
* [x] __Challenge__: Connecting pivotal stories to Github PRs
  - Solution: Searches PR title for story id
  - Example: "Create user profile  page [Fixes #1234567890]" finds story id: `#1234567890`
* [x] __Challenge__: Service will be managing GitHub labels, it shouldn't remove other labels
  - Solution: Service manages the following labels: `unstarted`, `started`, `finished`, `delivered`, `accepted`, `rejected` -- ignoring other labels.
* [x] __Challenge__: One Pull Request -> many stories
* [ ] __Challenge__: Service should proactively notify users about failures
  - For now, there's good logging
* [x] __Challenge__: __\*Security\*__. Strangers shouldn't be able to send fake data to the service.
  - Two part solution:
    1. Secret key passed by url guards the service.
    2. The service refetches data from Pivotal -- effectively data sent by webhook isn't trusted.
  - TODO: Figure out url whitelisting. (Need help)
* [x] __Challenge__: New PRs & Changes to PRs.  By only listening to Pivotal events, these PR's could get out of sync.  No Good!
  - Solution: Listen to GitHub PR events!
