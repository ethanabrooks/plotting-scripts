#!/usr/bin/env zsh
plot --names Ours 'No roll' 'No scan' 'No roll or scan' 'OLSK' Transformer --paths ~/neurips/ours ~/neurips/no-roll ~/neurips/no-scan ~/neurips/no-roll-or-scan ~/neurips/olsk ~/neurips/transformer --tag eval_success_fraction_30 --limit 80000000 --fname ~/neurips/progress-30-40
