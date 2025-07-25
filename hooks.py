from functools import partial

from util import shell

def run_hook(hook_name):
    shell(f"test -f build_hooks/{hook_name} && ./build/{hook_name}")

pre_squash_copy_hook = partial(run_hook, "pre_squash_copy")
pre_squash_hook = partial(run_hook, "pre_squash")
post_squash_hook = partial(run_hook, "post_squash")

