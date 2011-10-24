'''
#
# File: rpc_list.py
# Description: 
#   Handler for all List RPCs (setting up Lists and managing items) 
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

from rpc.rpc_meta import RpcGroupBase, RpcReqHandler, Rpc
from rpc.rpc_params import RpcParamString, RpcParamInt, RpcParamBoolean
from core.model import ListOwner, WishList, ListItem
from core.exception import PermissionDeniedError, DuplicateNameError,\
    UserVisibleError

class ListRpcGroup(RpcGroupBase):
    rpcs = (
        Rpc(name='add_list', params=(
            RpcParamInt('owner_id'),
            RpcParamString('name'),
            RpcParamString('desc'),
        )),
        Rpc(name='update_list', params=(
            RpcParamInt('list_id'),
            RpcParamString('name'),
            RpcParamString('desc'),
        )),
        Rpc(name='delete_list', params=(
            RpcParamInt('list_id'),
        )),
        Rpc(name='get_lists', params=(
            RpcParamInt('owner_id'),
        )),
        Rpc(name='add_item', params=(
            RpcParamInt('list_id'),
            RpcParamString('name'),
            RpcParamString('cat'),
            RpcParamString('desc'),
            RpcParamString('url'),
            RpcParamBoolean('surprise'),
        )),
        Rpc(name='update_item', params=(
            RpcParamInt('list_id'),
            RpcParamString('name'),
            RpcParamString('cat'),
            RpcParamString('desc'),
            RpcParamString('url'),
        )),
        Rpc(name='remove_item', params=(
            RpcParamInt('item_id'),
        )),
        Rpc(name='reserve_item', params=(
            RpcParamInt('item_id'),
        )),
        Rpc(name='unreserve_item', params=(
            RpcParamInt('item_id'),
        )),
        Rpc(name='purchase_item', params=(
            RpcParamInt('item_id'),
        )),
        Rpc(name='unpurchase_item', params=(
            RpcParamInt('item_id'),
        )),
        Rpc(name='get_reserved_and_purchased_items'),
    )

    def _verify_owner(self):
        self.owner = self.db.get_owner_by_user(self.db.user)
        if self.owner is None:
            raise PermissionDeniedError()

    def _can_add_to_list(self, owner_id):
        self._verify_owner()
        return self.owner.key().id() == owner_id

    def _can_read_list(self, owner_id):
        _ = lambda x: x.member.key().id()
        self._verify_owner()
        oids = [ self.owner.key().id() ]
        groups, memberships = (self.owner.groups, self.owner.memberships)
        oids.extend(g.owner.key().id() for g in groups)
        oids.extend(_(m) for g in groups for m in g.members)
        oids.extend(gm.group.owner.key().id() for gm in memberships)
        oids.extend(_(m) for gm in memberships for m in gm.group.members)
        return owner_id in oids

    def _item_already_taken(self, taken, by):
        msg = 'Item has been %s by %s<%s>' % (taken, by.nickname, by.email)
        raise UserVisibleError(msg)

    def add_list(self, owner_id, name, desc):
        '''
        Add a new wish list for the given owner, ensuring a unique name
        '''
        if not self._can_add_to_list(owner_id):
            raise PermissionDeniedError()

        if not self.db.is_list_name_unique(owner_id, name):
            raise DuplicateNameError(WishList, name)

        l = self.db.add_list(owner_id, name, desc)
        return WishList.from_db(l)

    def update_list(self, list_id, name, desc):
        '''
        Update the name/description of an existing wish list for 
        the given owner, ensuring a unique name
        '''
        l = self.db.get_list(list_id)
        oid = l.owner.key().id()
        if not self._can_add_to_list(oid):
            raise PermissionDeniedError()
        
        if not self.db.is_list_name_unique(oid, name, l.key()):
            raise DuplicateNameError(WishList, name)

        l.name = name
        l.description = desc
        return WishList.from_db(l.put())

    def delete_list(self, list_id):
        '''
        Delete the given List 
        '''
        l = self.db.get_list(list_id)
        oid = l.owner.key().id()
        if not self._can_add_to_list(oid):
            raise PermissionDeniedError()
       
        l.delete()
        return []

    def get_lists(self, owner_id):
        '''
        Retrieve all the wish lists for the given owner
        '''
        if not self._can_read_list(owner_id):
            raise PermissionDeniedError()
        
        owner = self.db.get_owner(owner_id)
        return [ WishList.from_db(l) for l in owner.lists ]
   
    def add_item(self, list_id, name, cat, desc, url, surprise):
        '''
        Add an item to the given wish list
        '''
        l = self.db.get_list(list_id)
        can_read = self._can_read_list(l.owner.key().id())
        can_add = self._can_add_to_list(l.owner.key().id())
        if not (can_add or (can_read and surprise)):
                raise PermissionDeniedError()

        item = self.db.add_list_item(list_id, name, cat, desc, url, surprise)
        if surprise:
            item.reserved_by = self.owner
            item.put()
        return ListItem.from_db(item)

    def update_item(self, item_id, name, cat, desc, url):
        '''
        Update the name, category, description and url of an existing item
        '''
        item = self.db.get_item(item_id)
        if not self._can_add_to_list(item.parent_list.owner.key().id()):
            raise PermissionDeniedError()

        item.name = name
        item.category = cat
        item.description = desc
        item.url = url
        return ListItem.from_db(item.put())

    def remove_item(self, item_id):
        '''
        Remove the given item. If the item has been reserved/purchased, send
        an email notification to the the reserver/purchaser
        '''
        self._verify_owner()
        item = self.db.get_item(item_id)
        if not self._can_add_to_list(item.parent_list.owner.key().id()):
            raise PermissionDeniedError()

        if item.reserved_by is not None:
            to = item.reserved_by.email
            subject = 'Wish List Item Deleted'
            name, email = self.owner.nickname, self.owner.email
            body = self.ae.DELETED_ITEM_TEMPLATE % (item.reserved_by.nickname,
                name, email, item.name, item.parent_list.name, 'Reserved',
                name, email)
            self.ae.send_mail(to, subject, body)
        elif item.purchased_by is not None:
            to = item.purchased_by.email
            subject = 'Wish List Item Deleted'
            name, email = self.owner.nickname, self.owner.email
            body = self.ae.DELETED_ITEM_TEMPLATE % (item.purchased_by.nickname,
                name, email, item.name, item.parent_list.name, 'Purchased',
                name, email)
            self.ae.send_mail(to, subject, body)

        l = item.parent_list
        self.db.delete(item)
        return WishList.from_db(l)

    def reserve_item(self, item_id):
        '''
        Mark the given item as reserved
        '''
        self._verify_owner()
        item = self.db.get_item(item_id)
        if not self._can_read_list(item.parent_list.owner.key().id()):
            raise PermissionDeniedError()

        if item.purchased_by is not None and item.purchased_by != self.owner:
            self._item_already_taken('purchased', item.purchased_by)
            
        if item.reserved_by is not None and item.reserved_by != self.owner:
            self._item_already_taken('reserved', item.reserved_by)

        item.reserved_by = self.owner
        item.purchased_by = None
        return ListItem.from_db(item.put())

    def unreserve_item(self, item_id):
        '''
        Mark the given item as not reserved if you were the one who reserved it
        '''
        self._verify_owner()
        item = self.db.get_item(item_id)
        if not self._can_read_list(item.parent_list.owner.key().id()):
            raise PermissionDeniedError()

        if item.purchased_by is not None and item.purchased_by != self.owner:
            self._item_already_taken('purchased', item.purchased_by)
            
        if item.reserved_by is not None and item.reserved_by != self.owner:
            self._item_already_taken('reserved', item.reserved_by)

        item.reserved_by = None
        return ListItem.from_db(item.put())

    def purchase_item(self, item_id):
        '''
        Mark the given item as purchased
        '''
        self._verify_owner()
        item = self.db.get_item(item_id)
        if not self._can_read_list(item.parent_list.owner.key().id()):
            raise PermissionDeniedError()

        if item.purchased_by is not None and item.purchased_by != self.owner:
            self._item_already_taken('purchased', item.purchased_by)
            
        if item.reserved_by is not None and item.reserved_by != self.owner:
            self._item_already_taken('reserved', item.reserved_by)

        item.reserved_by = None
        item.purchased_by = self.owner
        return ListItem.from_db(item.put())
    
    def unpurchase_item(self, item_id):
        '''
        Mark the given item as not purchased if you were the one who
        purchased it
        '''
        self._verify_owner()
        item = self.db.get_item(item_id)
        if not self._can_read_list(item.parent_list.owner.key().id()):
            raise PermissionDeniedError()

        if item.purchased_by is not None and item.purchased_by != self.owner:
            self._item_already_taken('purchased', item.purchased_by)
            
        if item.reserved_by is not None and item.reserved_by != self.owner:
            self._item_already_taken('reserved', item.reserved_by)

        item.purchased_by = None
        return ListItem.from_db(item.put())

    def get_reserved_and_purchased_items(self):
        '''
        Retrieve all items which have been reserved or purchased by you 
        '''
        # TODO: implement this
        pass


class ListRpcReqHandler(RpcReqHandler):
    group_cls = ListRpcGroup

