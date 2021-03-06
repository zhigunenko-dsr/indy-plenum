import types

from plenum.common.util import get_utc_epoch
from plenum.server.suspicion_codes import Suspicions
from plenum.test.helper import getNodeSuspicions


def get_timestamp_suspicion_count(node):
    return len(getNodeSuspicions(node, Suspicions.PPR_TIME_WRONG.code))


def make_clock_faulty(node, clock_slow_by_sec=None, ppr_always_wrong=True):
    if clock_slow_by_sec is None:
        clock_slow_by_sec = node.config.ACCEPTABLE_DEVIATION_PREPREPARE_SECS + 5

    def utc_epoch(self) -> int:
        return get_utc_epoch() - clock_slow_by_sec

    # slow_utc_epoch = types.MethodType(utc_epoch, node)
    # setattr(node, 'utc_epoch', property(slow_utc_epoch))
    node.utc_epoch = types.MethodType(utc_epoch, node)

    if ppr_always_wrong:
        def ppr_time_is_wrong(self, pp):
            return False

        for repl in node.replicas:
            repl.is_pre_prepare_time_correct = types.MethodType(
                ppr_time_is_wrong, repl)
