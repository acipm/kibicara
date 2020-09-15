# Kibicara Contribution HowTo


## Setup Development Environment

### Backend

1. Install `python>=3.8`
2. Create a virtual environment with `python3 -m venv .venv`
3. Activate your dev environment with `source .venv/bin/activate`
4. Update pip packages with `pip install -U pip setuptools wheel`
5. Install with `pip install .`
6. Install development dependencies with `pip install tox black`
7. Add git-hook to run test and stylecheck before commmit with
   `ln -s git-hooks/pre-commit .git/hooks/pre-commit`
8. Add git-hook to check commmit message format with
   `ln -s git-hooks/commit-msg .git/hooks/commit-msg`
9. Turn off production mode:
   `sudo su -c 'echo "production = 0" >> /etc/kibicara.conf'`

#### Cheatsheet

- Install Kibicara with `pip install .`
- Execute Kibicara with `kibicara` (verbose: `kibicara -vvv`)
- Interact with Swagger REST-API documentation:
`http://localhost:8000/api/docs`
- Test and stylecheck with `tox`
- Fix style issues with `black -S kibicara tests`

### Frontend

1. Install node.js (e.g. via
   [nvm](https://github.com/nvm-sh/nvm#installation-and-update))
2. `cd kibicara-frontend`
3. Install the dependencies with `npm i`
4. Install Angular with `npm i -g @angular/cli`
5. Turn off production mode if you have not already (see above in backend section).
6. Start the backend in a different terminal
7. Run `ng s -o` to serve and open the application. The application will open
   under [http://127.0.0.1:4200](http://127.0.0.1:4200).

### Creating an account

#### Without local mailserver setup

1. Start the server with `kibicara -vvv`.
2. Go to `http://localhost:8000/api/docs`. Use the `POST /api/admin/register`
endpoint to create an account (minimal password size is 8).
3. Check the log output for a line that contains a link with the token:
```
<sometimestamp> kibicara.webapi.admin http://127.0.0.1:4200/confirm?token=<copythistoken>
```
4. Paste the token into the `POST /api/admin/confirm/{register_token}` endpoint
at `http://localhost:8000/api/docs`.
5. Done! Try to log in with the `Authorize` button on the page or use the
frontend

#### With local mailserver (e.g. openSMTPd)

1. Install the opensmtpd package and start it.
2. The mails should be usually delivered in `~/Maildir`. Use your unix username
as email address and register via frontend or manually at
`http://localhost:8000/api/docs`.


## Contribution Guidelines
### Branches

- **Master:** The master branch tracks the latest stable release.
  - Releases will be done using release tags.
  - Force push and pushes without group consent are disallowed.
  - There should never be a merge commit from development into master!
- **Development:** The development branch is used to add new features.
  - Only rebase of feature branches is allowed.
  - On Release, the development branch will be rebased onto master and a
    release tag will be created on master
- **Feature-Branches:**
  - A feature branch will be used to develop a feature.
  - It belongs to one developer only so force push is allowed.
  - A rebase onto development is necessary to merge the feature. Code reviews
    are encouraged.

### Write Tests

We use [pytest](https://docs.pytest.org/en/stable/) as a test engine. It is
executed by `tox`, so you need to run `tox` on the command line to run the
tests.

### Commit Messages

Commits should define small components. Please write your commits in the
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
- [doc] Documentation
- [misc] e.g. github action files
- #\d+ if commit is related to specific issues or merge requests

Don't use tags which are not listed here. Don't start your commit message in
lowercase. Commit messages which do not fulfill these guidelines will not be
merged into the `development` branch.

### Comments

#### Python

We use pdoc3, which takes prose and comments automatically from the docstrings
in the repository to generate documentation.

Use [google style](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)
comments to secure correct display of your docstrings.

Please don't leave trailing whitespace or empty lines at the end of your files.

### Merge Requests

The main development team does not need to make merge requests.

If you open a merge request, please include a description which explains the
improvement.

#### Code reviews

Before a merge request gets rebased onto and merged into `development`, at
least one person has to approve it; this also increases the number of people
who are familiar with the codebase. Therefore please request a review from 
someone from the core development team.


## How to implement a new platform/social network

### tl;dr

1. Implement the following modules in `platforms/<your-platform>/`:
  - `bot.py`
  - `model.py`
  - `webapi.py`
2. Import your bot in `kibicara/webapi/__init__.py`.

### Explanation

In `kibicara/platforms/<your-platform>/bot.py`, you write the functions that
the platform needs to ask the social network for new messages and to publish
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

* let hood admins authenticate to the social network in the kibicara web
interface
* update platform-specific settings

To run the platform, you need to import the bot in
`kibicara/webapi/__init__.py`.

### Acceptance criteria for bots (Checklist)

A bot should have at least this functionality:

- Kibicara REST API (hood admins):
    - Endpoint for creating a bot associated with a hood
    - Endpoint for deleting a bot associated with a hood
    - Endpoint for updating a bot associated with a hood by id
        (_The update endpoint may be optional if it does not provide any
        additional benefit to delete and create.
        An example where it does provide additional benefit is when there is
        a database which holds state like user ids in telegram. Then deleting the bot
        would also delete the user ids which would stop the bot from working._)
    - Endpoint for getting the bot configuration by id
    - Endpoint for starting and enabling a created bot by id
    - Endpoint for stopping and disabling a created bot by id
    - Endpoint for getting the status of a bot (INSTANTIATED, RUNNING, STOPPED)
    - Endpoint for getting all bots of a hood

- Bot functionality (user):
    - Possibility for a user to subscribe to the bot on their platform
        - e.g. Twitter itself already covers this by their follow/unfollow button
        - e.g. Telegram /start command
        - e.g. E-Mail REST Endpoint for entering and confirming an email
    - Possibility for a user to unsubscribe to the bot on their platform
        - e.g. Twitter itself already covers this by their follow/unfollow button
        - e.g. Telegram /stop command
        - e.g. E-Mail REST Endpoint for removing an email by token
    - Possibility for a user to send a message to the bot that gets broadcasted
        - e.g. Twitter via mentions or direct message
        - e.g. Telegram via direct message to the bot
        - e.g. E-Mail via e-mail to a specified address
    - Possibility for a user to get bot messages
        - e.g. Twitter via posts or retweets
        - e.g. Telegram via direct message from the bot
        - e.g. E-Mail via e-mail to the user's address
