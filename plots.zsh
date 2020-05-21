#!/usr/bin/env zsh

# progress
tmux \
  new-session -s plots \
             "zsh progress1-10/plot.sh ; read" \; \
  new-window "zsh progress10-20/plot.sh ; read" \; \
  new-window "zsh progress20-30/plot.sh ; read" \; \
  new-window "zsh progress30-40/plot.sh ; read" \; \
  new-window "zsh progress40-50/plot.sh ; read" \; \
  new-window "zsh progress10-50/plot.sh ; read" \; \
  new-window "zsh rewards1-10/plot.sh ; read" \; \
  new-window "zsh rewards10-20/plot.sh ; read" \; \
  new-window "zsh rewards20-30/plot.sh ; read" \; \
  new-window "zsh rewards30-40/plot.sh ; read" \; \
  new-window "zsh rewards40-50/plot.sh ; read" \; \
  new-window "zsh rewards10-50/plot.sh ; read" \; \
  select-layout even-vertical
