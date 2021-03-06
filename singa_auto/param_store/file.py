#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import os
import uuid

from .param_store import ParamStore, Params


class FileParamStore(ParamStore):
    '''
       Stores parameters in the local filesystem.
    '''

    def __init__(self, params_dir=None, model_class=''):
        self._params_dir = params_dir or os.path.join(
            os.environ['WORKDIR_PATH'], os.environ['PARAMS_DIR_PATH'])
        self.model_class = model_class

    def save(self, params: Params):
        # Serialize params and save bytes to params dir
        file_name = '{}_{}.model'.format(self.model_class, uuid.uuid4())
        dest_file_path = os.path.join(self._params_dir, file_name)
        params_bytes = self._serialize_params(params)
        # Check the directory. In case the directory doesn't exist, if so, create the path
        if not os.path.exists(self._params_dir):
            os.makedirs(self._params_dir)
        with open(dest_file_path, 'wb') as f:
            f.write(params_bytes)

        # ID for params is its file name
        params_id = file_name

        return params_id

    def load(self, params_id):
        # Load bytes to params dir and deserialize params
        file_name = params_id
        file_path = os.path.join(self._params_dir, file_name)
        with open(file_path, 'rb') as f:
            params_bytes = f.read()
        params = self._deserialize_params(params_bytes)

        return params
