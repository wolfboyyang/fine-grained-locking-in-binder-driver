# Adnroid Goldfish 3.10

# Patch List
[[01/37] Revert "android: binder: Sanity check at binder ioctl"](https://patchwork.kernel.org/patch/9817743/)

- no need

[[02/37] binder: use group leader instead of open thread](https://patchwork.kernel.org/patch/9817803/)

- no need

[[03/37] binder: Use wake up hint for synchronous transactions.](https://patchwork.kernel.org/patch/9817747/)

- no need

[[04/37] binder: separate binder allocator structure from binder proc](https://patchwork.kernel.org/patch/9817745/)

- patched

[[05/37] binder: remove unneeded cleanup code](https://patchwork.kernel.org/patch/9817817/)

- patched

[[06/37] binder: separate out binder_alloc functions](https://patchwork.kernel.org/patch/9817753/)

- patched

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