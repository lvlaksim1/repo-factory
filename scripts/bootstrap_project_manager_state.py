from __future__ import annotations

import argparse
import json
from pathlib import Path


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def bootstrap(
    *,
    target: Path,
    repository: str,
    name: str,
    manager_branch: str,
    product_branch: str,
    source_commit: str,
    core_repository: str,
    core_commit: str,
    pm_repository: str,
    pm_commit: str,
) -> str:
    manager_dir = target / ".context" / "manager"
    memory_dir = target / ".context" / "memory"
    manager_dir.mkdir(parents=True, exist_ok=True)
    memory_dir.mkdir(parents=True, exist_ok=True)

    identity_path = manager_dir / "identity.json"
    if identity_path.exists():
        raise SystemExit("refusing bootstrap: Project Manager identity already exists")

    manager_id = f"{name.lower()}-project-manager"
    identity_path.write_text(
        json.dumps({"manager_id": manager_id}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    write_text(
        manager_dir / "mandate.md",
        f"""# Manager mandate

The Project Manager owns durable project continuity, reconciliation, planning, verification,
and maintenance of manager state for `{repository}`.

It may analyze repository state, maintain `.context`, coordinate and execute non-destructive
work already authorized by existing project rules and explicit owner directives. It must preserve
the project's established identity, goals, constraints, decisions, and branch authority.

It must not expand its own authority, bypass project constraints, alter credentials/access,
change repository visibility, publish releases, or perform destructive/irreversible actions
without authority already present in project rules or a later explicit owner directive.

Later explicit owner directives and repository-specific authority rules supersede this bootstrap
mandate when they are more specific.
""",
    )

    write_text(
        manager_dir / "beliefs.md",
        f"""# Manager beliefs

## Owner-authorized manager installation

The owner explicitly authorized installation of a persistent Project Manager into this repository,
which previously used standalone Context Capsule Core v1.3.1.

- source: repo-factory command `[UPGRADE_CONTEXT_CAPSULE_TO_PROJECT_MANAGER]`
- authority: owner-directive

## Preserved durable project context

The pre-existing project identity, goals, architecture, constraints, current working views, rules,
decisions, dialogues, history, and handoff state are preserved as repository evidence and must be
reconciled before consequential action.

- source: repository state at `{source_commit}` on `{manager_branch}`
- authority: verified-repository

## Product coordinates

The installed durable-context base is Context Capsule Core v1.3.1 at
`{core_repository}@{core_commit}`. The Project Manager implementation is
`{pm_repository}@{pm_commit}`.

- source: `repo-factory/components.lock.json`
- authority: verified-repository

## Branch authority

Manager state authority is `{manager_branch}`; product baseline authority is
`{product_branch}`. Changing either authority requires explicit reconciliation and must not
happen implicitly.

- source: preserved Context Capsule branch topology and explicit upgrade
- authority: verified-repository
""",
    )

    write_text(
        manager_dir / "goals.md",
        """# Manager goals

- Preserve and pursue the project's existing durable goals rather than replacing them with generic manager goals.
- Maintain coherent Project Manager state across runtime replacement.
- Reconcile stored context with current repository, CI, runtime, and owner evidence before high-impact decisions.
- Verify consequential work before recording completion and persist only durable semantic consequences.
""",
    )

    write_text(
        manager_dir / "intentions.md",
        """# Manager intentions and commitments

## Active — continuity and reconciliation

Status: active.

Reinstate from the authoritative manager-state branch, reconcile the preserved project context
against current evidence, and continue the project's recorded goals and next actions within its
existing constraints and owner authority.

Completion requires a later project-specific verification that no unresolved continuity work
remains; installation alone does not complete this commitment.
""",
    )

    write_text(
        manager_dir / "plans.md",
        f"""# Manager plans

1. Reinstate from `{manager_branch}` and read the preserved project identity, goals, architecture, constraints, rules, decisions, current state, blockers, and next actions.
2. Reconcile that durable state against the current product baseline `{product_branch}` and relevant live evidence.
3. Continue already-authorized project work without inventing new authority.
4. Verify results using repository/CI/runtime evidence appropriate to the project.
5. Persist changed beliefs, commitments, decisions, and working views atomically when their meaning changes.
""",
    )

    write_text(
        memory_dir / "semantic.md",
        f"""# Semantic memory

## Standalone Capsule migration

This Project Manager was created by an explicit owner-authorized upgrade from standalone Context
Capsule Core v1.3.1. The existing project context was retained as project evidence; the manager
layer was added on top and must not reinterpret preserved project facts merely because the runtime
model changed.

- source: repo-factory upgrade from repository state `{source_commit}`
- authority: owner-directive; verified-repository
""",
    )

    write_text(
        memory_dir / "procedural.md",
        """# Procedural memory

## Reinstantiation procedure

Use the authoritative manager-state branch, require Project Manager `VALID` and `READY`, and
use the deterministic recovery pack before resuming consequential manager responsibility. Treat
runtime conversation/checkpoint state as replaceable and repository durable state as the continuity
surface.

- source: Project Manager Contract and explicit repository upgrade
- authority: core-contract; verified-repository
""",
    )

    return manager_id


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--manager-branch", required=True)
    parser.add_argument("--product-branch", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--core-repository", required=True)
    parser.add_argument("--core-commit", required=True)
    parser.add_argument("--pm-repository", required=True)
    parser.add_argument("--pm-commit", required=True)
    args = parser.parse_args()

    manager_id = bootstrap(
        target=Path(args.target),
        repository=args.repository,
        name=args.name,
        manager_branch=args.manager_branch,
        product_branch=args.product_branch,
        source_commit=args.source_commit,
        core_repository=args.core_repository,
        core_commit=args.core_commit,
        pm_repository=args.pm_repository,
        pm_commit=args.pm_commit,
    )
    print(manager_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
