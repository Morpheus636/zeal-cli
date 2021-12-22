# jmt_flow Worflow
JMT uses our custom workflow (known as jmt_flow) for our versioned-release projects, as described below.

## Branches
### Main
The main branch is where all release branches are based. 

### Release
Release branches should be branched from name. They are long-lived
branches, only to be archived when the branch is officially unsupported.

A new release branch should be created for each major version.
Minor versions are created within a release branch using git tags.

Release branches should start with release/, and followed by the major version number. 

### Feature
Feature branches should be branched from a release branch. They are where active development of new features or improvements to existing features should take place.

Feature branches should start with feature/, and be followed by the GitHub issue number and a brief description of the feature to be added. Example:
feature/#32_rate_limiting

Feature branches should be merged back into their release, and
if appropriate, into main.

### Bugfix
Bugfix branches should be branched from a release branch. They are where bug fixes should be developed.

Bugfix branches should start with bugfix/, followed by the GitHub issue number and a brief description of the bug. Example:
bugfix/#33_rate_limit_crashes_client

Bugfix branches should be merged back into their release, and
if appropriate, into main.

## Commit Messages
Commit messages are very important. They tell other developers what you did without them having to read all the changes you made. Commit messages should be in the form:

#<GitHub issue number>: <Description of what you did>

IE:

#15: Added endpoints for adding/removing users

## Merging
All commits to `main` or to release branches should go through
pull requests, and all checks should pass, including at least one
code-review, before the pull request is merged.