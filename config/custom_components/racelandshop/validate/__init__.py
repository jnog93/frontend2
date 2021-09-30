import asyncio
import glob
import importlib
from os.path import dirname, join, sep

from custom_components.racelandshop.share import SHARE, get_racelandshop


def _initialize_rules():
    rules = glob.glob(join(dirname(__file__), "**/*.py"))
    for rule in rules:
        rule = rule.replace(sep, "/")
        rule = rule.split("custom_components/racelandshop")[-1]
        rule = f"custom_components/racelandshop{rule}".replace("/", ".")[:-3]
        importlib.import_module(rule)


async def async_initialize_rules():
    hass = get_racelandshop().hass
    await hass.async_add_executor_job(_initialize_rules)


async def async_run_repository_checks(repository):
    racelandshop = get_racelandshop()
    if not SHARE["rules"]:
        await async_initialize_rules()
    if not racelandshop.system.running:
        return
    checks = []
    for check in SHARE["rules"].get("common", []):
        checks.append(check(repository))
    for check in SHARE["rules"].get(repository.data.category, []):
        checks.append(check(repository))

    await asyncio.gather(
        *[
            check._async_run_check()
            for check in checks or []
            if racelandshop.system.action or not check.action_only
        ]
    )

    total = len([x for x in checks if racelandshop.system.action or not x.action_only])
    failed = len([x for x in checks if x.failed])

    if failed != 0:
        repository.logger.error("%s %s/%s checks failed", repository, failed, total)
        if racelandshop.system.action:
            exit(1)
    else:
        repository.logger.debug("%s All (%s) checks passed", repository, total)
