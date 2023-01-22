#!/usr/bin/env bash
# usage: ./deploy.sh PROJECT_ROOT
set -eux

PROJECT_DIR="$1/"

if [[ ! -d $PROJECT_DIR ]]; then
  echo "Usage: $0 <root-directory>"
  exit 1
fi

SOURCE="${PROJECT_DIR}src/"
APP_HOST="since.vtbassmatt.com"
APP_DIR="/data/since-app/"
APP_USER="since"
DEPLOY_NAME="$(date '+%Y-%m-%d-%H-%M-%S')-$(git rev-parse --short HEAD)"
DEPLOY_DIR="${APP_DIR}deploys/${DEPLOY_NAME}-src/"
VENV_DIR="${APP_DIR}deploys/${DEPLOY_NAME}-env"
SCP_TARGET="${APP_USER}@${APP_HOST}:${DEPLOY_DIR}"

echo "::::: Creating target directory"
MKDIR_CMD="ssh ${APP_USER}@$APP_HOST 'mkdir -p $DEPLOY_DIR'"
echo "On  : $APP_HOST"
echo "Dir : $DEPLOY_DIR"
eval $MKDIR_CMD

echo "::::: Overwriting commit.py with current commit"
COMMIT_PY_1="# written by deploy.sh"
COMMIT_PY_2="COMMIT = \\\"$(git rev-parse HEAD)\\\""
COMMIT_PY_3="DEPLOY_DATE = \\\"$(date)\\\""
COMMIT_PY_CMD_1="echo \"$COMMIT_PY_1\" > ${SOURCE}since/commit.py"
COMMIT_PY_CMD_2="echo \"$COMMIT_PY_2\" >> ${SOURCE}since/commit.py"
COMMIT_PY_CMD_3="echo \"$COMMIT_PY_3\" >> ${SOURCE}since/commit.py"
echo "Cmd1: $COMMIT_PY_CMD_1"
echo "Cmd2: $COMMIT_PY_CMD_2"
echo "Cmd3: $COMMIT_PY_CMD_3"
eval $COMMIT_PY_CMD_1
eval $COMMIT_PY_CMD_2
eval $COMMIT_PY_CMD_3

echo "::::: Copying code files"
SCP_OPTS="-B -r"
SCP_CMD="scp $SCP_OPTS $SOURCE $SCP_TARGET"
echo "From: $SOURCE"
echo "To  : $SCP_TARGET"
eval $SCP_CMD

echo "::::: Creating new venv"
VENV_CMD="ssh ${APP_USER}@$APP_HOST 'python3 -m venv ${VENV_DIR}'"
VENV_UPDATE_CMD="ssh ${APP_USER}@$APP_HOST '${VENV_DIR}/bin/python -m pip install -U pip setuptools wheel'"
echo "In  : $VENV_DIR"
eval $VENV_CMD
eval $VENV_UPDATE_CMD

echo "::::: Populating venv"
VENV_SCP_OPTS="-B"
VENV_SCP_CMD="scp $VENV_SCP_OPTS ${PROJECT_DIR}requirements.txt ${PROJECT_DIR}deploy/requirements-deploy.txt $SCP_TARGET"
VENV_POPULATE_CMD="ssh ${APP_USER}@$APP_HOST '${VENV_DIR}/bin/python -m pip install -r ${DEPLOY_DIR}requirements-deploy.txt'"
eval $VENV_SCP_CMD
eval $VENV_POPULATE_CMD

echo "::::: Updating symlinks for serving"
MV_SRC_CMD="ssh ${APP_USER}@$APP_HOST 'mv -f ${APP_DIR}current ${APP_DIR}prev || true'"
MV_VENV_CMD="ssh ${APP_USER}@$APP_HOST 'mv -f ${APP_DIR}env ${APP_DIR}prev-env || true'"
LN_SRC_CMD="ssh ${APP_USER}@$APP_HOST 'ln -snf ${DEPLOY_DIR} ${APP_DIR}current'"
LN_VENV_CMD="ssh ${APP_USER}@$APP_HOST 'ln -snf ${VENV_DIR} ${APP_DIR}env'"
eval $MV_SRC_CMD
eval $MV_VENV_CMD
eval $LN_SRC_CMD
eval $LN_VENV_CMD

echo "::::: Restarting uWSGI"
RESTART_CMD="ssh ${APP_USER}@$APP_HOST 'sudo systemctl restart since-app'"
eval $RESTART_CMD

echo "::::: List orphaned deploys"
ORPHAN_SCP_CMD="scp -B ${PROJECT_DIR}deploy/lsorphans.sh ${APP_USER}@${APP_HOST}:${APP_DIR}"
ORPHAN_LS_CMD="ssh ${APP_USER}@$APP_HOST '${APP_DIR}lsorphans.sh ${APP_DIR}'"
eval $ORPHAN_SCP_CMD
eval $ORPHAN_LS_CMD
