set -euo pipefail

if [[ -z $1 ]]; then
  echo "Enter new version: "
  read VERSION
else
  VERSION=$1
fi

read -p "Releasing $VERSION - are you sure? (y/n) " -n 1 -r

echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "Releasing $VERSION ..."
  export GIT_MERGE_AUTOEDIT=no
  git checkout develop
  git flow release start $VERSION
  npm version $VERSION
  npm run build:all
  git add .
  git commit --amend --no-edit
  git flow release publish $VERSION
  git flow release finish -m "$VERSION" $VERSION
  git checkout develop
  git push
  git checkout master
  git push --tags && git push
  git checkout develop
  unset GIT_MERGE_AUTOEDIT
fi
