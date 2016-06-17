# -*- coding: utf-8 -*-

# Copyright (C) 2015-2016 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import json

from xivo_lib_rest_client import RESTCommand


class TransfersCommand(RESTCommand):

    resource = 'transfers'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def get_transfer(self, transfer_id, token, **kwargs):
        self.headers['X-Auth-Token'] = token
        r = self.session.get('{url}/{transfer_id}'.format(url=self.base_url, transfer_id=transfer_id),
                             headers=self.headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def make_transfer(self, transfer, token, **kwargs):
        self.headers['X-Auth-Token'] = token
        r = self.session.post(self.base_url,
                              data=json.dumps(transfer),
                              params=kwargs,
                              headers=self.headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def make_transfer_from_user(self, exten, initiator, flow):
        body = {
            'exten': exten,
            'initiator_call': initiator,
            'flow': flow,
        }
        r = self.session.post(self._client.url('users', 'me', self.resource),
                              json=body,
                              headers=self.headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def complete_transfer(self, transfer_id, token, **kwargs):
        self.headers['X-Auth-Token'] = token
        self.session.put('{url}/{transfer_id}/complete'.format(url=self.base_url, transfer_id=transfer_id),
                         headers=self.headers)

    def cancel_transfer(self, transfer_id, token, **kwargs):
        self.headers['X-Auth-Token'] = token
        self.session.delete('{url}/{transfer_id}'.format(url=self.base_url, transfer_id=transfer_id),
                            headers=self.headers)
