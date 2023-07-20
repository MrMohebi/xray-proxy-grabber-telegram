import shutil

from git import Repo
from dotenv import load_dotenv
import os

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
PROXIES_REPO = os.getenv('PROXIES_REPO')
IS_DEBUG = bool(int(os.getenv('DEBUG_MODE')))

if os.path.exists("./repo/.git"):
    repo = Repo("./repo/")
else:
    repo = Repo.clone_from(
        "https://mrm:{TOKEN_GITHUB}@github.com/{REPO}".format(TOKEN_GITHUB=GITHUB_TOKEN, REPO=PROXIES_REPO), "./repo")

with repo.config_reader() as git_config:
    mainGitEmail = git_config.get_value('user', 'email')
    mainGitUser = git_config.get_value('user', 'name')


def changeGitUserToBot():
    with repo.config_writer() as gitConfig:
        gitConfig.set_value('user', 'email', 'bot@auto.com')
        gitConfig.set_value('user', 'name', 'Bot-auto')


def resetGitUser():
    global mainGitUser, mainGitEmail
    with repo.config_writer() as gitCnf:
        gitCnf.set_value('user', 'email', mainGitEmail)
        gitCnf.set_value('user', 'name', mainGitUser)


def getLatestRowProxy():
    if not IS_DEBUG:
        repo.git.execute(["git", "checkout", "remotes/origin/master", "proxies_row_url.txt"])
        shutil.copyfile("./repo/proxies_row_url.txt", "proxies_row_url.txt")

def commitPushRowProxiesFile(chanelUsername):
    if not IS_DEBUG:
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "reset", "--hard", "origin/master"])
        repo.git.execute(["git", "pull"])
        shutil.copyfile("proxies_row_url.txt", "./repo/proxies_row_url.txt")
        repo.index.add(["proxies_row_url.txt"])
        changeGitUserToBot()
        repo.index.commit('update proxies from {}'.format(chanelUsername))
        repo.remotes.origin.push()
        resetGitUser()
        print('pushed => update proxies from {}'.format(chanelUsername))


def commitPushRActiveProxiesFile():
    if not IS_DEBUG:
        repo.git.execute("git fetch --all")
        repo.git.execute("git reset --hard origin/master")
        repo.git.execute("git pull")
        shutil.copyfile("proxies_active.txt", "./repo/proxies_active.txt")
        repo.index.add(["proxies_active.txt"])
        changeGitUserToBot()
        repo.index.commit('update active proxies')
        repo.remotes.origin.push()
        resetGitUser()
        print('pushed => update active proxies')
