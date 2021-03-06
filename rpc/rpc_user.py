'''
#
# File: rpc_user.py
# Description: Handler for all User RPCs related to AE User and ListOwnerDb
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
'''

from core.exception import PermissionDeniedError
from core.model import User, ListOwner, AccessReq, ListPermission
from core.util import get_base_url, extract_name
from rpc.rpc_meta import RpcGroupBase, RpcReqHandler, Rpc
from rpc.rpc_params import (
    RpcParamBoolean as Boolean,
    RpcParamInt as Integer,
    RpcParamString as String,
)


class UserRpcGroup(RpcGroupBase):
    rpcs = (
        Rpc(name='get_current_user', params=(String('url'),)),
        Rpc(name='get_owner', params=(Integer('owner_id'),)),
        Rpc(name='get_permissions',
            params=(Integer('owner_id'), Boolean('by_email'),)),
        Rpc(name='add_permission',
            params=(Integer('owner_id'), String('email'),)),
        Rpc(name='remove_permission', params=(Integer('permission_id'),)),
        Rpc(name='update_owner',
            params=(Integer('owner_id'), String('name'), String('nickname'),)),
        Rpc(name='get_requests'),
        Rpc(name='approve_request', params=(Integer('req_id'),)),
        Rpc(name='deny_request', params=(Integer('req_id'),)),
    )

    def get_current_user(self, url):
        '''
        Return a User object with details of the current authenticated user,
        including a url for logging out.

        If user has not yet been authenticated, return a User object with a
        url to allow user to log in.
        '''
        e, n, ui, li, lo, oid, wrd = (None, None, None, None, None, -1, False)
        user = self.db.user
        ia = False
        if user is None:
            li = self.ae.create_login_url(url)
        else:
            ia = user.is_admin
            e, n, ui = user.email(), user.nickname(), user.user_id()
            # make sure ListOwnerDb record exists
            owner = self.db.get_owner_by_user(user)
            req = None
            if owner is None:
                if not user.is_admin:
                    req = self.db.get_req_by_user(user)
                    if req is None:
                        req = self.db.add_req(user)
                else:
                    owner = self.db.add_owner(user)
            oid = owner.key().id() if owner is not None else -1
            wrd = req.denied if req is not None else False
            base = get_base_url(url)
            lo = self.ae.create_logout_url('%s/#Goodbye:' % base)
        return User(email=e, nickname=n, user_id=ui, login_url=li,
                    logout_url=lo, owner_id=oid, was_req_denied=wrd,
                    is_admin=ia)

    def get_owner(self, owner_id):
        '''
        Return the ListOwner object with the given owner_id
        '''
        return ListOwner.from_db(self.db.get_owner(owner_id))

    def get_permissions(self, owner_id, by_email):
        '''
        Return the ListPermissions for the given ListOwner
        That's not the ListPermissionDb object with owner=owner, but rather
        those with email=owner.email
        '''
        _ = lambda x: ListPermission.from_db(x)
        owner = self.db.get_owner(owner_id)
        if not by_email:
            return [ _(p) for p in owner.permissions ]
        return [
            _(p) for p in self.db.get_permissions_by_email(owner.email)
        ]

    def add_permission(self, owner_id, email):
        '''
        Add a ListPermission record
        '''
        # TODO: confirm that the currently signed in user is owner_id
        owner = self.db.get_owner(owner_id)
        self.db.add_permission(owner, email)
        _ = lambda x: ListPermission.from_db(x)
        return [ _(p) for p in owner.permissions ]

    def remove_permission(self, permission_id):
        '''
        Remove a ListPermission record
        '''
        # TODO: confirm that the currently signed in user is owner_id
        p = self.db.get_permission(permission_id)
        self.db.delete(p)
        return []

    def update_owner(self, owner_id, name, nickname):
        '''
        Update the name and nickname of the ListOwner object with the given
        owner_id and return the updated object.
        '''
        owner = self.db.get_owner(owner_id)
        owner.name = name
        owner.nickname = nickname
        return ListOwner.from_db(owner.put())

    def get_requests(self):
        '''
        Return a list of all requests
        '''
        if not self.db.user.is_admin:
            raise PermissionDeniedError()

        return [ AccessReq.from_db(db) for db in self.db.get_reqs() ]

    def approve_request(self, req_id):
        '''
        Approve the given AccessRequestDb
        '''
        if not self.db.user.is_admin:
            raise PermissionDeniedError()

        req = self.db.get_req(req_id)
        self.db.add_owner(req.user)
        self.db.delete(req)
        to = req.user.email()
        subject = 'Account Activated'
        body = self.ae.APPROVE_TEMPLATE % extract_name(to)
        self.ae.send_mail(to, subject, body)
        return []

    def deny_request(self, req_id):
        '''
        Deny the given AccessRequestDb
        '''

        if not self.db.user.is_admin:
            raise PermissionDeniedError()

        req = self.db.get_req(req_id)
        req.denied = True
        req.put()
        to = req.user.email()
        subject = 'Account Not Activated'
        body = self.ae.DENY_TEMPLATE % extract_name(to)
        self.ae.send_mail(to, subject, body)
        return []


class UserRpcReqHandler(RpcReqHandler):
    group_cls = UserRpcGroup

