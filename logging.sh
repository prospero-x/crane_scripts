#!/usr/bin/env bash

####################################################
# Mikhail Rezazadeh 2020
# This bash script contains logging helper functions
# for Bash scripts to use. Example:

# source ./logging.sh

# MYVAR=foo

# LOG_LEVEL=WARN
# echo first try with log level: $LOG_LEVEL

# log_trace Hello, World!
# log_debug my var is $MYVAR
# log_info Hello, World!
# log_warn Hello, World!
# log_error Hello, World!
# echo
# echo


# LOG_LEVEL=TRACE
# echo second pass with log level: $LOG_LEVEL
# log_trace Hello, World!
# log_debug my var is $MYVAR
# log_info Hello, World!
# log_warn Hello, World!
# log_error Hello, World!

# # (Fatal exits the program)
# log_fatal Hello, World!
####################################################

LOG_LEVELS=(
  FATAL
  ERROR
  WARN
  INFO
  DEBUG
  TRACE
)

BASH_RED='\033[1;31m'
BASH_LIGHT_RED='\033[0;31m'
BASH_YELLOW='\033[0;33m'
BASH_GREEN='\033[0;32m'
BASH_BLUE='\033[0;34m'
BASH_LIGHT_BLUE='\033[2;36m'
BASH_GREY='\033[0;37m'
BASH_NOCOLOR='\033[0m'

# These variables can be changed during the execution of
# whatever script imports (sources) this script
_DEFAULT_LOG_LEVEL=WARN
LOG_LEVEL=$_DEFAULT_LOG_LEVEL

_DEFAULT_TIMESTAMP_FMT='+%Y-%m-%dT%H:%M:%S'
TIMESTAMP_FMT=$_DEFAULT_TIMESTAMP_FMT

# Only apply bash colors if we're outputting to a terminal (stdout)
APPLY_COLORS=false
if [ -t 1 ]; then
        APPLY_COLORS=true
fi


function log_fatal {
	log FATAL $BASH_RED $@
	exit 1
}

function log_error {
	log ERROR $BASH_LIGHT_RED $@
}

function log_warn {
	log WARN $BASH_YELLOW $@
}

function log_info {
	log INFO $BASH_GREEN $@
}

function log_debug {
	log DEBUG $BASH_BLUE $@
}

function log_trace {
	log TRACE $BASH_LIGHT_BLUE $@
}

function log {
	REQUESTED_LEVEL_NAME=$1
	shift

	LEVEL_COLOR=$1
	shift

	LOG_MESSAGE=$@

	get-log-level $REQUESTED_LEVEL_NAME
	REQUESTED_LEVEL=$GET_LOG_LEVEL_RV

	# Unfortunately, need to check every time, in case
	# wishes to change the log level during execution...
	get-log-level $LOG_LEVEL
	LOG_LEVEL_NUM=$GET_LOG_LEVEL_RV

	# Format the log message
	TIMESTAMP=$(date $TIMESTAMP_FMT)

	if (( $LOG_LEVEL_NUM < $REQUESTED_LEVEL )); then
		return
	fi
	if $APPLY_COLORS; then
		preamble="[$TIMESTAMP] ${LEVEL_COLOR} [$REQUESTED_LEVEL_NAME] "
		printf "${BASH_GREY}${preamble}${LOG_MESSAGE}${BASH_NOCOLOR}\n"
	else
		echo [$TIMESTAMP] [$REQUESTED_LEVEL_NAME] $LOG_MESSAGE
	fi

}

function get-log-level {
	LEVEL_NAME=$1
	GET_LOG_LEVEL_RV=0
	for levelNum in ${!LOG_LEVELS[@]}; do
		level=${LOG_LEVELS[$levelNum]}
                if [ $level == $LEVEL_NAME ]; then
			GET_LOG_LEVEL_RV=$levelNum
			break
		fi
	done
}

