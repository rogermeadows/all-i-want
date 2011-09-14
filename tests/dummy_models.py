'''
#
# File: dummy_models.py
# Description: Dummy Model objects
# 
# Copyright 2011 Adam Meadows 
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
'''

class Db(object):
    def __init__(self, id=None):
        if id is None:
            import random
            id = random.Random().randint(1, 1000)
        self.id_ = id

    def id(self):
        return self.id_

    def key(self):
        return self

class User:
    def __init__(self, nickname='Jobber', email='jobber@email.com', \
      is_admin=False):
        self.is_admin = is_admin
        self.nickname = nickname
        self.email = email

class Group(Db):
    def __init__(self, name='', description='', owner=None, **kwargs):
        super(Group, self).__init__(**kwargs)
        self.name = name
        self.description = description
        self.owner = owner
        self.invitations = []
        self.members = []
    
class GroupInvitation(Db):
    def __init__(self, group=None, email='', **kwargs):
        super(GroupInvitation, self).__init__(**kwargs)
        self.group = group
        self.email = email
    
class GroupMember(Db):
    def __init__(self, member=None, group=None, **kwargs):
        super(GroupMember, self).__init__(**kwargs)
        self.member = member
        self.group = group

class List(Db):
    def __init__(self, name='', owner=None, **kwargs):
        super(List, self).__init__(**kwargs)
        self.name = name
        self.owner = owner

class ListItem(Db):
    def __init__(self, parent=None, name='', category='', description='',\
      url='', reserved_by=None, purchased_by=None, owner=None, **kwargs):
        super(ListItem, self).__init__(**kwargs)
        self.parent = parent
        self.name = name
        self.category = category
        self.description = description
        self.url = url
        self.reserved_by = reserved_by
        self.purchased_by = purchased_by
        self.owner = owner

