#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Top level
"""

from . import utils
from . import config
# from .reg import Register
from .regmap import RegisterMap
# from .bitfield import BitField
# from .enum import EnumValue
import json
import yaml


class TopLevel():
    """CSR top level"""

    def __init__(self, name='top0'):
        self._regmaps = []

        self._name = name

    def __repr__(self):
        return 'TopLevel()'

    def __str__(self):
        return self.as_str()

    def as_str(self, indent=''):
        """Create indented string with the informatioin about top level."""
        inner_indent = indent + '  '
        regmaps = [regmap.as_str(inner_indent) for regmap in self.regmaps]
        regmaps_str = '\n'.join(regmaps) if regmaps else 2*inner_indent + 'empty'
        return 'top:\n' + inner_indent + 'name: ' + self._name + '\n' + \
                inner_indent + 'maps:\n' + regmaps_str

    def __iter__(self):
        """Create iteration over register maps."""
        return iter(self._regmaps)

    @property
    def name(self):
        """Name of the top level."""
        return utils.force_name_case(self._name)

    @name.setter
    def name(self, value):
        if not utils.is_str(value):
            raise ValueError("Top: 'name' attribute has to be a string")
        self._name = value

    @property
    def regmaps(self):
        """List with register map objects."""
        return self._regmaps

    @property
    def regmap_offsets(self):
        """List of all register map offsets."""
        return [regmap.offset for regmap in self]

    def _off_check_alignment(self, regmap):
        """Check offset alignment."""
        if config.globcfg['offset_alignment'] == 'none':
            align_val = 0x1000
        else:
            align_val = config.globcfg['offset_alignment']

        assert (regmap.offset % align_val) == 0, \
            "Register map '%s' with offset 0x%x is not aligned to 0x%x" % (regmap.name, regmap.offset, align_val)

    def _off_check_conflicts(self, regmap):
        """"""
        offsets = [regmap.offset for regmap in self]
        if regmap.offset in offsets:
            conflict_regmap = self[offsets.index(regmap.offset)]
            assert False, "Register map '%s' with offset 0x%x conflicts with register map '%s' with the same offset!" % \
                (regmap.name, regmap.offset, conflict_regmap.name)

    def add_regmaps(self, new_regmaps):
        """Add list of register maps.
        
        Register maps are automatically sorted and stored in the ascending order by offset.
        """
        # hack to handle single elements
        new_regmaps = utils.listify(new_regmaps)

        # add register maps to the list one by one
        for regmap in new_regmaps:
            # check for duplicates
            assert regmap.offset not in self.regmap_offsets, \
                "Register with offset 0x%x is already present!" % (regmap.offset)
            # check offset alignment
            self._off_check_alignment(regmap)
            # check offset conflicts
            self._off_check_conflicts(regmap)
            # if we are here all is ok and the register map can be added
            try:
                # find position to insert register map and not to break ascending order of offsets
                regmap_idx = next(i for i, rm in enumerate(self._regmaps) if rm.offset > regmap.offset)
                self._regmaps.insert(regmap_idx, regmap)
            except StopIteration:
                # when register map list is empty or all offsets are smaller than the current one
                self._regmaps.append(regmap)
        return self

    def read_file(self, path):
        """Read top level definition from file (based on extension)."""
        ext = utils.get_file_ext(path)
        if ext in ['.yaml', '.yml']:
            self.read_yaml(path)
        else:
            raise ValueError("Unknown extension '%s' of the file '%s'" % (ext, path))
    
    def read_yaml(self, path):
        """Read top level definition from YAML file."""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            self._fill_from_file_data(data['top'])

    def _fill_from_file_data(self, data):
        """Fill register map with data from file."""
        # print('yaml data:\n', data)
        self._name = data['name']
        self._regmaps = []
        for data_regmap in data['regmaps']:
            regmap = RegisterMap()
            regmap.read_file(data_regmap['include'])
            regmap.name = data_regmap['name']
            regmap.description = data_regmap['description']
            regmap.offset = data_regmap['offset']
            regmap.instance = data_regmap['instance']
            regmap.group = data_regmap['group']
            # print('new regmap:\n', regmap)

            self.add_regmaps(regmap)

