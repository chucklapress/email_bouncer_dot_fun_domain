#!/usr/bin/python3
import os
import unbound
from unbound import ub_ctx,RR_TYPE_A,RR_CLASS_IN

ctx = ub_ctx()
ctx.set_option("module-config:","iterator")
ctx.resolvconf("/etc/resolv.conf")

status, result = ctx.resolve("icloud.com", RR_TYPE_A, RR_CLASS_IN)
if status == 0 and result.havedata:
    List = result.data.address_list
    results = " ".join(str(x) for x in List)
    print( results)
    status, result = ctx.resolve(unbound.reverse(results) + ".in-addr.arpa.", unbound.RR_TYPE_PTR, unbound.RR_CLASS_IN)
    if status == 0 and result.havedata:
        NL = result.data.domain_list
        reverse = " ".join(str(x) for x in NL)
        print(  reverse)
    elif status != 0:
        print( "Resolve error:", unbound.ub_strerror(status))
