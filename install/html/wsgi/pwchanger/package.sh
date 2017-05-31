#!/bin/sh

mkdir -p package/pk
rm -rf package/pk/*

rsync -r -v --delete \
	--exclude package \
	--exclude _* \
	--exclude venv \
	--exclude doxydoc \
	* package/pk/






