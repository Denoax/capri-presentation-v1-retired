# Start with the source

CAPRI is a public development preview. Offline inspection is the entry point; live native operation remains experimental. Commands below are tied to the source described in [SOURCE.md](SOURCE.md).

## Offline setup

Use a Linux host, Python 3.11+ with venv/pip, Git, and bubblewrap (`bwrap`). The full suite needs working unprivileged user, mount, PID and network namespaces. Follow your distribution's bubblewrap installation instructions; verify the collector rather than assuming installation proves isolation.

```sh
git clone https://github.com/Denoax/capri.git
cd capri
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes -r requirements.lock
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s controller/tests -p test_portability.py -k test_required_collector_namespaces -v
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s controller/tests -v
```

These are the checked-in CI dependency/test commands plus an isolated virtual environment. Tests use disposable fixtures; they do not call models or need Codex auth or Obsidian. A namespace denial means this host cannot complete the required isolation checks. Preserve the failure and use a supported host; do not silently skip the check. [CI configuration](../.github/workflows/tests.yml) · [Actual runs](https://github.com/Denoax/capri/actions/workflows/tests.yml).

The presentation validation checks command paths, CLI source and lock consistency. It does not claim a new successful full runtime suite. See [current status](STATUS.md).

## Before native use

The inherited target is Codex CLI **0.163.0**, the exact profile selected by this implementation, working existing authentication, `websockets==17.1`, namespaces and tmux for the ordinary three-pane route. Later CLI versions are unqualified here. The project uses native Codex sessions with existing authentication; it does not add a provider or promise any billing outcome.

Read the unchanged [native startup and continuation instructions](../IMPLEMENTATION_README.md#native-startup), [example configuration](../examples/config.json), [architecture](../ARCHITECTURE.md) and [security boundaries](../SECURITY.md). Configuration paths are intentional placeholders. Choose private owner-only state and short socket paths; never commit credentials, state, capabilities or recordings. Keep `production_automation` disabled and use explicitly registered disposable fixtures.

The initial request requires a real foreground terminal. Attaching a client, seeing a process in status, or receiving an RPC acknowledgement does not prove turn completion. Do not use this preview to replace an active controller. Native qualification, evaluation and the final human gate remain separate.

## Presentation media

The source and deterministic commands for rebuilding the authored media live in [ASSETS.md](ASSETS.md). They have a separate optional Pillow dependency and do not alter the controller lock.
