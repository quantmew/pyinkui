from __future__ import annotations

from typing import Any

_patched = False


def patchRefSupport() -> None:
    global _patched
    if _patched:
        return

    from pyinkcli.packages.react_reconciler import ReactFiberConfig

    originalApplyProps = ReactFiberConfig.applyProps

    def applyPropsWithRef(reconciler: Any, dom_node: Any, props: dict[str, Any], vnode_key: str | None) -> None:
        ref = props.get('ref')
        originalApplyProps(reconciler, dom_node, props, vnode_key)
        if ref is None:
            return
        try:
            if callable(ref):
                ref(dom_node)
            elif isinstance(ref, dict):
                ref['current'] = dom_node
            elif hasattr(ref, 'current'):
                ref.current = dom_node
        except Exception:
            return

    ReactFiberConfig.applyProps = applyPropsWithRef
    _patched = True
