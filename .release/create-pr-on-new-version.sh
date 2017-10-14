#!/bin/bash
set -ex

echo Scrap tomcat website and fetch the version.
VERSION=$(.release/fetch-version.sh)

echo Check if version $VERSION is already commited
git branch -a |grep "r${VERSION}$" && exit 0
git tag |grep "\.${VERSION}$" && exit 0

echo Update specfile with new version $VERSION
.release/update-version.sh $VERSION
git diff --exit-code && exit 0

echo Create branch r${VERSION}
git checkout -b "r${VERSION}"
git commit --author="Filirom1 <Filirom1@gmail.com>" -am "release $VERSION"

echo Push branch r${VERSION}
NAME=`git remote -v |sed 's#.*/##'|sed 's/ .*//g'|sed 's/\.git//g'|head -n1` 
git remote set-url origin https://Filirom1-bot:$TOKEN@github.com/scl-tomcat/$NAME.git
git push --set-upstream origin r${VERSION}

echo create new Merge Request
curl -f --user "Filirom1-bot:$TOKEN" --request POST --data "{ \"title\": \"New release ${VERSION}\", \"body\": \"A new release is available\", \"head\": \"r${VERSION}\", \"base\": \"master\" }" https://api.github.com/repos/scl-tomcat/$NAME/pulls
