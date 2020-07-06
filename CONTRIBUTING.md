# Kibicara Contribution Guidelines

## Setup Development Environment

1. Install `python>=3.7`
2. Create a virtual environment with `python3 -m venv .venv`
3. Activate your dev environment with `source .venv/bin/activate`
4. Install with `pip install .`
5. Install development dependencies with `pip install tox black`
6. Add git-hook to run test and stylecheck before commmit with
   `ln -s ../../git-hooks/pre-commit .git/hooks/pre-commit`
7. Add git-hook to check commmit message format with
   `ln -s ../../git-hooks/commit-msg .git/hooks/commit-msg`

### Build and Test Cycle

- Install with `pip install .`
- Execute with `kibicara`
- Interact with Swagger REST-API Documentation: http://localhost:8000/docs
- Test and stylecheck with `tox`
- Fix style issues with `black -S kibicara tests`

## Branches

- **Master:** The master branch tracks the last stable release.
  - Releases will be done using release tags.
  - Force push and pushes without group consent are disallowed.
  - There never should be a merge commit from development into master!
- **Development:** The development branch is used to add new features.
  - Only rebase of feature branches is allowed.
  - On Release the development branch will be rebased onto master and a release
    tag will be created on master
- **Feature-Branches:**
  - A feature branch will be used to develop a feature.
  - It belongs to one developer only and force push is allowed.
  - A rebase onto development is necessary to merge the feature. Code reviews
    are encouraged.

## Write Tests

We use [pytest](https://docs.pytest.org/en/stable/) as a test engine. It is
executed by `tox`, so you need to run `tox` on the command line to run the tests.

## Commit Messages

Commits should define small components. Please write your commits with the
following pattern:

`[core] Add censor for filtering messages #1312`

You can use these tags:

- [core] Feature for Kibicara core
- [frontend] Feature for Kibicara frontend
- [$platform] Feature for platforms, e.g.
    - [twitter]
    - [telegram]
    - [email]
    - ...
- [tests] Tests
- [misc] e.g. github action files
- #\d+ if commit is related to specific issues or merge requests

Don't use tags which are not listed here. Don't start your commit message with
lower case. Commit messages which do not fulfill these guidelines will not be
merged into the `development` branch.

## Comments

### Python

We use pdoc3, which takes prose and comments automatically from the docstrings
in the repository.

Use [google
style](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)
comments to secure correct display of your docstrings.

Please don't leave trailing whitespace or empty lines at the end of your files.

## Merge Requests

The main development team does not need to make merge requests.

If you open a merge request, please include a description which explains the
improvement.

### Code reviews

Before a merge request gets rebased onto and merged into `development`, at
least one person has to approve it; this also increases the number of people
who know the code. So please request a review from someone from the core
development team.

## Implement a new Platform/Social Network

### tl;dr

1. Implement the following modules in `platforms/<your-platform>/`:
  - `bot.py`
  - `model.py`
  - `webapi.py`
2. Import your bot in `kibicara/webapi/__init__.py`.

### Explanation

In `kibicara/platforms/<your-platform>/bot.py`, you write the functions through
which the platform asks the social network for new messages, and publishes
messages to the social network. You need to inherit the bot from the `Censor`
class at `kibicara/platformapi.py`.

In `kibicara/platforms/<your-platform>/model.py`, you define a database layout.
You will probably need to store the following things:

* authentication credentials,
* timestamps/IDs of the last seen message,
* recipients if the social network doesn't post publicly,
* platform-specific settings
* anything else your platform needs

In `kibicara/platforms/<your-platform>/webapi.py`, you can define HTTP routes.
You will need them to:

* let admins authenticate to the social network in the kibicara web interface
* update platform-specific settings

To run the platform, you need to import the bot in
`kibicara/webapi/__init__.py`.
