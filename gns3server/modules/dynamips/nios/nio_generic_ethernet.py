# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 GNS3 Technologies Inc.
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Interface for generic Ethernet NIOs (PCAP library).
"""

from .nio import NIO

import logging
log = logging.getLogger(__name__)


class NIO_GenericEthernet(NIO):
    """
    Dynamips generic Ethernet NIO.

    :param hypervisor: Dynamips hypervisor instance
    :param ethernet_device: Ethernet device name (e.g. eth0)
    """

    _instance_count = 0

    def __init__(self, hypervisor, ethernet_device):

        NIO.__init__(self, hypervisor)

        # create an unique ID
        self._id = NIO_GenericEthernet._instance_count
        NIO_GenericEthernet._instance_count += 1
        self._name = 'nio_gen_eth' + str(self._id)
        self._ethernet_device = ethernet_device

        self._hypervisor.send("nio create_gen_eth {name} {eth_device}".format(name=self._name,
                                                                              eth_device=ethernet_device))

        log.info("NIO Generic Ethernet {name} created with device {device}".format(name=self._name,
                                                                                   device=ethernet_device))

    @classmethod
    def reset(cls):
        """
        Reset the instance count.
        """

        cls._instance_count = 0

    @property
    def ethernet_device(self):
        """
        Returns the Ethernet device used by this NIO.

        :returns: the Ethernet device name
        """

        return self._ethernet_device
