#!/usr/bin/bash
#
# route-test.sh - check which installed skill Claude Code picks for sample requests.
#
# Each case is sent to a headless `claude -p` session whose only tool is Skill,
# so the session cannot read files or run commands. The first skill it invokes
# is compared with the expected one.
#
# Inputs:  a tab-separated cases file (id, expected skill, request text);
#          lines starting with # and blank lines are ignored.
# Outputs: one line per case (PASS/FAIL/NONE, expected, picked), a summary,
#          and each session's raw stream-json transcript in the output directory.
# Exit:    0 all cases passed, 1 at least one case failed or picked nothing,
#          2 usage or setup error.
#
# NONE means the session invoked no skill (for example, it stopped to say it
# lacks file access); rerun that case or reword it before calling it a miss.
# Each run uses the account's normal model quota.

set -Eeuo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cases_file=""
jobs=6
out_dir=""
timeout_seconds=240

usage() {
    cat <<EOF
Usage: $(basename "$0") -c CASES_FILE [-j JOBS] [-o OUT_DIR] [-t SECONDS]

Check which installed skill Claude Code picks for each sample request.

Options:
  -c, --cases FILE     Tab-separated cases file to run (the bundled set is
                       $script_dir/route-cases.tsv).
  -j, --jobs N         Sessions to run at the same time (default: $jobs).
  -o, --out-dir DIR    Where to keep each session's transcript (default: a new
                       temporary directory, printed at the end).
  -t, --timeout SECS   Time limit per session in seconds (default: $timeout_seconds).
  -h, --help           Show this help.

Needs a signed-in Claude Code CLI (run 'claude auth login' if not).
EOF
}

die() {
    echo "Error: $*" >&2
    exit 2
}

is_positive_int() {
    [[ "$1" =~ ^[1-9][0-9]*$ ]]
}

if [[ $# -eq 0 ]]; then
    usage
    exit 0
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        -c|--cases) cases_file="${2:-}"; shift 2 ;;
        -j|--jobs) jobs="${2:-}"; shift 2 ;;
        -o|--out-dir) out_dir="${2:-}"; shift 2 ;;
        -t|--timeout) timeout_seconds="${2:-}"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) usage >&2; die "unknown option: $1" ;;
    esac
done

[[ -n "$cases_file" ]] || die "--cases is required"
[[ -f "$cases_file" ]] || die "cases file not found: $cases_file"
is_positive_int "$jobs" || die "--jobs must be a positive whole number, got '$jobs'"
is_positive_int "$timeout_seconds" || die "--timeout must be a positive whole number of seconds, got '$timeout_seconds'"
command -v claude >/dev/null || die "the claude CLI is not on PATH"

# An expired login makes every session fail before it can pick a skill.
if ! claude auth status --json 2>/dev/null | grep -q '"loggedIn": *true'; then
    die "the Claude Code CLI is not signed in; run 'claude auth login' first"
fi

if [[ -z "$out_dir" ]]; then
    out_dir="$(mktemp -d "${TMPDIR:-/tmp}/route-test.XXXXXX")"
else
    mkdir -p "$out_dir"
fi
results_dir="$out_dir/results"
mkdir -p "$results_dir"

# Run one case and write "STATUS<TAB>id<TAB>expected<TAB>picked" to its result file.
run_case() {
    local id="$1" expected="$2" prompt="$3"
    local transcript="$out_dir/$id.jsonl"
    local picked status

    timeout "$timeout_seconds" claude -p "$prompt" \
        --tools Skill --allowedTools Skill \
        --output-format stream-json --verbose --no-session-persistence \
        < /dev/null > "$transcript" 2>&1 || true

    picked="$(grep -o '"name":"Skill","input":{"skill":"[^"]*"' "$transcript" \
        | head -n 1 | sed 's/.*"skill":"//; s/"$//' || true)"

    if [[ -z "$picked" ]]; then
        status="NONE"
    elif [[ "$picked" == "$expected" ]]; then
        status="PASS"
    else
        status="FAIL"
    fi
    printf '%s\t%s\t%s\t%s\n' "$status" "$id" "$expected" "${picked:-<none>}" \
        > "$results_dir/$id.tsv"
}

declare -A seen_ids=()
running=0
while IFS=$'\t' read -r id expected prompt || [[ -n "${id:-}" ]]; do
    [[ -z "${id// }" || "$id" == \#* ]] && continue
    [[ -n "${expected:-}" && -n "${prompt:-}" ]] || die "case '$id' needs three tab-separated columns"
    [[ "$id" =~ ^[A-Za-z0-9._-]+$ ]] || die "case id '$id' may only use letters, digits, '.', '_' and '-'"
    [[ -z "${seen_ids[$id]:-}" ]] || die "duplicate case id: $id"
    seen_ids[$id]=1

    run_case "$id" "$expected" "$prompt" &
    running=$((running + 1))
    if (( running >= jobs )); then
        wait -n || true
        running=$((running - 1))
    fi
done < "$cases_file"
wait

(( ${#seen_ids[@]} > 0 )) || die "no cases found in $cases_file"

# Print results in cases-file order.
pass=0 fail=0 none=0
while IFS=$'\t' read -r id _; do
    [[ -z "${id// }" || "$id" == \#* ]] && continue
    IFS=$'\t' read -r status rid expected picked < "$results_dir/$id.tsv"
    printf '%-4s  %-28s  expected %-34s  picked %s\n' "$status" "$rid" "$expected" "$picked"
    case "$status" in
        PASS) pass=$((pass + 1)) ;;
        FAIL) fail=$((fail + 1)) ;;
        *) none=$((none + 1)) ;;
    esac
done < "$cases_file"

echo
echo "Passed $pass of ${#seen_ids[@]}; failed $fail; no skill picked $none."
echo "Transcripts: $out_dir"

(( fail == 0 && none == 0 ))
