#
# File: Makefile
# Description: makefile for all-i-want
#
# Copyright 2011-2013 Adam Meadows
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

HIDE := @
PYTHON ?= python
BUILD := build

.PHONY : build coverage flake8-test python-test test clean

IGNORES := -not -path "*.git" \
	-not -path "*tests"\
	-not -path "*build"\
	-not -path "*mocks"\
	-not -path "*.config"

build:
	$(HIDE)rm -rf $(BUILD)
	$(HIDE)mkdir $(BUILD)
	$(HIDE)cp *.py $(BUILD)
	$(HIDE)cp *.yaml $(BUILD)
	$(HIDE)find . -type d -d 1 $(IGNORES) -exec cp -R {} $(BUILD) \;
	$(HIDE)find $(BUILD) -name tests | xargs rm -rf

coverage: export PYTHON := coverage run -a
coverage:
	$(HIDE)make python-test
	$(HIDE)echo -e "\nCoverage Stats:\n"
	$(HIDE)coverage report --omit /Applications/*.py

flake8-test:
	$(HIDE)flake8 --config=.config/flake8 .

python-test:
	$(HIDE)nosetests

test: flake8-test python-test

clean:
	$(HIDE)rm -rf $(BUILD)
	$(HIDE)echo "Removing *.pyc files"
	$(HIDE)find . -name \*.pyc | xargs rm -f

