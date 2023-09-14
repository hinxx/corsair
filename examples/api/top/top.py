#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Demostration of TopLevel API
"""

import copy
from corsair import BitField, Register, RegisterMap, TopLevel, generators

# create
# top level
top = TopLevel('test app 0')
print('Empty top level')
print(top)

# top.read_file('top.yaml')
# print('Loaded top level')
# print(top)

# exit(0)

# create a register map
# rmap = RegisterMap()
# rmap.name = "Test regmap 1"
# rmap.offset = 0x50000
# rmap.instance = 2

# first register map
rmap = RegisterMap('Test rmap 1', 'just for testing', 'Example function 45', 0x401000, 'Example group 22', 3)
# add a single register
# csr_id = Register('ID', 'IP-core ID register', 0x0).add_bitfields([
#     BitField('IDX', 'Instance', width=8, lsb=0, access='ro', hardware='o'),
#     BitField('GID', 'Group ID', width=8, lsb=8, access='ro', hardware='o'),
#     BitField('FID', 'Function ID', width=16, lsb=16, access='ro', hardware='o')])
# rmap.add_registers(csr_id, True)
top.add_regmaps(rmap)

print('One register map')
print(top)

# second register map
rmap2 = RegisterMap('Test rmap 2', 'more testing', 'foo function', 0x40A000, 'fake group', 9)
# add a single register
# csr_id2 = Register('ID', 'IP-core ID register', 0x0).add_bitfields([
#     BitField('IDX', 'Instance', width=8, lsb=0, access='ro', hardware='o'),
#     BitField('GID', 'Group ID', width=8, lsb=8, access='ro', hardware='o'),
#     BitField('FID', 'Function ID', width=16, lsb=16, access='ro', hardware='o')])
# rmap2.add_registers(csr_id2)
top.add_regmaps(rmap2)

print('Two register map')
print(top)

generators.Markdown(rmap, 'regs.md', print_images=True).generate()
generators.CHeader(rmap, 'regs.h').generate()
