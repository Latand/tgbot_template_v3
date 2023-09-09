tail_lines := 100

# Makefile for tailing logs with a parameter for the number of lines
# usage: "make show-logs N=20", where N is the number of lines to tail.
#         ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
ifeq ($(strip $(N)),)
    # No COUNT parameter provided, using default value
    tail_cmd := tail -n $(tail_lines) -f
else
    # COUNT parameter provided, using it as the line count
    tail_cmd := tail -n $(N) -f
endif

.PHONY: tail

show-logs:
	$(tail_cmd) logs/logs.txt
