# BinderPatch
[fine-grained locking in binder driver by Todd Kjos](https://www.mail-archive.com/linux-kernel@vger.kernel.org/msg1434375.html)

The binder driver uses a global mutex to serialize access to state in a
multi-threaded environment. This global lock has been increasingly
problematic as Android devices have scaled to more cores. The problem is
not so much contention for the global lock which still remains relatively
low, but the priority inversion which occurs regularly when a lower
priority thread is preempted while holding the lock and a higher priority
thread becomes blocked on it. These cases can be especially painful if the
lower priority thread runs in the background on a slow core at a low
frequency. This often manifests as missed frames or other glitches.

For several years, a hacky solution has been used in many Android devices
which disables preemption for most of the time the global mutex is held.
This dramatically decreased the cases of glitches induced by priority
inversion and increased the average throughput for binder transactions.

Moving to fine-grained locking in this patchset results is a cleaner
and more scalable solution than the preempt disable hack. Priority
inversion is decreased significantly.

Here is a comparison of the binder throughputs for the 3 cases
with no payload (using binderThroughputTest on a 4-core Pixel device):

1 Client/Server Pair (iterations/s):
Global Mutex:    4267
+ No-Preempt:   69688
Fine-Grained:   52313

2 Client/Server Pairs (iterations/s):
Global Mutex:     5608
+ No-Preempt:   111346
Fine-Grained:   117039

4 Client/Server Pairs (iterations/s):
Global Mutex:    12839
+ No-Preempt:   118049
Fine-Grained:   189805

8 Client/Server Pairs (iterations/s):
Global Mutex:    12991
+ No-Preempt:   111780
Fine-Grained:   203607

16 Client/Server Pairs (iterations/s):
Global Mutex:    14467
+ No-Preempt:   106763
Fine-Grained:   202942

Note that global lock performance without preempt disable seems to perform
significantly worse on Pixel than on some other devices. This run used the
4.4 version of the binder driver that is currently upstream (and there
have been few lines changed since then which wouldn't explain the poor
performance).

The no-preempt version has better throughput in the single threaded case
where the new locking overhead adds to the transacton latency. However
with multiple concurent transactions, the lack of contention results in
better throughput for the fine-grained case.

In the patchset, the binder allocator is moved to a separate file and
protected with its own per-process mutex.

Most of the binder driver is now protected by 3 spinlocks which must be
acquired in the order shown:
1) proc->outer_lock : protects binder_ref binder_proc_lock() and
   binder_proc_unlock() are used to acq/rel.
2) node->lock : protects most fields of binder_node.  binder_node_lock()
   and binder_node_unlock() are used to acq/rel
3) proc->inner_lock : protects the thread and node lists (proc->threads,
   proc->waiting_threads, proc->nodes) and all todo lists associated with
   the binder_proc (proc->todo, thread->todo, proc->delivered_death and
   node->async_todo), as well as thread->transaction_stack
   binder_inner_proc_lock() and binder_inner_proc_unlock() are used
   to acq/rel

Any lock under procA must never be nested under any lock at the same
level or below on procB.

There was significant refactoring needed to implement the locking so there
are 37 patches in the set.

Here are the patches grouped into 4 categories:

1) bugfixes: 3 patches to fix behavior and are
   needed for fine-grained locking implementation
        Revert "binder: Sanity check at binder ioctl"
          - note: introduces kernel race to fix userspace bug. An
                  attempt to fix this was submitted in
                  "[PATCH v2] android: binder: fix dangling pointer comparison"
                  however that discussion concluded that this
                  patch should be reverted and the problem fixed
                  in userspace. Doing the revert now since this patch
                  conflicts with some of the fine-grained locking
                  patches.
        binder: use group leader instead of open thread
        binder: Use wake up hint for synchronous transactions.

2) Separate binder allocator into a separate file from binder driver
        binder: separate binder allocator structure from binder proc
        binder: remove unneeded cleanup code
        binder: separate out binder_alloc functions
        binder: move binder_alloc to separate file

3) Refactor binder driver to support locking
        binder: remove binder_debug_no_lock mechanism
        binder: add protection for non-perf cases
        binder: change binder_stats to atomics
        binder: make binder_last_id an atomic
        binder: add log information for binder transaction failures
        binder: refactor queue management in binder_thread_read
        binder: avoid race conditions when enqueuing txn 
        binder: don't modify thread->looper from other threads
        binder: remove dead code in binder_get_ref_for_node
        binder: protect against two threads freeing buffer
        binder: add more debug info when allocation fails.
        binder: use atomic for transaction_log index
        binder: refactor binder_pop_transaction
        binder: guarantee txn complete / errors delivered in-order
        binder: make sure target_node has strong ref 
        binder: make sure accesses to proc/thread are safe
        binder: refactor binder ref inc/dec for thread safety
        binder: use node->tmp_refs to ensure node safety

4) Add the locks and remove the global lock
        binder: introduce locking helper functions
        binder: use inner lock to sync work dq and node counts
        binder: add spinlocks to protect todo lists
        binder: add spinlock to protect binder_node
        binder: protect proc->nodes with inner lock
        binder: protect proc->threads with inner_lock
        binder: protect transaction_stack with inner lock.
        binder: use inner lock to protect thread accounting
        binder: protect binder_ref with outer lock
        binder: protect against stale pointers in print_binder_transaction
        binder: fix death race conditions
        binder: remove global binder lock

```
drivers/android/Makefile       |    2 +-
drivers/android/binder.c       | 3467 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------------
drivers/android/binder_alloc.c |  802 ++++++++++++++++++++++++++++++++
drivers/android/binder_alloc.h |  163 +++++++
drivers/android/binder_trace.h |   41 +-
5 files changed, 3235 insertions(+), 1240 deletions(-)
```
# Patch List
[[01/37] Revert "android: binder: Sanity check at binder ioctl"](https://patchwork.kernel.org/patch/9817743/)

[[02/37] binder: use group leader instead of open thread](https://patchwork.kernel.org/patch/9817803/)

[[03/37] binder: Use wake up hint for synchronous transactions.](https://patchwork.kernel.org/patch/9817747/)

[[04/37] binder: separate binder allocator structure from binder proc](https://patchwork.kernel.org/patch/9817745/)

[[05/37] binder: remove unneeded cleanup code](https://patchwork.kernel.org/patch/9817817/)

[[06/37] binder: separate out binder_alloc functions](https://patchwork.kernel.org/patch/9817753/)

[[07/37] binder: move binder_alloc to separate file](https://patchwork.kernel.org/patch/9817759/)

[[08/37] binder: remove binder_debug_no_lock mechanism](https://patchwork.kernel.org/patch/9817811/)

[[09/37] binder: add protection for non-perf cases](https://patchwork.kernel.org/patch/9817749/)

[[10/37] binder: change binder_stats to atomics](https://patchwork.kernel.org/patch/9817755/)

[[11/37] binder: make binder_last_id an atomic](https://patchwork.kernel.org/patch/9817809/)

[[12/37] binder: add log information for binder transaction failures](https://patchwork.kernel.org/patch/9817751/)

[[13/37] binder: refactor queue management in binder_thread_read](https://patchwork.kernel.org/patch/9817757/)

[[14/37] binder: avoid race conditions when enqueuing txn](https://patchwork.kernel.org/patch/9817813/)

[[15/37] binder: don't modify thread->looper from other threads](https://patchwork.kernel.org/patch/9817799/)

[[16/37] binder: remove dead code in binder_get_ref_for_node](https://patchwork.kernel.org/patch/9817819/)

[[17/37] binder: protect against two threads freeing buffer](https://patchwork.kernel.org/patch/9817815/)

[[18/37] binder: add more debug info when allocation fails.](https://patchwork.kernel.org/patch/9817797/)

[[19/37] binder: use atomic for transaction_log index](https://patchwork.kernel.org/patch/9817807/)

[[20/37] binder: refactor binder_pop_transaction](https://patchwork.kernel.org/patch/9817793/)

[[21/37] binder: guarantee txn complete / errors delivered in-order](https://patchwork.kernel.org/patch/9817805/)

[[22/37] binder: make sure target_node has strong ref](https://patchwork.kernel.org/patch/9817787/)

[[23/37] binder: make sure accesses to proc/thread are safe](https://patchwork.kernel.org/patch/9817785/)

[[24/37] binder: refactor binder ref inc/dec for thread safety](https://patchwork.kernel.org/patch/9817781/)

[[25/37] binder: use node->tmp_refs to ensure node safety](https://patchwork.kernel.org/patch/9817795/)

[[26/37] binder: introduce locking helper functions](https://patchwork.kernel.org/patch/9817791/)

[[27/37] binder: use inner lock to sync work dq and node counts](https://patchwork.kernel.org/patch/9817789/)

[[28/37] binder: add spinlocks to protect todo lists](https://patchwork.kernel.org/patch/9817769/)

[[29/37] binder: add spinlock to protect binder_node](https://patchwork.kernel.org/patch/9817777/)

[[30/37] binder: protect proc->nodes with inner lock](https://patchwork.kernel.org/patch/9817783/)

[[31/37] binder: protect proc->threads with inner_lock](https://patchwork.kernel.org/patch/9817775/)

[[32/37] binder: protect transaction_stack with inner lock.](https://patchwork.kernel.org/patch/9817779/)

[[33/37] binder: use inner lock to protect thread accounting](https://patchwork.kernel.org/patch/9817763/)

[[34/37] binder: protect binder_ref with outer lock](https://patchwork.kernel.org/patch/9817771/)

[[35/37] binder: protect against stale pointers in print_binder_transaction](https://patchwork.kernel.org/patch/9817761/)

[[36/37] binder: fix death race conditions](https://patchwork.kernel.org/patch/9817765/)

[[37/37] binder: remove global binder lock](https://patchwork.kernel.org/patch/9817773/)
