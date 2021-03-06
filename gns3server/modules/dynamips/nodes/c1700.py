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
Interface for Dynamips virtual Cisco 1700 instances module ("c1700")
http://github.com/GNS3/dynamips/blob/master/README.hypervisor#L428
"""

from .router import Router
from ..adapters.c1700_mb_1fe import C1700_MB_1FE
from ..adapters.c1700_mb_wic1 import C1700_MB_WIC1

import logging
log = logging.getLogger(__name__)


class C1700(Router):
    """
    Dynamips c1700 router.

    :param hypervisor: Dynamips hypervisor instance
    :param name: name for this router
    :param router_id: router instance ID
    :param chassis: chassis for this router:
    1720, 1721, 1750, 1751 or 1760 (default = 1720).
    1710 is not supported.
    """

    def __init__(self, hypervisor, name, router_id=None, chassis="1720"):
        Router.__init__(self, hypervisor, name, router_id, platform="c1700")

        # Set default values for this platform
        self._ram = 128
        self._nvram = 32
        self._disk0 = 0
        self._disk1 = 0
        self._chassis = chassis
        self._iomem = 15  # percentage
        self._clock_divisor = 8
        self._sparsemem = False

        if chassis != "1720":
            self.chassis = chassis

        self._setup_chassis()

    def defaults(self):
        """
        Returns all the default attribute values for this platform.

        :returns: default values (dictionary)
        """

        router_defaults = Router.defaults(self)

        platform_defaults = {"ram": self._ram,
                             "nvram": self._nvram,
                             "disk0": self._disk0,
                             "disk1": self._disk1,
                             "chassis": self._chassis,
                             "iomem": self._iomem,
                             "clock_divisor": self._clock_divisor,
                             "sparsemem": self._sparsemem}

        # update the router defaults with the platform specific defaults
        router_defaults.update(platform_defaults)
        return router_defaults

    def list(self):
        """
        Returns all c1700 instances

        :returns: c1700 instance list
        """

        return self._hypervisor.send("c1700 list")

    def _setup_chassis(self):
        """
        Sets up the router with the corresponding chassis
        (create slots and insert default adapters).
        """

        # With 1751 and 1760, WICs in WIC slot 1 show up as in slot 1, not 0
        # e.g. s1/0 not s0/2
        if self._chassis in ['1751', '1760']:
            self._create_slots(2)
            self._slots[1] = C1700_MB_WIC1()
        else:
            self._create_slots(1)
        self._slots[0] = C1700_MB_1FE()

    @property
    def chassis(self):
        """
        Returns the chassis.

        :returns: chassis string
        """

        return self._chassis

    @chassis.setter
    def chassis(self, chassis):
        """
        Sets the chassis.

        :param: chassis string:
        1720, 1721, 1750, 1751 or 1760
        """

        self._hypervisor.send("c1700 set_chassis {name} {chassis}".format(name=self._name,
                                                                          chassis=chassis))

        log.info("router {name} [id={id}]: chassis set to {chassis}".format(name=self._name,
                                                                            id=self._id,
                                                                            chassis=chassis))

        self._chassis = chassis
        self._setup_chassis()

    @property
    def iomem(self):
        """
        Returns I/O memory size for this router.

        :returns: I/O memory size (integer)
        """

        return self._iomem

    @iomem.setter
    def iomem(self, iomem):
        """
        Sets I/O memory size for this router.

        :param iomem: I/O memory size
        """

        self._hypervisor.send("c1700 set_iomem {name} {size}".format(name=self._name,
                                                                     size=iomem))

        log.info("router {name} [id={id}]: I/O memory updated from {old_iomem}% to {new_iomem}%".format(name=self._name,
                                                                                                        id=self._id,
                                                                                                        old_iomem=self._iomem,
                                                                                                        new_iomem=iomem))
        self._iomem = iomem
