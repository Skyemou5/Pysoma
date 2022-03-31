[ -n "$BASH_SOURCE" ] \
    || { echo 1>&2 "source (.) this with Bash."; exit 2; }
(
    cd "$(dirname "$BASH_SOURCE")"
    [ -d .build/virtualenv ] || {
        virtualenv .build/virtualenv
        . .build/virtualenv/bin/activate
        pip install -r requirements.txt
    }
)
. "$(dirname "$BASH_SOURCE")/.build/virtualenv/bin/activate"                                                                                                                                                                                                              